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
import re


@dataclass
class CheckTypes:
    def __post_init__(self):
        for name, field_type in self.__annotations__.items():
            if not isinstance(self.__dict__[name], field_type):
                current_type = type(self.__dict__[name])
                raise TypeError(
                    f"The field `{name}` was assigned by `{current_type}` instead of `{field_type}`"
                )

        print("Check is passed successfully")


class Status(Enum):
    ACTIVE = "Active"
    RESOLVED = "Resolved"
    ERROR = "Error"


@dataclass
class IntelligentOracle(CheckTypes):
    global Status  # needed due to limitation in the simulator imports
    global datetime  # needed due to limitation in the simulator imports

    id: str
    prediction_market_id: (
        str  # Used to communicate back to the prediction market through the bridge
    )
    creator: str
    title: str
    description: str
    potential_outcomes: list[str]
    rules: list[str]
    valid_data_sources: list[
        str
    ]  # List of regex URL patterns for valid data sources. Users will provide data that matches on these patterns.
    data_sources: list[
        str
    ]  # List of URLs that need to match with one of valid_data_sources
    earliest_resolution_date: (
        datetime  # Minimum date and time when the oracle can be resolved
    )
    status: Status

    def __post_init__(self):
        if not isinstance(self.id, str):
            raise ValueError("ID must be a string.")
        if self.id == "":  # TODO: should we have a predefined schema like uuid?
            raise ValueError("ID cannot be empty.")

        if len(self.potential_outcomes) < 2:
            raise ValueError("At least two potential outcomes are required.")

        for valid_data_source in self.valid_data_sources:

            try:
                re.compile(valid_data_source)
            except re.error:
                raise ValueError(
                    f"Invalid regex pattern for data source: {valid_data_source}"
                )

        for data_source in self.data_sources:
            if not any(
                re.match(valid_data_source, data_source)
                for valid_data_source in self.valid_data_sources
            ):
                raise ValueError(
                    f"Data source {data_source} does not match any valid data source pattern."
                )

    async def submit_data_source(self, data_source: str):
        if self.status != Status.ACTIVE:
            raise ValueError("Cannot submit data source to a non-active oracle.")

        final_result = {}
        async with EquivalencePrinciple(
            result=final_result,
            principle="The output should be the exact same",
            comparative=True,
        ) as eq:
            task = (
                f"""Verify that the provided data source is valid among the valid data sources. The valid data sources can be in the form of regex, URLs, or natural language.

            Valid data sources: {self.valid_data_sources}

            Data source to verify: {data_source}

            Respond only with True if the data source is valid, False otherwise.

            Do not respond with anything else, the result will be used as a boolean value in Python.
""",
            )
            result = await eq.call_llm(task)
            eq.set(result)
        self.data_sources.append(data_source)

    def resolve(self):
        if self.status != Status.ACTIVE:
            raise ValueError("Cannot resolve a non-active oracle.")
        if datetime.now() < self.earliest_resolution_date:
            raise ValueError("Cannot resolve before the earliest resolution date.")

        if not self.data_sources:
            raise ValueError("No data sources loaded.")

        # TODO: call llms and web scrapers like the example contract PredictionMarket does
        self.status = Status.RESOLVED

    def to_dict(self):
        return {
            "id": self.id,
            "creator": self.creator,
            "title": self.title,
            "description": self.description,
            "potential_outcomes": self.potential_outcomes,
            "rules": self.rules,
            "valid_data_sources": self.valid_data_sources,
            "data_sources": self.data_sources,
            "status": self.status.value,
            "earliest_resolution_date": self.earliest_resolution_date.isoformat(),
        }


class IntelligentOracleFactory(IContract):

    def __init__(self):
        self.oracles: dict[str, IntelligentOracle] = {}

    def register(
        self,
        id: str,  # will change to oracleContractAddress in the future
    ) -> None:
        """
        Create a new oracle and register it with the factory.
        """
        from datetime import datetime

        if id in self.oracles:
            raise ValueError(f"Oracle with ID {id} already exists.")

        oracle = IntelligentOracle(  # TODO: Replace with actual values.
            id=id,
            creator=contract_runner.from_address,
            title="",
            description="",
            potential_outcomes=[],
            rules=[],
            valid_data_sources=[],
            data_sources=[],
            earliest_resolution_date=datetime.now(),
            status=Status.ACTIVE,
        )
        self.oracles[id] = oracle

    async def resolve(self, oracle_id: str):
        await self.oracles[oracle_id].resolve()

    async def submit_data_source(self, oracle_id: str, data_source: str):
        await self.oracles[oracle_id].submit_data_source(data_source)

    def get_oracle(self, oracle_id: str):
        """
        Get an oracle by its ID.
        """
        return self.oracles[oracle_id].to_dict()
