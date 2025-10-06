const timestamp = new Date().toISOString().slice(0, 19).replace(/[:.]/g, '-');

module.exports = {
  testEnvironment: 'jsdom',
  setupFilesAfterEnv: ['<rootDir>/tests/setup.js'],
  collectCoverage: true,
  coverageDirectory: process.env.CI ? 'coverage' : `test-results/coverage-${timestamp}`,
  coverageReporters: ['text', 'lcov', 'html', 'cobertura'],
  coverageThreshold: {
    global: {
      branches: 80,
      functions: 85,
      lines: 85,
      statements: 85
    }
  },
  testMatch: ['**/tests/**/*.test.js'],
  testPathIgnorePatterns: [
    '<rootDir>/node_modules/',
    '<rootDir>/venv/',
    '<rootDir>/static/',
    '<rootDir>/templates/'
  ],
  modulePathIgnorePatterns: ['<rootDir>/venv/'],
  roots: ['<rootDir>/tests/']
};
