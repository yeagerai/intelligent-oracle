execute_icontract_function_response_structure = {
    "consensus_data": {
        "final": bool,
        "leader_receipt": {
            "calldata": str,
            "class_name": str,
            "contract_state": str,
            "eq_outputs": {"leader": dict},
            "error": str | None,
            "execution_result": str,
            "gas_used": int,
            "method": str,
            "mode": str,
            "node_config": {
                "address": str,
                "config": dict,
                "model": str,
                "provider": str,
                "stake": int,
                "plugin": str,
                "plugin_config": dict,
            },
            "vote": str,
            "pending_transactions": list,
        },
        "validators": list,
        "votes": dict,
    },
    "created_at": str,
    "data": {
        "calldata": str,
    },
    "from_address": str,
    "hash": str,
    "status": str,
    "to_address": str,
    "type": int,
    "value": int,
}
