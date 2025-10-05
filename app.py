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
from flask import (Flask, jsonify, redirect, render_template, request, session,
                   url_for)
from flask_cors import CORS


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
    # Development: Allow all origins
    CORS(app)

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


@app.route("/")
def index():
    """Main dashboard"""
    if "access_token" not in session:
        return render_template("login.html")

    return render_template("dashboard.html")


@app.route("/auth/login")
def login():
    """Redirect to TeamSnap OAuth"""
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
        return redirect(url_for("index"))

    except requests.RequestException as e:
        return f"Token exchange failed: {str(e)}", 400


@app.route("/api/teams")
def get_teams():
    """Get user's teams from TeamSnap or demo data"""
    if "access_token" not in session:
        return jsonify({"error": "Not authenticated"}), 401

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
        return jsonify({"error": "Not authenticated"}), 401

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
                        print(f"    ✅ Including (ALL STATES mode)")
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
                        print(f"    ✅ ADDED TO LINEUP LIST!")
                    else:
                        is_future = start_time > now
                        reason = "Past event" if not is_future else "Too far in future"
                        print(f"    ❌ SKIPPED: {reason}")

                except (ValueError, TypeError) as e:
                    print(f"    ❌ DATE ERROR: {e}")
                    continue
            else:
                if not is_game:
                    print(f"    ⚠️  SKIPPED: Not marked as a game")
                else:
                    print(f"    ⚠️  SKIPPED: No start time")

            print()  # Blank line between events

        print("=" * 80)
        print(f"📊 SUMMARY:")
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
        return jsonify({"error": "Not authenticated"}), 401

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

                            print(f"  📋 Member Details:")
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


def assign_positions_smart(
    available_players,
    available_positions,
    must_play_players,
    position_candidates,
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
        # Fall back to simple assignment
        return None

    # Sort positions by scarcity (fewest candidates first)
    position_scarcity = []
    for pos in remaining_positions:
        candidates = []
        for p in remaining_players:
            prefs = p.get("position_preferences", [])
            if not prefs:  # Can play any position
                candidates.append(p)
            elif pos in prefs:  # Can ONLY play specified positions
                candidates.append(p)
        position_scarcity.append((pos, len(candidates)))
    position_scarcity.sort(key=lambda x: x[1])

    # Assign positions in order of scarcity
    for position, _ in position_scarcity:
        # Get candidates for this position
        candidates = []
        for p in remaining_players:
            prefs = p.get("position_preferences", [])
            if not prefs:  # Can play any position
                candidates.append(p)
            elif position in prefs:  # Can ONLY play specified positions
                candidates.append(p)

        # Prioritize must-play players
        must_play_candidates = [p for p in candidates if p in must_play_players]
        if must_play_candidates:
            candidates = must_play_candidates

        # Sort candidates by:
        # 1. How many times they've played this position (prefer rotation)
        # 2. Their flexibility (less flexible players first)
        def candidate_sort_key(player):
            player_id = player["id"]
            position_count = 0
            if player_position_history and player_id in player_position_history:
                position_count = player_position_history[player_id].count(position)

            prefs = player.get("position_preferences", [])
            flexibility = len(prefs) if prefs else 9

            # Return tuple: (times played this position, flexibility)
            return (position_count, flexibility)

        candidates.sort(key=candidate_sort_key)

        if candidates:
            chosen_player = candidates[0]
            assignments[position] = chosen_player
            remaining_players.remove(chosen_player)

    return assignments


@app.route("/api/lineup/generate", methods=["POST"])
def generate_lineup():
    """Generate 3 complete lineups for 6-inning game with pitcher rotation"""
    data = request.get_json()
    players = data.get("players", [])

    if len(players) < 9:
        return jsonify({"error": "Need at least 9 players for a full lineup"}), 400

    print(f"\n⚾ GENERATING 3 LINEUPS FOR 6-INNING GAME ({len(players)} PLAYERS)")
    print("=" * 70)

    # Create a mapping of position -> list of players who can play it
    position_candidates = {pos: [] for pos in range(1, 10)}
    flexible_players = []  # Players who can play any position

    for player in players:
        prefs = player.get("position_preferences", [])
        if not prefs:  # Empty array means any position
            flexible_players.append(player)
            for pos in range(1, 10):
                position_candidates[pos].append(player)
        else:
            for pos in prefs:
                position_candidates[pos].append(player)

    # Check if we have at least one player who can pitch
    if len(position_candidates[1]) < 1:
        return jsonify({"error": "Need at least 1 player who can pitch"}), 400

    # Log position availability
    print(f"🥎 Position availability:")
    for pos, candidates in position_candidates.items():
        pos_name = FIELDING_POSITIONS[pos]
        print(f"  {pos}. {pos_name}: {len(candidates)} players")
    print(f"🥎 Flexible players (any position): {len(flexible_players)}")

    lineups = []
    used_catchers = []

    # Track consecutive innings on bench for each player
    bench_tracker = {player["id"]: 0 for player in players}

    # Track which positions each player has played across lineups
    player_position_history = {player["id"]: [] for player in players}

    # Get all available pitchers
    available_pitchers = position_candidates[1].copy()
    print(f"\n⚾ GENERATING {len(available_pitchers)} LINEUPS (One per pitcher)")

    # Generate one lineup for each pitcher
    for lineup_num, pitcher in enumerate(available_pitchers):
        print(f"\n🏟️ LINEUP {lineup_num + 1} - Pitcher: {pitcher['name']}")
        print("-" * 40)

        # Show position rotation info
        if lineup_num > 0:
            print(
                "  🔄 Position rotation active - players will try different positions"
            )

        lineup = {}
        assigned_players = set()
        available_positions = list(FIELDING_POSITIONS.keys())

        # First, identify players who MUST play (sat out 2 consecutive lineups)
        must_play_players = []
        if lineup_num > 0:  # Can only check after first lineup
            for player_id, bench_count in bench_tracker.items():
                if bench_count >= 2:  # Player has sat out 2 consecutive lineups
                    player = next(p for p in players if p["id"] == player_id)
                    must_play_players.append(player)
                    print(
                        f"  ⚠️  MUST PLAY: {player['name']} (sat out {bench_count} lineups)"
                    )

        # Pitcher is already determined from the loop

        lineup[1] = {
            "player_name": pitcher["name"],
            "position_name": FIELDING_POSITIONS[1],
        }
        assigned_players.add(pitcher["id"])
        available_positions.remove(1)
        # Track pitcher position history
        player_position_history[pitcher["id"]].append(1)
        print(f"  🥎 Pitcher: {pitcher['name']}")

        # Assign catcher (prioritize must-play players)
        catcher = None

        # Get available catchers
        available_catchers = [
            p for p in position_candidates[2] if p["id"] not in assigned_players
        ]

        # Check if any must-play player can catch
        for p in must_play_players:
            if p["id"] not in assigned_players and p in available_catchers:
                catcher = p
                break

        # If no must-play catcher, use rotation logic
        if not catcher and available_catchers:
            # Rotate catchers if multiple available
            catchers_not_used = [
                p for p in available_catchers if p["id"] not in used_catchers
            ]
            if not catchers_not_used:
                # Reset rotation
                used_catchers = []
                catchers_not_used = available_catchers

            if catchers_not_used:
                # Prefer specialized catchers (those with fewer position options)
                catchers_not_used.sort(
                    key=lambda p: (
                        len(p.get("position_preferences", []))
                        if p.get("position_preferences")
                        else 9
                    )
                )
                catcher = catchers_not_used[0]
                used_catchers.append(catcher["id"])

        if catcher:
            lineup[2] = {
                "player_name": catcher["name"],
                "position_name": FIELDING_POSITIONS[2],
            }
            assigned_players.add(catcher["id"])
            available_positions.remove(2)
            # Track catcher position history
            player_position_history[catcher["id"]].append(2)
            print(f"  🥎 Catcher: {catcher['name']}")

        # Assign remaining positions using smart algorithm
        # Get unassigned players prioritizing must-play and bench time
        remaining_must_play = [
            p for p in must_play_players if p["id"] not in assigned_players
        ]
        remaining_players = [p for p in players if p["id"] not in assigned_players]

        # Try smart assignment first with position history
        assignments = assign_positions_smart(
            remaining_players,
            available_positions,
            remaining_must_play,
            position_candidates,
            player_position_history,
        )

        if assignments:
            # Use smart assignments
            for position, player in assignments.items():
                lineup[position] = {
                    "player_name": player["name"],
                    "position_name": FIELDING_POSITIONS[position],
                }
                assigned_players.add(player["id"])
                # Track position history for rotation
                player_position_history[player["id"]].append(position)
                print(f"  {FIELDING_POSITIONS[position]}: {player['name']}")
        else:
            # Fallback to simple assignment with bench time priority
            remaining_players.sort(key=lambda p: bench_tracker[p["id"]], reverse=True)
            all_remaining = remaining_must_play + [
                p for p in remaining_players if p not in remaining_must_play
            ]

            # Simple assignment
            for position in available_positions:
                if all_remaining:
                    # Find first player who can play this position
                    assigned = False
                    for i, player in enumerate(all_remaining):
                        prefs = player.get("position_preferences", [])
                        can_play = False

                        if not prefs:  # Empty list = can play any position
                            can_play = True
                        elif (
                            position in prefs
                        ):  # Has preferences and this position is one of them
                            can_play = True

                        if can_play:
                            lineup[position] = {
                                "player_name": player["name"],
                                "position_name": FIELDING_POSITIONS[position],
                            }
                            assigned_players.add(player["id"])
                            # Track position history for rotation
                            player_position_history[player["id"]].append(position)
                            print(f"  {FIELDING_POSITIONS[position]}: {player['name']}")
                            all_remaining.pop(i)
                            assigned = True
                            break

                    if not assigned:
                        # This should not happen if position preferences are set correctly
                        print(
                            f"  ❌ ERROR: No valid player for {FIELDING_POSITIONS[position]}!"
                        )
                        if all_remaining:
                            # Emergency assignment - this violates position preferences
                            player = all_remaining.pop(0)
                            lineup[position] = {
                                "player_name": player["name"],
                                "position_name": FIELDING_POSITIONS[position],
                            }
                            assigned_players.add(player["id"])
                            print(
                                f"  ⚠️  WARNING: {player['name']} forced to {FIELDING_POSITIONS[position]} (violates preferences!)"
                            )

        # Update bench tracking
        for player in players:
            if player["id"] in assigned_players:
                bench_tracker[player["id"]] = 0  # Reset bench count
            else:
                bench_tracker[player["id"]] += 1  # Increment bench count

        # Bench players
        bench = [p for p in players if p["id"] not in assigned_players]

        lineups.append({"lineup": lineup, "bench": bench, "pitcher": pitcher["name"]})

        bench_info = ", ".join(
            [f"{p['name']} ({bench_tracker[p['id']]} lineups)" for p in bench]
        )
        print(f"  📋 Bench ({len(bench)}): {bench_info}")

    # Verify no player sat out more than 2 consecutive lineups
    max_bench_time = max(bench_tracker.values()) if bench_tracker else 0
    if max_bench_time > 2:
        print(f"\n⚠️  WARNING: Some players sat out {max_bench_time} lineups!")

    print(f"\n📊 SUMMARY: {len(lineups)} lineups generated (one per pitcher)")
    print(f"📊 Max consecutive bench time: {max_bench_time} lineups (should be ≤ 2)")
    print("=" * 70)

    return jsonify(
        {
            "lineups": lineups,
            "positions": FIELDING_POSITIONS,
            "game_format": f"{len(lineups)} lineups available - one per pitcher",
        }
    )


def load_demo_data():
    """Load demo data from JSON file"""
    import json

    try:
        with open("static/demo-data.json", "r") as f:
            return json.load(f)
    except FileNotFoundError:
        print("Demo data file not found!")
        return None
    except json.JSONDecodeError as e:
        print(f"Error parsing demo data: {e}")
        return None


@app.route("/demo")
def demo_mode():
    """Initialize demo mode and redirect to dashboard"""
    session["demo_mode"] = True
    session["access_token"] = "demo_token"  # Fake token for demo mode
    return redirect(url_for("index"))


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
