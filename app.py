#!/usr/bin/env python3
"""
Baseball Lineup Manager - TeamSnap Integration
Main Flask application for managing baseball fielding positions
"""

import os
import random
from datetime import datetime, timedelta
from urllib.parse import urlencode

import requests
from dotenv import load_dotenv
from flask import Flask, jsonify, redirect, render_template, request, session, url_for
from flask_cors import CORS
from flask_wtf.csrf import CSRFProtect


def obfuscate_name(full_name):
    """
    Obfuscate player name using format: First letter + stars + Last letter + stars
    Example: "Adam White" -> "A*** W****"
    """
    if not full_name or not full_name.strip():
        return "Unknown Player"

    parts = full_name.strip().split()
    if len(parts) < 2:
        # Handle single names
        name = parts[0]
        if len(name) == 1:
            return name
        return f"{name[0]}{'*' * (len(name) - 1)}"

    first_name = parts[0]
    last_name = parts[-1]  # Handle middle names by taking last part

    # Handle very short names
    if len(first_name) == 1:
        first_part = first_name
    else:
        first_part = f"{first_name[0]}{'*' * (len(first_name) - 1)}"

    if len(last_name) == 1:
        last_part = last_name
    else:
        last_part = f"{last_name[0]}{'*' * (len(last_name) - 1)}"

    return f"{first_part} {last_part}"


# Load environment variables
load_dotenv()

app = Flask(__name__)
# Generate secure secret key for production if not provided
import secrets

app.secret_key = os.getenv("SECRET_KEY") or secrets.token_hex(32)

# Enable CSRF protection
csrf = CSRFProtect(app)

# Detect environment
is_development = not (os.getenv("RENDER") or os.getenv("FLASK_ENV") == "production")

# Session security configuration
if not is_development:
    app.config["SESSION_COOKIE_SECURE"] = True  # HTTPS only in production
    app.config["SESSION_COOKIE_HTTPONLY"] = True  # Prevent XSS access
    app.config["SESSION_COOKIE_SAMESITE"] = "Lax"  # CSRF protection
    app.config["PERMANENT_SESSION_LIFETIME"] = timedelta(hours=24)  # 24-hour timeout
else:
    # Development: Allow HTTP, but still protect from XSS
    app.config["SESSION_COOKIE_HTTPONLY"] = True
    app.config["SESSION_COOKIE_SAMESITE"] = "Lax"

# Configure CORS for production
if os.getenv("RENDER") or os.getenv("FLASK_ENV") == "production":
    # Production: Allow specific origins
    app_name = os.getenv("RENDER_SERVICE_NAME", "baseball-lineup-app")
    CORS(app, origins=[f"https://{app_name}.onrender.com"])
else:
    # Development: Restrict to localhost only for security
    CORS(
        app,
        origins=[
            "http://localhost:5000",
            "https://localhost:5000",
            "http://localhost:5001",
            "https://localhost:5001",
            "http://127.0.0.1:5000",
            "https://127.0.0.1:5000",
            "http://127.0.0.1:5001",
            "https://127.0.0.1:5001",
        ],
        supports_credentials=True,
    )

# Port configuration - Render provides PORT environment variable
PORT = int(os.getenv("PORT", 5001))

# TeamSnap API configuration
TEAMSNAP_CLIENT_ID = os.getenv("TEAMSNAP_CLIENT_ID")
TEAMSNAP_CLIENT_SECRET = os.getenv("TEAMSNAP_CLIENT_SECRET")
# Dynamic redirect URI based on environment
if os.getenv("RENDER"):
    # Production on Render
    app_name = os.getenv("RENDER_SERVICE_NAME", "baseball-lineup-app")
    TEAMSNAP_REDIRECT_URI = f"https://{app_name}.onrender.com/auth/callback"
else:
    # Development
    TEAMSNAP_REDIRECT_URI = os.getenv(
        "TEAMSNAP_REDIRECT_URI", f"https://localhost:{PORT}/auth/callback"
    )
TEAMSNAP_API_BASE = "https://api.teamsnap.com/v3"
TEAMSNAP_AUTH_BASE = "https://auth.teamsnap.com"

# Multi-sport configuration
VALID_SPORTS = ["baseball", "volleyball", "soccer"]

# Baseball positions
FIELDING_POSITIONS = {
    1: "Pitcher",
    2: "Catcher",
    3: "First Base",
    4: "Second Base",
    5: "Third Base",
    6: "Shortstop",
    7: "Left Field",
    8: "Center Field",
    9: "Right Field",
}

# Error messages
ERROR_NOT_AUTHENTICATED = "Not authenticated"


@app.route("/")
def index():
    """Sport selection landing page"""
    return render_template("landing.html")


@app.route("/baseball")
def baseball_dashboard():
    """Baseball lineup manager dashboard"""
    if "access_token" not in session:
        return render_template("login.html", sport="baseball")

    return render_template("baseball_dashboard.html")


@app.route("/volleyball")
def volleyball_dashboard():
    """Volleyball lineup manager dashboard"""
    if "access_token" not in session:
        return render_template("login.html", sport="volleyball")

    return render_template("volleyball_dashboard.html")


@app.route("/soccer")
def soccer_dashboard():
    """Soccer lineup manager dashboard (coming soon)"""
    return render_template("soccer_dashboard.html", sport="soccer")


@app.route("/auth/login")
def login():
    """Redirect to TeamSnap OAuth"""
    # Preserve sport context for post-auth redirect
    sport = request.args.get("sport", "baseball")
    # Validate sport before storing in session (defense in depth)
    if sport not in VALID_SPORTS:
        sport = "baseball"
    session["oauth_sport"] = sport

    auth_url = f"{TEAMSNAP_AUTH_BASE}/oauth/authorize"
    params = {
        "client_id": TEAMSNAP_CLIENT_ID,
        "redirect_uri": TEAMSNAP_REDIRECT_URI,
        "response_type": "code",
        "scope": "read write",
    }

    auth_redirect = f"{auth_url}?{urlencode(params)}"
    return redirect(auth_redirect)


@app.route("/auth/callback")
def auth_callback():
    """Handle OAuth callback from TeamSnap"""
    code = request.args.get("code")
    if not code:
        return "Authentication failed", 400

    # Exchange code for access token
    token_url = f"{TEAMSNAP_AUTH_BASE}/oauth/token"
    token_data = {
        "client_id": TEAMSNAP_CLIENT_ID,
        "client_secret": TEAMSNAP_CLIENT_SECRET,
        "redirect_uri": TEAMSNAP_REDIRECT_URI,
        "grant_type": "authorization_code",
        "code": code,
    }

    try:
        response = requests.post(token_url, data=token_data)
        response.raise_for_status()
        token_info = response.json()

        session["access_token"] = token_info["access_token"]

        # Retrieve sport context and redirect to correct dashboard
        sport = session.pop("oauth_sport", "baseball")

        # Validate sport and construct route name
        if sport not in VALID_SPORTS:
            sport = "baseball"

        return redirect(url_for(f"{sport}_dashboard"))

    except requests.RequestException as e:
        return f"Token exchange failed: {str(e)}", 400


@app.route("/api/teams")
def get_teams():
    """Get user's teams from TeamSnap or demo data"""
    if "access_token" not in session:
        return jsonify({"error": ERROR_NOT_AUTHENTICATED}), 401

    # Demo mode handling
    if session.get("demo_mode"):
        demo_data = load_demo_data()
        if demo_data:
            # Return demo team in Collection+JSON format
            return jsonify(
                {
                    "collection": {
                        "items": [
                            {
                                "data": [
                                    {"name": "id", "value": demo_data["team"]["id"]},
                                    {
                                        "name": "name",
                                        "value": demo_data["team"]["name"],
                                    },
                                    {"name": "location", "value": "Demo City"},
                                ]
                            }
                        ]
                    }
                }
            )
        else:
            return jsonify({"error": "Demo data not available"}), 500

    headers = {"Authorization": f"Bearer {session['access_token']}"}

    try:
        # First, get user info
        me_response = requests.get(f"{TEAMSNAP_API_BASE}/me", headers=headers)
        me_response.raise_for_status()
        me_data = me_response.json()

        # Debug: log the me response structure
        print("ME Response:", me_data)

        # Get user ID from me response
        user_id = None
        if "collection" in me_data and "items" in me_data["collection"]:
            for item in me_data["collection"]["items"]:
                for data in item.get("data", []):
                    if data["name"] == "id":
                        user_id = data["value"]
                        break

        # Look for user-specific teams link
        teams_url = None
        if "collection" in me_data and "items" in me_data["collection"]:
            for item in me_data["collection"]["items"]:
                for link in item.get("links", []):
                    if link.get("rel") == "teams":
                        teams_url = link.get("href")
                        break

        # If no user-specific teams link, construct the search URL with user_id
        if not teams_url and user_id:
            teams_url = f"{TEAMSNAP_API_BASE}/teams/search?user_id={user_id}"

        if teams_url:
            print(f"Teams URL: {teams_url}")
            teams_response = requests.get(teams_url, headers=headers)
            teams_response.raise_for_status()
            teams_data = teams_response.json()
            print("Teams Response:", teams_data)
            return jsonify(teams_data)
        else:
            return jsonify({"error": "Teams URL not found", "debug": me_data}), 404

    except requests.RequestException as e:
        print(f"API Error: {str(e)}")
        return jsonify({"error": f"API request failed: {str(e)}"}), 500


@app.route("/api/games/<team_id>")
def get_games(team_id):
    """Get recent games for a team or demo data"""
    if "access_token" not in session:
        return jsonify({"error": ERROR_NOT_AUTHENTICATED}), 401

    # Demo mode handling
    if session.get("demo_mode"):
        demo_data = load_demo_data()
        if demo_data and team_id == demo_data["team"]["id"]:
            # Transform demo games to match expected format
            transformed_games = []
            for game in demo_data["games"]:
                # Convert time format (e.g., "10:00 AM" to "10:00")
                time_str = game["time"]
                if "AM" in time_str or "PM" in time_str:
                    time_obj = datetime.strptime(time_str, "%I:%M %p")
                    time_24h = time_obj.strftime("%H:%M")
                else:
                    time_24h = time_str

                transformed_games.append(
                    {
                        "id": game["id"],
                        "name": f"vs {game['opponent']}",
                        "starts_at": f"{game['date']}T{time_24h}:00Z",
                        "location": "Demo Stadium",
                    }
                )
            return jsonify({"games": transformed_games})
        else:
            return jsonify({"error": "Demo team not found"}), 404

    headers = {"Authorization": f"Bearer {session['access_token']}"}

    # Check if we should include all games regardless of state
    include_all_states = (
        request.args.get("include_all_states", "false").lower() == "true"
    )

    try:
        if include_all_states:
            # Get all events for this team (no date filter)
            events_url = f"{TEAMSNAP_API_BASE}/events/search?team_id={team_id}"
            print(f"Events URL (ALL STATES): {events_url}")
        else:
            # Use the events search endpoint with team_id parameter and date filter
            today = datetime.now().strftime("%Y-%m-%d")
            thirty_days_later = (datetime.now() + timedelta(days=30)).strftime(
                "%Y-%m-%d"
            )
            events_url = f"{TEAMSNAP_API_BASE}/events/search?team_id={team_id}&started_after={today}&started_before={thirty_days_later}"
            print(f"Events URL (UPCOMING): {events_url}")

        response = requests.get(events_url, headers=headers)
        response.raise_for_status()

        events_data = response.json()

        # Filter games based on request type
        games = []
        all_events = []
        # Make timezone-aware datetime for comparison
        from datetime import timezone

        now = datetime.now(timezone.utc)

        print("\n" + "=" * 80)
        filter_type = (
            "ALL GAMES (ANY STATE)" if include_all_states else "UPCOMING GAMES"
        )
        print(f"🏟️  SEARCHING FOR {filter_type} - Team ID: {team_id}")
        print("=" * 80)
        print(f"📅 Current time: {now.strftime('%Y-%m-%d %H:%M:%S')}")
        if not include_all_states:
            thirty_days = now + timedelta(days=30)
            print(f"📅 Looking until: {thirty_days.strftime('%Y-%m-%d %H:%M:%S')}")
        print()

        total_events = len(events_data.get("collection", {}).get("items", []))
        print(f"📋 Found {total_events} total events for this team:")
        print("-" * 50)

        for i, item in enumerate(events_data.get("collection", {}).get("items", []), 1):
            event_data = {d["name"]: d.get("value") for d in item.get("data", [])}
            all_events.append(event_data)

            # Debug: Show raw event data for first few events
            if i <= 3:
                print(f"🔍 RAW EVENT {i} DATA:")
                for key, value in event_data.items():
                    print(f"    {key}: {value}")
                print()

            # Use formatted_title if name is empty, fallback to label
            event_name = (
                event_data.get("name")
                or event_data.get("formatted_title")
                or event_data.get("label")
                or "Unnamed Event"
            )
            is_game = event_data.get("is_game", False)
            starts_at = event_data.get("start_date", "No date")

            print(f"{i:2d}. 📝 {event_name}")
            print(f"    🏆 Is Game: {'YES' if is_game else 'NO'}")
            print(f"    📅 Start: {starts_at}")

            # Check if it's a game and upcoming
            if is_game and starts_at and starts_at != "No date":
                try:
                    # Handle TeamSnap's UTC datetime format
                    start_time_str = starts_at
                    if start_time_str.endswith("Z"):
                        # Remove Z and add UTC timezone
                        start_time = datetime.fromisoformat(
                            start_time_str.replace("Z", "+00:00")
                        )
                    else:
                        # Assume UTC if no timezone
                        start_time = datetime.fromisoformat(start_time_str).replace(
                            tzinfo=timezone.utc
                        )

                    readable_date = start_time.strftime("%Y-%m-%d %H:%M:%S")

                    print(f"    🕐 Parsed: {readable_date}")

                    should_include = False
                    if include_all_states:
                        # Include all games regardless of date or state
                        should_include = True
                        print("    ✅ Including (ALL STATES mode)")
                    else:
                        # Only include future games within 30 days
                        is_future = start_time > now
                        thirty_days = now + timedelta(days=30)
                        is_within_range = start_time <= thirty_days

                        print(f"    ⏭️  Future: {'YES' if is_future else 'NO'}")
                        print(f"    📊 In Range: {'YES' if is_within_range else 'NO'}")

                        should_include = is_future and is_within_range

                    if should_include:
                        games.append(
                            {
                                "id": event_data.get("id"),
                                "name": event_name,
                                "starts_at": starts_at,
                                "location": event_data.get("location_name", "TBD"),
                            }
                        )
                        print("    ✅ ADDED TO LINEUP LIST!")
                    else:
                        is_future = start_time > now
                        reason = "Past event" if not is_future else "Too far in future"
                        print(f"    ❌ SKIPPED: {reason}")

                except (ValueError, TypeError) as e:
                    print(f"    ❌ DATE ERROR: {e}")
                    continue
            else:
                if not is_game:
                    print("    ⚠️  SKIPPED: Not marked as a game")
                else:
                    print("    ⚠️  SKIPPED: No start time")

            print()  # Blank line between events

        print("=" * 80)
        print("📊 SUMMARY:")
        print(f"   Total Events: {len(all_events)}")
        game_type = "Games (All States)" if include_all_states else "Upcoming Games"
        print(f"   {game_type}: {len(games)}")
        print("=" * 80)

        print(f"Found {len(games)} {game_type.lower()}")
        return jsonify({"games": games})

    except requests.RequestException as e:
        print(f"Games API Error: {str(e)}")
        return jsonify({"error": f"API request failed: {str(e)}"}), 500


@app.route("/api/availability/<event_id>")
def get_availability(event_id):
    """Get player availability for a specific game or demo data"""
    if "access_token" not in session:
        return jsonify({"error": ERROR_NOT_AUTHENTICATED}), 401

    # Demo mode handling
    if session.get("demo_mode"):
        demo_data = load_demo_data()
        if demo_data:
            # Find the game in demo data
            for game in demo_data["games"]:
                if game["id"] == event_id:
                    # Return all demo players as attending
                    return jsonify({"attending_players": demo_data["players"]})
            return jsonify({"error": "Demo game not found"}), 404
        else:
            return jsonify({"error": "Demo data not available"}), 500

    headers = {"Authorization": f"Bearer {session['access_token']}"}

    try:
        print(f"\n🔍 GETTING AVAILABILITY FOR EVENT: {event_id}")
        print("=" * 60)

        # Use search endpoint instead of direct path
        avail_url = f"{TEAMSNAP_API_BASE}/availabilities/search?event_id={event_id}"
        print(f"📡 Availability URL: {avail_url}")

        response = requests.get(avail_url, headers=headers)
        response.raise_for_status()

        availability_data = response.json()
        print(
            f"📊 Found {len(availability_data.get('collection', {}).get('items', []))} availability records"
        )

        attending_players = []

        for i, item in enumerate(
            availability_data.get("collection", {}).get("items", []), 1
        ):
            avail_info = {d["name"]: d.get("value") for d in item.get("data", [])}

            # Debug first few availability records
            if i <= 3:
                print(f"\n📋 AVAILABILITY RECORD {i}:")
                for key, value in avail_info.items():
                    print(f"    {key}: {value}")

            member_id = avail_info.get("member_id")
            status_code = avail_info.get("status_code")

            # Decode status codes for better debugging
            status_meaning = {
                0: "No Response/Unknown",
                1: "Yes/Attending",
                2: "No/Not Attending",
                3: "Maybe",
            }
            status_text = status_meaning.get(status_code, f"Unknown ({status_code})")

            print(f"👤 Member {member_id}: Status {status_code} = {status_text}")

            if status_code == 1:  # Only include confirmed attending players
                if member_id:
                    # Get member details using search endpoint
                    member_url = f"{TEAMSNAP_API_BASE}/members/search?id={member_id}"
                    member_response = requests.get(member_url, headers=headers)

                    if member_response.status_code == 200:
                        member_data = member_response.json()

                        if member_data.get("collection", {}).get("items"):
                            member_info = {
                                d["name"]: d.get("value")
                                for d in member_data["collection"]["items"][0].get(
                                    "data", []
                                )
                            }

                            player_name = f"{member_info.get('first_name', '')} {member_info.get('last_name', '')}".strip()
                            member_type = member_info.get("type", "unknown")
                            is_manager = member_info.get("is_manager", False)
                            is_owner = member_info.get("is_owner", False)

                            print("  📋 Member Details:")
                            print(f"    Name: {player_name}")
                            print(f"    Type: {member_type}")
                            print(f"    Is Manager: {is_manager}")
                            print(f"    Is Owner: {is_owner}")

                            # Only add players, skip managers/coaches
                            if member_type == "player" or (
                                not is_manager and not is_owner
                            ):
                                # Send both original and obfuscated names for frontend toggle
                                original_name = player_name or f"Player {member_id}"
                                obfuscated_name = obfuscate_name(original_name)

                                attending_players.append(
                                    {
                                        "id": member_id,
                                        "name": original_name,  # Send original name
                                        "obfuscated_name": obfuscated_name,  # Send obfuscated name
                                        "position_preference": None,
                                        "status_code": status_code,
                                        "type": member_type,
                                    }
                                )
                                print(
                                    f"  ✅ Added as player: {player_name} -> {obfuscated_name}"
                                )
                            else:
                                print(f"  🚫 Skipped (Manager/Coach): {player_name}")
                    else:
                        print(
                            f"  ❌ Failed to get member details: {member_response.status_code}"
                        )
            else:
                print(
                    f"  🚫 Skipped Member {member_id}: Status {status_code} = {status_text} (not attending)"
                )

        print(f"\n📊 SUMMARY: {len(attending_players)} players attending")
        print("=" * 60)

        return jsonify({"attending_players": attending_players})

    except requests.RequestException as e:
        print(f"❌ API Error: {str(e)}")
        return jsonify({"error": f"API request failed: {str(e)}"}), 500


def can_fill_all_positions(players, positions_to_fill, assignments=None):
    """
    Check if all positions can be filled with available players.
    Uses recursive backtracking to verify a valid assignment exists.
    """
    if assignments is None:
        assignments = {}

    # Base case: all positions filled
    if not positions_to_fill:
        return True

    # Get next position to fill
    position = positions_to_fill[0]
    remaining_positions = positions_to_fill[1:]

    # Try each player who can play this position
    for player in players:
        player_id = player["id"]

        # Skip if player already assigned
        if player_id in assignments.values():
            continue

        # Check if player can play this position
        prefs = player.get("position_preferences", [])
        if not prefs:  # Empty list means any position
            can_play = True
        else:  # Has specific preferences - can ONLY play those positions
            can_play = position in prefs

        if not can_play:
            continue

        # Try assigning this player
        assignments[position] = player_id

        # Recursively check if remaining positions can be filled
        if can_fill_all_positions(players, remaining_positions, assignments):
            return True

        # Backtrack
        del assignments[position]

    return False


def _get_candidates_for_position(position, players):
    """Helper: Get list of players who can play a specific position"""
    candidates = []
    for player in players:
        prefs = player.get("position_preferences", [])
        if not prefs or position in prefs:
            candidates.append(player)
    return candidates


def _calculate_position_scarcity(positions, players):
    """Helper: Calculate scarcity (number of candidates) for each position"""
    position_scarcity = []
    for pos in positions:
        candidates = _get_candidates_for_position(pos, players)
        position_scarcity.append((pos, len(candidates)))
    position_scarcity.sort(key=lambda x: x[1])
    return position_scarcity


def _create_candidate_sort_key(position, player_position_history):
    """Helper: Create a sort key function for candidate prioritization"""

    def candidate_sort_key(player):
        player_id = player["id"]
        position_count = 0
        if player_position_history and player_id in player_position_history:
            position_count = player_position_history[player_id].count(position)

        prefs = player.get("position_preferences", [])
        flexibility = len(prefs) if prefs else 9

        return (position_count, flexibility)

    return candidate_sort_key


def assign_positions_smart(
    available_players,
    available_positions,
    must_play_players,
    player_position_history=None,
):
    """
    Assign players to positions using a smart algorithm that considers:
    1. Must-play players get priority
    2. Position scarcity (positions with fewer candidates are filled first)
    3. Player flexibility (less flexible players are assigned first)
    4. Position rotation (prefer positions players haven't played recently)
    """
    assignments = {}
    remaining_players = available_players.copy()
    remaining_positions = available_positions.copy()

    # First, ensure we can fill all positions
    if not can_fill_all_positions(remaining_players, remaining_positions):
        print("  ⚠️  WARNING: Cannot fill all positions with current constraints!")
        return None

    # Sort positions by scarcity (fewest candidates first)
    position_scarcity = _calculate_position_scarcity(
        remaining_positions, remaining_players
    )

    # Assign positions in order of scarcity
    for position, _ in position_scarcity:
        candidates = _get_candidates_for_position(position, remaining_players)

        # Prioritize must-play players
        must_play_candidates = [p for p in candidates if p in must_play_players]
        if must_play_candidates:
            candidates = must_play_candidates

        # Sort candidates by rotation history and flexibility
        candidates.sort(
            key=_create_candidate_sort_key(position, player_position_history)
        )

        if candidates:
            chosen_player = candidates[0]
            assignments[position] = chosen_player
            remaining_players.remove(chosen_player)

    return assignments


@app.route("/api/lineup/generate", methods=["POST"])
def generate_lineup():
    """Generate lineups using sport-specific generator via factory pattern."""
    from sports.models.lineup import Player
    from sports.services import (
        get_lineup_generator,
        get_supported_sports,
        is_sport_supported,
    )

    data = request.get_json()

    # Extract request data
    sport_id = data.get(
        "sport", "baseball"
    )  # Default to baseball for backwards compatibility
    players_data = data.get("players", [])
    game_info_data = data.get("game_info", {})

    # Validate input
    if players_data is None:
        return jsonify({"error": "Players array is required"}), 400

    if not isinstance(players_data, list):
        return jsonify({"error": "Players must be an array"}), 400

    if len(players_data) < 9:
        return jsonify({"error": "Need at least 9 players for a full lineup"}), 400

    # Validate sport
    if not is_sport_supported(sport_id):
        supported = ", ".join(get_supported_sports())
        return (
            jsonify(
                {
                    "error": f"Sport '{sport_id}' is not yet supported. Supported sports: {supported}"
                }
            ),
            400,
        )

    try:
        # Convert JSON player data to Player objects
        players = []
        for p_data in players_data:
            try:
                player = Player.from_dict(p_data)
                players.append(player)
            except (KeyError, ValueError) as e:
                return jsonify({"error": f"Invalid player data: {str(e)}"}), 400

        # Add default game_info fields if not provided
        if "game_id" not in game_info_data:
            game_info_data["game_id"] = "web_generated"
        if "team_id" not in game_info_data:
            game_info_data["team_id"] = "web_team"

        # Get the appropriate generator for this sport
        generator = get_lineup_generator(sport_id)

        # Generate lineups
        lineups = generator.generate(players, game_info_data)

        # Convert lineups to JSON format
        lineups_json = [lineup.to_dict() for lineup in lineups]

        return jsonify(
            {
                "lineups": lineups_json,
                "sport": sport_id,
                "num_periods": len(lineups),
                "total_players": len(players),
            }
        )

    except ValueError as e:
        # Validation errors from generator
        return jsonify({"error": str(e)}), 400
    except NotImplementedError as e:
        # Sport not yet implemented
        return jsonify({"error": str(e)}), 501
    except Exception as e:
        # Unexpected errors
        import traceback

        traceback.print_exc()
        return jsonify({"error": f"Internal server error: {str(e)}"}), 500


def load_demo_data(sport=None):
    """Load demo data from JSON file based on sport"""
    import json

    # Determine which sport's demo data to load
    if sport is None:
        sport = session.get("demo_sport", "baseball")

    # Map sport to demo data file
    demo_files = {
        "baseball": "static/demo-data.json",
        "volleyball": "static/volleyball-demo-data.json",
        "soccer": "static/demo-data.json",  # Fallback to baseball for now
    }

    demo_file = demo_files.get(sport, "static/demo-data.json")

    try:
        with open(demo_file, "r") as f:
            return json.load(f)
    except FileNotFoundError:
        print(f"Demo data file not found: {demo_file}")
        return None
    except json.JSONDecodeError as e:
        print(f"Error parsing demo data: {e}")
        return None


@app.route("/demo")
@app.route("/demo/<sport>")
def demo_mode(sport="baseball"):
    """Initialize demo mode and redirect to sport-specific dashboard"""
    session["demo_mode"] = True
    session["access_token"] = "demo_token"  # Fake token for demo mode

    # Validate sport and redirect to sport-specific dashboard
    if sport not in VALID_SPORTS:
        sport = "baseball"  # Default to baseball for backwards compatibility

    # Store the sport in session for demo data loading
    session["demo_sport"] = sport

    return redirect(url_for(f"{sport}_dashboard"))


@app.route("/logout")
def logout():
    """Clear session and logout"""
    session.clear()
    return redirect(url_for("index"))


if __name__ == "__main__":
    port = PORT

    # Check if running in production (Render sets this)
    is_production = os.getenv("RENDER") or os.getenv("FLASK_ENV") == "production"
    debug = not is_production and os.getenv("FLASK_DEBUG", "True").lower() == "true"

    if debug and os.getenv("FLASK_SSL", "false").lower() == "true":
        # Development with SSL
        import ssl

        context = ssl.create_default_context(ssl.Purpose.CLIENT_AUTH)
        context.load_cert_chain("cert.pem", "key.pem")
        app.run(host="0.0.0.0", port=port, debug=debug, ssl_context=context)
    else:
        # Production (Render) or development without SSL
        # Render handles SSL automatically, no need for SSL context
        app.run(host="0.0.0.0", port=port, debug=debug)
