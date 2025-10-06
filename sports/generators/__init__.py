"""
Lineup generators for different sports.

This package contains the abstract base class and sport-specific implementations
for generating optimal lineups.
"""

from sports.generators.base import LineupGenerator
from sports.generators.baseball import BaseballLineupGenerator

__all__ = ["LineupGenerator", "BaseballLineupGenerator"]
