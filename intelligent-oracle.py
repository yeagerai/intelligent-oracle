"""
Temporary solutions:
* Imports are done in weird places given current limitations on how imports work in GenVM.
* Classes are nested. They should be defined at the top level.
"""

from typing import Any
from backend.node.genvm.icontract import IContract
from backend.node.genvm.equivalence_principle import EquivalencePrinciple
from enum import Enum


class Status(Enum):
    ACTIVE = "Active"
    RESOLVED = "Resolved"
    ERROR = "Error"


class IntelligentOracle:

    from datetime import datetime

    def __init__(
        self,
        id: str,
        creator: str,
        title: str,
        description: str,
        potential_outcomes: list[str],
        rules: list[str],
        data_sources: list[str],
        earliest_resolution_date: datetime,
    ):
        if not isinstance(id, str):
            raise ValueError("ID must be a string.")
        if id == "":  # TODO: should we have a predefined schema like uuid?
            raise ValueError("ID cannot be empty.")

        self.id = id
        self.creator = creator
        self.title = title
        self.description = description
        self.potential_outcomes = potential_outcomes
        self.rules = rules
        self.data_sources = data_sources
        self.status = Status.ACTIVE
        self.earliest_resolution_date = earliest_resolution_date

    def to_dict(self):
        return {
            "id": self.id,
            "creator": self.creator,
            "title": self.title,
            "description": self.description,
            "potential_outcomes": self.potential_outcomes,
            "rules": self.rules,
            "data_sources": self.data_sources,
            "status": self.status.value,
            "earliest_resolution_date": self.earliest_resolution_date.isoformat(),
        }


class IntelligentOracleFactory(IContract):

    def __init__(self):
        self.oracles: dict[str, IntelligentOracle] = {}

    async def register(
        self,
        id: str,
    ) -> None:
        """
        Create a new oracle and register it with the factory.
        """
        from datetime import datetime

        if id in self.oracles:
            raise ValueError(f"Oracle with ID {id} already exists.")

        oracle = IntelligentOracle(  # TODO: Replace with actual values.
            id=id,
            creator="",
            title="",
            description="",
            potential_outcomes=[],
            rules=[],
            data_sources=[],
            earliest_resolution_date=datetime.now(),
        )
        self.oracles[id] = oracle

    def get_oracle(self, oracle_id: str):
        """
        Get an oracle by its ID.
        """
        return self.oracles[oracle_id].to_dict()
