/**
 * User Guidance System
 * Handles user guidance progress tracking and UI feedback
 */

const userGuidanceSteps = [
    'step1',  // Select team
    'step2',  // Select game
    'step3'   // Generate lineup
];

const UserGuidance = {
    /**
     * Reset user guidance to initial state
     */
    resetUserGuidance() {
        try {
            const elements = [
                { id: 'step1', class: 'pending' },
                { id: 'step2', class: 'pending' },
                { id: 'step3', class: 'pending' }
            ];

            elements.forEach(({ id, class: className }) => {
                const element = document.getElementById(id);
                if (element) {
                    element.className = className;
                }
            });

            console.log('User guidance reset to initial state');
            return true;
        } catch (error) {
            console.error('Error resetting user guidance:', error);
            return false;
        }
    },

    /**
     * Update user guidance progress when a step is completed
     * @param {string} completedStep - The step that was completed
     */
    updateUserGuidanceProgress(completedStep) {
        try {
            if (!userGuidanceSteps.includes(completedStep)) {
                console.warn('Invalid guidance step:', completedStep);
                return false;
            }

            const element = document.getElementById(completedStep);
            if (element) {
                element.className = 'completed';
                console.log(`User guidance: ${completedStep} marked as completed`);

                // Enable next step if applicable
                const currentIndex = userGuidanceSteps.indexOf(completedStep);
                if (currentIndex < userGuidanceSteps.length - 1) {
                    const nextStep = userGuidanceSteps[currentIndex + 1];
                    const nextElement = document.getElementById(nextStep);
                    if (nextElement && nextElement.className === 'pending') {
                        nextElement.className = 'active';
                        console.log(`User guidance: ${nextStep} marked as active`);
                    }
                }

                return true;
            }

            console.warn('User guidance element not found:', completedStep);
            return false;
        } catch (error) {
            console.error('Error updating user guidance progress:', error);
            return false;
        }
    },

    /**
     * Get current guidance state
     * @returns {Object} Current state of all guidance steps
     */
    getCurrentState() {
        try {
            const state = {};
            userGuidanceSteps.forEach(step => {
                const element = document.getElementById(step);
                state[step] = element ? element.className : 'unknown';
            });
            return state;
        } catch (error) {
            console.error('Error getting guidance state:', error);
            return {};
        }
    },

    /**
     * Check if a specific step is completed
     * @param {string} step - Step to check
     * @returns {boolean} True if step is completed
     */
    isStepCompleted(step) {
        try {
            if (!userGuidanceSteps.includes(step)) {
                return false;
            }

            const element = document.getElementById(step);
            return element ? element.className === 'completed' : false;
        } catch (error) {
            console.error('Error checking step completion:', error);
            return false;
        }
    },

    /**
     * Get list of valid guidance steps
     * @returns {Array} Array of valid step names
     */
    getValidSteps() {
        return [...userGuidanceSteps];
    }
};

// Export for testing
if (typeof module !== 'undefined' && module.exports) {
    module.exports = { UserGuidance, userGuidanceSteps };
}