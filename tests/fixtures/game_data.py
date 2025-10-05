"""
Reusable test data for games
"""

from datetime import datetime, timedelta


def create_game(game_id, name, starts_at, location="Test Stadium"):
    """Create a game dictionary for testing"""
    return {"id": game_id, "name": name, "starts_at": starts_at, "location": location}


def create_upcoming_games(count=3):
    """Create upcoming games starting tomorrow"""
    games = []
    for i in range(count):
        game_date = datetime.now() + timedelta(days=i + 1)
        game_time = game_date.replace(hour=18, minute=0, second=0)
        games.append(
            create_game(
                game_id=f"game_{i+1}",
                name=f"vs Opponent {i+1}",
                starts_at=game_time.isoformat() + "Z",
            )
        )
    return games


def create_past_games(count=3):
    """Create past games"""
    games = []
    for i in range(count):
        game_date = datetime.now() - timedelta(days=count - i)
        game_time = game_date.replace(hour=18, minute=0, second=0)
        games.append(
            create_game(
                game_id=f"past_game_{i+1}",
                name=f"vs Past Opponent {i+1}",
                starts_at=game_time.isoformat() + "Z",
            )
        )
    return games


# Pre-defined test scenarios
SINGLE_UPCOMING_GAME = create_upcoming_games(1)
THREE_UPCOMING_GAMES = create_upcoming_games(3)
MIX_PAST_AND_UPCOMING = create_past_games(2) + create_upcoming_games(3)
