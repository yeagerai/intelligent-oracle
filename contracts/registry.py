from genlayer import *

@gl.contract
class Registry:
    # Declare persistent storage fields
    contract_addresses: DynArray[str]

    def __init__(self):
        self.contract_addresses = DynArray[str]()

    @gl.public.write
    def register_contract(self, contract_address: str) -> None:  # TODO: add permissioning
        self.contract_addresses.append(contract_address)

    @gl.public.view
    def get_contract_addresses(self) -> list[str]:
        return list(self.contract_addresses)
