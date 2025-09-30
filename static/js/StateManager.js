/**
 * StateManager - Centralized application state management
 * Handles team selection, game selection, and UI state coordination
 */

// Initialize application state
const createInitialState = () => ({
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

// Global application state
let appState = createInitialState();

const StateManager = {
    // Team selection methods
    setSelectedTeam(teamId, teamName, teamData = null) {
        console.log('StateManager: Setting selected team:', teamId, teamName);
        appState.selectedTeam = {
            id: teamId,
            name: teamName,
            data: teamData,
            selectedAt: new Date().toISOString()
        };
        this.updateUI();
        return appState.selectedTeam;
    },

    getSelectedTeam() {
        return { ...appState.selectedTeam };
    },

    clearSelectedTeam() {
        console.log('StateManager: Clearing selected team');
        appState.selectedTeam = { id: null, name: null, data: null, selectedAt: null };
        // Clear game when team is cleared since games depend on team selection
        appState.selectedGame = { id: null, name: null, data: null, selectedAt: null };
        this.updateUI();
        return appState.selectedTeam;
    },

    // Game selection methods
    setSelectedGame(gameId, gameName, gameData = null) {
        console.log('StateManager: Setting selected game:', gameId, gameName);
        appState.selectedGame = {
            id: gameId,
            name: gameName,
            data: gameData,
            selectedAt: new Date().toISOString()
        };
        this.updateUI();
        return appState.selectedGame;
    },

    getSelectedGame() {
        return { ...appState.selectedGame };
    },

    clearSelectedGame() {
        console.log('StateManager: Clearing selected game');
        appState.selectedGame = { id: null, name: null, data: null, selectedAt: null };
        this.updateUI();
        return appState.selectedGame;
    },

    // UI state methods
    updateUI() {
        appState.ui.gamesVisible = appState.selectedTeam.id !== null;
        appState.ui.playersVisible = appState.selectedGame.id !== null;
        console.log('StateManager: UI state updated:', appState.ui);
        return { ...appState.ui };
    },

    getUIState() {
        return { ...appState.ui };
    },

    // Validation methods
    isTeamSelected() {
        return appState.selectedTeam.id !== null;
    },

    isGameSelected() {
        return appState.selectedGame.id !== null;
    },

    // State management methods
    getFullState() {
        return JSON.parse(JSON.stringify(appState));
    },

    resetState() {
        appState = createInitialState();
        console.log('StateManager: State reset to initial values');
        return this.getFullState();
    },

    // Debug method
    logCurrentState() {
        console.log('Current App State:', JSON.stringify(appState, null, 2));
        return appState;
    }
};

// Export for testing
if (typeof module !== 'undefined' && module.exports) {
    module.exports = { StateManager, createInitialState };
}