"""
Baseball lineup generator with pitcher rotation rules.

This module implements baseball-specific lineup generation that enforces:
- Max 2 consecutive innings per pitcher
- 3 lineups for 6-inning games (innings 1-2, 3-4, 5-6)
- Position preferences (pitcher, catcher, any position)
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


class BaseballLineupGenerator(LineupGenerator):
    """
    Lineup generator for baseball with pitcher rotation rules.

    Generates 3 lineups for a 6-inning game (innings 1-2, 3-4, 5-6) while
    enforcing pitcher rotation rules (max 2 consecutive innings).
    """

    def __init__(self, sport_config):
        """
        Initialize baseball lineup generator.

        Args:
            sport_config: Baseball sport configuration
        """
        super().__init__(sport_config)

        # Get pitcher max innings from config (default to 2)
        self.pitcher_max_innings = 2
        if hasattr(sport_config, "rules") and hasattr(sport_config.rules, "pitcher_max_consecutive_innings"):
            self.pitcher_max_innings = sport_config.rules.pitcher_max_consecutive_innings

    def generate(
        self,
        players: List[Player],
        game_info: dict,
        player_history: Optional[Dict] = None,
    ) -> List[Lineup]:
        """
        Generate 3 baseball lineups (innings 1-2, 3-4, 5-6).

        Args:
            players: List of available players
            game_info: Game metadata (game_id, team_id, num_periods)
            player_history: Optional history of previous assignments

        Returns:
            List of 3 Lineup objects (one per 2-inning period)

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
        pitcher_history = {}  # Track which periods each pitcher has worked
        bench_tracker = {p.id: 0 for p in players}  # Track consecutive bench periods

        lineups = []
        num_periods = game_info.get("num_periods", 3)  # Default to 3 periods

        # Generate lineup for each 2-inning period
        for period in range(1, num_periods + 1):
            lineup = self._generate_period_lineup(
                period=period,
                players=players,
                position_history=position_history,
                pitcher_history=pitcher_history,
                bench_tracker=bench_tracker,
            )

            lineups.append(lineup)

            # Update tracking
            track_player_position_history(lineup.assignments, position_history)
            self._update_pitcher_history(lineup, pitcher_history)
            self._update_bench_tracker(lineup, players, bench_tracker)

        return lineups

    def _generate_period_lineup(
        self,
        period: int,
        players: List[Player],
        position_history: dict,
        pitcher_history: dict,
        bench_tracker: dict,
    ) -> Lineup:
        """
        Generate lineup for a single 2-inning period.

        Args:
            period: Period number (1-3)
            players: Available players
            position_history: Position assignment history
            pitcher_history: Pitcher period history
            bench_tracker: Consecutive bench tracking

        Returns:
            Lineup object for this period
        """
        # Determine period name (e.g., "Innings 1-2")
        start_inning = (period - 1) * 2 + 1
        end_inning = period * 2
        period_name = f"Innings {start_inning}-{end_inning}"

        # Get eligible pitchers (not pitched previous period)
        eligible_pitchers = self._get_eligible_pitchers(
            players, pitcher_history, period
        )

        if not eligible_pitchers:
            raise ValueError(
                f"No eligible pitchers for period {period}. "
                f"All pitchers have reached max consecutive innings ({self.pitcher_max_innings})."
            )

        # Identify must-play players (sat out previous periods)
        must_play_players = self._get_must_play_players(
            players, bench_tracker, period
        )

        # Filter out ineligible pitchers by creating modified player list
        # Players who pitched last period temporarily lose ability to pitch
        eligible_pitcher_ids = {p.id for p in eligible_pitchers}
        filtered_players = []

        for player in players:
            # Create a copy with modified preferences if needed
            if player.can_play_position("P") and player.id not in eligible_pitcher_ids:
                # Player can pitch but not eligible this period - remove P temporarily
                modified_prefs = [pos for pos in player.position_preferences if pos != "P"]
                # If they had only P, give them all non-P positions
                if not modified_prefs and player.position_preferences == ["P"]:
                    # Pitcher-only player who can't pitch this period - can play any non-P position
                    all_non_p_positions = [pos.id for pos in self.config.positions if pos.id != "P"]
                    modified_player = Player(
                        id=player.id,
                        name=player.name,
                        position_preferences=all_non_p_positions,
                        jersey_number=player.jersey_number,
                        metadata=player.metadata,
                    )
                else:
                    modified_player = Player(
                        id=player.id,
                        name=player.name,
                        position_preferences=modified_prefs,
                        jersey_number=player.jersey_number,
                        metadata=player.metadata,
                    )
                filtered_players.append(modified_player)
            else:
                filtered_players.append(player)

        # Assign positions using smart algorithm
        assignments = assign_positions_smart(
            available_players=filtered_players,
            available_positions=self.config.positions,
            must_play_players=must_play_players,
            player_position_history=position_history,
        )

        # Verify all positions were assigned
        if len(assignments) != len(self.config.positions):
            assigned_positions = {a.position for a in assignments}
            all_positions = {p.id for p in self.config.positions}
            missing = all_positions - assigned_positions
            raise ValueError(
                f"Not all positions were assigned in period {period}. "
                f"Got {len(assignments)}/{len(self.config.positions)}. "
                f"Missing: {missing}"
            )

        # Determine bench players
        assigned_player_ids = {a.player.id for a in assignments}
        bench_players = [p for p in players if p.id not in assigned_player_ids]

        # Create lineup
        return Lineup(
            period=period,
            period_name=period_name,
            assignments=assignments,
            bench_players=bench_players,
        )

    def _get_eligible_pitchers(
        self, players: List[Player], pitcher_history: dict, current_period: int
    ) -> List[Player]:
        """
        Get pitchers who haven't pitched in the previous period.

        Args:
            players: All players
            pitcher_history: Dict of player_id -> [periods pitched]
            current_period: Current period number

        Returns:
            List of eligible pitcher Players
        """
        eligible = []

        for player in players:
            # Check if player can pitch
            if not player.can_play_position("P"):
                continue

            # Check if pitched in previous period
            periods_pitched = pitcher_history.get(player.id, [])

            # If this is period 1, everyone is eligible
            if current_period == 1:
                eligible.append(player)
                continue

            # Check if pitched in immediately previous period
            if (current_period - 1) not in periods_pitched:
                eligible.append(player)

        return eligible

    def _get_must_play_players(
        self, players: List[Player], bench_tracker: dict, current_period: int
    ) -> List[Player]:
        """
        Get players who must play (sat out too many periods).

        Args:
            players: All players
            bench_tracker: Dict of player_id -> consecutive bench count
            current_period: Current period number

        Returns:
            List of Players who must play
        """
        must_play = []

        # Only check after first period
        if current_period == 1:
            return must_play

        for player in players:
            # If sat out 2 consecutive periods, must play
            if bench_tracker.get(player.id, 0) >= 2:
                must_play.append(player)

        return must_play

    def _update_pitcher_history(self, lineup: Lineup, pitcher_history: dict) -> None:
        """
        Track which periods each pitcher has worked.

        Args:
            lineup: Completed lineup
            pitcher_history: Dict to update (player_id -> [periods])
        """
        for assignment in lineup.assignments:
            if assignment.position == "P":
                if assignment.player.id not in pitcher_history:
                    pitcher_history[assignment.player.id] = []
                pitcher_history[assignment.player.id].append(lineup.period)

    def _update_bench_tracker(
        self, lineup: Lineup, players: List[Player], bench_tracker: dict
    ) -> None:
        """
        Update consecutive bench tracking.

        Args:
            lineup: Completed lineup
            players: All players
            bench_tracker: Dict to update (player_id -> consecutive bench count)
        """
        assigned_player_ids = {a.player.id for a in lineup.assignments}

        for player in players:
            if player.id in assigned_player_ids:
                bench_tracker[player.id] = 0  # Reset - they played
            else:
                bench_tracker[player.id] += 1  # Increment - they sat out
