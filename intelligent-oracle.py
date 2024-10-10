"""
Temporary solutions:
* Imports are done in weird places given current limitations on how imports work in GenVM.
* Classes are nested. They should be defined at the top level.
"""

from typing import Any
import uuid
from backend.node.genvm.icontract import IContract
from backend.node.genvm.equivalence_principle import EquivalencePrinciple


class IntelligentOracleFactory(IContract):

    def __init__(self):
        self.oracles: dict[str, IntelligentOracleFactory.IntelligentOracle] = {}

    async def register(
        self,
    ) -> None:
        """
        Create a new oracle and register it with the factory.
        """
        oracle = IntelligentOracleFactory.IntelligentOracle()
        self.oracles[oracle.id] = oracle

    async def get(self, oracle_id: str):
        """
        Get an oracle by its ID.
        """
        return self.oracles[oracle_id]

    class IntelligentOracle:
        from datetime import datetime

        def __init__(
            self,
            creator: str,
            title: str,
            description: str,
            potential_outcomes: list[str],
            rules: Any,
            data_sources: list[str],
            earliest_resolution_date: datetime,
        ):
            self.id = uuid.uuid4()
            self.creator = creator
            self.title = title
            self.description = description
            self.potential_outcomes = potential_outcomes
            self.rules = rules
            self.data_sources = data_sources
            self.status = IntelligentOracleFactory.IntelligentOracle.Status.ACTIVE
            self.earliest_resolution_date = earliest_resolution_date

        from enum import Enum

        class Status(Enum):
            ACTIVE = "Active"
            RESOLVED = "Resolved"
            ERROR = "Error"
