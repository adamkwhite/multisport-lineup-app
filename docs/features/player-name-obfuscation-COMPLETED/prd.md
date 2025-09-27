# PRD: Player Name Obfuscation Toggle

## Overview
Add a user-controllable toggle to enable/disable player name obfuscation throughout the Baseball Lineup Manager application. This feature will allow users to switch between showing real player names and obfuscated names (e.g., "Adam White" → "A*** W****") for privacy during demos, screenshots, or public displays.

## Problem Statement
Currently, player names are always obfuscated in the application. While this provides privacy protection, users need the flexibility to view real names during normal team management activities while maintaining the ability to quickly switch to obfuscated view for demos, screenshots, or when sharing screens publicly.

## Goals

### Primary Goals
- Allow users to toggle between obfuscated and real player names instantly
- Maintain privacy protection capabilities for demos and screenshots
- Provide intuitive access through a new navigation menu system

### Secondary Goals
- Remember user preference within browser session
- Ensure consistent obfuscation behavior across all app views
- Lay foundation for future settings and menu expansion

## User Stories

**As a coach**, I want to toggle name obfuscation on/off so that I can view real names during team management but quickly switch to privacy mode for screenshots.

**As a coach**, I want to access the toggle through an easy-to-find menu so that I don't have to search for the setting.

**As a coach**, I want the obfuscation setting to remain active during my session so that I don't have to re-enable it for multiple screenshots.

**As a team member**, I want the same toggle functionality so that I can control my own privacy preferences when using the app.

## Functional Requirements

### Navigation Menu System
1. The system must add a hamburger menu (☰) icon to the application header/navigation
2. The menu must be accessible from all pages in the application
3. The menu must expand/collapse when clicked
4. The menu must display clearly labeled options

### Obfuscation Toggle
5. The menu must include a toggle control labeled "Hide Player Names" or similar
6. The toggle must have clear on/off states (e.g., switch, checkbox, or button)
7. When enabled, the system must obfuscate all player names using the existing obfuscation function
8. When disabled, the system must display real player names
9. The toggle state must apply immediately without page refresh

### Scope of Obfuscation
10. The obfuscation setting must affect player names in lineup displays
11. The obfuscation setting must affect player names in availability lists
12. The obfuscation setting must affect player names in bench displays
13. The obfuscation setting must affect player names in any other location where they appear

### Session Persistence
14. The system must remember the user's toggle preference within the current browser session
15. The preference must reset to default (obfuscated) when the user closes/reopens the browser
16. The system must use browser localStorage to store the preference (no backend storage required)

## Technical Requirements

### Frontend Implementation
1. Add hamburger menu component to existing template layout
2. Implement JavaScript toggle functionality using existing obfuscation function
3. Use localStorage API for session persistence
4. Ensure responsive design for mobile devices

### Integration Points
5. Integrate with existing `obfuscate_name()` function in app.py
6. Modify all templates that display player names to check toggle state
7. Ensure compatibility with existing CORS and authentication systems

## Non-Goals (Out of Scope)

- User account management or backend user storage
- Cross-device synchronization of preferences
- Granular obfuscation control (e.g., obfuscating only first names)
- Password protection for the toggle
- Audit logging of when obfuscation is enabled/disabled
- Admin-only restrictions on toggle access

## Design Considerations

### Menu Placement
- Hamburger menu should be positioned in the top-right or top-left of the header
- Menu should overlay content when expanded (not push content down)
- Menu should be accessible but not visually prominent

### Toggle Design
- Use standard web toggle/switch component for familiarity
- Include clear labeling and current state indication
- Consider using icons (👁️ / 🙈) alongside text for quick recognition

### Responsive Behavior
- Menu must work on mobile devices
- Toggle controls must be touch-friendly
- Menu should close when clicking outside of it

## Success Criteria

- [ ] Users can toggle between obfuscated and real names in under 3 clicks
- [ ] Toggle setting persists throughout browser session
- [ ] All player names across the application respect the toggle setting
- [ ] Menu system provides foundation for future settings additions
- [ ] Feature works consistently across desktop and mobile browsers
- [ ] No impact on existing TeamSnap authentication or lineup generation functionality

## Technical Specifications

### JavaScript Implementation
```javascript
// Example localStorage usage
localStorage.setItem('hidePlayerNames', 'true');
const hideNames = localStorage.getItem('hidePlayerNames') === 'true';
```

### Template Integration
Templates will need conditional logic to check obfuscation preference before displaying names.

## Dependencies

### Internal Dependencies
- Existing obfuscation function in app.py
- Current template system (dashboard.html, login.html)
- Existing CSS/styling framework

### External Dependencies
- None (uses standard browser localStorage API)

## Risks and Mitigation

**Risk:** Users forget obfuscation is enabled and make decisions based on obfuscated names
**Mitigation:** Clear visual indicator when obfuscation is active, default to obfuscated state

**Risk:** Menu system conflicts with existing layout on mobile devices
**Mitigation:** Thorough testing on various screen sizes, responsive design principles

**Risk:** localStorage not supported in older browsers
**Mitigation:** Graceful degradation to session-only storage or default behavior

## Default Behavior

- **Default state for new users**: obfuscated=false (show real names)
- **No additional visual indicators**: Toggle state is sufficient indication
- **Keyboard shortcuts**: Not included in initial implementation (future enhancement)