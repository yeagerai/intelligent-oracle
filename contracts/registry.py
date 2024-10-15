from backend.node.genvm.icontract import IContract


class Registry(IContract):

    def __init__(self):
        self.contract_addresses = []

    def register_contract(self, contract_address: str):  # TODO: add permissioning
        self.contract_addresses.append(contract_address)

    def get_contract_addresses(self) -> list[str]:
        return self.contract_addresses
