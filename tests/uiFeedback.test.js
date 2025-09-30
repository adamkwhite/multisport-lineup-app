/**
 * UIFeedback Unit Tests
 * Tests for user feedback messages, error display, and success notifications
 * Focus on logic and error handling rather than complex DOM operations
 */

const { UIFeedback } = require('../static/js/uiFeedback');

beforeAll(() => {
  global.console = {
    ...console,
    log: jest.fn(),
    error: jest.fn(),
    warn: jest.fn()
  };

  // Simple mocks that focus on the core logic
  global.document = {
    createElement: () => ({
      className: '',
      textContent: '',
      innerHTML: '',
      style: { cssText: '' },
      parentNode: null
    }),
    body: { appendChild: () => {}, removeChild: () => {} },
    head: { appendChild: () => {} },
    getElementById: () => null,
    querySelectorAll: () => []
  };

  global.setTimeout = jest.fn();
});

describe('UIFeedback', () => {
  beforeEach(() => {
    jest.clearAllMocks();
  });

  describe('showError', () => {
    test('should log error message', () => {
      UIFeedback.showError('Test error');
      expect(console.error).toHaveBeenCalledWith('UI Error:', 'Test error');
    });

    test('should handle custom duration', () => {
      UIFeedback.showError('Test error', 3000);
      expect(setTimeout).toHaveBeenCalledWith(expect.any(Function), 3000);
    });

    test('should skip timeout when duration is 0', () => {
      UIFeedback.showError('Test error', 0);
      expect(setTimeout).not.toHaveBeenCalled();
    });

    test('should return element when successful', () => {
      const result = UIFeedback.showError('Test error');
      expect(result).toBeTruthy();
    });
  });

  describe('showSuccess', () => {
    test('should log success message', () => {
      UIFeedback.showSuccess('Test success');
      expect(console.log).toHaveBeenCalledWith('UI Success:', 'Test success');
    });

    test('should handle custom duration', () => {
      UIFeedback.showSuccess('Test success', 2000);
      expect(setTimeout).toHaveBeenCalledWith(expect.any(Function), 2000);
    });

    test('should return element when successful', () => {
      const result = UIFeedback.showSuccess('Test success');
      expect(result).toBeTruthy();
    });
  });

  describe('clearMessages', () => {
    test('should execute without throwing errors', () => {
      expect(() => {
        UIFeedback.clearMessages('test-message');
      }).not.toThrow();
    });
  });

  describe('clearAllMessages', () => {
    test('should call clearMessages for error and success types', () => {
      const clearSpy = jest.spyOn(UIFeedback, 'clearMessages');

      UIFeedback.clearAllMessages();

      expect(clearSpy).toHaveBeenCalledWith('error-message');
      expect(clearSpy).toHaveBeenCalledWith('success-message');

      clearSpy.mockRestore();
    });
  });

  describe('showLoading', () => {
    test('should handle default loading message', () => {
      const result = UIFeedback.showLoading();
      expect(result).toBeTruthy();
    });

    test('should handle custom loading message', () => {
      const result = UIFeedback.showLoading('Custom loading...');
      expect(result).toBeTruthy();
    });
  });

  describe('hideLoading', () => {
    test('should call clearMessages with loading-message', () => {
      const clearSpy = jest.spyOn(UIFeedback, 'clearMessages');

      UIFeedback.hideLoading();

      expect(clearSpy).toHaveBeenCalledWith('loading-message');

      clearSpy.mockRestore();
    });
  });

  describe('Error Resilience', () => {
    test('should not throw errors during normal operations', () => {
      expect(() => {
        UIFeedback.showError('Test error');
        UIFeedback.showSuccess('Test success');
        UIFeedback.showLoading('Loading...');
        UIFeedback.clearMessages('any-class');
        UIFeedback.hideLoading();
      }).not.toThrow();
    });
  });

  describe('Integration', () => {
    test('should handle multiple operations without errors', () => {
      expect(() => {
        UIFeedback.showError('Error 1');
        UIFeedback.showSuccess('Success 1');
        UIFeedback.showLoading('Loading...');
        UIFeedback.clearAllMessages();
        UIFeedback.hideLoading();
      }).not.toThrow();
    });

    test('should log appropriate console messages', () => {
      UIFeedback.showError('Test error');
      UIFeedback.showSuccess('Test success');

      expect(console.error).toHaveBeenCalledWith('UI Error:', 'Test error');
      expect(console.log).toHaveBeenCalledWith('UI Success:', 'Test success');
    });
  });
});