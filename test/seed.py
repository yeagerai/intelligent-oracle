"""
Seeds the project idempotently with:
- 1 validator
- Contracts:
  - 1 registry
  - 2 identical football prediction markets
"""

import json
import os
from dotenv import load_dotenv, set_key
from eth_account._utils.validation import is_valid_address
from tools.response import has_success_status, has_successful_execution
from tools.accounts import create_new_account
from tools.request import (
    deploy_intelligent_contract,
    payload,
    post_request,
    send_transaction,
)


def create_registry() -> str:
    contract_code = open("contracts/registry.py", "r").read()
    account = create_new_account()

    contract_address, transaction_response_deploy = deploy_intelligent_contract(
        account,
        contract_code,
        json.dumps({}),
    )
    assert has_success_status(transaction_response_deploy)
    assert has_successful_execution(transaction_response_deploy)

    return contract_address


def create_football_prediction_market(registry_contract_address: str) -> str:
    contract_code = open("contracts/intelligent-oracle.py", "r").read()
    account = create_new_account()

    title = "Football Prediction Market"
    description = "A market test"
    rules = ["The outcome is the winner of the match"]
    valid_data_sources = ["bbc"]
    potential_outcomes = ["Bayern Munich", "Arsenal"]
    earliest_resolution_date = "2024-01-01T00:00:00+00:00"
    prediction_market_id = "1"

    # Contract Deploy
    contract_address, transaction_response_deploy = deploy_intelligent_contract(
        account,
        contract_code,
        json.dumps(
            {
                "prediction_market_id": prediction_market_id,
                "title": title,
                "description": description,
                "potential_outcomes": potential_outcomes,
                "rules": rules,
                "valid_data_sources": valid_data_sources,
                "earliest_resolution_date": earliest_resolution_date,
            }
        ),
    )
    assert has_success_status(transaction_response_deploy)
    assert has_successful_execution(transaction_response_deploy)

    # Register the contract in the registry
    register_result = send_transaction(
        account,
        registry_contract_address,
        "register_contract",
        [contract_address],
    )
    assert has_success_status(register_result)
    assert has_successful_execution(register_result)

    return contract_address


if __name__ == "__main__":
    # Check if VITE_CONTRACT_ADDRESS is already set
    VITE_CONTRACT_ADDRESS_KEY = "VITE_CONTRACT_ADDRESS"
    load_dotenv()
    contract_address = os.getenv(VITE_CONTRACT_ADDRESS_KEY)
    if contract_address is not None and is_valid_address(contract_address):
        print(f"Registry already created at {contract_address}")
        exit(0)

    # Seed

    # Validators
    result = post_request(payload("sim_deleteAllValidators"))
    assert has_success_status(result)

    result = post_request(
        payload("sim_createRandomValidators", 1, 1, 2, ["openai"], ["gpt-4o"])
    ).json()
    assert has_success_status(result)

    registry_address = create_registry()
    for i in range(2):
        print(f"Creating football prediction market {i + 1}")
        create_football_prediction_market(registry_address)

    print(f"Registry address: {registry_address}")
    set_key(".env", "VITE_CONTRACT_ADDRESS", registry_address)
