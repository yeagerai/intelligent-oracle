# intelligent-oracle

## Current state

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
- explorer

### Contract tests

Started adding e2e test like in the simulator

### Explorer

Copied UI from boilerplate repo

## Running

This still has many manual steps that need to be addresssed with new features in the simulator + docker compose orchestration.

### Python dependencies

Activate your Python virtual environment and then

```bash
pip install -r test/requirements.txt
```

### Spin up the simulator

In a separate terminal run

```bash
docker-compose up --build jsonrpc
```

### Seeding the database

```bash
python test/seed.py
```

This will print the address of the registry contract that can be used to interact with the contracts.

### Spin up the explorer

Fill the `.env` file with the registry contract address and then in a separate terminal run

```bash
docker-compose up --build explorer
```

### Tests

```bash
pytest test/
```
