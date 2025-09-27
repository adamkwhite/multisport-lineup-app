# PRD: Default Team Selection with Auto-Load

## Overview
Add the ability for users to set a default team that persists across browser sessions using localStorage. When a default team is set, the application will automatically load that team's games on page load, eliminating the need to manually select their team every session.

## Problem Statement
Users currently have to manually select their active team from their available teams every time they visit the application. For users with multiple teams (especially those with access to historical teams through TeamSnap), this creates friction and slows down the workflow, particularly for coaches who primarily manage one active team.

## Goals

### Primary Goals
- Reduce time-to-content from team selection to game management
- Eliminate repetitive team selection for users who primarily use one team
- Provide seamless auto-loading of default team's games on page load

### Secondary Goals
- Add clear visual indicators for default team status
- Allow easy switching between teams when needed
- Maintain backward compatibility for users who prefer manual selection

## User Stories

**As a coach**, I want to set my current active team as the default so that I don't have to find and select it from my available teams every time I open the app.

**As a coach**, I want the app to automatically load my default team's games when I visit the dashboard so that I can immediately see upcoming games and manage lineups.

**As a coach**, I want to easily identify which team is my default and change it when the season ends or I switch teams.

**As a team manager**, I want the same default team functionality so that I can quickly access the team I'm currently managing without navigating through inactive teams.

## Functional Requirements

### Default Team Selection
1. The system must add a "Set as Default" action for each team in the team selection interface
2. The system must provide clear visual indication (e.g., star icon or "Default" badge) showing which team is currently set as default
3. The system must allow users to change their default team by selecting a different team and choosing "Set as Default"
4. The system must persist the default team selection using browser localStorage
5. The system must handle cases where no default team is set (current behavior)

### Auto-Loading Functionality
6. When a user visits the application and has a default team set, the system must automatically load that team's games
7. The system must automatically switch to the appropriate tab (Games tab) after auto-loading
8. If the default team has no upcoming games, the system must display an empty state message
9. The system must skip the team selection step and go directly to the dashboard when a default team exists

### Visual Indicators and UX
10. The system must display a clear indicator (star icon, "Default" text, or badge) next to the default team name
11. The system must show the currently loaded team name prominently in the interface
12. The system must provide an easy way to switch teams (access to team selector) even after auto-loading
13. The system must maintain all existing team selection functionality for users without a default set

### Session Persistence
14. The system must remember the default team selection indefinitely until manually changed by the user
15. The system must use browser localStorage with key naming that won't conflict with existing storage
16. The system must gracefully handle localStorage unavailability (fallback to no default behavior)

## Technical Requirements

### Frontend Implementation
1. Modify team selection interface to include "Set as Default" action for each team
2. Implement localStorage integration for storing/retrieving default team ID
3. Add auto-loading logic to page initialization that checks for default team
4. Ensure responsive design for new UI elements (star icons, badges)

### Integration Points
5. Integrate with existing team loading functionality in `loadTeams()` and `loadGames()`
6. Modify existing game loading workflow to support automatic team selection
7. Ensure compatibility with existing TeamSnap API calls and error handling
8. Maintain existing team switching functionality

## Non-Goals (Out of Scope)

- Backend user management or server-side storage of preferences
- Cross-device synchronization of default team settings
- Filtering or hiding inactive teams (separate feature consideration)
- Multiple default teams or team groups
- Automatic team switching based on game schedules
- Admin controls or restrictions on default team selection

## Design Considerations

### Default Team Indicators
- Use a star icon (⭐) next to default team name for quick visual recognition
- Consider adding "Default" badge or highlight to the team in lists
- Ensure indicators are visible but not overwhelming in the interface

### Auto-Loading UX
- Show brief loading indicator during auto-load process
- Display confirmation message like "Loaded [Team Name] (Default)"
- Maintain breadcrumb or header showing current team name
- Keep team selector easily accessible for switching

### Empty State Design
- Clear message when default team has no upcoming games
- Include option to "Choose Different Team" or "View All Teams"
- Maintain consistent styling with existing empty states

## Success Criteria

- [ ] Users can set any team as their default in under 3 clicks
- [ ] Default team setting persists across browser sessions and page refreshes
- [ ] App automatically loads default team's games on page load without user intervention
- [ ] Visual indicators clearly show which team is set as default
- [ ] Users can easily switch to non-default teams when needed
- [ ] No impact on existing team selection workflow for users without defaults
- [ ] Feature works consistently across desktop and mobile browsers

## Technical Specifications

### localStorage Implementation
```javascript
// Example localStorage usage
localStorage.setItem('defaultTeamId', 'team_12345');
const defaultTeamId = localStorage.getItem('defaultTeamId');
```

### Integration Points
- Modify existing `loadTeams()` function to check for and apply default
- Update team selection UI to include default indicators and actions
- Enhance page initialization to trigger auto-loading when default exists

## Dependencies

### Internal Dependencies
- Existing team loading functionality (`loadTeams()`, `loadGames()`)
- Current TeamSnap API integration
- Existing localStorage usage patterns (similar to name obfuscation toggle)
- Current tab switching and navigation system

### External Dependencies
- Browser localStorage API support
- TeamSnap API continued stability for team and game data

## Risks and Mitigation

**Risk:** Default team becomes inactive or inaccessible, causing app to fail on load
**Mitigation:** Implement error handling that falls back to manual team selection if auto-load fails

**Risk:** localStorage not supported in older browsers
**Mitigation:** Graceful degradation to manual selection when localStorage unavailable

**Risk:** Users forget they have a default set and expect to see team selection
**Mitigation:** Clear indication of loaded team and easy access to team switcher

## Default Behavior

- **Default state for new users**: No default team set, normal team selection required
- **Auto-loading trigger**: Page load/refresh when default team exists in localStorage
- **Fallback behavior**: Manual team selection if auto-load fails or no default set
- **Storage key**: Use descriptive key like 'defaultTeamId' to avoid conflicts