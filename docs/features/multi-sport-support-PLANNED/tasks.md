# Multi-Sport Frontend UI Support - Task List

**Issue:** #66
**PRD:** `docs/features/multi-sport-support-PLANNED/prd.md`
**Scope:** Frontend UI only (backend already complete)

## Relevant Files

- `templates/landing.html` - NEW: Sport selection landing page with 3 image-based boxes
- `templates/dashboard.html` - Rename to `baseball_dashboard.html` or update to be sport-agnostic
- `templates/volleyball_dashboard.html` - NEW: Volleyball-specific dashboard
- `templates/soccer_dashboard.html` - NEW: Soccer-specific dashboard (placeholder for now)
- `app.py` - Update routes: `/` (landing), `/baseball`, `/volleyball`, `/soccer`
- `static/images/` - Sport selection images (volleyball.jpg, baseball.jpg, soccer.jpg)
- `config/sports/baseball.json` - Baseball sport configuration (reference for positions)
- `config/sports/volleyball.json` - Volleyball sport configuration (reference for positions)
- `config/sports/soccer.json` - Soccer sport configuration (reference for positions)

### Notes

- Backend API already supports `sport` parameter in `/api/lineup/generate`
- Factory pattern and sport-specific generators already implemented
- Focus is purely on frontend UI and user experience
- Tests should verify sport selection persists and diagrams render correctly

## Tasks

- [ ] 1.0 Create sport selection landing page
  - [ ] 1.1 Create `templates/landing.html` with 3 sport selection boxes
  - [ ] 1.2 Design CSS grid/flexbox layout for 3 boxes (Volleyball, Baseball, Soccer order)
  - [ ] 1.3 Create image placeholders in `static/images/` directory (volleyball.jpg, baseball.jpg, soccer.jpg)
  - [ ] 1.4 Add sport box styling (hover effects, clickable cards with images)
  - [ ] 1.5 Add links: Volleyball → `/volleyball`, Baseball → `/baseball`, Soccer → `/soccer`
  - [ ] 1.6 Make layout responsive for mobile/tablet/desktop
  - [ ] 1.7 Add sport names and brief descriptions to each box

- [ ] 2.0 Update Flask routes and app structure
  - [ ] 2.1 Update `app.py` root route `/` to render `landing.html` instead of dashboard
  - [ ] 2.2 Create `/baseball` route that renders existing dashboard (rename to `baseball_dashboard.html`)
  - [ ] 2.3 Create `/volleyball` route that renders `volleyball_dashboard.html`
  - [ ] 2.4 Create `/soccer` route that renders `soccer_dashboard.html` (placeholder for future)
  - [ ] 2.5 Update `/demo` route to redirect to landing page first (or create sport-specific demo routes)
  - [ ] 2.6 Update TeamSnap OAuth callback to handle sport-specific redirects

- [ ] 3.0 Create baseball-specific dashboard
  - [ ] 3.1 Rename `templates/dashboard.html` to `templates/baseball_dashboard.html`
  - [ ] 3.2 Update all baseball dashboard references in `app.py` routes
  - [ ] 3.3 Hardcode `sport = "baseball"` in baseball dashboard JavaScript
  - [ ] 3.4 Update page title to "Baseball Lineup Manager"
  - [ ] 3.5 Test that existing baseball functionality works unchanged

- [ ] 4.0 Create volleyball-specific dashboard
  - [ ] 4.1 Copy `baseball_dashboard.html` to `volleyball_dashboard.html` as starting point
  - [ ] 4.2 Update page title to "Volleyball Lineup Manager"
  - [ ] 4.3 Hardcode `sport = "volleyball"` in volleyball dashboard JavaScript
  - [ ] 4.4 Update minimum player validation to 6 (instead of 9)
  - [ ] 4.5 Update position checkboxes to show volleyball positions (OH, MB, S, OPP, L, DS)
  - [ ] 4.6 Create `displayVolleyballLineups(data)` function for volleyball court diagram
  - [ ] 4.7 Design volleyball court HTML/CSS (6-position layout with front/back row)
  - [ ] 4.8 Add rotation indicators to volleyball court
  - [ ] 4.9 Update `generateLineup()` to pass `sport: "volleyball"` to API
  - [ ] 4.10 Replace baseball diamond with volleyball court in lineup display

- [ ] 5.0 Create soccer-specific dashboard (placeholder)
  - [ ] 5.1 Create minimal `soccer_dashboard.html` with "Coming Soon" message
  - [ ] 5.2 Add note: "Soccer support is planned - check back soon!"
  - [ ] 5.3 Include link back to landing page
  - [ ] 5.4 (Future) Full soccer implementation will be separate task

- [ ] 6.0 Testing and validation
  - [ ] 6.1 Test landing page displays 3 sport boxes correctly
  - [ ] 6.2 Test clicking Volleyball box navigates to `/volleyball`
  - [ ] 6.3 Test clicking Baseball box navigates to `/baseball`
  - [ ] 6.4 Test clicking Soccer box navigates to `/soccer` (shows coming soon)
  - [ ] 6.5 Test baseball dashboard works identically to before (regression test)
  - [ ] 6.6 Test volleyball dashboard loads and displays 6 positions
  - [ ] 6.7 Test volleyball lineup generation with 6+ players
  - [ ] 6.8 Test volleyball court diagram displays correctly
  - [ ] 6.9 Test demo mode works from landing page
  - [ ] 6.10 Test TeamSnap OAuth flow from each sport-specific page
  - [ ] 6.11 Verify responsive design works on mobile devices
