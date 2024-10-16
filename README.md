# intelligent-oracle

## Current state

TODO: think of how to handle registration of contracts in the registry. Currently needs to be done "manually", like in the `seed.py` script.

### intelligent-oracle.py

- using `Registry` pattern
  - each contract deployment needs to be registered in the registry "manually". This is not the best UX.
- `Factory` pattern is missing given limitations in the Simulator.

### docker-compose.yml

Boots:

- simulator
  - postgres
  - database migration
  - jsonrpc
- seed: creates validators and registers contracts
- explorer

### Contract tests

There's only one e2e test with football prediction market.

TODO: Add more tests, with happy and sad paths.

### Explorer

Simple display working

TODO:

- add appeals (currently blocked by the simulator)
- allow submitting data sources
  - this feature might not make it to the final version, but it's great to tinker around

## Running

TODO:

- automate the creation of validators with https://github.com/yeagerai/genlayer-simulator/issues/567

### Common pitfalls

The envvar `VITE_CONTRACT_ADDRESS` is set at start time, and it's not dynamically updated. You will need to restart the explorer container to update it.

### Spin up

In a separate terminal run

```bash
docker-compose up --build
```

### Tests

Activate your Python virtual environment and then

```bash
pip install -r test/requirements.txt
```

```bash
pytest test/
```
