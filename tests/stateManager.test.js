/**
 * StateManager Unit Tests
 * Tests for centralized application state management
 */

const { StateManager, createInitialState } = require('../static/js/StateManager');

// Mock console methods for cleaner test output
beforeAll(() => {
  global.console = {
    ...console,
    log: jest.fn(),
    error: jest.fn(),
    warn: jest.fn()
  };
});

describe('StateManager', () => {
  beforeEach(() => {
    // Reset state before each test
    StateManager.resetState();
    jest.clearAllMocks();
  });

  describe('Initial State', () => {
    test('should have correct initial state structure', () => {
      const initialState = createInitialState();

      expect(initialState).toEqual({
        selectedTeam: {
          id: null,
          name: null,
          data: null,
          selectedAt: null
        },
        selectedGame: {
          id: null,
          name: null,
          data: null,
          selectedAt: null
        },
        ui: {
          gamesVisible: false,
          playersVisible: false
        }
      });
    });

    test('should return initial state when reset', () => {
      // Modify state first
      StateManager.setSelectedTeam('team1', 'Test Team');
      StateManager.setSelectedGame('game1', 'Test Game');

      // Reset and verify
      const resetState = StateManager.resetState();
      const initialState = createInitialState();

      expect(resetState).toEqual(initialState);
    });
  });

  describe('Team Selection', () => {
    test('should set selected team with basic info', () => {
      const teamId = 'team123';
      const teamName = 'Test Team';

      const result = StateManager.setSelectedTeam(teamId, teamName);

      expect(result.id).toBe(teamId);
      expect(result.name).toBe(teamName);
      expect(result.data).toBe(null);
      expect(result.selectedAt).toMatch(/^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}\.\d{3}Z$/);
    });

    test('should set selected team with additional data', () => {
      const teamId = 'team123';
      const teamName = 'Test Team';
      const teamData = { division: 'Major', players: 15 };

      const result = StateManager.setSelectedTeam(teamId, teamName, teamData);

      expect(result.id).toBe(teamId);
      expect(result.name).toBe(teamName);
      expect(result.data).toEqual(teamData);
      expect(result.selectedAt).toBeTruthy();
    });

    test('should get selected team information', () => {
      const teamId = 'team123';
      const teamName = 'Test Team';

      StateManager.setSelectedTeam(teamId, teamName);
      const retrieved = StateManager.getSelectedTeam();

      expect(retrieved.id).toBe(teamId);
      expect(retrieved.name).toBe(teamName);
      expect(retrieved.selectedAt).toBeTruthy();
    });

    test('should return copy of team data, not reference', () => {
      const teamData = { division: 'Major' };
      StateManager.setSelectedTeam('team1', 'Team', teamData);

      const retrieved1 = StateManager.getSelectedTeam();
      const retrieved2 = StateManager.getSelectedTeam();

      expect(retrieved1).toEqual(retrieved2);
      expect(retrieved1).not.toBe(retrieved2);
    });

    test('should clear selected team', () => {
      StateManager.setSelectedTeam('team1', 'Test Team');

      const cleared = StateManager.clearSelectedTeam();

      expect(cleared.id).toBe(null);
      expect(cleared.name).toBe(null);
      expect(cleared.data).toBe(null);
      expect(cleared.selectedAt).toBe(null);
    });

    test('should validate team selection status', () => {
      expect(StateManager.isTeamSelected()).toBe(false);

      StateManager.setSelectedTeam('team1', 'Test Team');
      expect(StateManager.isTeamSelected()).toBe(true);

      StateManager.clearSelectedTeam();
      expect(StateManager.isTeamSelected()).toBe(false);
    });
  });

  describe('Game Selection', () => {
    test('should set selected game with basic info', () => {
      const gameId = 'game123';
      const gameName = 'Test vs Opponent';

      const result = StateManager.setSelectedGame(gameId, gameName);

      expect(result.id).toBe(gameId);
      expect(result.name).toBe(gameName);
      expect(result.data).toBe(null);
      expect(result.selectedAt).toMatch(/^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}\.\d{3}Z$/);
    });

    test('should set selected game with additional data', () => {
      const gameId = 'game123';
      const gameName = 'Test vs Opponent';
      const gameData = { date: '2023-06-15', location: 'Home Field' };

      const result = StateManager.setSelectedGame(gameId, gameName, gameData);

      expect(result.id).toBe(gameId);
      expect(result.name).toBe(gameName);
      expect(result.data).toEqual(gameData);
      expect(result.selectedAt).toBeTruthy();
    });

    test('should get selected game information', () => {
      const gameId = 'game123';
      const gameName = 'Test vs Opponent';

      StateManager.setSelectedGame(gameId, gameName);
      const retrieved = StateManager.getSelectedGame();

      expect(retrieved.id).toBe(gameId);
      expect(retrieved.name).toBe(gameName);
      expect(retrieved.selectedAt).toBeTruthy();
    });

    test('should return copy of game data, not reference', () => {
      const gameData = { location: 'Home Field' };
      StateManager.setSelectedGame('game1', 'Game', gameData);

      const retrieved1 = StateManager.getSelectedGame();
      const retrieved2 = StateManager.getSelectedGame();

      expect(retrieved1).toEqual(retrieved2);
      expect(retrieved1).not.toBe(retrieved2);
    });

    test('should clear selected game', () => {
      StateManager.setSelectedGame('game1', 'Test Game');

      const cleared = StateManager.clearSelectedGame();

      expect(cleared.id).toBe(null);
      expect(cleared.name).toBe(null);
      expect(cleared.data).toBe(null);
      expect(cleared.selectedAt).toBe(null);
    });

    test('should validate game selection status', () => {
      expect(StateManager.isGameSelected()).toBe(false);

      StateManager.setSelectedGame('game1', 'Test Game');
      expect(StateManager.isGameSelected()).toBe(true);

      StateManager.clearSelectedGame();
      expect(StateManager.isGameSelected()).toBe(false);
    });
  });

  describe('UI State Management', () => {
    test('should update UI state when team is selected', () => {
      const uiState = StateManager.setSelectedTeam('team1', 'Test Team');

      // updateUI is called internally by setSelectedTeam
      const currentUI = StateManager.getUIState();
      expect(currentUI.gamesVisible).toBe(true);
      expect(currentUI.playersVisible).toBe(false);
    });

    test('should update UI state when game is selected after team', () => {
      StateManager.setSelectedTeam('team1', 'Test Team');
      StateManager.setSelectedGame('game1', 'Test Game');

      const currentUI = StateManager.getUIState();
      expect(currentUI.gamesVisible).toBe(true);
      expect(currentUI.playersVisible).toBe(true);
    });

    test('should update UI state when team is cleared', () => {
      StateManager.setSelectedTeam('team1', 'Test Team');
      StateManager.setSelectedGame('game1', 'Test Game');

      StateManager.clearSelectedTeam();

      const currentUI = StateManager.getUIState();
      expect(currentUI.gamesVisible).toBe(false);
      expect(currentUI.playersVisible).toBe(false);
    });

    test('should return copy of UI state, not reference', () => {
      StateManager.setSelectedTeam('team1', 'Test Team');

      const ui1 = StateManager.getUIState();
      const ui2 = StateManager.getUIState();

      expect(ui1).toEqual(ui2);
      expect(ui1).not.toBe(ui2);
    });
  });

  describe('State Persistence and Retrieval', () => {
    test('should return full state snapshot', () => {
      StateManager.setSelectedTeam('team1', 'Test Team');
      StateManager.setSelectedGame('game1', 'Test Game');

      const fullState = StateManager.getFullState();

      expect(fullState.selectedTeam.id).toBe('team1');
      expect(fullState.selectedGame.id).toBe('game1');
      expect(fullState.ui.gamesVisible).toBe(true);
      expect(fullState.ui.playersVisible).toBe(true);
    });

    test('should return deep copy of state, not reference', () => {
      StateManager.setSelectedTeam('team1', 'Test Team');

      const state1 = StateManager.getFullState();
      const state2 = StateManager.getFullState();

      expect(state1).toEqual(state2);
      expect(state1).not.toBe(state2);
      expect(state1.selectedTeam).not.toBe(state2.selectedTeam);
    });
  });

  describe('Logging and Debugging', () => {
    test('should log current state', () => {
      StateManager.setSelectedTeam('team1', 'Test Team');

      const loggedState = StateManager.logCurrentState();

      expect(loggedState.selectedTeam.id).toBe('team1');
      expect(console.log).toHaveBeenCalledWith(
        'Current App State:',
        expect.stringContaining('"team1"')
      );
    });

    test('should log state changes', () => {
      StateManager.setSelectedTeam('team1', 'Test Team');

      expect(console.log).toHaveBeenCalledWith(
        'StateManager: Setting selected team:',
        'team1',
        'Test Team'
      );
      expect(console.log).toHaveBeenCalledWith(
        'StateManager: UI state updated:',
        expect.objectContaining({ gamesVisible: true, playersVisible: false })
      );
    });
  });

  describe('Edge Cases and Error Handling', () => {
    test('should handle null values gracefully', () => {
      expect(() => {
        StateManager.setSelectedTeam(null, null);
      }).not.toThrow();

      const team = StateManager.getSelectedTeam();
      expect(team.id).toBe(null);
      expect(team.name).toBe(null);
    });

    test('should handle undefined values gracefully', () => {
      expect(() => {
        StateManager.setSelectedTeam(undefined, undefined);
      }).not.toThrow();

      const team = StateManager.getSelectedTeam();
      expect(team.id).toBe(undefined);
      expect(team.name).toBe(undefined);
    });

    test('should handle empty string values', () => {
      StateManager.setSelectedTeam('', '');

      const team = StateManager.getSelectedTeam();
      expect(team.id).toBe('');
      expect(team.name).toBe('');
    });
  });
});