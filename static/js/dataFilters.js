/**
 * Data Filtering Utilities
 * Handles filtering of teams, games, and other data collections
 */

const DataFilters = {
    /**
     * Filter teams based on search criteria
     * @param {Array} teams - Array of team objects
     * @param {string} searchTerm - Search term to filter by
     * @returns {Array} Filtered teams array
     */
    filterTeams(teams, searchTerm) {
        try {
            if (!Array.isArray(teams)) {
                console.warn('filterTeams: teams parameter is not an array');
                return [];
            }

            if (!searchTerm || searchTerm.trim() === '') {
                return teams;
            }

            const term = searchTerm.toLowerCase().trim();

            return teams.filter(team => {
                if (!team) return false;

                // Search in team name, ID, or division/league
                return team.name?.toLowerCase().includes(term) ||
                       team.id?.toString().toLowerCase().includes(term) ||
                       team.division?.toLowerCase().includes(term);
            });
        } catch (error) {
            console.error('Error filtering teams:', error);
            return [];
        }
    },

    /**
     * Filter games based on search criteria and team selection
     * @param {Array} games - Array of game objects
     * @param {string} searchTerm - Search term to filter by
     * @param {Object} options - Additional filtering options
     * @returns {Array} Filtered games array
     */
    filterGames(games, searchTerm, options = {}) {
        try {
            if (!Array.isArray(games)) {
                console.warn('filterGames: games parameter is not an array');
                return [];
            }

            let filtered = games;

            // Apply search term filter
            if (searchTerm && searchTerm.trim() !== '') {
                const term = searchTerm.toLowerCase().trim();

                filtered = filtered.filter(game => {
                    if (!game) return false;

                    // Search in opponent name, location, or date
                    return game.opponent?.toLowerCase().includes(term) ||
                           game.location?.toLowerCase().includes(term) ||
                           game.start_date?.includes(term);
                });
            }

            // Apply date range filter if specified
            if (options.startDate || options.endDate) {
                filtered = filtered.filter(game => {
                    if (!game.start_date) return false;

                    const gameDate = new Date(game.start_date);

                    if (options.startDate) {
                        const start = new Date(options.startDate);
                        if (gameDate < start) return false;
                    }

                    if (options.endDate) {
                        const end = new Date(options.endDate);
                        if (gameDate > end) return false;
                    }

                    return true;
                });
            }

            // Sort by date (most recent first) if no other sorting specified
            if (!options.skipSorting) {
                filtered = filtered.slice().sort((a, b) => {
                    const dateA = new Date(a.start_date || 0);
                    const dateB = new Date(b.start_date || 0);
                    return dateB - dateA;
                });
            }

            return filtered;
        } catch (error) {
            console.error('Error filtering games:', error);
            return [];
        }
    },

    /**
     * Filter players based on various criteria
     * @param {Array} players - Array of player objects
     * @param {string} searchTerm - Search term to filter by
     * @param {Object} options - Additional filtering options
     * @returns {Array} Filtered players array
     */
    filterPlayers(players, searchTerm, options = {}) {
        try {
            if (!Array.isArray(players)) {
                console.warn('filterPlayers: players parameter is not an array');
                return [];
            }

            let filtered = players;

            // Apply search term filter
            if (searchTerm && searchTerm.trim() !== '') {
                const term = searchTerm.toLowerCase().trim();

                filtered = filtered.filter(player => {
                    if (!player) return false;

                    // Search in player name, position, or jersey number
                    return player.first_name?.toLowerCase().includes(term) ||
                           player.last_name?.toLowerCase().includes(term) ||
                           player.position?.toLowerCase().includes(term) ||
                           player.jersey_number?.toString().includes(term);
                });
            }

            // Apply availability filter
            if (options.availableOnly) {
                filtered = filtered.filter(player => {
                    return player.availability_status === 'available' ||
                           player.availability_status === 'maybe';
                });
            }

            // Apply position filter
            if (options.position) {
                filtered = filtered.filter(player => {
                    return player.position &&
                           player.position.toLowerCase() === options.position.toLowerCase();
                });
            }

            return filtered;
        } catch (error) {
            console.error('Error filtering players:', error);
            return [];
        }
    },

    /**
     * Generic search function for arrays of objects
     * @param {Array} items - Array of objects to search
     * @param {string} searchTerm - Term to search for
     * @param {Array} searchFields - Fields to search in each object
     * @returns {Array} Filtered results
     */
    genericSearch(items, searchTerm, searchFields = []) {
        try {
            if (!Array.isArray(items) || !searchTerm || searchTerm.trim() === '') {
                return items || [];
            }

            const term = searchTerm.toLowerCase().trim();

            return items.filter(item => {
                if (!item) return false;

                // If no specific fields provided, search all string properties
                if (searchFields.length === 0) {
                    return Object.values(item).some(value =>
                        typeof value === 'string' &&
                        value.toLowerCase().includes(term)
                    );
                }

                // Search specific fields
                return searchFields.some(field => {
                    const value = item[field];
                    return typeof value === 'string' &&
                           value.toLowerCase().includes(term);
                });
            });
        } catch (error) {
            console.error('Error in generic search:', error);
            return [];
        }
    }
};

// Export for testing
if (typeof module !== 'undefined' && module.exports) {
    module.exports = { DataFilters };
}