/**
 * UI Feedback System
 * Handles user feedback messages, error display, and success notifications
 */

const UIFeedback = {
    /**
     * Show an error message to the user
     * @param {string} message - The error message to display
     * @param {number} duration - Duration in milliseconds (optional, default 5000)
     */
    showError(message, duration = 5000) {
        try {
            console.error('UI Error:', message);

            // Remove existing error messages
            this.clearMessages('error-message');

            // Create error message element
            const errorDiv = document.createElement('div');
            errorDiv.className = 'error-message';
            errorDiv.style.cssText = `
                position: fixed;
                top: 20px;
                right: 20px;
                background-color: #f44336;
                color: white;
                padding: 15px;
                border-radius: 5px;
                box-shadow: 0 2px 10px rgba(0,0,0,0.3);
                z-index: 1000;
                max-width: 400px;
                word-wrap: break-word;
            `;
            errorDiv.textContent = message;

            // Add to document
            document.body.appendChild(errorDiv);

            // Auto-remove after duration
            if (duration > 0) {
                setTimeout(() => {
                    if (errorDiv.parentNode) {
                        errorDiv.parentNode.removeChild(errorDiv);
                    }
                }, duration);
            }

            return errorDiv;
        } catch (error) {
            console.error('Error showing error message:', error);
            return null;
        }
    },

    /**
     * Show a success message to the user
     * @param {string} message - The success message to display
     * @param {number} duration - Duration in milliseconds (optional, default 3000)
     */
    showSuccess(message, duration = 3000) {
        try {
            console.log('UI Success:', message);

            // Remove existing success messages
            this.clearMessages('success-message');

            // Create success message element
            const successDiv = document.createElement('div');
            successDiv.className = 'success-message';
            successDiv.style.cssText = `
                position: fixed;
                top: 20px;
                right: 20px;
                background-color: #4CAF50;
                color: white;
                padding: 15px;
                border-radius: 5px;
                box-shadow: 0 2px 10px rgba(0,0,0,0.3);
                z-index: 1000;
                max-width: 400px;
                word-wrap: break-word;
            `;
            successDiv.textContent = message;

            // Add to document
            document.body.appendChild(successDiv);

            // Auto-remove after duration
            if (duration > 0) {
                setTimeout(() => {
                    if (successDiv.parentNode) {
                        successDiv.parentNode.removeChild(successDiv);
                    }
                }, duration);
            }

            return successDiv;
        } catch (error) {
            console.error('Error showing success message:', error);
            return null;
        }
    },

    /**
     * Clear all messages of a specific type
     * @param {string} className - Class name of messages to clear
     */
    clearMessages(className) {
        try {
            const messages = document.querySelectorAll(`.${className}`);
            messages.forEach(message => {
                if (message.parentNode) {
                    message.parentNode.removeChild(message);
                }
            });
        } catch (error) {
            console.error('Error clearing messages:', error);
        }
    },

    /**
     * Clear all feedback messages
     */
    clearAllMessages() {
        this.clearMessages('error-message');
        this.clearMessages('success-message');
    },

    /**
     * Show a loading indicator
     * @param {string} message - Loading message (optional)
     * @returns {HTMLElement} The loading element
     */
    showLoading(message = 'Loading...') {
        try {
            // Remove existing loading indicators
            this.clearMessages('loading-message');

            const loadingDiv = document.createElement('div');
            loadingDiv.className = 'loading-message';
            loadingDiv.style.cssText = `
                position: fixed;
                top: 50%;
                left: 50%;
                transform: translate(-50%, -50%);
                background-color: rgba(0, 0, 0, 0.8);
                color: white;
                padding: 20px;
                border-radius: 10px;
                text-align: center;
                z-index: 1001;
            `;
            loadingDiv.innerHTML = `
                <div style="margin-bottom: 10px;">${message}</div>
                <div style="border: 3px solid #f3f3f3; border-top: 3px solid #3498db; border-radius: 50%; width: 30px; height: 30px; animation: spin 1s linear infinite; margin: 0 auto;"></div>
            `;

            // Add CSS animation for spinner
            if (!document.getElementById('loading-styles')) {
                const style = document.createElement('style');
                style.id = 'loading-styles';
                style.textContent = `
                    @keyframes spin {
                        0% { transform: rotate(0deg); }
                        100% { transform: rotate(360deg); }
                    }
                `;
                document.head.appendChild(style);
            }

            document.body.appendChild(loadingDiv);
            return loadingDiv;
        } catch (error) {
            console.error('Error showing loading indicator:', error);
            return null;
        }
    },

    /**
     * Hide loading indicator
     */
    hideLoading() {
        this.clearMessages('loading-message');
    }
};

// Export for testing
if (typeof module !== 'undefined' && module.exports) {
    module.exports = { UIFeedback };
}