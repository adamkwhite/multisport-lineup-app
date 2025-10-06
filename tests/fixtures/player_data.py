"""
Reusable test data for players
"""


def create_player(player_id, name, position_preferences=None):
    """Create a player dictionary for testing"""
    return {
        "id": player_id,
        "name": name,
        "position_preferences": (
            position_preferences if position_preferences is not None else []
        ),
    }


def create_flexible_players(count=9, start_id=1):
    """Create players that can play any position"""
    return [
        create_player(i, f"Player {i}", []) for i in range(start_id, start_id + count)
    ]


def create_pitchers(count=3, start_id=1):
    """Create players who can only pitch"""
    return [
        create_player(i, f"Pitcher {i}", ["P"])
        for i in range(start_id, start_id + count)
    ]


def create_catchers(count=2, start_id=1):
    """Create players who can only catch"""
    return [
        create_player(i, f"Catcher {i}", ["C"])
        for i in range(start_id, start_id + count)
    ]


def create_infielders(count=4, start_id=1):
    """Create players who can play infield positions (1B, 2B, 3B, SS)"""
    return [
        create_player(i, f"Infielder {i}", ["1B", "2B", "3B", "SS"])
        for i in range(start_id, start_id + count)
    ]


def create_outfielders(count=3, start_id=1):
    """Create players who can play outfield positions (LF, CF, RF)"""
    return [
        create_player(i, f"Outfielder {i}", ["LF", "CF", "RF"])
        for i in range(start_id, start_id + count)
    ]


# Pre-defined test scenarios
NINE_FLEXIBLE_PLAYERS = create_flexible_players(9)

TWELVE_FLEXIBLE_PLAYERS = create_flexible_players(12)

MIXED_POSITION_PLAYERS = (
    create_pitchers(1)
    + create_catchers(1, start_id=2)
    + create_flexible_players(7, start_id=3)
)

SPECIALIZED_PLAYERS = (
    create_pitchers(2)
    + create_catchers(2, start_id=3)
    + create_infielders(4, start_id=5)
    + create_outfielders(3, start_id=9)
)
