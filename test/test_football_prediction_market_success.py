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


def test_football_prediction_market_success():
    # Account
    account = create_new_account()
    # Validators
    # result = post_request(
    #     payload("sim_createRandomValidators", 5, 8, 12, ["openai"], ["gpt-4o"])
    # ).json()
    # assert has_success_status(result)

    # Contract Schema
    contract_code = open("contracts/intelligent-oracle.py", "r").read()
    result_schema = post_request(
        payload("gen_getContractSchemaForCode", contract_code)
    ).json()
    assert has_success_status(result_schema)
    # assert_dict_exact(result_schema, football_prediction_market_contract_schema)

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

    # Get Initial State
    contract_state = call_contract_method(contract_address, account, "get_dict", [])
    assert contract_state == {
        "creator": account.address,
        "title": title,
        "description": description,
        "potential_outcomes": potential_outcomes,
        "rules": rules,
        "valid_data_sources": valid_data_sources,
        "data_sources": [],
        "status": "Active",
        "earliest_resolution_date": earliest_resolution_date,
        "analysis": None,
        "outcome": None,
        "prediction_market_id": prediction_market_id,
    }

    data_source = "https://www.bbc.com/sport/football/scores-fixtures/2024-10-09"
    # Submit Data Source

    submit_data_source_result = send_transaction(
        account,
        contract_address,
        "submit_data_source",
        [data_source],
    )
    assert has_success_status(submit_data_source_result)
    assert_dict_struct(
        submit_data_source_result,
        execute_icontract_function_response_structure,
    )

    # Check that the data source was added to the list of data sources
    contract_state = call_contract_method(contract_address, account, "get_dict", [])
    assert contract_state["data_sources"] == [data_source]

    # Resolve the Prediction
    resolve_prediction_result = send_transaction(
        account,
        contract_address,
        "resolve",
        [],
    )
    print(resolve_prediction_result)
    assert has_success_status(resolve_prediction_result)
    assert_dict_struct(
        resolve_prediction_result, execute_icontract_function_response_structure
    )
    assert has_successful_execution(resolve_prediction_result)

    # Check that the outcome was set
    contract_state = call_contract_method(contract_address, account, "get_dict", [])
    print(contract_state)
    assert contract_state["outcome"] == "Bayern Munich"
