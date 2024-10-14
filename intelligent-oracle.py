"""
Temporary solutions:
- `global` imports are done in weird places given current limitations on how imports work in GenVM.
- we don't use a factory since we cannot deploy new contracts from a contract
"""

import json
from backend.node.genvm.icontract import IContract
from backend.node.genvm.equivalence_principle import EquivalencePrinciple
from enum import Enum
from datetime import datetime


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
        potential_outcomes: list[str],
        rules: list[str],
        valid_data_sources: list[
            str
        ],  # List of regex URL patterns for valid data sources. Users will provide data that matches on these patterns.
        data_sources: list[
            str
        ],  # List of URLs that need to match with one of valid_data_sources
        earliest_resolution_date: (
            datetime  # Minimum date and time when the oracle can be resolved
        ),
    ):
        self.prediction_market_id = prediction_market_id
        self.creator = contract_runner.from_address
        self.title = title
        self.description = description
        self.potential_outcomes = potential_outcomes
        self.rules = rules
        self.valid_data_sources = valid_data_sources
        self.earliest_resolution_date = earliest_resolution_date

        self.status = Status.ACTIVE

        if not isinstance(self.id, str):
            raise ValueError("ID must be a string.")
        if self.id == "":  # TODO: should we have a predefined schema like uuid?
            raise ValueError("ID cannot be empty.")

        if len(self.potential_outcomes) < 2:
            raise ValueError("At least two potential outcomes are required.")

        if len(self.potential_outcomes) != len(set(self.potential_outcomes)):
            raise ValueError("Potential outcomes must be unique.")

    async def submit_data_source(self, data_source: str):
        if self.status != Status.ACTIVE:
            raise ValueError("Cannot submit data source to a non-active oracle.")

        if data_source in self.data_sources:
            return  # skip duplicates

        final_result = {}
        async with EquivalencePrinciple(
            result=final_result,
            principle="The output should be the exact same",
            comparative=True,
        ) as eq:
            task = f"""Verify that the provided data source:
            - is valid among the valid data sources
            - is not already in the list of current data sources
            
            The valid data sources can be in the form of regex, URLs, or natural language.

            Valid data sources: {self.valid_data_sources}

            Current data sources: {self.data_sources}

            Data source to verify: {data_source}

            Respond only with True if the data source is valid, False otherwise.

            Do not respond with anything else, the result will be used as a boolean value in Python."""
            result = await eq.call_llm(task)
            eq.set(result)

        if final_result["output"] == "True":
            self.data_sources.append(data_source)

    async def resolve(self):
        if self.status != Status.ACTIVE:
            raise ValueError("Cannot resolve a non-active oracle.")
        if datetime.now() < self.earliest_resolution_date:
            raise ValueError("Cannot resolve before the earliest resolution date.")

        if not self.data_sources:
            raise ValueError("No data sources loaded.")

        # Analyze each webpage separately
        analyzed_data_sources_output = []
        for data_source in self.data_sources:
            final_result = {}
            async with EquivalencePrinciple(
                result=final_result,
                principle="`vote` field must be exactly the same. All other fields must be similar",
                comparative=True,
            ) as eq:
                web_data = await eq.get_webpage(data_source, "text")
                print(web_data)

                task = f"""You are an AI Validator tasked with resolving a prediction market Oracle. Your goal is to determine the correct outcome based on the user-defined rules, the provided webpage HTML content, the resolution date, and the list of potential outcomes.


### **Inputs:**

1. **Rules (Natural Language):**
   ```
   {self.rules}
   ```

2. **Webpage HTML Content:**
   ```
   {web_data}
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
   - If the information is insufficient or inconclusive, and you cannot confidently determine an outcome, select `None`.

3. **Provide a Justification:**
   - Write a clear, self-contained justification for your vote.
   - Reference specific parts of the rules and the extracted data that support your decision.
   - Ensure that someone reading the justification can understand your reasoning without needing additional information.

4. **Include Metadata:**
   - Add additional useful metadata, such as:
   - Confidence level (e.g., High, Medium, Low).
   - Any assumptions made during your analysis.
   - Relevant URLs or sources extracted from the HTML content.


### **Output Format:**

Provide your response in **valid JSON** format with the following structure:

```json
{
  "vote": "Chosen outcome from the potential outcomes list or `null` if undetermined",
  "justification": "Your detailed justification here.",
  "metadata": {
    "confidenceLevel": "High | Medium | Low",
    "assumptions": "Any assumptions you made during analysis.",
    "additionalSources": ["List of relevant URLs or sources, if any."]
  }
}
```

### **Constraints and Considerations:**

- **Accuracy:** Base your decision strictly on the provided inputs.
- **Objectivity:** Remain neutral and unbiased.
- **Clarity:** Make sure your justification is easy to understand.
- **Validity:** Ensure the JSON output is properly formatted and free of errors.
"""
                result = await eq.call_llm(task)
                print(result)
                eq.set(result)

            result_json = json.loads(final_result["output"])
            analyzed_data_sources_output.append(result_json)

        # Gather all results to form one final decision

        final_result = {}
        async with EquivalencePrinciple(
            result=final_result,
            principle="`vote` field must be exactly the same. All other fields must be similar",
            comparative=True,
        ) as eq:
            task = f"""You are an AI Validator tasked with resolving a prediction market Oracle. Your goal is to determine the correct outcome based on processed data from other AI Validators for many data sources. Here are your inputs

### **Inputs:**

1. **Rules (Natural Language):**
   ```
   {self.rules}
   ```

2. **Processed data from AI Validators:**
   ```
   {analyzed_data_sources_output}
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
{
  "vote": "Chosen outcome from the potential outcomes list or `null` if undetermined",
  "justification": "Your detailed justification here.",
  "metadata": {
    "confidenceLevel": "High | Medium | Low",
    "assumptions": "Any assumptions you made during analysis.",
    "additionalSources": ["List of relevant URLs or sources, if any."]
  }
}
```

### **Constraints and Considerations:**

- **Accuracy:** Base your decision strictly on the provided inputs.
- **Objectivity:** Remain neutral and unbiased.
- **Clarity:** Make sure your justification is easy to understand.
- **Validity:** Ensure the JSON output is properly formatted and free of errors.

"""
            result = await eq.call_llm(task)
            print(result)
            eq.set(result)

        result_json = json.loads(final_result["output"])

        # TODO: analyze output and update accordingly

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
