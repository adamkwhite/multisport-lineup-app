# Multiple Position Preferences Implementation Plan

## Overview
Allow each player to be assigned multiple position preferences (e.g., Player 1 can play Pitcher, Catcher, and 1st Base) instead of just one position or "any position".

## Priority 1: UI Changes (Start Here)

### Task 1.1: Update Player Display Interface
**Location**: `templates/dashboard.html` (lines 595-612)

**Current Code**:
```html
<select class="position-preference" data-player-id="${player.id}">
    <option value="any">Any Position</option>
    <option value="pitcher">Pitcher</option>
    <option value="catcher">Catcher</option>
</select>
```

**New Implementation**:
Replace the dropdown with checkboxes for each position.

**Step-by-Step**:
1. Find the `displayPlayers()` function around line 587
2. Replace the select dropdown with a checkbox grid
3. Use position numbers (1-9) as values
4. Add CSS styling for compact display

**New HTML Structure**:
```html
<div class="position-checkboxes" data-player-id="${player.id}">
    <label><input type="checkbox" value="1"> P</label>
    <label><input type="checkbox" value="2"> C</label>
    <label><input type="checkbox" value="3"> 1B</label>
    <label><input type="checkbox" value="4"> 2B</label>
    <label><input type="checkbox" value="5"> 3B</label>
    <label><input type="checkbox" value="6"> SS</label>
    <label><input type="checkbox" value="7"> LF</label>
    <label><input type="checkbox" value="8"> CF</label>
    <label><input type="checkbox" value="9"> RF</label>
    <label><input type="checkbox" value="0" class="any-position"> Any</label>
</div>
```

**CSS to Add** (in the `<style>` section):
```css
.position-checkboxes {
    display: inline-flex;
    gap: 10px;
    flex-wrap: wrap;
}

.position-checkboxes label {
    display: flex;
    align-items: center;
    gap: 3px;
    font-size: 12px;
    background: #f0f0f0;
    padding: 3px 6px;
    border-radius: 3px;
    cursor: pointer;
}

.position-checkboxes input[type="checkbox"] {
    margin: 0;
}

.position-checkboxes label:has(input:checked) {
    background: #3498db;
    color: white;
}
```

### Task 1.2: Add "Any Position" Logic
**What to do**:
- When "Any" is checked, disable and uncheck all other checkboxes
- When any specific position is checked, uncheck and disable "Any"

**JavaScript to Add**:
```javascript
// Add this to the displayPlayers() function after creating the checkboxes
document.querySelectorAll('.position-checkboxes').forEach(container => {
    const anyCheckbox = container.querySelector('.any-position');
    const positionCheckboxes = container.querySelectorAll('input[type="checkbox"]:not(.any-position)');
    
    // Handle "Any" checkbox
    anyCheckbox.addEventListener('change', function() {
        if (this.checked) {
            positionCheckboxes.forEach(cb => {
                cb.checked = false;
                cb.disabled = true;
            });
        } else {
            positionCheckboxes.forEach(cb => {
                cb.disabled = false;
            });
        }
    });
    
    // Handle position checkboxes
    positionCheckboxes.forEach(cb => {
        cb.addEventListener('change', function() {
            if (Array.from(positionCheckboxes).some(c => c.checked)) {
                anyCheckbox.checked = false;
                anyCheckbox.disabled = true;
            } else {
                anyCheckbox.disabled = false;
            }
        });
    });
    
    // Set "Any" as default
    anyCheckbox.checked = true;
    anyCheckbox.dispatchEvent(new Event('change'));
});
```

## Priority 2: Update Data Collection

### Task 2.1: Modify generateLineup() Function
**Location**: `templates/dashboard.html` (around line 628)

**Current Code**:
```javascript
const preferenceSelect = document.querySelector(`[data-player-id="${player.id}"]`);
return {
    ...player,
    position_preference: preferenceSelect ? preferenceSelect.value : 'any'
};
```

**New Implementation**:
```javascript
const checkboxContainer = document.querySelector(`.position-checkboxes[data-player-id="${player.id}"]`);
const checkedBoxes = checkboxContainer.querySelectorAll('input[type="checkbox"]:checked');
const positions = Array.from(checkedBoxes).map(cb => parseInt(cb.value));

return {
    ...player,
    position_preferences: positions.includes(0) ? [] : positions  // Empty array means "any position"
};
```

## Priority 3: Backend API Changes

### Task 3.1: Update the generate_lineup() Function
**Location**: `app.py` (line 357)

**Changes Needed**:
1. Accept `position_preferences` array instead of `position_preference` string
2. Update the algorithm to handle multiple positions per player

**Key Areas to Modify**:
- Lines 374-381: Change how we categorize players
- Instead of separating into pitcher_candidates, catcher_candidates, and other_players, create a structure that tracks which positions each player can play

**New Data Structure**:
```python
# Create a mapping of position -> list of players who can play it
position_candidates = {pos: [] for pos in range(1, 10)}
flexible_players = []  # Players who can play any position

for player in players:
    prefs = player.get('position_preferences', [])
    if not prefs:  # Empty array means any position
        flexible_players.append(player)
        for pos in range(1, 10):
            position_candidates[pos].append(player)
    else:
        for pos in prefs:
            position_candidates[pos].append(player)
```

## Priority 4: Implement Smart Position Assignment

### Task 4.1: Create Position Assignment Algorithm
**Location**: `app.py` (in the generate_lineup function)

**Algorithm Steps**:
1. Identify "scarce" positions (positions with fewest available players)
2. Assign players to positions in order of scarcity
3. Use backtracking if needed

**Pseudo-code**:
```python
def assign_positions(players, must_play_players):
    # 1. Build position availability matrix
    # 2. Sort positions by scarcity (fewest candidates first)
    # 3. Assign must-play players first
    # 4. Fill remaining positions
    # 5. Return assignment or None if impossible
```

### Task 4.2: Integrate with Existing Lineup Logic
- Maintain the 2-innings-max bench time rule
- Keep pitcher rotation logic (max 2 innings per pitcher)
- Ensure the assignment algorithm runs for each of the 3 lineups

## Priority 5: Testing & Edge Cases

### Task 5.1: Test Scenarios
1. **All players select "Any"** - Should work like current system
2. **Only one player can catch** - Must be assigned to catcher
3. **Impossible assignment** - Show error if positions can't be filled
4. **Multiple scarce positions** - Algorithm should handle complex cases

### Task 5.2: Add Validation
- Check if all positions can be filled before generating lineup
- Show helpful error messages:
  - "Need at least one player who can play catcher"
  - "Not enough players for position X"

### Task 5.3: UI Polish
1. Add tooltips explaining position abbreviations
2. Add "Select All" / "Clear All" buttons
3. Show position counts (e.g., "3 players can pitch")

## Implementation Order for Junior Developer

1. **Start with Task 1.1**: Update the HTML structure
2. **Then Task 1.2**: Add the checkbox interaction logic
3. **Test the UI**: Make sure checkboxes work correctly
4. **Move to Task 2.1**: Update data collection
5. **Console.log the data**: Verify the structure before sending to backend
6. **Work on Task 3.1**: Update backend to accept new data format
7. **Finally Task 4.1-4.2**: Implement the new assignment algorithm

## Tips for Junior Developer

- **Test frequently**: After each step, verify it works
- **Use console.log**: Debug by printing data structures
- **Start simple**: Get basic checkbox UI working before complex logic
- **Ask questions**: If the algorithm seems complex, break it into smaller parts
- **Version control**: Commit after each working feature

## Example Data Flow

**Frontend sends**:
```json
{
  "players": [
    {"id": "1", "name": "John", "position_preferences": [1, 2]},
    {"id": "2", "name": "Jane", "position_preferences": []},  // Any position
    {"id": "3", "name": "Bob", "position_preferences": [6, 5]}
  ]
}
```

**Backend processes** and returns the same lineup structure as before, but now respecting multiple position preferences.