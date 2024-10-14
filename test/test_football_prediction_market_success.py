# tests/e2e/test_wizard_of_coin.py

import json
from tools.accounts import create_new_account
from tools.request import (
    deploy_intelligent_contract,
    send_transaction,
    call_contract_method,
    payload,
    post_request_localhost,
)
from tools.structure import execute_icontract_function_response_structure
from tools.response import (
    assert_dict_struct,
    assert_dict_exact,
    has_success_status,
    has_successful_execution,
)


def test_football_prediction_market_success():
    # Account
    account = create_new_account()
    # Validators
    # result = post_request_localhost(
    #     payload("sim_createRandomValidators", 5, 8, 12, ["openai"], ["gpt-4o"])
    # ).json()
    # assert has_success_status(result)

    # Contract Schema
    contract_code = open("contracts/intelligent-oracle.py", "r").read()
    result_schema = post_request_localhost(
        payload("gen_getContractSchemaForCode", contract_code)
    ).json()
    assert has_success_status(result_schema)
    # assert_dict_exact(result_schema, football_prediction_market_contract_schema)

    title = "Football Prediction Market"
    description = "A market test"
    rules = []
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

    # "https://www.bbc.com/sport/football/scores-fixtures/2024-10-09"

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

    # # Create Successful Prediction
    # create_successful_prediction_result = send_transaction(
    #     account,
    #     contract_address,
    #     "create_prediction",
    #     ["2024-06-20", "Spain", "Italy", "1"],
    # )
    # assert has_success_status(create_successful_prediction_result)
    # assert_dict_struct(
    #     create_successful_prediction_result,
    #     execute_icontract_function_response_structure,
    # )

    # # Get Predictions
    # get_prediction_result = call_contract_method(
    #     contract_address, account, "get_predictions", []
    # )
    # print("~ ~ ~ ~ ~ get_prediction_result", get_prediction_result)
    # assert get_prediction_result == {
    #     account.address: test_football_prediction_market_predictions_win_unresolved
    # }

    # # Get Player Predictions
    # get_player_predictions_result = call_contract_method(
    #     contract_address, account, "get_player_predictions", [account.address]
    # )
    # assert (
    #     get_player_predictions_result
    #     == test_football_prediction_market_predictions_win_unresolved
    # )

    # # Resolve Successful Prediction
    # resolve_successful_prediction_result = send_transaction(
    #     account, contract_address, "resolve_prediction", ["2024-06-20_spain_italy"]
    # )
    # assert has_success_status(resolve_successful_prediction_result)
    # assert_dict_struct(
    #     resolve_successful_prediction_result,
    #     execute_icontract_function_response_structure,
    # )

    # # Get Predictions
    # get_prediction_result = call_contract_method(
    #     contract_address, account, "get_predictions", []
    # )
    # assert get_prediction_result == {
    #     account.address: test_football_prediction_market_predictions_win_resolved
    # }

    # # Get Player Predictions
    # get_player_predictions_result = call_contract_method(
    #     contract_address, account, "get_player_predictions", [account.address]
    # )
    # assert (
    #     get_player_predictions_result
    #     == test_football_prediction_market_predictions_win_resolved
    # )

    # # Get Points
    # get_points_result = call_contract_method(
    #     contract_address, account, "get_points", []
    # )
    # assert get_points_result == {account.address: 1}

    # # Get Player Points
    # get_player_points_result = call_contract_method(
    #     contract_address, account, "get_player_points", [account.address]
    # )
    # assert get_player_points_result == 1

    # # Delete Validators
    # delete_validators_result = post_request_localhost(
    #     payload("sim_deleteAllValidators")
    # ).json()
    # assert has_success_status(delete_validators_result)
