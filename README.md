# Intelligent Oracle System

A complete system for deploying and managing AI-powered oracles on the GenLayer blockchain. This system enables the creation and resolution of prediction markets using natural language processing and web data analysis.

## Prerequisites

Before running this project, ensure you have:

1. [GenLayer Studio](https://github.com/yeagerai/genlayer-simulator) installed and running locally
   - Docker 26+
   - Node.js 18+
   - Install with: `npm install -g genlayer`
   - Start with: `genlayer init --branch v0.21.1`

## Project Components

### 1. Intelligent Oracle Contracts
Located in [`/contracts`](/contracts)
- Intelligent Oracle contract for prediction market resolution
- Registry contract for managing deployed oracles
- Supports flexible data sources, multiple outcomes, and rule-based resolution

### 2. Bridge & Chat API
Located in [`/bridge`](/bridge)
- Handles oracle deployment to GenLayer blockchain
- Provides Chat API integration with OpenAI's GPT models

### 3. Configuration Wizard UI
Located in [`/ui-wizard`](/ui-wizard)
- Interactive chatbot interface for oracle configuration
- Step-by-step guidance through setup process
- Real-time AI assistance using GPT-4

### 4. Explorer Interface
Located in [`/explorer`](/explorer) 
- Simple dashboard for viewing deployed oracles
- Monitor oracle status and outcomes
- View market details and resolution data

## Getting Started

1. Start GenLayer Studio:
```bash
genlayer up
```

2. Spin up the project:
```bash
docker-compose up --build
```

3. Run tests:
```bash
# Activate your Python virtual environment first
pip install -r test/requirements.txt
pytest test/
```

## Common Pitfalls

- The `VITE_CONTRACT_ADDRESS` environment variable is set at startup and requires explorer container restart to update
- Contract registration currently needs manual handling through the `seed.py` script
- Factory pattern implementation is limited due to current Simulator constraints

## TODO List

- [ ] Implement appeals functionality (blocked by simulator development)
- [ ] Implement prodction market resolution via Bridge
- [ ] Add data source submission interface
- [ ] Implement factory pattern for Intelligent Oracle contract deployment

## Architecture

```
├── contracts/         # Smart contracts implementation
├── bridge/           # Backend API & blockchain integration
├── ui-wizard/        # Configuration wizard frontend
├── explorer/         # Oracle monitoring interface
└── test/            # E2E and contract tests
```

## Contributing

Contributions are welcome! Please check the individual component READMEs for specific development guidelines.

## License

MIT
