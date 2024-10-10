"""
Temporary solutions:
* Imports are done in weird places given current limitations on how imports work in GenVM.
* Classes are nested. They should be defined at the top level.
"""

from backend.node.genvm.icontract import IContract
from backend.node.genvm.equivalence_principle import EquivalencePrinciple
from enum import Enum
from dataclasses import dataclass
from datetime import datetime


class Status(Enum):
    ACTIVE = "Active"
    RESOLVED = "Resolved"
    ERROR = "Error"


@dataclass
class IntelligentOracle:
    global Status  # needed due to limitation in the simulator imports
    global datetime  # needed due to limitation in the simulator imports

    id: str
    creator: str
    title: str
    description: str
    potential_outcomes: list[str]
    rules: list[str]
    data_sources: list[str]
    earliest_resolution_date: datetime
    status: Status

    def __post_init__(self):
        if not isinstance(self.id, str):
            raise ValueError("ID must be a string.")
        if self.id == "":  # TODO: should we have a predefined schema like uuid?
            raise ValueError("ID cannot be empty.")

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
            status=Status.ACTIVE,
        )
        self.oracles[id] = oracle

    def get_oracle(self, oracle_id: str):
        """
        Get an oracle by its ID.
        """
        return self.oracles[oracle_id].to_dict()
