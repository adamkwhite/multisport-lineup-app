# Task List: Demo Mode Implementation

Based on PRD: Demo Mode for Baseball Lineup Manager

## Relevant Files

- `static/demo-data.json` - New file containing demo team, players (12-15 famous baseball players), and games data
- `app.py` - Main Flask application file that needs new demo mode routes and data handling functions
- `templates/login.html` - Landing page template that needs demo/TeamSnap mode selection buttons
- `templates/dashboard.html` - Main dashboard template that needs demo mode indicator and 9-inning lineup display
- `static/style.css` - Stylesheet that needs styling for demo mode indicator and landing page buttons

### Notes

- Demo mode must maintain complete separation from TeamSnap authentication flows
- All existing functionality (player filtering, position preferences, printing) must work identically in demo mode
- Static demo data file should be easily updatable for future maintenance
- 9-inning extension should work for both demo and TeamSnap modes
- Demo mode indicator should be clearly visible but not intrusive

## Tasks

- [x] 1.0 Create Demo Data File with Famous Baseball Players
  - [x] 1.1 Create `static/demo-data.json` file with team object containing name "Demo All-Stars" and id "demo-001"
  - [x] 1.2 Add players array with 15 famous baseball players including Mike Trout, Aaron Judge, Mookie Betts, Derek Jeter, Babe Ruth, Willie Mays, etc.
  - [x] 1.3 Include realistic position preferences for each player (some "pitcher", some "catcher", most "any")
  - [x] 1.4 Add jersey numbers for each player (use their real numbers where possible)
  - [x] 1.5 Create games array with 4 October 2025 games including dates, times, and opponent names
  - [x] 1.6 Validate JSON structure matches existing TeamSnap data format for compatibility

- [x] 2.0 Modify Landing Page to Show Demo vs TeamSnap Options
  - [x] 2.1 Open `templates/login.html` and locate the existing TeamSnap login section
  - [x] 2.2 Wrap existing TeamSnap content in a container div with class "mode-option teamsnap-option"
  - [x] 2.3 Add new container div with class "mode-option demo-option" containing demo mode button
  - [x] 2.4 Create "Try Demo Mode" button that links to `/demo` route
  - [x] 2.5 Add CSS in `static/style.css` to style both options as equal-sized cards or buttons
  - [x] 2.6 Update page title and description to mention both options are available

- [x] 3.0 Update Flask Routes to Handle Demo Mode Data Flow
  - [x] 3.1 In `app.py`, add new route `@app.route('/demo')` that loads demo data and redirects to dashboard
  - [x] 3.2 Create function `load_demo_data()` that reads and parses `static/demo-data.json`
  - [x] 3.3 Modify existing data loading functions to check for demo mode flag in session
  - [x] 3.4 Update `get_teams()` function to return demo team when in demo mode
  - [x] 3.5 Update `get_games()` function to return demo games when in demo mode
  - [x] 3.6 Update `get_availability()` function to return demo players when in demo mode
  - [x] 3.7 Add session variable `session['demo_mode'] = True` when demo route is accessed
  - [x] 3.8 Ensure all existing TeamSnap routes continue to work unchanged when not in demo mode

- [x] 4.0 Extend Lineup Generation Algorithm from 6 to 9 Innings
  - [x] 4.1 In `app.py`, locate the `generate_lineup()` function (around line 623)
  - [x] 4.2 Update function documentation and print statements from 6 to 9 innings
  - [x] 4.3 Maintain existing pitcher rotation logic (max 2 innings per pitcher handled by lineup-per-pitcher approach)
  - [x] 4.4 Adjust bench time calculations to work with 9 innings instead of 6 (3 consecutive lineups max instead of 2)
  - [x] 4.5 Update hardcoded "6" references in comments and print statements to "9"
  - [x] 4.6 Verified that the algorithm respects position preferences and randomization (imports random, uses position_preferences)
  - [x] 4.7 Algorithm generates lineups based on available pitchers, suitable for 9-inning games

- [x] 5.0 Add Demo Mode Visual Indicator to Header
  - [x] 5.1 In `templates/dashboard.html`, locate the header section with "⚾ Baseball Lineup Manager" (found at line 353)
  - [x] 5.2 Add conditional logic to check if `session.demo_mode` is True
  - [x] 5.3 When in demo mode, append " **(DEMO)**" text next to the app title
  - [x] 5.4 Add styling for `.demo-indicator` class with bold font weight and red color
  - [x] 5.5 Demo indicator appears in dashboard header (other pages would inherit same pattern)
  - [x] 5.6 Conditional logic ensures indicator only shows when `session.demo_mode` is True
