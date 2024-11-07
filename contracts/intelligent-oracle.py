"""
Temporary solutions:
- `global` imports are done in weird places given current limitations on how imports work in GenVM.
- we don't use a factory since we cannot deploy new contracts from a contract
"""

import json
from backend.node.genvm.icontract import IContract
from backend.node.genvm.equivalence_principle import (
    call_llm_with_principle,
    get_webpage_with_principle,
)
from enum import Enum
from datetime import datetime, timezone


class Status(Enum):
    ACTIVE = "Active"
    RESOLVED = "Resolved"
    ERROR = "Error"


class IntelligentOracle(IContract):
    global Status  # needed due to limitation in the simulator imports
    global datetime  # needed due to limitation in the simulator imports

    def __init__(
        self,
        # TODO # oragle_registry: str, # the registry where this contract will register itself
        prediction_market_id: (
            str  # Used to communicate back to the prediction market through the bridge
        ),
        title: str,
        description: str,
        potential_outcomes: str,
        rules: str,
        data_source_domains: str,  # List of domains for valid data sources.
        resolution_urls: str,  # List of URL to resolve the prediction.
        earliest_resolution_date: (
            str  # Minimum date and time when the oracle can be resolved
        ),
    ):
        if (
            not prediction_market_id
            or not title
            or not description
            or not potential_outcomes
            or not rules
            or not earliest_resolution_date
        ):
            raise ValueError("Missing required fields.")

        if not resolution_urls and not data_source_domains:
            raise ValueError("Missing resolution URLs or data source domains.")

        if len(resolution_urls) > 0 and len(data_source_domains) > 0:
            raise ValueError(
                "Cannot provide both resolution URLs and data source domains."
            )

        self.potential_outcomes = [
            outcome.strip() for outcome in potential_outcomes.split(",")
        ]

        if len(self.potential_outcomes) < 2:
            raise ValueError("At least two potential outcomes are required.")

        if len(self.potential_outcomes) != len(set(self.potential_outcomes)):
            raise ValueError("Potential outcomes must be unique.")

        self.prediction_market_id = prediction_market_id
        self.title = title
        self.description = description

        self.rules = [rule.strip() for rule in rules.split(",")]
        self.data_source_domains = [
            datasource.strip()
            .replace("http://", "")
            .replace("https://", "")
            .replace("www.", "")
            for datasource in data_source_domains.split(",")
            if datasource.strip()
        ]
        self.resolution_urls = [
            url.strip() for url in resolution_urls.split(",") if url.strip()
        ]

        # Parse earliest_resolution_date with timezone info
        self.earliest_resolution_date = datetime.fromisoformat(earliest_resolution_date)
        if self.earliest_resolution_date.tzinfo is None:
            # Assume UTC if no timezone is provided
            self.earliest_resolution_date = self.earliest_resolution_date.replace(
                tzinfo=timezone.utc
            )

        self.status = Status.ACTIVE
        self.analysis = None
        self.outcome = None

    async def _check_evidence(self, evidenze: str):
        if evidenze in self.data_source_domains:
            return True

        if any(data_source in evidenze for data_source in self.data_source_domains):
            return True

        return False

    async def resolve(self, evidence_url: str = ""):
        if self.status == Status.RESOLVED:
            raise ValueError("Cannot resolve an already resolved oracle.")

        if datetime.now().astimezone() < self.earliest_resolution_date:
            raise ValueError("Cannot resolve before the earliest resolution date.")

        if len(self.resolution_urls) > 0 and evidence_url:
            raise ValueError(
                "An evidence URL was provided but the oracle is configured to use resolution URLs already provided."
            )

        if len(self.resolution_urls) == 0 and not evidence_url:
            raise ValueError(
                "No evidence URL provided and the oracle is not configured to use resolution URLs."
            )

        if evidence_url:
            is_valid = await self._check_evidence(evidence_url)
            if not is_valid:
                raise ValueError(
                    "The evidence URL does not match any of the data source domains."
                )

        # Analyze each webpage separately
        analyzed_outputs = []
        resources_to_check = (
            self.resolution_urls if len(self.resolution_urls) > 0 else [evidence_url]
        )

        for resource_url in resources_to_check:
            resource_web_data = await get_webpage_with_principle(
                resource_url, "Web page data should coincide"
            )
            print(resource_web_data)

            task = f"""You are an AI Validator tasked with resolving a prediction market Oracle. 
            Your goal is to determine the correct outcome based on the user-defined rules, 
            the provided webpage HTML content, the resolution date, and the list of potential outcomes.

            ### **Inputs:**
            1. **Rules (Natural Language):**
            ```
            {self.rules}
            ```

            2. **Webpage HTML Content:**
            ```
            The following URL was used to provide resolution: {resource_url}
            Content extracted from the webpage:
            {resource_web_data}
            ```

            3. **Resolution Date:**
            ```
            {self.earliest_resolution_date}
            ```

            4. **Potential Outcomes:**
            ```
            {self.potential_outcomes}
            ```
         

            ### **Your Task:**
            1. **Analyze the Inputs:**
            - Carefully read and interpret the user-defined rules.
            - Parse the HTML content to extract meaningful information relevant to the rules.
            - Consider the resolution date in your analysis to ensure timeliness of the data.

            2. **Determine Your Vote:**
            - Based on your analysis, decide which potential outcome is correct.
            - If the information is insufficient or inconclusive, and you cannot confidently determine an outcome, your output vote should be `null`.

            3. **Provide Reasoning:**
            - Write a clear, self-contained reasoning for your vote.
            - Reference specific parts of the rules and the extracted data that support your decision.
            - Ensure that someone reading the reasoning can understand it without needing additional information.

            4. **Include Metadata:**
            - Add additional useful metadata, such as:
            - Confidence level (e.g., High, Medium, Low).
            - Any assumptions made during your analysis.
            - Relevant URLs or sources extracted from the HTML content.


            ### **Output Format:**

            Provide your response in **valid JSON** format with the following structure:

            ```json
            {{
                "vote": "Chosen outcome from the potential outcomes list or `null` if undetermined",
                "reasoning": "Your detailed reasoning here.",
                "metadata": {{
                    "confidenceLevel": "High | Medium | Low",
                    "assumptions": "Any assumptions you made during analysis.",
                    "additionalSources": ["List of relevant URLs or sources, if any."]
                }}
            }}
            ```

            ### **Constraints and Considerations:**

            - **Accuracy:** Base your decision strictly on the provided inputs.
            - **Objectivity:** Remain neutral and unbiased.
            - **Clarity:** Make sure your reasoning is easy to understand.
            - **Validity:** Ensure the JSON output is properly formatted and free of errors. It should be parseable by Python.
            """
            result = await call_llm_with_principle(
                task,
                "`vote` field must be exactly the same. All other fields must be similar",
            )
            result_dict = _parse_json_dict(result)
            analyzed_outputs.append(result_dict)

        # Gather all results to form one final decision

        task = f"""You are an AI Validator tasked with resolving a prediction market Oracle. Your goal is to determine 
        the correct outcome based on processed data from other AI Validators for many data sources. Here are your inputs

        ### **Inputs:**
        1. **Rules (Natural Language):**
        ```
        {self.rules}
        ```

        2. **Processed data from AI Validators:**
        ```
        {analyzed_outputs}
        ```

        3. **Resolution Date:**
        ```
        {self.earliest_resolution_date}
        ```

        4. **Potential Outcomes:**
        ```
        {self.potential_outcomes}
        ```

        ### **Your Task:**
        1. **Analyze the Inputs:**
        - Carefully read and interpret the user-defined rules.
        - Take into account all the processed data form the other AI Validators.
        - Consider the resolution date in your analysis to ensure timeliness of the data.

        2. **Determine Your Vote:**
        - The output should be determined mainly from the processed data form the other AI Validators.
        - Based on your analysis, decide which potential outcome is correct.
        - Your response should reflect a coherent summary outcome from the previous analysis.

        ### **Output Format:**

        Provide your response in **valid JSON** format with the following structure:

        ```json
        {{
        "vote": "Chosen outcome from the potential outcomes list or `null` if undetermined",
        "reasoning": "Your detailed reasoning here.",
        "metadata": {{
                "confidenceLevel": "High | Medium | Low",
                "assumptions": "Any assumptions you made during analysis.",
                "additionalSources": ["List of relevant URLs or sources, if any."]
            }}
        }}
        ```

        ### **Constraints and Considerations:**

        - **Accuracy:** Base your decision strictly on the provided inputs.
        - **Objectivity:** Remain neutral and unbiased.
        - **Clarity:** Make sure your reason is easy to understand.
        - **Validity:** Ensure the JSON output is properly formatted and free of errors.

        """

        result = await call_llm_with_principle(
            task,
            "`vote` field must be exactly the same. All other fields must be similar",
        )
        result_dict = _parse_json_dict(result)
        self.analysis = result_dict

        if (
            result_dict["vote"] is None
            or result_dict["vote"] not in self.potential_outcomes
        ):
            self.status = Status.ERROR
            return

        self.outcome = result_dict["vote"]
        self.status = Status.RESOLVED

    def get_dict(self) -> dict[str]:
        return {
            "title": self.title,
            "description": self.description,
            "potential_outcomes": self.potential_outcomes,
            "rules": self.rules,
            "data_sources_domains": self.data_source_domains,
            "resolution_urls": self.resolution_urls,
            "status": self.status.value,
            "earliest_resolution_date": self.earliest_resolution_date.isoformat(),
            "analysis": self.analysis,
            "outcome": self.outcome,
            "prediction_market_id": self.prediction_market_id,
        }

    def get_status(self) -> str:
        return self.status.value


def _parse_json_dict(json_str: str) -> dict:
    """
    Used to sanitize the JSON output from the LLM.
    Remove everything before the first '{' and after the last '}'
    """
    first_brace = json_str.find("{")
    last_brace = json_str.rfind("}")
    json_str = json_str[first_brace : last_brace + 1]
    return json.loads(json_str)
