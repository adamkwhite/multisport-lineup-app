/**
 * UserGuidance Unit Tests
 * Tests for user guidance progress tracking and UI feedback
 */

const { UserGuidance, userGuidanceSteps } = require('../static/js/userGuidance');

// Mock DOM elements
const mockElements = {
  step1: { className: 'pending' },
  step2: { className: 'pending' },
  step3: { className: 'pending' }
};

// Mock console methods
beforeAll(() => {
  global.console = {
    ...console,
    log: jest.fn(),
    error: jest.fn(),
    warn: jest.fn()
  };

  // Mock document.getElementById
  global.document = {
    getElementById: jest.fn((id) => mockElements[id] || null)
  };
});

describe('UserGuidance', () => {
  beforeEach(() => {
    // Reset mock elements to initial state
    mockElements.step1.className = 'pending';
    mockElements.step2.className = 'pending';
    mockElements.step3.className = 'pending';

    // Restore original getElementById mock
    global.document.getElementById = jest.fn((id) => mockElements[id] || null);

    jest.clearAllMocks();
  });

  describe('resetUserGuidance', () => {
    test('should reset all guidance steps to pending state', () => {
      // Set some steps to completed first
      mockElements.step1.className = 'completed';
      mockElements.step2.className = 'active';

      const result = UserGuidance.resetUserGuidance();

      expect(result).toBe(true);
      expect(mockElements.step1.className).toBe('pending');
      expect(mockElements.step2.className).toBe('pending');
      expect(mockElements.step3.className).toBe('pending');
    });

    test('should handle missing elements gracefully', () => {
      // Mock getElementById to return null for one element
      global.document.getElementById = jest.fn((id) => {
        if (id === 'step2') return null;
        return mockElements[id] || null;
      });

      const result = UserGuidance.resetUserGuidance();

      expect(result).toBe(true);
      expect(mockElements.step1.className).toBe('pending');
      expect(mockElements.step3.className).toBe('pending');
    });

    test('should return false and log error on exception', () => {
      // Mock getElementById to throw error
      global.document.getElementById = jest.fn(() => {
        throw new Error('DOM error');
      });

      const result = UserGuidance.resetUserGuidance();

      expect(result).toBe(false);
      expect(console.error).toHaveBeenCalledWith(
        'Error resetting user guidance:',
        expect.any(Error)
      );
    });
  });

  describe('updateUserGuidanceProgress', () => {
    test('should mark step as completed', () => {
      const result = UserGuidance.updateUserGuidanceProgress('step1');

      expect(result).toBe(true);
      expect(mockElements.step1.className).toBe('completed');
      expect(console.log).toHaveBeenCalledWith(
        'User guidance: step1 marked as completed'
      );
    });

    test('should activate next step when current is completed', () => {
      const result = UserGuidance.updateUserGuidanceProgress('step1');

      expect(result).toBe(true);
      expect(mockElements.step1.className).toBe('completed');
      expect(mockElements.step2.className).toBe('active');
      expect(console.log).toHaveBeenCalledWith(
        'User guidance: step2 marked as active'
      );
    });

    test('should not activate next step if it is already completed', () => {
      mockElements.step2.className = 'completed';

      const result = UserGuidance.updateUserGuidanceProgress('step1');

      expect(result).toBe(true);
      expect(mockElements.step1.className).toBe('completed');
      expect(mockElements.step2.className).toBe('completed'); // Should remain completed
    });

    test('should handle last step completion without trying to activate next', () => {
      const result = UserGuidance.updateUserGuidanceProgress('step3');

      expect(result).toBe(true);
      expect(mockElements.step3.className).toBe('completed');
      // No next step to activate
    });

    test('should return false for invalid step', () => {
      const result = UserGuidance.updateUserGuidanceProgress('invalidStep');

      expect(result).toBe(false);
      expect(console.warn).toHaveBeenCalledWith(
        'Invalid guidance step:',
        'invalidStep'
      );
    });

    test('should return false and warn when element not found', () => {
      global.document.getElementById = jest.fn(() => null);

      const result = UserGuidance.updateUserGuidanceProgress('step1');

      expect(result).toBe(false);
      expect(console.warn).toHaveBeenCalledWith(
        'User guidance element not found:',
        'step1'
      );
    });

    test('should return false and log error on exception', () => {
      global.document.getElementById = jest.fn(() => {
        throw new Error('DOM error');
      });

      const result = UserGuidance.updateUserGuidanceProgress('step1');

      expect(result).toBe(false);
      expect(console.error).toHaveBeenCalledWith(
        'Error updating user guidance progress:',
        expect.any(Error)
      );
    });
  });

  describe('getCurrentState', () => {
    test('should return current state of all steps', () => {
      mockElements.step1.className = 'completed';
      mockElements.step2.className = 'active';
      mockElements.step3.className = 'pending';

      const state = UserGuidance.getCurrentState();

      expect(state).toEqual({
        step1: 'completed',
        step2: 'active',
        step3: 'pending'
      });
    });

    test('should handle missing elements by marking as unknown', () => {
      global.document.getElementById = jest.fn((id) => {
        if (id === 'step2') return null;
        return mockElements[id] || null;
      });

      const state = UserGuidance.getCurrentState();

      expect(state).toEqual({
        step1: 'pending',
        step2: 'unknown',
        step3: 'pending'
      });
    });

    test('should return empty object and log error on exception', () => {
      global.document.getElementById = jest.fn(() => {
        throw new Error('DOM error');
      });

      const state = UserGuidance.getCurrentState();

      expect(state).toEqual({});
      expect(console.error).toHaveBeenCalledWith(
        'Error getting guidance state:',
        expect.any(Error)
      );
    });
  });

  describe('isStepCompleted', () => {
    test('should return true for completed step', () => {
      mockElements.step1.className = 'completed';

      const isCompleted = UserGuidance.isStepCompleted('step1');

      expect(isCompleted).toBe(true);
    });

    test('should return false for non-completed step', () => {
      mockElements.step1.className = 'pending';

      const isCompleted = UserGuidance.isStepCompleted('step1');

      expect(isCompleted).toBe(false);
    });

    test('should return false for invalid step', () => {
      const isCompleted = UserGuidance.isStepCompleted('invalidStep');

      expect(isCompleted).toBe(false);
    });

    test('should return false when element not found', () => {
      global.document.getElementById = jest.fn(() => null);

      const isCompleted = UserGuidance.isStepCompleted('step1');

      expect(isCompleted).toBe(false);
    });

    test('should return false and log error on exception', () => {
      global.document.getElementById = jest.fn(() => {
        throw new Error('DOM error');
      });

      const isCompleted = UserGuidance.isStepCompleted('step1');

      expect(isCompleted).toBe(false);
      expect(console.error).toHaveBeenCalledWith(
        'Error checking step completion:',
        expect.any(Error)
      );
    });
  });

  describe('getValidSteps', () => {
    test('should return array of valid step names', () => {
      const validSteps = UserGuidance.getValidSteps();

      expect(validSteps).toEqual(['step1', 'step2', 'step3']);
      expect(validSteps).not.toBe(userGuidanceSteps); // Should be a copy
    });

    test('should return copy of steps array', () => {
      const validSteps1 = UserGuidance.getValidSteps();
      const validSteps2 = UserGuidance.getValidSteps();

      expect(validSteps1).toEqual(validSteps2);
      expect(validSteps1).not.toBe(validSteps2);
    });
  });

  describe('Integration Tests', () => {
    test('should handle complete workflow progression', () => {
      // Reset to initial state
      UserGuidance.resetUserGuidance();

      // Progress through steps
      UserGuidance.updateUserGuidanceProgress('step1');
      expect(mockElements.step1.className).toBe('completed');
      expect(mockElements.step2.className).toBe('active');

      UserGuidance.updateUserGuidanceProgress('step2');
      expect(mockElements.step2.className).toBe('completed');
      expect(mockElements.step3.className).toBe('active');

      UserGuidance.updateUserGuidanceProgress('step3');
      expect(mockElements.step3.className).toBe('completed');

      // Check final state
      const finalState = UserGuidance.getCurrentState();
      expect(finalState).toEqual({
        step1: 'completed',
        step2: 'completed',
        step3: 'completed'
      });
    });

    test('should validate step completion status throughout workflow', () => {
      UserGuidance.resetUserGuidance();

      expect(UserGuidance.isStepCompleted('step1')).toBe(false);
      expect(UserGuidance.isStepCompleted('step2')).toBe(false);
      expect(UserGuidance.isStepCompleted('step3')).toBe(false);

      UserGuidance.updateUserGuidanceProgress('step1');
      expect(UserGuidance.isStepCompleted('step1')).toBe(true);
      expect(UserGuidance.isStepCompleted('step2')).toBe(false);

      UserGuidance.updateUserGuidanceProgress('step2');
      expect(UserGuidance.isStepCompleted('step1')).toBe(true);
      expect(UserGuidance.isStepCompleted('step2')).toBe(true);
      expect(UserGuidance.isStepCompleted('step3')).toBe(false);
    });
  });
});