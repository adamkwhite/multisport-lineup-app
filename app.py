#!/usr/bin/env python3
"""
Baseball Lineup Manager - TeamSnap Integration
Main Flask application for managing baseball fielding positions
"""

import os
from flask import Flask, render_template, request, redirect, url_for, session, jsonify
from flask_cors import CORS
from dotenv import load_dotenv
import requests
from datetime import datetime, timedelta
import random

# Load environment variables
load_dotenv()

app = Flask(__name__)
app.secret_key = os.getenv('SECRET_KEY', 'dev-secret-key-change-in-production')
CORS(app)

# TeamSnap API configuration
TEAMSNAP_CLIENT_ID = os.getenv('TEAMSNAP_CLIENT_ID')
TEAMSNAP_CLIENT_SECRET = os.getenv('TEAMSNAP_CLIENT_SECRET')
TEAMSNAP_REDIRECT_URI = os.getenv('TEAMSNAP_REDIRECT_URI', 'https://localhost:5000/auth/callback')
TEAMSNAP_API_BASE = 'https://api.teamsnap.com/v3'
TEAMSNAP_AUTH_BASE = 'https://auth.teamsnap.com'

# Baseball positions
FIELDING_POSITIONS = {
    1: 'Pitcher',
    2: 'Catcher', 
    3: 'First Base',
    4: 'Second Base',
    5: 'Third Base',
    6: 'Shortstop',
    7: 'Left Field',
    8: 'Center Field',
    9: 'Right Field'
}

@app.route('/')
def index():
    """Main dashboard"""
    if 'access_token' not in session:
        return render_template('login.html')
    
    return render_template('dashboard.html')

@app.route('/auth/login')
def login():
    """Redirect to TeamSnap OAuth"""
    auth_url = f"{TEAMSNAP_AUTH_BASE}/oauth/authorize"
    params = {
        'client_id': TEAMSNAP_CLIENT_ID,
        'redirect_uri': TEAMSNAP_REDIRECT_URI,
        'response_type': 'code',
        'scope': 'read write'
    }
    
    auth_redirect = f"{auth_url}?{'&'.join([f'{k}={v}' for k, v in params.items()])}"
    return redirect(auth_redirect)

@app.route('/auth/callback')
def auth_callback():
    """Handle OAuth callback from TeamSnap"""
    code = request.args.get('code')
    if not code:
        return "Authentication failed", 400
    
    # Exchange code for access token
    token_url = f"{TEAMSNAP_AUTH_BASE}/oauth/token"
    token_data = {
        'client_id': TEAMSNAP_CLIENT_ID,
        'client_secret': TEAMSNAP_CLIENT_SECRET,
        'redirect_uri': TEAMSNAP_REDIRECT_URI,
        'grant_type': 'authorization_code',
        'code': code
    }
    
    try:
        response = requests.post(token_url, data=token_data)
        response.raise_for_status()
        token_info = response.json()
        
        session['access_token'] = token_info['access_token']
        return redirect(url_for('index'))
        
    except requests.RequestException as e:
        return f"Token exchange failed: {str(e)}", 400

@app.route('/api/teams')
def get_teams():
    """Get user's teams from TeamSnap"""
    if 'access_token' not in session:
        return jsonify({'error': 'Not authenticated'}), 401
    
    headers = {'Authorization': f"Bearer {session['access_token']}"}
    
    try:
        # First, get user info
        me_response = requests.get(f"{TEAMSNAP_API_BASE}/me", headers=headers)
        me_response.raise_for_status()
        me_data = me_response.json()
        
        # Debug: log the me response structure
        print("ME Response:", me_data)
        
        # Get user ID from me response 
        user_id = None
        if 'collection' in me_data and 'items' in me_data['collection']:
            for item in me_data['collection']['items']:
                for data in item.get('data', []):
                    if data['name'] == 'id':
                        user_id = data['value']
                        break
        
        # Look for user-specific teams link
        teams_url = None
        if 'collection' in me_data and 'items' in me_data['collection']:
            for item in me_data['collection']['items']:
                for link in item.get('links', []):
                    if link.get('rel') == 'teams':
                        teams_url = link.get('href')
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
            return jsonify({'error': 'Teams URL not found', 'debug': me_data}), 404
            
    except requests.RequestException as e:
        print(f"API Error: {str(e)}")
        return jsonify({'error': f'API request failed: {str(e)}'}), 500

@app.route('/api/games/<team_id>')
def get_games(team_id):
    """Get recent games for a team"""
    if 'access_token' not in session:
        return jsonify({'error': 'Not authenticated'}), 401
    
    headers = {'Authorization': f"Bearer {session['access_token']}"}
    
    try:
        # Use the events search endpoint with team_id parameter and date filter
        today = datetime.now().strftime('%Y-%m-%d')
        thirty_days_later = (datetime.now() + timedelta(days=30)).strftime('%Y-%m-%d')
        events_url = f"{TEAMSNAP_API_BASE}/events/search?team_id={team_id}&started_after={today}&started_before={thirty_days_later}"
        print(f"Events URL: {events_url}")
        
        response = requests.get(events_url, headers=headers)
        response.raise_for_status()
        
        events_data = response.json()
        
        # Filter for upcoming games (next 30 days)
        upcoming_games = []
        all_events = []
        # Make timezone-aware datetime for comparison
        from datetime import timezone
        now = datetime.now(timezone.utc)
        thirty_days = now + timedelta(days=30)
        
        print("\n" + "="*80)
        print(f"🏟️  SEARCHING FOR GAMES - Team ID: {team_id}")
        print("="*80)
        print(f"📅 Current time: {now.strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"📅 Looking until: {thirty_days.strftime('%Y-%m-%d %H:%M:%S')}")
        print()
        
        total_events = len(events_data.get('collection', {}).get('items', []))
        print(f"📋 Found {total_events} total events for this team:")
        print("-" * 50)
        
        for i, item in enumerate(events_data.get('collection', {}).get('items', []), 1):
            event_data = {d['name']: d.get('value') for d in item.get('data', [])}
            all_events.append(event_data)
            
            # Debug: Show raw event data for first few events
            if i <= 3:
                print(f"🔍 RAW EVENT {i} DATA:")
                for key, value in event_data.items():
                    print(f"    {key}: {value}")
                print()
            
            # Use formatted_title if name is empty, fallback to label
            event_name = event_data.get('name') or event_data.get('formatted_title') or event_data.get('label') or 'Unnamed Event'
            is_game = event_data.get('is_game', False)
            starts_at = event_data.get('start_date', 'No date')
            
            print(f"{i:2d}. 📝 {event_name}")
            print(f"    🏆 Is Game: {'YES' if is_game else 'NO'}")
            print(f"    📅 Start: {starts_at}")
            
            # Check if it's a game and upcoming
            if is_game and starts_at and starts_at != 'No date':
                try:
                    # Handle TeamSnap's UTC datetime format
                    start_time_str = starts_at
                    if start_time_str.endswith('Z'):
                        # Remove Z and add UTC timezone
                        start_time = datetime.fromisoformat(start_time_str.replace('Z', '+00:00'))
                    else:
                        # Assume UTC if no timezone
                        start_time = datetime.fromisoformat(start_time_str).replace(tzinfo=timezone.utc)
                    
                    readable_date = start_time.strftime('%Y-%m-%d %H:%M:%S')
                    is_future = start_time > now
                    is_within_range = start_time <= thirty_days
                    
                    print(f"    🕐 Parsed: {readable_date}")
                    print(f"    ⏭️  Future: {'YES' if is_future else 'NO'}")
                    print(f"    📊 In Range: {'YES' if is_within_range else 'NO'}")
                    
                    if is_future and is_within_range:
                        upcoming_games.append({
                            'id': event_data.get('id'),
                            'name': event_name,
                            'starts_at': starts_at,
                            'location': event_data.get('location_name', 'TBD')
                        })
                        print(f"    ✅ ADDED TO LINEUP LIST!")
                    else:
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
        
        print("="*80)
        print(f"📊 SUMMARY:")
        print(f"   Total Events: {len(all_events)}")
        print(f"   Upcoming Games: {len(upcoming_games)}")
        print("="*80)
        
        print(f"Found {len(upcoming_games)} upcoming games")
        return jsonify({'games': upcoming_games})
        
    except requests.RequestException as e:
        print(f"Games API Error: {str(e)}")
        return jsonify({'error': f'API request failed: {str(e)}'}), 500

@app.route('/api/availability/<event_id>')
def get_availability(event_id):
    """Get player availability for a specific game"""
    if 'access_token' not in session:
        return jsonify({'error': 'Not authenticated'}), 401
    
    headers = {'Authorization': f"Bearer {session['access_token']}"}
    
    try:
        print(f"\n🔍 GETTING AVAILABILITY FOR EVENT: {event_id}")
        print("="*60)
        
        # Use search endpoint instead of direct path
        avail_url = f"{TEAMSNAP_API_BASE}/availabilities/search?event_id={event_id}"
        print(f"📡 Availability URL: {avail_url}")
        
        response = requests.get(avail_url, headers=headers)
        response.raise_for_status()
        
        availability_data = response.json()
        print(f"📊 Found {len(availability_data.get('collection', {}).get('items', []))} availability records")
        
        attending_players = []
        
        for i, item in enumerate(availability_data.get('collection', {}).get('items', []), 1):
            avail_info = {d['name']: d.get('value') for d in item.get('data', [])}
            
            # Debug first few availability records
            if i <= 3:
                print(f"\n📋 AVAILABILITY RECORD {i}:")
                for key, value in avail_info.items():
                    print(f"    {key}: {value}")
            
            member_id = avail_info.get('member_id')
            status_code = avail_info.get('status_code')
            
            # Decode status codes for better debugging
            status_meaning = {
                0: "No Response/Unknown",
                1: "Yes/Attending", 
                2: "No/Not Attending",
                3: "Maybe"
            }
            status_text = status_meaning.get(status_code, f"Unknown ({status_code})")
            
            print(f"👤 Member {member_id}: Status {status_code} = {status_text}")
            
            # Check only attending players (status code 1 = Yes/Attending)
            if status_code == 1:  # Only include confirmed attending players
                if member_id:
                    # Get member details using search endpoint
                    member_url = f"{TEAMSNAP_API_BASE}/members/search?id={member_id}"
                    member_response = requests.get(member_url, headers=headers)
                    
                    if member_response.status_code == 200:
                        member_data = member_response.json()
                        
                        if member_data.get('collection', {}).get('items'):
                            member_info = {d['name']: d.get('value') for d in member_data['collection']['items'][0].get('data', [])}
                            
                            player_name = f"{member_info.get('first_name', '')} {member_info.get('last_name', '')}".strip()
                            member_type = member_info.get('type', 'unknown')
                            is_manager = member_info.get('is_manager', False)
                            is_owner = member_info.get('is_owner', False)
                            
                            print(f"  📋 Member Details:")
                            print(f"    Name: {player_name}")
                            print(f"    Type: {member_type}")
                            print(f"    Is Manager: {is_manager}")
                            print(f"    Is Owner: {is_owner}")
                            
                            # Only add players, skip managers/coaches
                            if member_type == 'player' or (not is_manager and not is_owner):
                                attending_players.append({
                                    'id': member_id,
                                    'name': player_name or f"Player {member_id}",
                                    'position_preference': None,
                                    'status_code': status_code,
                                    'type': member_type
                                })
                                print(f"  ✅ Added as player: {player_name}")
                            else:
                                print(f"  🚫 Skipped (Manager/Coach): {player_name}")
                    else:
                        print(f"  ❌ Failed to get member details: {member_response.status_code}")
            else:
                print(f"  ⚠️  Skipped: {status_text}")
        
        print(f"\n📊 SUMMARY: {len(attending_players)} players attending")
        print("="*60)
        
        return jsonify({'attending_players': attending_players})
        
    except requests.RequestException as e:
        print(f"❌ API Error: {str(e)}")
        return jsonify({'error': f'API request failed: {str(e)}'}), 500

@app.route('/api/lineup/generate', methods=['POST'])
def generate_lineup():
    """Generate 3 complete lineups for 6-inning game with pitcher rotation"""
    data = request.get_json()
    players = data.get('players', [])
    
    if len(players) < 9:
        return jsonify({'error': 'Need at least 9 players for a full lineup'}), 400
    
    print(f"\n⚾ GENERATING 3 LINEUPS FOR 6-INNING GAME ({len(players)} PLAYERS)")
    print("="*70)
    
    # Identify potential pitchers
    pitcher_candidates = []
    catcher_candidates = []
    other_players = []
    
    for player in players:
        preference = player.get('position_preference', 'any')
        if preference == 'pitcher':
            pitcher_candidates.append(player)
        elif preference == 'catcher':
            catcher_candidates.append(player)
        else:
            other_players.append(player)
    
    # If we don't have enough designated pitchers, use other players
    all_available_pitchers = pitcher_candidates + other_players
    
    if len(all_available_pitchers) < 3:
        return jsonify({'error': 'Need at least 3 players who can pitch for 6-inning rotation'}), 400
    
    print(f"🥎 Pitcher candidates: {len(pitcher_candidates)} designated + {len(other_players)} others")
    print(f"🥎 Catcher candidates: {len(catcher_candidates)}")
    
    lineups = []
    used_pitchers = []
    used_catchers = []
    
    # Generate 3 lineups (Innings 1-2, 3-4, 5-6)
    for lineup_num in range(3):
        innings = f"{lineup_num*2 + 1}-{lineup_num*2 + 2}"
        print(f"\n🏟️ LINEUP {lineup_num + 1} (Innings {innings})")
        print("-" * 40)
        
        lineup = {}
        assigned_players = set()
        available_positions = list(FIELDING_POSITIONS.keys())
        
        # Select pitcher (avoid repeating)
        available_pitchers = [p for p in all_available_pitchers if p['id'] not in used_pitchers]
        if not available_pitchers:
            available_pitchers = all_available_pitchers  # Reset if we run out
            used_pitchers = []
        
        # Prefer designated pitchers, then others
        pitcher = None
        for p in available_pitchers:
            if p.get('position_preference') == 'pitcher':
                pitcher = p
                break
        if not pitcher:
            pitcher = available_pitchers[0]
        
        used_pitchers.append(pitcher['id'])
        
        lineup[1] = {
            'player_name': pitcher['name'],
            'position_name': FIELDING_POSITIONS[1]
        }
        assigned_players.add(pitcher['id'])
        available_positions.remove(1)
        print(f"  🥎 Pitcher: {pitcher['name']}")
        
        # Assign catcher (rotate if multiple catchers available)
        catcher = None
        if len(catcher_candidates) > 1:
            # Rotate catchers across lineups
            available_catchers = [p for p in catcher_candidates if p['id'] not in used_catchers and p['id'] not in assigned_players]
            if not available_catchers:
                # Reset rotation if we've used all catchers
                used_catchers = []
                available_catchers = [p for p in catcher_candidates if p['id'] not in assigned_players]
            
            if available_catchers:
                catcher = available_catchers[0]
                used_catchers.append(catcher['id'])
        else:
            # Single catcher or prefer any designated catcher
            available_catchers = [p for p in catcher_candidates if p['id'] not in assigned_players]
            if available_catchers:
                catcher = available_catchers[0]
        
        # If no designated catchers available, use any other player
        if not catcher:
            available_others = [p for p in other_players if p['id'] not in assigned_players]
            if available_others:
                catcher = available_others[0]
        
        if catcher:
            lineup[2] = {
                'player_name': catcher['name'],
                'position_name': FIELDING_POSITIONS[2]
            }
            assigned_players.add(catcher['id'])
            available_positions.remove(2)
            print(f"  🥎 Catcher: {catcher['name']}")
        
        # Assign remaining positions (randomize for variety across lineups)
        remaining_players = [p for p in players if p['id'] not in assigned_players]
        
        # Shuffle remaining players to randomize position assignments
        random.shuffle(remaining_players)
        
        for position in available_positions:
            if remaining_players:
                player = remaining_players.pop(0)
                lineup[position] = {
                    'player_name': player['name'],
                    'position_name': FIELDING_POSITIONS[position]
                }
                assigned_players.add(player['id'])
                print(f"  {FIELDING_POSITIONS[position]}: {player['name']}")
        
        # Bench players
        bench = [p for p in players if p['id'] not in assigned_players]
        
        lineups.append({
            'innings': innings,
            'lineup': lineup,
            'bench': bench,
            'pitcher': pitcher['name']
        })
        
        print(f"  📋 Bench ({len(bench)}): {', '.join([p['name'] for p in bench])}")
    
    print(f"\n📊 SUMMARY: 3 lineups generated with pitcher rotation")
    print("="*70)
    
    return jsonify({
        'lineups': lineups,
        'positions': FIELDING_POSITIONS,
        'game_format': '6 innings, 3 lineups, 2 innings per pitcher'
    })

@app.route('/logout')
def logout():
    """Clear session and logout"""
    session.clear()
    return redirect(url_for('index'))

if __name__ == '__main__':
    port = int(os.getenv('PORT', 5000))
    debug = os.getenv('FLASK_DEBUG', 'True').lower() == 'true'
    
    # For development - disable SSL for easier local access
    if debug and os.getenv('FLASK_SSL', 'false').lower() == 'true':
        # Create a simple SSL context for development
        import ssl
        context = ssl.create_default_context(ssl.Purpose.CLIENT_AUTH)
        context.load_cert_chain('cert.pem', 'key.pem')
        app.run(host='0.0.0.0', port=port, debug=debug, ssl_context=context)
    elif debug:
        # Run without SSL for easier local development
        app.run(host='0.0.0.0', port=port, debug=debug)
    else:
        app.run(host='0.0.0.0', port=port, debug=debug)