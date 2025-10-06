"""
Common utilities for lineup generation across all sports.

This module provides reusable functions for position assignment, player rotation,
and lineup validation that work regardless of sport type.
"""

from typing import Dict, List, Optional

from sports.models.lineup import Player, PositionAssignment
from sports.models.sport_config import Position


def assign_positions_smart(
    available_players: List[Player],
    available_positions: List[Position],
    must_play_players: Optional[List[Player]] = None,
    player_position_history: Optional[Dict[str, List[str]]] = None,
) -> List[PositionAssignment]:
    """
    Assign players to positions using smart algorithm.

    Algorithm priorities:
    1. Must-play players get priority (players who sat out multiple periods)
    2. Position scarcity - positions with fewer candidates are filled first
    3. Player flexibility - less flexible players assigned first
    4. Position rotation - prefer positions players haven't played recently

    Args:
        available_players: Players available for assignment
        available_positions: Positions to fill
        must_play_players: Players who must be included (high priority)
        player_position_history: Dict of player_id -> [position_ids played]

    Returns:
        List of PositionAssignment objects

    Raises:
        ValueError: If cannot fill all positions with available players
    """
    if must_play_players is None:
        must_play_players = []
    if player_position_history is None:
        player_position_history = {}

    # First verify we can fill all positions
    position_ids = [p.id for p in available_positions]
    if not can_fill_all_positions(available_players, position_ids):
        raise ValueError(
            f"Cannot fill all positions with available players. "
            f"Need {len(position_ids)} positions, have {len(available_players)} players"
        )

    assignments = []
    remaining_players = available_players.copy()
    remaining_positions = available_positions.copy()

    # Calculate position scarcity (positions with fewest candidates first)
    position_scarcity = _calculate_position_scarcity(
        remaining_positions, remaining_players
    )

    # Assign positions in order of scarcity
    for position, _ in position_scarcity:
        # Get candidates who can play this position
        candidates = _get_candidates_for_position(position, remaining_players)

        # Prioritize must-play players
        must_play_candidates = [p for p in candidates if p in must_play_players]
        if must_play_candidates:
            candidates = must_play_candidates

        # Sort candidates by rotation history and flexibility
        candidates.sort(
            key=_create_candidate_sort_key(position.id, player_position_history)
        )

        if not candidates:
            raise ValueError(
                f"No candidates available for position {position.name} ({position.id}). "
                f"Remaining players: {len(remaining_players)}."
            )

        # Try candidates in order until we find one that doesn't block future assignments
        # Use look-ahead to avoid painting ourselves into a corner
        chosen_player = None
        for candidate in candidates:
            # Temporarily assign this candidate
            temp_remaining = [p for p in remaining_players if p.id != candidate.id]
            temp_remaining_positions = [
                pos for pos, _ in position_scarcity
                if pos.id != position.id
            ]

            # Check if remaining positions can still be filled
            remaining_position_ids = [p.id for p in temp_remaining_positions]
            if not remaining_position_ids or can_fill_all_positions(
                temp_remaining, remaining_position_ids
            ):
                # This assignment won't block future positions
                chosen_player = candidate
                break

        if not chosen_player:
            # All candidates would block future positions - use first one anyway
            chosen_player = candidates[0]

        assignment = PositionAssignment(
            player=chosen_player,
            position=position.id,
        )
        assignments.append(assignment)
        remaining_players.remove(chosen_player)

    return assignments


def can_fill_all_positions(
    players: List[Player],
    position_ids: List[str],
    assignments: Optional[Dict[str, str]] = None,
) -> bool:
    """
    Check if all positions can be filled with available players.

    Uses recursive backtracking to verify a valid assignment exists.

    Args:
        players: Available players
        position_ids: Position IDs that need to be filled
        assignments: Current assignments (used in recursion)

    Returns:
        True if all positions can be filled, False otherwise
    """
    if assignments is None:
        assignments = {}

    # Base case: all positions filled
    if not position_ids:
        return True

    # Get next position to fill
    position = position_ids[0]
    remaining_positions = position_ids[1:]

    # Try each player who can play this position
    for player in players:
        # Skip if player already assigned
        if player.id in assignments.values():
            continue

        # Check if player can play this position
        if not player.can_play_position(position):
            continue

        # Try assigning this player
        new_assignments = {**assignments, position: player.id}

        # Recursively try to fill remaining positions
        if can_fill_all_positions(players, remaining_positions, new_assignments):
            return True

    # No valid assignment found
    return False


def track_player_position_history(
    assignments: List[PositionAssignment],
    player_position_history: Dict[str, List[str]],
) -> None:
    """
    Update player position history with new assignments.

    Modifies player_position_history in-place.

    Args:
        assignments: Position assignments to track
        player_position_history: Dict to update (player_id -> [position_ids])
    """
    for assignment in assignments:
        player_id = assignment.player.id
        position_id = assignment.position

        if player_id not in player_position_history:
            player_position_history[player_id] = []

        player_position_history[player_id].append(position_id)


def validate_lineup_completeness(
    assignments: List[PositionAssignment],
    required_position_ids: List[str],
) -> List[str]:
    """
    Validate that lineup has all required positions filled.

    Args:
        assignments: Position assignments to validate
        required_position_ids: Position IDs that must be present

    Returns:
        List of validation error messages (empty if valid)
    """
    errors = []

    assigned_positions = {a.position for a in assignments}

    for req_pos in required_position_ids:
        if req_pos not in assigned_positions:
            errors.append(f"Required position not filled: {req_pos}")

    # Check for duplicate positions
    position_counts = {}
    for assignment in assignments:
        pos = assignment.position
        position_counts[pos] = position_counts.get(pos, 0) + 1

    for pos, count in position_counts.items():
        if count > 1:
            errors.append(f"Position {pos} assigned {count} times (should be 1)")

    return errors


def calculate_position_balance(
    player_position_history: Dict[str, List[str]],
    player_ids: Optional[List[str]] = None,
) -> Dict[str, Dict[str, int]]:
    """
    Calculate how many times each player has played each position.

    Useful for analyzing whether playing time is balanced.

    Args:
        player_position_history: Dict of player_id -> [position_ids played]
        player_ids: Optional list to filter specific players

    Returns:
        Dict of player_id -> {position_id: count}
    """
    balance = {}

    if player_ids is None:
        player_ids = list(player_position_history.keys())

    for player_id in player_ids:
        if player_id not in player_position_history:
            balance[player_id] = {}
            continue

        position_counts = {}
        for position in player_position_history[player_id]:
            position_counts[position] = position_counts.get(position, 0) + 1

        balance[player_id] = position_counts

    return balance


# Private helper functions


def _get_candidates_for_position(
    position: Position, players: List[Player]
) -> List[Player]:
    """Get list of players who can play a specific position."""
    return [p for p in players if p.can_play_position(position.id)]


def _calculate_position_scarcity(
    positions: List[Position],
    players: List[Player],
) -> List[tuple]:
    """
    Calculate scarcity (number of candidates) for each position.

    Returns positions sorted by scarcity (fewest candidates first).

    Args:
        positions: Positions to evaluate
        players: Available players

    Returns:
        List of (Position, candidate_count) tuples, sorted by count
    """
    position_scarcity = []

    for pos in positions:
        candidates = _get_candidates_for_position(pos, players)
        position_scarcity.append((pos, len(candidates)))

    # Sort by candidate count (fewest first)
    position_scarcity.sort(key=lambda x: x[1])

    return position_scarcity


def _create_candidate_sort_key(
    position_id: str, player_position_history: Dict[str, List[str]]
):
    """
    Create a sort key function for candidate prioritization.

    Prioritizes:
    1. Players who haven't played this position recently (lower count)
    2. Players with fewer position preferences (less flexible)

    Args:
        position_id: Position being filled
        player_position_history: History of assignments

    Returns:
        Sort key function
    """

    def candidate_sort_key(player: Player) -> tuple:
        # Count how many times player has played this position
        position_count = 0
        if player.id in player_position_history:
            position_count = player_position_history[player.id].count(position_id)

        # Calculate flexibility (fewer preferences = less flexible = higher priority)
        flexibility = (
            len(player.position_preferences) if player.position_preferences else 99
        )

        # Return tuple for sorting (lower is better)
        return (position_count, flexibility)

    return candidate_sort_key
