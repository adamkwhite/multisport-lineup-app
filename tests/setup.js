require('@testing-library/jest-dom');

// Global test setup
global.fetch = jest.fn();

// Mock DOM APIs that aren't available in jsdom
// delete + reassign is compatible with jsdom 30.x (which makes location non-configurable)
delete window.location;
window.location = {
  href: 'http://localhost',
  assign: jest.fn(),
  reload: jest.fn()
};

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
