"""
Volleyball lineup generator with basic rotation support.

This module implements volleyball-specific lineup generation that handles:
- 3-5 sets per match (configurable)
- 6 players on court per set
- Basic rotation tracking between sets
- Position preferences (Setter required, OH, MB, OPP, L, DS)
- Smart position assignment with history tracking
"""

from typing import Dict, List, Optional

from sports.generators.base import LineupGenerator
from sports.models.lineup import Lineup, Player, PositionAssignment
from sports.models.sport_config import Position
from sports.utils.lineup_utils import (
    assign_positions_smart,
    track_player_position_history,
)


class VolleyballLineupGenerator(LineupGenerator):
    """
    Lineup generator for volleyball with basic rotation support.

    Generates 3-5 lineups for a volleyball match (one per set) while
    tracking basic rotation patterns.
    """

    def __init__(self, sport_config):
        """
        Initialize volleyball lineup generator.

        Args:
            sport_config: Volleyball sport configuration
        """
        super().__init__(sport_config)

    def generate(
        self,
        players: List[Player],
        game_info: dict,
        player_history: Optional[Dict] = None,
    ) -> List[Lineup]:
        """
        Generate volleyball lineups (3-5 sets).

        Args:
            players: List of available players
            game_info: Game metadata (game_id, team_id, num_sets)
            player_history: Optional history of previous assignments

        Returns:
            List of Lineup objects (one per set)

        Raises:
            ValueError: If insufficient players or required positions unavailable
        """
        # Validate game info
        game_info_errors = self._validate_game_info(game_info)
        if game_info_errors:
            raise ValueError(f"Invalid game_info: {', '.join(game_info_errors)}")

        # Validate players
        player_errors = self.validate_players(players)
        if player_errors:
            raise ValueError(f"Invalid players: {', '.join(player_errors)}")

        # Initialize tracking dictionaries
        position_history = player_history or {}
        bench_tracker = {p.id: 0 for p in players}  # Track consecutive bench periods

        lineups = []
        num_sets = game_info.get("num_sets", 3)  # Default to 3 sets

        for set_num in range(1, num_sets + 1):
            # Determine which players must play (sat out 2+ periods)
            must_play_players = self._get_must_play_players(
                players, bench_tracker, set_num
            )

            # Fill positions for this set
            assignments, bench_players = self._generate_set_lineup(
                players, must_play_players, position_history
            )

            # Update bench tracker
            for player in players:
                if player in bench_players:
                    bench_tracker[player.id] += 1
                else:
                    bench_tracker[player.id] = 0

            # Create lineup
            period_name = f"Set {set_num}"
            lineup = Lineup(
                period=set_num,
                period_name=period_name,
                assignments=assignments,
                bench_players=bench_players,
                metadata={
                    "game_id": game_info.get("game_id"),
                    "team_id": game_info.get("team_id"),
                },
            )
            lineups.append(lineup)

        return lineups

    def _generate_set_lineup(
        self,
        players: List[Player],
        must_play_players: List[Player],
        position_history: Dict,
    ) -> tuple[List[PositionAssignment], List[Player]]:
        """
        Generate lineup for a single set.

        Args:
            players: All available players
            must_play_players: Players who must play this set
            position_history: History of position assignments
            set_num: Current set number (1-based)

        Returns:
            Tuple of (assignments, bench_players)

        Raises:
            ValueError: If unable to fill all positions
        """
        # Get required positions (6 total for volleyball)
        # Typical: S, OH, OH, MB, MB, OPP/L/DS
        required_positions = self._get_required_positions()

        # Get eligible players (those who can play in this set)
        eligible_players = list(players)

        # Assign positions using smart assignment
        assignments = assign_positions_smart(
            available_players=eligible_players,
            available_positions=required_positions,
            must_play_players=must_play_players,
            player_position_history=position_history,
        )

        if not assignments or len(assignments) < len(required_positions):
            raise ValueError(
                f"Cannot fill all positions with available players. "
                f"Need {len(required_positions)} positions, "
                f"have {len(players)} players"
            )

        # Track position history for all assignments
        track_player_position_history(assignments, position_history)

        # Determine bench players
        assigned_player_ids = {a.player.id for a in assignments}
        bench_players = [p for p in players if p.id not in assigned_player_ids]

        return assignments, bench_players

    def _get_required_positions(self) -> List[Position]:
        """
        Get the required positions for a volleyball lineup.

        Returns 6 positions:
        - 1 Setter (S) - required
        - 2 Outside Hitters (OH)
        - 2 Middle Blockers (MB)
        - 1 Opposite/Libero/DS (flexible)

        Returns:
            List of Position objects needed for a complete lineup
        """
        positions = []

        # Always need 1 Setter
        setter = next((p for p in self.config.positions if p.id == "S"), None)
        if setter:
            positions.append(setter)

        # Need 2 Outside Hitters
        oh = next((p for p in self.config.positions if p.id == "OH"), None)
        if oh:
            positions.extend([oh, oh])

        # Need 2 Middle Blockers
        mb = next((p for p in self.config.positions if p.id == "MB"), None)
        if mb:
            positions.extend([mb, mb])

        # Need 1 Opposite (or Libero or DS if OPP not available)
        opp = next((p for p in self.config.positions if p.id == "OPP"), None)
        if opp:
            positions.append(opp)
        else:
            # Fallback to L or DS
            l_pos = next((p for p in self.config.positions if p.id == "L"), None)
            ds_pos = next((p for p in self.config.positions if p.id == "DS"), None)
            if l_pos:
                positions.append(l_pos)
            elif ds_pos:
                positions.append(ds_pos)

        return positions

    def _get_must_play_players(
        self, players: List[Player], bench_tracker: Dict[str, int], current_set: int
    ) -> List[Player]:
        """
        Identify players who must play because they've been benched too long.

        Players who sat out 2+ consecutive sets must play.

        Args:
            players: All available players
            bench_tracker: Dictionary tracking consecutive bench periods per player
            current_set: Current set number

        Returns:
            List of players who must play this set
        """
        if current_set == 1:
            return []  # No must-play in first set

        must_play = []
        for player in players:
            if bench_tracker.get(player.id, 0) >= 2:
                must_play.append(player)

        return must_play
