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
    EquivalencePrinciple,
)
from enum import Enum
from datetime import datetime, timezone
from urllib.parse import urlparse


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
        potential_outcomes: list,
        rules: list,
        data_source_domains: list,  # List of domains for valid data sources.
        resolution_urls: list,  # List of URL to resolve the prediction.
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

        self.potential_outcomes = [outcome.strip() for outcome in potential_outcomes]

        if len(self.potential_outcomes) < 2:
            raise ValueError("At least two potential outcomes are required.")

        if len(self.potential_outcomes) != len(set(self.potential_outcomes)):
            raise ValueError("Potential outcomes must be unique.")

        self.prediction_market_id = prediction_market_id
        self.title = title
        self.description = description

        self.rules = [rule.strip() for rule in rules]
        self.data_source_domains = [
            datasource.strip()
            .lower()
            .replace("http://", "")
            .replace("https://", "")
            .replace("www.", "")
            for datasource in data_source_domains
            if datasource.strip()
        ]
        self.resolution_urls = [url.strip() for url in resolution_urls if url.strip()]

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
        self.creator = contract_runner.from_address

    async def _check_evidence(self, evidence: str):
        try:
            # Parse the evidence URL
            parsed_url = urlparse(evidence)
            evidence_domain = parsed_url.netloc.lower().replace('www.', '')
            
            # Compare with allowed domains (which are already normalized)
            return evidence_domain in self.data_source_domains
            
        except Exception:
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
            result_dict = {}
            async with EquivalencePrinciple(
                result=result_dict,
                principle="`outcome` field must be exactly the same. All other fields must be similar",
                comparative=True,
            ) as eq:
                resource_web_data = await eq.get_webpage(resource_url, "text") 
                print(resource_web_data)

                task = f"""
You are an AI Validator tasked with resolving a prediction market. 
Your goal is to determine the correct outcome based on the user-defined rules, 
the provided webpage HTML content, the resolution date, and the list of potential outcomes.

### Inputs
<title>
{self.title}
</title>

<description>
{self.description}
</description>

<potential_outcomes>
{self.potential_outcomes}
</potential_outcomes>

<rules>
{self.rules}
</rules>

<source_url>
{resource_url}
</source_url>

<webpage_content>
{resource_web_data}
</webpage_content>

<current_date>
{datetime.now().astimezone()}
</current_date>

<earliest_resolution_date>
{self.earliest_resolution_date}
</earliest_resolution_date>




### **Your Task:**
1. **Analyze the Inputs:**
- Carefully read and interpret the user-defined rules.
- Parse the HTML content to extract meaningful information relevant to the rules.
- Determine if the source pertains to the event that is being predicted.
- Determine if the event has occurred yet.

2. **Provide Reasoning:**
- Write a clear, self-contained reasoning for the outcome.
- Reference specific parts of the rules and the extracted data that support your decision.
- Ensure that someone reading the reasoning can understand it without needing additional information.

3. **Determine The Outcome:**
- Based on your analysis, decide which potential outcome is correct.
- If an outcome can be determined, but the outcome is not in the list of potential outcomes, the outcome should be `ERROR`.
- If the information is insufficient or inconclusive, or the event has not occurred yet, and you cannot confidently determine an outcome based on this source, the outcome should be `UNDETERMINED`.




### **Output Format:**

Provide your response in **valid JSON** format with the following structure:

```json
{{
    "valid_source": "true | false",
    "event_has_occurred": "true | false",
    "reasoning": "Your detailed reasoning here",
    "outcome": "Chosen outcome from the potential outcomes list, `UNDETERMINED` if no outcome can be determined based on this source, `ERROR` if the outcome is not in the potential outcomes list"                
}}
```

### **Constraints and Considerations:**

- **Accuracy:** Base your decision strictly on the provided inputs.
- **Objectivity:** Remain neutral and unbiased.
- **Clarity:** Make sure your reasoning is easy to understand.
- **Validity:** Ensure the JSON output is properly formatted and free of errors. Do not include trailing commas.
                """
                result = await eq.call_llm(task)
                print(result)
                result_dict = _parse_json_dict(result)
                eq.set(analyzed_outputs)
            
            analyzed_outputs.append((resource_url, result_dict))

        # Gather all results to form one final decision

        task = f"""
You are an AI Validator tasked with resolving a prediction market Oracle. Your goal is to determine 
the correct outcome based on processed data from all of the individial data sources. Here are your inputs

### Inputs
<title>
{self.title}
</title>

<description>
{self.description}
</description>

<potential_outcomes>
{self.potential_outcomes}
</potential_outcomes>

<rules>
{self.rules}
</rules>

<processed_data>
{analyzed_outputs}
</processed_data>

<current_date>
{datetime.now().astimezone()}
</current_date>

<earliest_resolution_date>
{self.earliest_resolution_date}
</earliest_resolution_date>

### **Your Task:**
1. **Analyze the Inputs:**
- Carefully read and interpret the user-defined rules.
- Take into account all the processed data form the sources.
- Consider the resolution date in your analysis to ensure timeliness of the data.

2. **Determine The Outcome:**
- The output should be determined from the processed data form the resolution sources.
- Based on your analysis, decide which potential outcome is correct.
- If an outcome can be determined, but the outcome is not in the list of potential outcomes, the outcome should be `ERROR`.
- If the information is insufficient or inconclusive, and you cannot confidently determine an outcome, the outcome should be `UNDETERMINED`.
- Your response should reflect a coherent summary outcome from the previous analysis.
- If multiple sources contradict each other, refer to the rules to determine how to resolve the contradiction.
- If the rules do not provide a clear resolution, the outcome should be `ERROR`.

### **Output Format:**

Provide your response in **valid JSON** format with the following structure:

```json
{{
"relevant_sources": "List of URLs that are relevant to the outcome",
"reasoning": "Your detailed reasoning here",
"outcome": "Chosen outcome from the potential outcomes list, `UNDETERMINED` if undetermined, `ERROR` if the outcome is not in the potential outcomes list"        
}}
```

### **Constraints and Considerations:**

- **Accuracy:** Base your decision strictly on the provided inputs.
- **Objectivity:** Remain neutral and unbiased.
- **Clarity:** Make sure your reason is easy to understand.
- **Validity:** Ensure the JSON output is properly formatted and free of errors. Do not include trailing commas.

        """

        result = await call_llm_with_principle(
            task,
            "`outcome` field must be exactly the same. All other fields must be similar",
        )
        print(result)
        result_dict = _parse_json_dict(result)
        self.analysis = result_dict

        if result_dict["outcome"] == "UNDETERMINED":
            # Not enough information to determine the outcome, keep the oracle active
            return
        
        if result_dict["outcome"] == "ERROR" or result_dict["outcome"] not in self.potential_outcomes:
            self.status = Status.ERROR
            return

        self.outcome = result_dict["outcome"]
        self.status = Status.RESOLVED

    def get_dict(self) -> dict[str]:
        return {
            "creator": self.creator,
            "title": self.title,
            "description": self.description,
            "potential_outcomes": self.potential_outcomes,
            "rules": self.rules,
            "data_source_domains": self.data_source_domains,
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
    Remove everything before the first '{' and after the last '}', and remove trailing commas before closing braces/brackets
    """
    first_brace = json_str.find("{")
    last_brace = json_str.rfind("}")
    json_str = json_str[first_brace : last_brace + 1]

    # Remove trailing commas before closing braces/brackets
    import re
    json_str = re.sub(r',(?!\s*?[\{\[\"\'\w])', '', json_str)
    print(json_str)

    return json.loads(json_str)
