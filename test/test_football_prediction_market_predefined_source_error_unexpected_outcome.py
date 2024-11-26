import json
from tools.accounts import create_new_account
from tools.request import (
    deploy_intelligent_contract,
    send_transaction,
    call_contract_method,
    payload,
    post_request,
)
from tools.structure import execute_icontract_function_response_structure
from tools.response import (
    assert_dict_struct,
    has_success_status,
    has_successful_execution,
)


def test_football_prediction_market_predefined_source_error_unexpected_outcome():
    # Account
    account = create_new_account()
    
    # Contract Schema
    contract_code = open("contracts/intelligent-oracle.py", "r").read()
    result_schema = post_request(
        payload("gen_getContractSchemaForCode", contract_code)
    ).json()
    assert has_success_status(result_schema)

    data_source = "https://www.bbc.com/sport/football/scores-fixtures/2024-10-10"

    title = "Football Prediction Market - Unexpected Outcome Test"
    description = "Testing market behavior with unexpected draw outcome"
    rules = ["The outcome is the result of the match"]
    data_source_domains = []
    resolution_urls = [data_source]
    # Deliberately excluding 'Draw' as a potential outcome
    potential_outcomes = ["Italy", "Belgium"]  
    earliest_resolution_date = "2024-01-01T00:00:00+00:00"
    prediction_market_id = "unexpected_outcome_test"

    # Contract Deploy
    contract_address, transaction_response_deploy = deploy_intelligent_contract(
        account,
        contract_code,
        [
            prediction_market_id,
            title,
            description,
            potential_outcomes,
            rules,
            data_source_domains,
            resolution_urls,
            earliest_resolution_date,
        ]
    )
    assert has_success_status(transaction_response_deploy)
    assert has_successful_execution(transaction_response_deploy)

    # Get Initial State
    contract_state = call_contract_method(contract_address, account, "get_dict", [])
    assert contract_state == {
        "creator": account.address,
        "title": title,
        "description": description,
        "potential_outcomes": potential_outcomes,
        "rules": rules,
        "data_source_domains": data_source_domains,
        "resolution_urls": resolution_urls,
        "status": "Active",
        "earliest_resolution_date": earliest_resolution_date,
        "analysis": None,
        "outcome": None,
        "prediction_market_id": prediction_market_id,
    }

    # Resolve the Prediction
    resolve_prediction_result = send_transaction(
        account,
        contract_address,
        "resolve",
        [],
    )
    assert has_success_status(resolve_prediction_result)
    assert has_successful_execution(resolve_prediction_result)

    # Check that the market entered Error state
    contract_state = call_contract_method(contract_address, account, "get_dict", [])
    assert contract_state["status"] == "Error"
    assert contract_state["outcome"] == None