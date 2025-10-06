require('@testing-library/jest-dom');

// Global test setup
global.fetch = jest.fn();

// Mock DOM APIs that aren't available in jsdom
Object.defineProperty(window, 'location', {
  value: {
    href: 'http://localhost',
    assign: jest.fn(),
    reload: jest.fn()
  },
  writable: true
});

// Mock localStorage
const localStorageMock = {
  getItem: jest.fn(),
  setItem: jest.fn(),
  removeItem: jest.fn(),
  clear: jest.fn(),
};
global.localStorage = localStorageMock;

// Reset all mocks before each test
beforeEach(() => {
  jest.clearAllMocks();
  fetch.mockClear();
});
