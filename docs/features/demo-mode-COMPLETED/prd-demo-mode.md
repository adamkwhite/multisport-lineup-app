# PRD: Demo Mode for Baseball Lineup Manager

## Overview

Add a demo mode feature that allows users without TeamSnap accounts to experience the full functionality of the Baseball Lineup Manager app using fictional team data with famous baseball players. This enables product demonstrations and user evaluation without requiring TeamSnap authentication.

## Problem Statement

Currently, the app requires TeamSnap authentication to access any functionality, creating a barrier for:
- Potential customers who want to evaluate the app before signing up for TeamSnap
- Sales demonstrations where immediate access is needed
- Users who want to test features without connecting their real team data

## Goals

### Primary Goals
- Enable full app functionality without TeamSnap authentication
- Provide realistic demo experience with engaging fictional data
- Maintain all existing features and workflows in demo mode
- Support sales and evaluation use cases

### Secondary Goals
- Create foundation for future CSV upload functionality
- Increase user engagement and conversion rates
- Reduce friction in the user onboarding process

## Success Criteria

- [ ] Users can access demo mode without any authentication
- [ ] Demo mode includes all current app features (lineup generation, printing, preferences)
- [ ] Demo experience feels realistic and engaging
- [ ] No impact on existing TeamSnap functionality
- [ ] Demo mode clearly identified to prevent user confusion

## Requirements

### Functional Requirements

1. **Landing Page Split** - Add two options to the initial page in a side-by-side layout:
   - "Try Demo Mode" (new functionality) - positioned on the LEFT side
   - "Connect to TeamSnap" (existing functionality) - positioned on the RIGHT side

2. **Demo Data Loading** - Load fictional team data from static file including:
   - Team name and basic information
   - Roster of 12-15 players with famous baseball player names
   - 3-4 upcoming games in October 2025
   - Realistic player position preferences

3. **9-Inning Game Support** - Extend lineup generation to support 9-inning games:
   - Generate lineups for 9 innings instead of 6
   - Maintain existing pitcher rotation rules (max 2 innings per pitcher)
   - Preserve position preference functionality
   - Keep player randomization for development

4. **Visual Demo Indicator** - Add "(DEMO)" text in header next to "⚾ Baseball Lineup Manager"

5. **Complete Workflow Preservation** - All screens and workflows must function identically to TeamSnap mode:
   - Team selection (shows demo team)
   - Game selection (shows demo games)
   - Player management and preferences
   - Player filtering and availability management
   - Lineup generation and display
   - Print functionality

6. **Session Isolation** - Demo mode is one-way choice for the session (no switching back to TeamSnap mode)

### Technical Requirements

7. **Static Data File** - Create JSON/CSV file with demo team data
8. **Code Path Separation** - Maintain clean separation between demo and TeamSnap data sources
9. **No Authentication Bypass** - Demo mode should not affect TeamSnap OAuth security

### Non-Functional Requirements

10. **Performance** - Demo mode should load as quickly as TeamSnap mode
11. **Maintainability** - Demo data should be easily updatable via static file
12. **Scalability** - Foundation should support future CSV upload feature

## User Stories

### Sales/Demo Persona
- As a sales person, I want to show the app's capabilities immediately without requiring the prospect to have TeamSnap credentials
- As a sales person, I want engaging demo data that resonates with baseball coaches and players

### Evaluation Persona
- As a potential customer, I want to try all app features before committing to integration with my TeamSnap account
- As a coach, I want to see how the lineup generation works with familiar player names

### Development Persona
- As a developer, I want to test app functionality without needing TeamSnap API access
- As a developer, I want realistic test data for development and debugging

## Technical Specifications

### Demo Data Structure
```json
{
  "team": {
    "name": "Demo All-Stars",
    "id": "demo-001"
  },
  "players": [
    {
      "id": "player-001",
      "name": "Mike Trout",
      "position_preference": "any",
      "jersey_number": "27"
    }
    // ... 12-15 players total
  ],
  "games": [
    {
      "id": "game-001",
      "date": "2025-10-05",
      "time": "10:00 AM",
      "opponent": "Demo Rivals"
    }
    // ... 3-4 games total
  ]
}
```

### Player Roster (Mix of Current and Past Stars)
- Mike Trout, Aaron Judge, Mookie Betts, Ronald Acuña Jr.
- Derek Jeter, Ken Griffey Jr., Tony Gwynn, Cal Ripken Jr.
- Babe Ruth, Willie Mays, Hank Aaron, Mickey Mantle
- Additional players to reach 12-15 total roster size

### UI Changes
- Landing page: Add demo mode section/button on LEFT side, TeamSnap section on RIGHT side
- Use two-column layout with demo mode prominently positioned first (left)
- Header: Add "(DEMO)" indicator when in demo mode
- Maintain all existing styling and layouts for other pages

#### Specific Implementation Details (IMPLEMENTED)
- **Two-column card layout**: Side-by-side cards using flexbox (`flex-wrap: nowrap`)
- **Demo mode card (LEFT)**: Green theme (#28a745), positioned first in HTML
- **TeamSnap card (RIGHT)**: Red theme (#e74c3c), positioned second in HTML
- **Card sizing**: Each card takes 45% width with 30px gap between cards
- **Features section**: Moved outside cards, positioned below both options as shared functionality
- **Responsive design**: Cards stack vertically on mobile screens (<768px)
- **Clean card content**: Removed internal bullet lists, focused on primary action buttons

## Dependencies

### External Dependencies
- None (removes dependency on TeamSnap API for demo users)

### Internal Dependencies
- Existing lineup generation algorithm
- Current UI components and styling
- Print functionality
- Position preference system

## Timeline

### Phase 1: Foundation (Week 1)
- Create demo data file with team/player/game data
- Implement landing page split (TeamSnap vs Demo)
- Add demo mode routing and state management

### Phase 2: Integration (Week 2)
- Integrate demo data with existing components
- Extend lineup generation to 9 innings
- Add demo mode visual indicator

### Phase 3: Testing & Polish (Week 3)
- Test all workflows in demo mode
- Verify print functionality works with demo data
- Validate no impact on TeamSnap functionality

## Risks and Mitigation

| Risk | Mitigation Strategy |
|------|-------------------|
| Demo data becomes stale/uninteresting | Use mix of current stars and legends; easy static file updates |
| Code complexity from dual data sources | Clean abstraction layer between data source and UI components |
| User confusion about demo vs real data | Clear visual indicators and messaging |
| Performance impact from demo data loading | Optimize static file size and loading strategy |

## Out of Scope

- User authentication in demo mode
- Persistent demo data across sessions
- Switching between demo and TeamSnap modes within session
- Advanced configuration options (reserved for future releases)
- Real-time data updates in demo mode

## Acceptance Criteria

### Landing Page
- [x] Two clear options in side-by-side layout: "Try Demo Mode" (LEFT) and "Connect to TeamSnap" (RIGHT)
- [x] Demo mode section prominently positioned on the left side
- [x] Demo mode button navigates to team selection with demo data
- [x] TeamSnap option maintains existing OAuth flow

#### Implementation Status (COMPLETED)
- [x] **CSS Layout**: Flexbox with `flex-wrap: nowrap` for side-by-side positioning
- [x] **Color Themes**: Demo mode green (#28a745), TeamSnap red (#e74c3c)
- [x] **Card Structure**: Clean design with title, description, button, and subtitle
- [x] **Features Positioning**: Shared features list moved below both cards
- [x] **Responsive Behavior**: Mobile stacking at 768px breakpoint
- [x] **HTML Order**: Demo mode card first in DOM for left positioning

### Demo Data Experience
- [ ] Demo team loads with 12-15 famous baseball players
- [ ] 3-4 October 2025 games available for selection
- [ ] Player names are recognizable mix of current and past stars
- [ ] All players have realistic position preferences

### Lineup Generation
- [ ] Generates 9-inning lineups instead of 6
- [ ] Pitcher rotation rules maintained (max 2 innings per pitcher)
- [ ] Position preferences respected
- [ ] Player randomization across lineups works

### Visual Indicators
- [ ] Bolded "(DEMO)" bolded appears in header next to app title
- [ ] No other visual changes to existing UI
- [ ] Print layouts work correctly with demo data

### Workflow Preservation
- [ ] All existing screens function identically in demo mode
- [ ] Team selection shows demo team
- [ ] Game selection shows demo games
- [ ] Player management interface works with demo players
- [ ] Player filtering and availability controls function with demo data
- [ ] Lineup display and print functionality unchanged

### Technical Validation
- [ ] No impact on existing TeamSnap functionality
- [ ] Demo data loads from static file
- [ ] Clean separation between demo and production data paths
- [ ] Performance equivalent to TeamSnap mode