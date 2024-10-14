from eth_account import Account
from eth_utils import to_hex
import rlp
from eth_account._utils.legacy_transactions import Transaction


def encode_transaction_data(data: list) -> str:
    params_bytes = [bytes(param, "utf-8") for param in data]
    serialized_data = rlp.encode(params_bytes)
    return to_hex(serialized_data)


def sign_transaction(
    account: Account, data: list = None, to: str = None, value: int = 0
) -> dict:
    transaction = {
        "nonce": 0,
        "gasPrice": 0,
        "gas": 0,
        "to": to,
        "value": value,
    }

    if data is not None:
        encoded_data = encode_transaction_data(data)
        transaction["data"] = encoded_data

    signed_transaction = Account.sign_transaction(transaction, account.key)
    return to_hex(signed_transaction.raw_transaction)
