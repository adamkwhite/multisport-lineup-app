# PRD: Multi-Sport Support for Lineup Manager

## Overview

Transform the Baseball Lineup Manager into a multi-sport lineup management platform that supports baseball, soccer, and volleyball. Users will select their sport upfront, and the application will adapt all features (position names, lineup rules, field diagrams, demo mode) to match the selected sport. This architectural change enables market expansion while maintaining sport-specific expertise in lineup generation.

## Problem Statement

Currently, the application is hardcoded for baseball, limiting its usefulness to:
- Soccer coaches who need goalkeeper rotation and substitution management
- Volleyball coaches who need 6-position rotation and libero tracking
- Any coach managing multiple sports teams

User requests and personal need drive the requirement for multi-sport support. The challenge is maintaining sport-specific rule complexity (pitcher rotation rules, goalkeeper requirements, volleyball rotation) while sharing common infrastructure (TeamSnap integration, lineup generation patterns, UI framework).

## Goals

### Primary Goals
1. Support three sports: Baseball, Soccer, Volleyball with full sport-specific rules
2. Maintain sport-specific lineup generation logic for optimal player development
3. Provide sport-appropriate field diagrams and position terminology
4. Enable sport selection before authentication (no login required)
5. Preserve 97% test coverage across all sports

### Secondary Goals
1. Create extensible architecture for adding future sports (basketball, hockey, etc.)
2. Leverage TeamSnap API's built-in sport classification when available
3. Maintain single codebase with sport-specific modules (no code duplication)
4. Support demo mode for all sports with realistic data

## Success Criteria

### Phase 1: Soccer Support (MVP)
- [ ] Users can select Baseball or Soccer on landing page
- [ ] Soccer shows 11 positions (GK, defenders, midfielders, forwards)
- [ ] Soccer field diagram displays correctly
- [ ] Soccer lineup generation respects goalkeeper rules
- [ ] Soccer demo mode works with famous soccer players
- [ ] All existing baseball functionality remains unchanged
- [ ] Test coverage remains at 97%+

### Phase 2: Volleyball Support
- [ ] Users can select Volleyball
- [ ] Volleyball shows 6 positions with rotation
- [ ] Volleyball court diagram displays correctly
- [ ] Libero restrictions enforced
- [ ] Volleyball demo mode available

### Phase 3: Architecture Validation
- [ ] Adding a 4th sport requires <2 days of development
- [ ] No sport-specific code exists in shared modules
- [ ] Sport configuration is data-driven, not code-driven

## Requirements

### Functional Requirements

#### FR1: Sport Selection
1.1. Landing page displays sport selection as first step
1.2. Sports available: Baseball, Soccer, Volleyball (initially Baseball + Soccer)
1.3. Sport selection stored in session/local storage
1.4. After sport selection, user sees existing flow: Demo Mode or TeamSnap login
1.5. Sport selection persists across page refreshes within session

#### FR2: Sport-Specific Position Names
2.1. **Baseball**: P (Pitcher), C (Catcher), 1B, 2B, 3B, SS, LF, CF, RF
2.2. **Soccer**: GK (Goalkeeper), LB/RB (Left/Right Back), CB (Center Back), LM/RM (Left/Right Mid), CM (Center Mid), LW/RW (Left/Right Wing), ST (Striker)
2.3. **Volleyball**: OH (Outside Hitter), MB (Middle Blocker), S (Setter), OPP (Opposite), L (Libero), DS (Defensive Specialist)
2.4. Position names displayed in team selection, lineup generation, and printouts

#### FR3: Sport-Specific Lineup Generation Rules

**Baseball (existing):**
- 3.1. 6 innings, 9 fielding positions
- 3.2. Pitchers limited to 2 innings max
- 3.3. Catchers get breaks between innings
- 3.4. Players rotated for equal development

**Soccer (new):**
- 3.5. Goalkeeper must always be present
- 3.6. Substitution limits enforced (max 3-5 depending on league)
- 3.7. Players get equal playing time across halves
- 3.8. Position preferences respected (defense, midfield, forward)

**Volleyball (new):**
- 3.9. 6 positions rotate after each point/serve
- 3.10. Libero cannot play front row or serve
- 3.11. Sets-based game structure
- 3.12. Automatic rotation enforcement

#### FR4: Sport-Specific Field Diagrams
4.1. **Baseball**: Diamond diagram with 9 positions (existing)
4.2. **Soccer**: Rectangular field with 11 positions (4-4-2, 4-3-3, 3-5-2 formations)
4.3. **Volleyball**: Court diagram with 6 positions and rotation order
4.4. SVG-based diagrams for print quality
4.5. Diagrams show player names/numbers in correct positions

#### FR5: Sport-Specific Demo Mode
5.1. Demo data includes sport-appropriate players (baseball: Babe Ruth; soccer: Messi; volleyball: Kerri Walsh)
5.2. Demo games reflect sport structure (innings vs halves vs sets)
5.3. Demo rosters sized appropriately (baseball: 12-15; soccer: 11-16; volleyball: 6-10)

#### FR6: TeamSnap API Integration
6.1. Query `/v3/sports` endpoint to get available sports
6.2. Query `/v3/sport_positions` to get sport-specific positions
6.3. Map TeamSnap sport IDs to app sport configurations
6.4. Fall back to manual sport selection if API doesn't provide sport data
6.5. Cache sport data to reduce API calls

### Technical Requirements

#### TR1: Sport Configuration System
1.1. Create `SportConfig` class with sport-specific settings
1.2. Store configurations in `config/sports/` directory (baseball.json, soccer.json, volleyball.json)
1.3. Configuration includes: positions, field dimensions, rotation rules, substitution limits
1.4. Runtime sport selection loads appropriate config

#### TR2: Sport-Specific Lineup Engines
2.1. Create abstract `LineupGenerator` base class
2.2. Implement sport-specific subclasses: `BaseballLineupGenerator`, `SoccerLineupGenerator`, `VolleyballLineupGenerator`
2.3. Each engine handles sport-specific rules (pitcher limits, goalkeeper requirements, libero restrictions)
2.4. Factory pattern for engine selection based on sport

#### TR3: Frontend Routing
3.1. Add `/select-sport` route as new landing page
3.2. Update existing `/` route to require sport selection
3.3. Pass sport parameter through all API calls
3.4. Store selected sport in session state

#### TR4: Database Schema (if applicable)
4.1. Add `sport` field to teams table (if using database)
4.2. Add `sport` field to demo data JSON files
4.3. Migration path for existing data (default to 'baseball')

### Non-Functional Requirements

#### NFR1: Performance
1.1. Sport selection adds <100ms to page load
1.2. Lineup generation performance identical across sports
1.3. Field diagram rendering optimized for mobile devices

#### NFR2: Maintainability
2.1. Adding new sport requires only: config file + lineup engine + field diagram
2.2. No sport-specific logic in shared modules (app.py, API routes)
2.3. Sport configurations use JSON/YAML for easy modification

#### NFR3: Testing
3.1. Test coverage remains at 97%+ across all sports
3.2. Each sport has dedicated test suite (test_baseball.py, test_soccer.py, test_volleyball.py)
3.3. Integration tests verify sport switching
3.4. Visual regression tests for each sport's field diagram

#### NFR4: Accessibility
4.1. Sport selection screen is keyboard navigable
4.2. Screen readers announce selected sport
4.3. Field diagrams include alt text for positions

## User Stories

### Coach - Sport Selection
**As a** soccer coach
**I want to** select "Soccer" when I first open the app
**So that** I see soccer-specific positions and rules instead of baseball positions

**Acceptance Criteria:**
- Sport selection page loads first (before login/demo choice)
- Soccer option clearly labeled with icon
- After selection, app remembers choice for session

### Coach - Soccer Lineup Generation
**As a** youth soccer coach
**I want to** generate lineups that ensure every player gets equal playing time and the goalkeeper position is always filled
**So that** I can focus on coaching instead of manual rotation calculations

**Acceptance Criteria:**
- Goalkeeper position required in every lineup
- Substitution limits enforced (if configured)
- Players rotate through different positions
- Print-friendly format for sideline use

### Coach - Volleyball Rotation
**As a** volleyball coach
**I want to** generate lineups that automatically rotate players through the 6 positions
**So that** I comply with volleyball rotation rules and develop all players

**Acceptance Criteria:**
- 6-position rotation enforced
- Libero restrictions applied (cannot play front row)
- Rotation order clearly displayed
- Set-based structure supported

### Coach - Demo Mode Multi-Sport
**As a** potential customer
**I want to** try the app with demo data for my sport (soccer)
**So that** I can evaluate if it meets my needs before connecting my real team

**Acceptance Criteria:**
- Demo mode available for all sports
- Demo data realistic (famous players, appropriate game structures)
- All features work identically to real mode

## Technical Specifications

### Sport Configuration File Structure

```json
{
  "sport_id": "soccer",
  "display_name": "Soccer",
  "positions": [
    {"id": "GK", "name": "Goalkeeper", "abbrev": "GK", "required": true, "max_per_lineup": 1},
    {"id": "LB", "name": "Left Back", "abbrev": "LB", "required": false},
    {"id": "CB", "name": "Center Back", "abbrev": "CB", "required": false},
    {"id": "RB", "name": "Right Back", "abbrev": "RB", "required": false},
    {"id": "LM", "name": "Left Midfield", "abbrev": "LM", "required": false},
    {"id": "CM", "name": "Center Midfield", "abbrev": "CM", "required": false},
    {"id": "RM", "name": "Right Midfield", "abbrev": "RM", "required": false},
    {"id": "LW", "name": "Left Wing", "abbrev": "LW", "required": false},
    {"id": "RW", "name": "Right Wing", "abbrev": "RW", "required": false},
    {"id": "ST", "name": "Striker", "abbrev": "ST", "required": false}
  ],
  "game_structure": {
    "type": "halves",
    "periods": 2,
    "period_name": "Half"
  },
  "rules": {
    "total_positions": 11,
    "substitution_limit": 3,
    "required_positions": ["GK"],
    "rotation_type": "substitution_based"
  },
  "field_diagram": {
    "type": "rectangle",
    "width": 800,
    "height": 600,
    "position_coordinates": {
      "GK": {"x": 50, "y": 300},
      "LB": {"x": 150, "y": 450},
      "CB": {"x": 150, "y": 300},
      "RB": {"x": 150, "y": 150}
      // ... additional positions
    }
  }
}
```

### API Endpoint Changes

#### New Endpoint: Get Available Sports
```
GET /api/sports
Response: [
  {"id": "baseball", "name": "Baseball", "icon": "⚾"},
  {"id": "soccer", "name": "Soccer", "icon": "⚽"},
  {"id": "volleyball", "name": "Volleyball", "icon": "🏐"}
]
```

#### Modified Endpoint: Get Teams
```
GET /api/teams?sport=soccer
Response: {
  "sport": "soccer",
  "teams": [...]
}
```

#### Modified Endpoint: Generate Lineup
```
POST /api/lineup/generate
Body: {
  "team_id": "team123",
  "game_id": "game456",
  "sport": "soccer"
}
```

### Lineup Generator Architecture

```python
# Abstract base class
class LineupGenerator(ABC):
    def __init__(self, sport_config):
        self.config = sport_config

    @abstractmethod
    def generate(self, players, game_info):
        """Generate lineup based on sport-specific rules"""
        pass

    @abstractmethod
    def validate_lineup(self, lineup):
        """Validate lineup meets sport requirements"""
        pass

# Soccer-specific implementation
class SoccerLineupGenerator(LineupGenerator):
    def generate(self, players, game_info):
        # Ensure goalkeeper is present
        goalkeepers = [p for p in players if 'GK' in p.positions]
        if not goalkeepers:
            raise ValueError("No goalkeeper available")

        # Build lineup with substitution limits
        lineup = self._build_lineup(players, goalkeepers)
        return lineup

    def validate_lineup(self, lineup):
        # Check goalkeeper present
        # Check substitution limits
        # Check total players = 11
        pass

# Factory function
def get_lineup_generator(sport_id):
    generators = {
        'baseball': BaseballLineupGenerator,
        'soccer': SoccerLineupGenerator,
        'volleyball': VolleyballLineupGenerator
    }
    config = load_sport_config(sport_id)
    return generators[sport_id](config)
```

### Frontend Sport Selection Component

```javascript
// Sport selection page
class SportSelector {
    constructor() {
        this.sports = [
            { id: 'baseball', name: 'Baseball', icon: '⚾', description: 'Youth baseball lineup rotation' },
            { id: 'soccer', name: 'Soccer', icon: '⚽', description: 'Soccer formations and substitutions' },
            { id: 'volleyball', name: 'Volleyball', icon: '🏐', description: 'Volleyball rotation management' }
        ];
    }

    render() {
        return this.sports.map(sport => this.renderSportCard(sport));
    }

    selectSport(sportId) {
        localStorage.setItem('selected_sport', sportId);
        window.location.href = '/';
    }
}
```

## Dependencies

### External Dependencies
1. **TeamSnap API** - `/v3/sports` and `/v3/sport_positions` endpoints
2. **SVG Libraries** - For rendering sport-specific field diagrams (consider D3.js or plain SVG)
3. **Browser Storage** - localStorage or sessionStorage for sport persistence

### Internal Dependencies
1. **Demo Data Files** - Need soccer and volleyball demo data (`demo_soccer.json`, `demo_volleyball.json`)
2. **Test Fixtures** - Sport-specific test data for each sport
3. **Configuration System** - JSON/YAML parser for sport configs

## Timeline

### Phase 1: Architecture Foundation (Week 1-2)
- Create sport configuration system
- Implement abstract LineupGenerator class
- Add sport selection page
- Set up routing changes
- **Estimated:** 5-7 days

### Phase 2: Soccer Support (Week 3-4)
- Implement SoccerLineupGenerator
- Create soccer field diagram
- Build soccer demo mode
- Add soccer-specific tests
- **Estimated:** 7-10 days

### Phase 3: Volleyball Support (Week 5-6)
- Implement VolleyballLineupGenerator
- Create volleyball court diagram
- Build volleyball demo mode
- Add volleyball-specific tests
- **Estimated:** 7-10 days

### Phase 4: Integration & Testing (Week 7)
- Integration testing across sports
- Visual regression testing
- Performance optimization
- Documentation updates
- **Estimated:** 5 days

**Total Timeline:** 6-7 weeks for full multi-sport support

## Risks and Mitigation

### Risk 1: TeamSnap API Sport Data Incomplete
**Likelihood:** Medium
**Impact:** Medium
**Mitigation:**
- Implement fallback manual sport selection
- Cache sport configurations locally
- Design system to work without API sport data

### Risk 2: Sport-Specific Rules Too Complex
**Likelihood:** Medium
**Impact:** High
**Mitigation:**
- Start with simplified rules (MVP)
- Make rules configurable in JSON
- Allow coaches to customize rules per team
- Gather user feedback early

### Risk 3: Test Coverage Degradation
**Likelihood:** Low
**Impact:** High
**Mitigation:**
- Require tests for each sport module
- Set up CI to block PRs with <97% coverage
- Write tests before implementation (TDD)

### Risk 4: UI Complexity Explosion
**Likelihood:** Medium
**Impact:** Medium
**Mitigation:**
- Keep field diagrams simple (SVG primitives)
- Use component-based approach
- Limit initial formations (soccer: 4-4-2 only)
- Progressive enhancement approach

### Risk 5: Performance Degradation on Mobile
**Likelihood:** Low
**Impact:** Medium
**Mitigation:**
- Optimize SVG rendering
- Lazy load sport configurations
- Test on real devices early
- Use performance budgets

## Out of Scope

### Not Included in Initial Release
1. **Custom Sports** - Users cannot define their own sports
2. **Formation Editor** - Soccer formations are predefined (no drag-and-drop formation builder)
3. **Real-time Rotation** - No live game tracking or rotation adjustments
4. **Multi-Sport Teams** - One team = one sport (cannot switch sports mid-season)
5. **Advanced Stats** - No sport-specific statistics tracking (shots on goal, kill percentage, etc.)
6. **Rule Customization UI** - Rules are code/config-based, not user-configurable in UI
7. **Additional Sports** - Basketball, hockey, lacrosse deferred to Phase 4+
8. **TeamSnap Sport Auto-Detection** - Manual sport selection required if API doesn't provide sport

### Future Considerations
- Export lineups to PDF with sport-specific templates
- Mobile app versions
- Multi-language support for international sports
- Integration with league management systems
- Video highlights integration

## Acceptance Criteria

### Phase 1: Soccer MVP
- [ ] Sport selection page is first page users see
- [ ] Baseball users can continue using app without changes
- [ ] Soccer users see 11-position field diagram
- [ ] Soccer lineup generation works with goalkeeper rules
- [ ] Soccer demo mode available with 15 famous players
- [ ] All 151 existing tests still pass
- [ ] New tests added for soccer (target: 50+ tests)
- [ ] Test coverage remains at 97%+
- [ ] Documentation updated with sport selection flow
- [ ] Mobile responsive on all new pages

### Phase 2: Volleyball Addition
- [ ] Volleyball selectable from sport selection page
- [ ] Volleyball court diagram renders correctly
- [ ] 6-position rotation enforced
- [ ] Libero restrictions working
- [ ] Volleyball demo mode available
- [ ] Volleyball test suite complete (30+ tests)

### Phase 3: Architecture Validation
- [ ] Code review confirms no sport-specific logic in shared modules
- [ ] Sport configurations are data-driven (JSON/YAML)
- [ ] Adding 4th sport estimated at <2 days by dev team
- [ ] Performance benchmarks met (page load <2s, lineup gen <500ms)

## Related Work

**GitHub Issues:** (To be created)
- Issue #TBD: Backend - Sport configuration and data models
- Issue #TBD: Backend - Sport-specific lineup generation engines
- Issue #TBD: Frontend - Sport selection page and routing
- Issue #TBD: Frontend - Sport-specific field diagrams (SVG components)
- Issue #TBD: API - TeamSnap sport detection/mapping
- Issue #TBD: Testing - Multi-sport test infrastructure
- Issue #TBD: Demo Mode - Multi-sport demo data

**Related PRDs:**
- Demo Mode PRD (`docs/features/demo-mode-COMPLETED/prd.md`) - Multi-sport demo data builds on this
- Team Selection UX PRD (`docs/features/team-game-selection-ux-improvement-COMPLETED/prd.md`) - Sport selection follows similar UX patterns

## References

- TeamSnap API Documentation: https://api.teamsnap.com/
- TeamSnap Sports Endpoint: `/v3/sports`
- TeamSnap Sport Positions Endpoint: `/v3/sport_positions`
- Current Baseball Lineup Logic: `app.py:250-450` (to be refactored)

---

🤖 Generated with [Claude Code](https://claude.com/claude-code)
