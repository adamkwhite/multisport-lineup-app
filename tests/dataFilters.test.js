/**
 * DataFilters Unit Tests
 * Tests for filtering of teams, games, and other data collections
 */

const { DataFilters } = require('../static/js/dataFilters');

// Mock console methods for cleaner test output
beforeAll(() => {
  global.console = {
    ...console,
    log: jest.fn(),
    error: jest.fn(),
    warn: jest.fn()
  };
});

describe('DataFilters', () => {
  beforeEach(() => {
    jest.clearAllMocks();
  });

  describe('filterTeams', () => {
    const mockTeams = [
      { id: 1, name: 'Mighty Eagles', division: 'Major' },
      { id: 2, name: 'Thunder Hawks', division: 'Minor' },
      { id: 3, name: 'Lightning Bolts', division: 'Major' },
      { id: 4, name: 'Storm Riders', division: 'Minor' }
    ];

    test('should return all teams when no search term provided', () => {
      const result = DataFilters.filterTeams(mockTeams, '');
      expect(result).toEqual(mockTeams);

      const result2 = DataFilters.filterTeams(mockTeams, null);
      expect(result2).toEqual(mockTeams);
    });

    test('should filter teams by name', () => {
      const result = DataFilters.filterTeams(mockTeams, 'eagle');
      expect(result).toHaveLength(1);
      expect(result[0].name).toBe('Mighty Eagles');
    });

    test('should filter teams by division', () => {
      const result = DataFilters.filterTeams(mockTeams, 'major');
      expect(result).toHaveLength(2);
      expect(result.every(team => team.division === 'Major')).toBe(true);
    });

    test('should filter teams by ID', () => {
      const result = DataFilters.filterTeams(mockTeams, '1');
      expect(result).toHaveLength(1);
      expect(result[0].id).toBe(1);
    });

    test('should be case insensitive', () => {
      const result = DataFilters.filterTeams(mockTeams, 'EAGLES');
      expect(result).toHaveLength(1);
      expect(result[0].name).toBe('Mighty Eagles');
    });

    test('should handle empty array', () => {
      const result = DataFilters.filterTeams([], 'test');
      expect(result).toEqual([]);
    });

    test('should handle non-array input', () => {
      const result = DataFilters.filterTeams(null, 'test');
      expect(result).toEqual([]);
      expect(console.warn).toHaveBeenCalledWith('filterTeams: teams parameter is not an array');
    });

    test('should handle teams with missing properties', () => {
      const incompleteTeams = [
        { id: 1, name: 'Complete Team' },
        { id: 2 }, // Missing name
        { name: 'No ID Team' },
        null
      ];

      const result = DataFilters.filterTeams(incompleteTeams, 'complete');
      expect(result).toHaveLength(1);
      expect(result[0].name).toBe('Complete Team');
    });

    test('should handle errors gracefully', () => {
      // Create a mock team that throws error when accessed
      const problematicTeams = [
        {
          get name() { throw new Error('Property error'); },
          id: 1
        }
      ];

      const result = DataFilters.filterTeams(problematicTeams, 'test');
      expect(result).toEqual([]);
      expect(console.error).toHaveBeenCalledWith('Error filtering teams:', expect.any(Error));
    });
  });

  describe('filterGames', () => {
    const mockGames = [
      {
        id: 1,
        opponent: 'Thunder Hawks',
        location: 'Home Field',
        start_date: '2023-06-15T10:00:00Z'
      },
      {
        id: 2,
        opponent: 'Lightning Bolts',
        location: 'Away Field',
        start_date: '2023-06-20T14:00:00Z'
      },
      {
        id: 3,
        opponent: 'Storm Riders',
        location: 'Central Park',
        start_date: '2023-06-25T16:00:00Z'
      }
    ];

    test('should return all games when no search term provided', () => {
      const result = DataFilters.filterGames(mockGames, '');
      expect(result).toHaveLength(3);
    });

    test('should filter games by opponent name', () => {
      const result = DataFilters.filterGames(mockGames, 'thunder');
      expect(result).toHaveLength(1);
      expect(result[0].opponent).toBe('Thunder Hawks');
    });

    test('should filter games by location', () => {
      const result = DataFilters.filterGames(mockGames, 'home');
      expect(result).toHaveLength(1);
      expect(result[0].location).toBe('Home Field');
    });

    test('should filter games by date', () => {
      const result = DataFilters.filterGames(mockGames, '2023-06-15');
      expect(result).toHaveLength(1);
      expect(result[0].start_date).toContain('2023-06-15');
    });

    test('should sort games by date (most recent first)', () => {
      const result = DataFilters.filterGames(mockGames, '');
      expect(result[0].start_date).toBe('2023-06-25T16:00:00Z'); // Most recent
      expect(result[2].start_date).toBe('2023-06-15T10:00:00Z'); // Oldest
    });

    test('should skip sorting when option specified', () => {
      const result = DataFilters.filterGames(mockGames, '', { skipSorting: true });
      expect(result[0].id).toBe(1); // Original order maintained
    });

    test('should filter by date range', () => {
      const options = {
        startDate: '2023-06-16',
        endDate: '2023-06-24'
      };

      const result = DataFilters.filterGames(mockGames, '', options);
      expect(result).toHaveLength(1);
      expect(result[0].start_date).toBe('2023-06-20T14:00:00Z');
    });

    test('should handle non-array input', () => {
      const result = DataFilters.filterGames(null, 'test');
      expect(result).toEqual([]);
      expect(console.warn).toHaveBeenCalledWith('filterGames: games parameter is not an array');
    });

    test('should handle errors gracefully', () => {
      const problematicGames = [
        {
          get opponent() { throw new Error('Property error'); },
          id: 1
        }
      ];

      const result = DataFilters.filterGames(problematicGames, 'test');
      expect(result).toEqual([]);
      expect(console.error).toHaveBeenCalledWith('Error filtering games:', expect.any(Error));
    });
  });

  describe('filterPlayers', () => {
    const mockPlayers = [
      {
        id: 1,
        first_name: 'John',
        last_name: 'Smith',
        position: 'Pitcher',
        jersey_number: 15,
        availability_status: 'available'
      },
      {
        id: 2,
        first_name: 'Jane',
        last_name: 'Doe',
        position: 'Catcher',
        jersey_number: 8,
        availability_status: 'maybe'
      },
      {
        id: 3,
        first_name: 'Bob',
        last_name: 'Johnson',
        position: 'First Base',
        jersey_number: 22,
        availability_status: 'unavailable'
      }
    ];

    test('should filter players by first name', () => {
      const result = DataFilters.filterPlayers(mockPlayers, 'jane');
      expect(result).toHaveLength(1);
      expect(result[0].first_name).toBe('Jane');
    });

    test('should filter players by name substring (partial match)', () => {
      const result = DataFilters.filterPlayers(mockPlayers, 'john');
      expect(result).toHaveLength(2); // Finds "John" in first name and "john" in "Johnson" last name
      expect(result.some(p => p.first_name === 'John')).toBe(true);
      expect(result.some(p => p.last_name === 'Johnson')).toBe(true);
    });

    test('should filter players by last name', () => {
      const result = DataFilters.filterPlayers(mockPlayers, 'doe');
      expect(result).toHaveLength(1);
      expect(result[0].last_name).toBe('Doe');
    });

    test('should filter players by position', () => {
      const result = DataFilters.filterPlayers(mockPlayers, 'pitcher');
      expect(result).toHaveLength(1);
      expect(result[0].position).toBe('Pitcher');
    });

    test('should filter players by jersey number', () => {
      const result = DataFilters.filterPlayers(mockPlayers, '8');
      expect(result).toHaveLength(1);
      expect(result[0].jersey_number).toBe(8);
    });

    test('should filter available players only', () => {
      const result = DataFilters.filterPlayers(mockPlayers, '', { availableOnly: true });
      expect(result).toHaveLength(2);
      expect(result.every(p => p.availability_status !== 'unavailable')).toBe(true);
    });

    test('should filter by specific position', () => {
      const result = DataFilters.filterPlayers(mockPlayers, '', { position: 'Catcher' });
      expect(result).toHaveLength(1);
      expect(result[0].position).toBe('Catcher');
    });

    test('should handle non-array input', () => {
      const result = DataFilters.filterPlayers(null, 'test');
      expect(result).toEqual([]);
      expect(console.warn).toHaveBeenCalledWith('filterPlayers: players parameter is not an array');
    });
  });

  describe('genericSearch', () => {
    const mockItems = [
      { name: 'Apple', category: 'Fruit', price: 1.50 },
      { name: 'Banana', category: 'Fruit', price: 0.75 },
      { name: 'Carrot', category: 'Vegetable', price: 2.00 }
    ];

    test('should search all string properties when no fields specified', () => {
      const result = DataFilters.genericSearch(mockItems, 'fruit');
      expect(result).toHaveLength(2);
    });

    test('should search specific fields when provided', () => {
      const result = DataFilters.genericSearch(mockItems, 'apple', ['name']);
      expect(result).toHaveLength(1);
      expect(result[0].name).toBe('Apple');
    });

    test('should return all items when no search term', () => {
      const result = DataFilters.genericSearch(mockItems, '');
      expect(result).toEqual(mockItems);
    });

    test('should handle empty array', () => {
      const result = DataFilters.genericSearch([], 'test');
      expect(result).toEqual([]);
    });

    test('should handle null input', () => {
      const result = DataFilters.genericSearch(null, 'test');
      expect(result).toEqual([]);
    });

    test('should handle errors gracefully', () => {
      const problematicItems = [
        {
          get name() { throw new Error('Property error'); }
        }
      ];

      const result = DataFilters.genericSearch(problematicItems, 'test');
      expect(result).toEqual([]);
      expect(console.error).toHaveBeenCalledWith('Error in generic search:', expect.any(Error));
    });
  });
});
