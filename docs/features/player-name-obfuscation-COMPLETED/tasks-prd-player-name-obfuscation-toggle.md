## Relevant Files

- `templates/dashboard.html` - Main application template that needs hamburger menu integration
- `templates/login.html` - Login template that may need menu integration
- `static/css/style.css` - CSS file for hamburger menu styling (may need to be created)
- `static/js/menu.js` - JavaScript file for menu functionality and obfuscation toggle (to be created)
- `app.py` - Backend Flask file containing obfuscate_name function to reference
- `templates/base.html` - Base template if it exists, or need to create for shared menu component

### Notes

- The hamburger menu and toggle functionality will be primarily frontend JavaScript
- localStorage will be used for session persistence without backend changes
- Existing obfuscate_name() function in app.py will be referenced for frontend implementation
- Menu system should be responsive and work across all screen sizes

## Tasks

- [x] 1.0 Create Navigation Menu System
  - [x] 1.1 Add hamburger menu icon (☰) to dashboard.html header section
  - [x] 1.2 Create hidden menu div with ID "menu-dropdown" in dashboard.html
  - [x] 1.3 Add CSS classes for hamburger icon styling (.hamburger-menu)
  - [x] 1.4 Add CSS classes for dropdown menu styling (.menu-dropdown, .menu-item)
  - [x] 1.5 Create JavaScript function toggleMenu() to show/hide dropdown
  - [x] 1.6 Add click event listener to hamburger icon to call toggleMenu()
  - [x] 1.7 Add click event listener to document body to close menu when clicking outside

- [x] 2.0 Implement Obfuscation Toggle Functionality
  - [x] 2.1 Add toggle switch HTML element inside menu dropdown with ID "name-toggle"
  - [x] 2.2 Add label "Show Real Names" next to toggle switch
  - [x] 2.3 Create JavaScript function toggleNameObfuscation() to handle toggle changes
  - [x] 2.4 Add event listener to toggle switch to call toggleNameObfuscation()
  - [x] 2.5 Create JavaScript function obfuscateName(fullName) that replicates Python logic
  - [x] 2.6 Create JavaScript function updateAllPlayerNames() to refresh all visible names

- [x] 3.0 Integrate Toggle with Existing Player Name Displays
  - [x] 3.1 Identify all elements that display player names and add class "player-name"
  - [x] 3.2 Add data-original-name attribute to each player name element
  - [x] 3.3 Modify lineup generation to include both real and obfuscated names in data attributes
  - [x] 3.4 Update dashboard.html template to use player-name class on all name displays
  - [x] 3.5 Test that updateAllPlayerNames() correctly finds and updates all name elements

- [x] 4.0 Add Session Persistence with localStorage
  - [x] 4.1 Create JavaScript function saveToggleState(isObfuscated) using localStorage.setItem()
  - [x] 4.2 Create JavaScript function loadToggleState() using localStorage.getItem()
  - [x] 4.3 Call loadToggleState() on page load to restore previous setting
  - [x] 4.4 Call saveToggleState() whenever toggle is changed
  - [x] 4.5 Set default state to false (show real names) if no saved preference exists

- [x] 5.0 Style and Responsive Design Implementation
  - [x] 5.1 Style hamburger menu icon with 3 horizontal lines and hover effects
  - [x] 5.2 Style dropdown menu with background, border, and shadow
  - [x] 5.3 Style toggle switch with on/off states and smooth transitions
  - [x] 5.4 Add mobile-responsive CSS for screens under 768px width
  - [x] 5.5 Ensure menu closes properly on mobile after selection
  - [x] 5.6 Test menu positioning doesn't break layout on different screen sizes

- [ ] 6.0 Testing and Cross-Browser Compatibility
  - [ ] 6.1 Test toggle functionality in Chrome, Firefox, Safari, Edge
  - [ ] 6.2 Test localStorage persistence across browser sessions
  - [ ] 6.3 Test that all player names update simultaneously when toggled
  - [ ] 6.4 Test mobile responsiveness on actual mobile devices
  - [ ] 6.5 Verify no JavaScript errors in browser console
  - [ ] 6.6 Test graceful degradation if localStorage is not available