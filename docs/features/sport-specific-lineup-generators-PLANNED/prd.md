# PRD: Sport-Specific Lineup Generators

## Overview

Implement sport-specific lineup generation engines that encapsulate the business logic for creating optimal lineups for baseball, soccer, and volleyball. This completes Phase 1 of the Multi-Sport Support initiative by providing the core algorithms that generate fair, rule-compliant lineups tailored to each sport's unique requirements.

## Problem Statement

Currently, all lineup generation logic is hardcoded in `app.py` for baseball only. To support multiple sports:
- Need to extract and modularize existing baseball logic
- Implement sport-specific rules (pitcher rotation, goalkeeper requirements, etc.)
- Provide consistent interface for all sports
- Enable easy addition of new sports in the future

The challenge is balancing shared functionality (fair player rotation, position assignment) with sport-specific requirements (pitching limits, mandatory positions) while maintaining the smart assignment algorithm that tracks player history.

## Goals

### Primary Goals
1. Create abstract `LineupGenerator` base class with common interface
2. Extract all baseball lineup logic from `app.py` into `BaseballLineupGenerator`
3. Implement `SoccerLineupGenerator` with goalkeeper validation
4. Implement `VolleyballLineupGenerator` with basic rotation
5. Build generator factory for runtime sport selection
6. Maintain 96%+ test coverage with comprehensive unit tests

### Secondary Goals
1. Make sport-specific rules configurable via sport config (pitcher max innings)
2. Share utility functions for common operations (position assignment, rotation tracking)
3. Enable future sports to be added with minimal code changes
4. Preserve existing functionality for baseball (backward compatibility during development)

## Success Criteria

### Phase 1: Architecture & Baseball
- [ ] Abstract `LineupGenerator` base class created with standardized interface
- [ ] `BaseballLineupGenerator` extracts ALL logic from `app.py`
- [ ] Baseball lineup generation produces identical results to current implementation
- [ ] Pitcher rotation rules (2 inning max) enforced
- [ ] Catcher rest periods respected
- [ ] All existing baseball tests pass with new generator

### Phase 2: Soccer Implementation
- [ ] `SoccerLineupGenerator` creates valid 11-player lineups
- [ ] Goalkeeper always present in every lineup
- [ ] Substitution limits enforced (configurable, default 3)
- [ ] Players rotated fairly across halves
- [ ] Smart position assignment respects player preferences

### Phase 3: Volleyball Implementation
- [ ] `VolleyballLineupGenerator` creates valid 6-player lineups
- [ ] Setter position always filled
- [ ] Rotation order enforced for sets
- [ ] Libero restrictions deferred to future phase

### Phase 4: Integration
- [ ] Generator factory provides runtime sport selection
- [ ] `app.py` uses generators via factory pattern
- [ ] All 3 sports work end-to-end through API
- [ ] Test coverage remains at 96%+
- [ ] 50+ new unit tests for generators

## Requirements

### Functional Requirements

#### FR1: Abstract LineupGenerator Base Class
1.1. Define abstract base class with common interface:
```python
class LineupGenerator(ABC):
    def __init__(self, sport_config: SportConfig)
    def generate(self, players: List[Player], game_info: dict) -> List[Lineup]
    def validate_lineup(self, lineup: Lineup) -> List[str]
    def validate_players(self, players: List[Player]) -> List[str]
```

1.2. Provide shared utility methods:
- `get_available_players()` - Filter by attendance
- `assign_positions()` - Base position assignment logic
- `track_position_history()` - Record player assignments

1.3. Define standardized data structures:
- `Player` dataclass with position preferences
- `Lineup` dataclass with period/inning structure
- `PositionAssignment` for tracking

#### FR2: Baseball Lineup Generator
2.1. Extract all baseball logic from `app.py:generate_lineup_for_game()`
2.2. Implement pitcher rotation rules:
- Max 2 consecutive innings per pitcher
- Track pitcher inning history
- Prevent same pitcher starting consecutive games (if history available)

2.3. Implement catcher rest rules:
- Prefer different catchers across innings when possible
- Balance catcher workload

2.4. Generate 3 lineups (innings 1-2, 3-4, 5-6)
2.5. Use smart position assignment with player preferences
2.6. Randomize player order for development fairness

#### FR3: Soccer Lineup Generator
3.1. Generate lineups for 2 halves (configurable periods)
3.2. Enforce goalkeeper requirement:
- Validate at least one player can play GK
- Always assign goalkeeper to lineup
- Prefer different goalkeepers per half when possible

3.3. Implement substitution limits:
- Read limit from sport config (default: 3)
- Track substitutions across halves
- Validate lineup changes don't exceed limit

3.4. Smart position assignment:
- Respect player position preferences (defender, midfielder, forward)
- Rotate players through different positions
- Balance playing time across all players

#### FR4: Volleyball Lineup Generator
4.1. Generate lineups for 3 sets (configurable periods)
4.2. Enforce setter requirement:
- Validate at least one setter available
- Always assign setter to lineup

4.3. Implement 6-position rotation:
- Players rotate positions after each point
- Track rotation order
- **Libero restrictions deferred to future phase**

4.4. Balance playing time across sets

#### FR5: Generator Factory
5.1. Create factory function:
```python
def get_lineup_generator(sport_id: str) -> LineupGenerator:
    config = load_sport_config(sport_id)
    generators = {
        'baseball': BaseballLineupGenerator,
        'soccer': SoccerLineupGenerator,
        'volleyball': VolleyballLineupGenerator
    }
    return generators[sport_id](config)
```

5.2. Validate sport_id before instantiation
5.3. Cache sport configurations (reuse existing loader cache)
5.4. Raise clear error for unsupported sports

#### FR6: Sport Configuration Integration
6.1. Read sport-specific rules from config:
- Pitcher max innings (baseball)
- Substitution limit (soccer)
- Required positions (all sports)

6.2. Make rules configurable via JSON:
```json
"rules": {
  "pitcher_max_consecutive_innings": 2,
  "catcher_rest_innings": 1,
  "substitution_limit": 3
}
```

6.3. Provide sensible defaults if config missing

### Technical Requirements

#### TR1: Shared Utility Functions
1.1. Create `sports/utils/lineup_utils.py` with:
- `assign_positions_smart(players, positions, history)` - Smart assignment algorithm
- `track_player_position_history(assignments)` - History tracking
- `rotate_players(players, rotation_type)` - Rotation strategies
- `validate_required_positions(lineup, required)` - Position validation

1.2. Extract reusable logic from existing `app.py` functions
1.3. Maintain compatibility with existing tests

#### TR2: Data Models
2.1. Create dataclasses in `sports/models/lineup.py`:
```python
@dataclass
class Player:
    id: str
    name: str
    position_preferences: List[str]
    availability: dict  # game_id -> attending status

@dataclass
class PositionAssignment:
    player: Player
    position: str
    period: int  # inning/half/set number

@dataclass
class Lineup:
    period: int
    period_name: str  # "Inning 1-2", "Half 1", "Set 1"
    assignments: List[PositionAssignment]
    substitutions_used: int = 0
```

2.2. Provide conversion from TeamSnap API format
2.3. Support serialization to JSON for API responses

#### TR3: Generator Interface
3.1. All generators inherit from `LineupGenerator`
3.2. Generators accept `SportConfig` in constructor
3.3. `generate()` method signature:
```python
def generate(
    self,
    players: List[Player],
    game_info: dict,  # Contains: game_id, team_id, num_periods
    player_history: Optional[dict] = None
) -> List[Lineup]:
```

3.4. Return list of `Lineup` objects (one per period)

#### TR4: Validation Hooks
4.1. Pre-generation validation:
- Sufficient players (min 9 for baseball, 11 for soccer, 6 for volleyball)
- Required positions available (pitchers, goalkeepers, setters)
- Player data complete (names, preferences)

4.2. Post-generation validation:
- All positions filled
- No duplicate players in same period
- Sport-specific rules met (pitcher limits, goalkeeper present, etc.)

4.3. Return clear validation errors with actionable messages

### Non-Functional Requirements

#### NFR1: Performance
1.1. Lineup generation completes in <2 seconds for 15 players
1.2. Smart assignment algorithm runs in O(n*p) where n=players, p=positions
1.3. Position history tracking doesn't degrade with large datasets

#### NFR2: Maintainability
2.1. Each generator is <300 lines of code
2.2. Shared utilities well-documented with docstrings
2.3. Clear separation: base class (interface) vs. sport-specific (logic)
2.4. Adding new sport requires:
    - New generator class (<200 lines)
    - Sport config JSON
    - Unit tests
    - Factory registration (1 line)

#### NFR3: Testing
3.1. Unit test coverage for generators: 95%+
3.2. Test shared utilities independently
3.3. Test each generator with:
    - Valid input (happy path)
    - Edge cases (min players, max players)
    - Invalid input (missing positions, bad data)
    - Sport-specific rules (pitcher limits, goalkeeper, etc.)

3.4. Integration tests verify factory + generators work together
3.5. Regression tests ensure baseball output unchanged

#### NFR4: Code Quality
4.1. Type hints for all public methods
4.2. Docstrings following NumPy/Google style
4.3. Black + isort formatting
4.4. Flake8 compliant

## User Stories

### Story 1: Baseball Coach Uses Existing Functionality
**As a** baseball coach
**I want** lineup generation to work exactly as before
**So that** my existing workflows aren't disrupted

**Acceptance Criteria:**
- Baseball lineup generation produces identical results
- All pitcher rotation rules enforced
- Catcher rest periods respected
- No changes to API endpoints or response format

### Story 2: Soccer Coach Generates First Lineup
**As a** soccer coach
**I want** to generate lineups that always include a goalkeeper
**So that** my team has valid formations for each half

**Acceptance Criteria:**
- System validates at least one goalkeeper available
- Every half's lineup includes exactly one goalkeeper
- Players rotated fairly between halves
- Position preferences respected (defender, midfielder, forward)

### Story 3: Volleyball Coach Creates Set Lineups
**As a** volleyball coach
**I want** to generate 6-player lineups for 3 sets
**So that** all players get equal court time

**Acceptance Criteria:**
- Each set has exactly 6 players
- Setter position always filled
- Players rotated across sets
- Playing time balanced

### Story 4: Developer Adds New Sport
**As a** developer
**I want** to add basketball support in <1 day
**So that** the system scales to new sports easily

**Acceptance Criteria:**
- Create basketball sport config (JSON)
- Implement `BasketballLineupGenerator` (<200 lines)
- Register in factory (1 line)
- Add unit tests (50+ tests)
- All existing tests still pass

## Technical Specifications

### LineupGenerator Base Class

```python
# sports/generators/base.py

from abc import ABC, abstractmethod
from typing import List, Optional, Dict
from sports.models.sport_config import SportConfig
from sports.models.lineup import Player, Lineup

class LineupGenerator(ABC):
    """Abstract base class for sport-specific lineup generators."""

    def __init__(self, sport_config: SportConfig):
        """
        Initialize generator with sport configuration.

        Args:
            sport_config: Configuration loaded from config/sports/{sport}.json
        """
        self.config = sport_config
        self.required_positions = sport_config.rules.required_positions

    @abstractmethod
    def generate(
        self,
        players: List[Player],
        game_info: dict,
        player_history: Optional[Dict] = None
    ) -> List[Lineup]:
        """
        Generate lineups for all periods in a game.

        Args:
            players: List of available players
            game_info: Game metadata (id, team_id, num_periods)
            player_history: Optional history of previous assignments

        Returns:
            List of Lineup objects (one per period)

        Raises:
            ValueError: If insufficient players or required positions unavailable
        """
        pass

    def validate_players(self, players: List[Player]) -> List[str]:
        """
        Validate that players meet sport requirements.

        Returns:
            List of validation error messages (empty if valid)
        """
        errors = []

        # Check minimum players
        if len(players) < self.config.rules.total_positions:
            errors.append(
                f"Insufficient players: need {self.config.rules.total_positions}, "
                f"have {len(players)}"
            )

        # Check required positions available
        for req_pos in self.required_positions:
            if not any(req_pos in p.position_preferences for p in players):
                errors.append(
                    f"No player available for required position: {req_pos}"
                )

        return errors

    def validate_lineup(self, lineup: Lineup) -> List[str]:
        """
        Validate a generated lineup meets sport rules.

        Returns:
            List of validation error messages (empty if valid)
        """
        errors = []

        # Check all positions filled
        if len(lineup.assignments) != self.config.rules.total_positions:
            errors.append(
                f"Incomplete lineup: {len(lineup.assignments)} positions filled, "
                f"need {self.config.rules.total_positions}"
            )

        # Check required positions present
        assigned_positions = {a.position for a in lineup.assignments}
        for req_pos in self.required_positions:
            if req_pos not in assigned_positions:
                errors.append(f"Required position not assigned: {req_pos}")

        # Check no duplicate players
        player_ids = [a.player.id for a in lineup.assignments]
        if len(player_ids) != len(set(player_ids)):
            errors.append("Duplicate players in lineup")

        return errors
```

### BaseballLineupGenerator

```python
# sports/generators/baseball.py

from typing import List, Optional, Dict
from sports.generators.base import LineupGenerator
from sports.models.lineup import Player, Lineup, PositionAssignment
from sports.utils.lineup_utils import assign_positions_smart, track_player_position_history

class BaseballLineupGenerator(LineupGenerator):
    """Lineup generator for baseball with pitcher rotation rules."""

    def __init__(self, sport_config):
        super().__init__(sport_config)
        self.pitcher_max_innings = sport_config.rules.get(
            'pitcher_max_consecutive_innings', 2
        )

    def generate(
        self,
        players: List[Player],
        game_info: dict,
        player_history: Optional[Dict] = None
    ) -> List[Lineup]:
        """Generate 3 baseball lineups (innings 1-2, 3-4, 5-6)."""

        # Validate players
        errors = self.validate_players(players)
        if errors:
            raise ValueError(f"Invalid players: {', '.join(errors)}")

        lineups = []
        position_history = player_history or {}
        pitcher_history = {}

        # Generate lineup for each 2-inning period
        for period in range(1, 4):  # Periods 1, 2, 3
            lineup = self._generate_period_lineup(
                period=period,
                players=players,
                position_history=position_history,
                pitcher_history=pitcher_history
            )

            lineups.append(lineup)

            # Update histories
            track_player_position_history(lineup.assignments, position_history)
            self._update_pitcher_history(lineup, pitcher_history)

        return lineups

    def _generate_period_lineup(
        self,
        period: int,
        players: List[Player],
        position_history: dict,
        pitcher_history: dict
    ) -> Lineup:
        """Generate lineup for a single 2-inning period."""

        # Get eligible pitchers (not pitched previous 2 innings)
        eligible_pitchers = self._get_eligible_pitchers(players, pitcher_history, period)

        # Assign positions using smart algorithm
        assignments = assign_positions_smart(
            available_players=players,
            available_positions=self.config.positions,
            must_play_players=[],
            pitcher_pool=eligible_pitchers,
            position_history=position_history
        )

        # Create lineup
        return Lineup(
            period=period,
            period_name=f"Innings {period*2-1}-{period*2}",
            assignments=assignments
        )

    def _get_eligible_pitchers(
        self,
        players: List[Player],
        pitcher_history: dict,
        current_period: int
    ) -> List[Player]:
        """Get pitchers who haven't reached inning limit."""
        eligible = []
        for player in players:
            if 'P' not in player.position_preferences:
                continue
            innings_pitched = pitcher_history.get(player.id, [])
            # Check if pitched in previous period
            if (current_period - 1) not in innings_pitched:
                eligible.append(player)
        return eligible

    def _update_pitcher_history(self, lineup: Lineup, pitcher_history: dict):
        """Track which periods each pitcher has worked."""
        for assignment in lineup.assignments:
            if assignment.position == 'P':
                if assignment.player.id not in pitcher_history:
                    pitcher_history[assignment.player.id] = []
                pitcher_history[assignment.player.id].append(lineup.period)
```

### Generator Factory

```python
# sports/generators/factory.py

from typing import Type
from sports.generators.base import LineupGenerator
from sports.generators.baseball import BaseballLineupGenerator
from sports.generators.soccer import SoccerLineupGenerator
from sports.generators.volleyball import VolleyballLineupGenerator
from sports.services.sport_loader import load_sport_config

_generator_registry: dict[str, Type[LineupGenerator]] = {
    'baseball': BaseballLineupGenerator,
    'soccer': SoccerLineupGenerator,
    'volleyball': VolleyballLineupGenerator,
}

def get_lineup_generator(sport_id: str) -> LineupGenerator:
    """
    Get a lineup generator for the specified sport.

    Args:
        sport_id: Sport identifier (e.g., 'baseball', 'soccer')

    Returns:
        Configured LineupGenerator instance

    Raises:
        ValueError: If sport not supported
        FileNotFoundError: If sport config not found
    """
    if sport_id not in _generator_registry:
        supported = ', '.join(_generator_registry.keys())
        raise ValueError(
            f"Sport '{sport_id}' not supported. "
            f"Supported sports: {supported}"
        )

    config = load_sport_config(sport_id)
    generator_class = _generator_registry[sport_id]
    return generator_class(config)

def register_generator(sport_id: str, generator_class: Type[LineupGenerator]):
    """Register a new sport generator (for extensions)."""
    _generator_registry[sport_id] = generator_class
```

## Dependencies

### Internal Dependencies
1. Sport configuration system (completed in Issue #39)
2. Existing `app.py` lineup generation logic (to be extracted)
3. TeamSnap API player data structures

### External Dependencies
1. Python 3.12+ (type hints, dataclasses)
2. pytest for testing
3. No new external packages required

## Timeline

### Phase 1: Foundation (Week 1)
- Create abstract `LineupGenerator` base class
- Extract shared utilities to `lineup_utils.py`
- Create lineup data models
- **Estimated:** 2-3 days

### Phase 2: Baseball Extraction (Week 1)
- Implement `BaseballLineupGenerator`
- Extract all logic from `app.py`
- Regression tests to verify identical output
- **Estimated:** 2-3 days

### Phase 3: Soccer & Volleyball (Week 2)
- Implement `SoccerLineupGenerator`
- Implement `VolleyballLineupGenerator`
- Sport-specific validation and rules
- **Estimated:** 3-4 days

### Phase 4: Integration & Testing (Week 2)
- Build generator factory
- Integrate with `app.py`
- End-to-end testing for all sports
- **Estimated:** 2-3 days

**Total Timeline:** 2 weeks for complete implementation

## Risks and Mitigation

### Risk 1: Baseball Logic Extraction Breaks Existing Functionality
**Likelihood:** Medium
**Impact:** High
**Mitigation:**
- Create comprehensive regression test suite first
- Extract incrementally with continuous testing
- Keep old code temporarily for comparison
- Extensive manual testing with real data

### Risk 2: Soccer/Volleyball Algorithms Too Complex
**Likelihood:** Medium
**Impact:** Medium
**Mitigation:**
- Start with simplified algorithms (round-robin)
- Iterate toward smart assignment once working
- Defer complex rules (libero) to future phases
- Get coach feedback early

### Risk 3: Performance Degradation with Smart Assignment
**Likelihood:** Low
**Impact:** Medium
**Mitigation:**
- Profile existing algorithm performance
- Set performance budgets (<2s for 15 players)
- Optimize hot paths (position assignment loop)
- Consider caching strategies if needed

### Risk 4: Shared Utilities Create Coupling Issues
**Likelihood:** Low
**Impact:** Medium
**Mitigation:**
- Keep utilities truly generic (no sport-specific logic)
- Each sport can override utility behavior if needed
- Clear documentation on utility contracts
- Test utilities independently

## Out of Scope

### Not Included in This Phase
1. **Frontend sport selection UI** - Deferred to Phase 2 of multi-sport support
2. **API endpoints for sport switching** - Will use existing endpoints with sport parameter later
3. **Libero restrictions for volleyball** - Deferred to future phase
4. **Advanced formation strategies** (soccer 4-3-3 vs 4-4-2) - Start with single formation
5. **Player skill ratings** - Use position preferences only
6. **Real-time lineup adjustments** - Static lineups only
7. **Multi-game tournament scheduling** - Single game focus
8. **Historical analytics** - Basic history tracking only

### Future Considerations
- Machine learning for optimal position assignment
- Coach feedback loop for lineup preferences
- Injury tracking and automatic replacements
- Weather-based lineup adjustments
- Integration with practice attendance data

## Acceptance Criteria

### All Generators
- [ ] Inherit from `LineupGenerator` base class
- [ ] Accept `SportConfig` in constructor
- [ ] Implement `generate()` method with standardized signature
- [ ] Implement sport-specific validation
- [ ] Return list of `Lineup` objects
- [ ] Handle edge cases (min players, missing positions, etc.)
- [ ] Include comprehensive docstrings
- [ ] Pass all unit tests (95%+ coverage)

### Baseball Generator
- [ ] Produces identical lineups to current `app.py` implementation
- [ ] Enforces pitcher rotation (max 2 consecutive innings)
- [ ] Respects catcher rest periods
- [ ] Generates 3 lineups (innings 1-2, 3-4, 5-6)
- [ ] Smart position assignment with history tracking
- [ ] All existing baseball tests pass

### Soccer Generator
- [ ] Always includes exactly one goalkeeper per lineup
- [ ] Enforces substitution limits (configurable via config)
- [ ] Generates 2 lineups (one per half)
- [ ] Smart position assignment respects player preferences
- [ ] Validates goalkeeper availability before generation
- [ ] Players rotated fairly across halves

### Volleyball Generator
- [ ] Always includes exactly one setter per lineup
- [ ] Generates 3 lineups (one per set)
- [ ] Enforces 6-player limit per lineup
- [ ] Validates setter availability before generation
- [ ] Players rotated fairly across sets
- [ ] Libero restrictions NOT implemented (future phase)

### Factory & Integration
- [ ] Factory returns correct generator for sport_id
- [ ] Factory validates sport_id before instantiation
- [ ] Clear error messages for unsupported sports
- [ ] `app.py` uses factory to get generator
- [ ] All 3 sports work end-to-end through existing API
- [ ] Integration tests verify complete flow

### Testing
- [ ] 50+ new unit tests added
- [ ] Each generator has dedicated test file
- [ ] Shared utilities tested independently
- [ ] Edge cases covered (min players, bad input, etc.)
- [ ] Regression tests for baseball
- [ ] Overall test coverage remains at 96%+

## Related Work

**GitHub Issues:**
- Issue #48: Create abstract LineupGenerator base class + shared utilities
- Issue #49: Implement BaseballLineupGenerator (extract from app.py)
- Issue #50: Implement SoccerLineupGenerator with goalkeeper rules
- Issue #51: Implement VolleyballLineupGenerator with basic rotation
- Issue #52: Create generator factory + integrate with app.py
- Issue #53: Add sport-specific configuration rules (pitcher innings, etc.)

**Related PRDs:**
- Multi-Sport Support PRD (`docs/features/multi-sport-support-PLANNED/prd.md`) - Parent PRD
- Sport Configuration Backend (#39 - COMPLETED) - Foundation for this work

**References:**
- Existing lineup logic: `app.py:250-600` (to be extracted)
- GitHub Issues: [#48](https://github.com/adamloec/baseball-lineup-app/issues/48), [#49](https://github.com/adamloec/baseball-lineup-app/issues/49), [#50](https://github.com/adamloec/baseball-lineup-app/issues/50), [#51](https://github.com/adamloec/baseball-lineup-app/issues/51), [#52](https://github.com/adamloec/baseball-lineup-app/issues/52), [#53](https://github.com/adamloec/baseball-lineup-app/issues/53)
- Sport configurations: `config/sports/*.json`
- Sport config models: `sports/models/sport_config.py`

---

🤖 Generated with [Claude Code](https://claude.com/claude-code)
