# Intelligent Oracle System

This repository contains the Intelligent Contracts for an AI-powered oracle system that can resolve prediction markets using natural language processing and web data analysis.

## Contracts Overview

### IntelligentOracle

The `IntelligentOracle` contract serves as an AI-powered oracle that can resolve prediction market outcomes by analyzing web content using Large Language Models (LLMs).

#### Key Features

- **Flexible Data Sources**: Supports both predefined resolution URLs and dynamic evidence URL validation
- **Multiple Outcome Support**: Handles multiple potential outcomes for prediction markets
- **Rule-based Resolution**: Uses natural language rules to guide the resolution process
- **AI-Powered Analysis**: Leverages LLMs to analyze web content and determine outcomes
- **Domain Validation**: Ensures evidence URLs come from trusted domains
- **Time-locked Resolution**: Prevents resolution before a specified date

#### Initialization Parameters

- `prediction_market_id`: Identifier for communication with the prediction market
- `title`: Title of the oracle
- `description`: Detailed description of what is being predicted
- `potential_outcomes`: Comma-separated list of possible outcomes
- `rules`: Comma-separated list of resolution rules
- `data_source_domains`: Allowed domains for evidence URLs. If set, `resolution_urls` need to be empty.
- `resolution_urls`: Predefined URLs for resolution. If set, `data_source_domains` need to be empty.
- `earliest_resolution_date`: Earliest date when the oracle can be resolved

### Registry

The `Registry` contract maintains a list of deployed intelligent oracle contracts, serving as a central directory.

#### Features

- **Contract Registration**: Stores addresses of deployed oracle contracts
- **Address Retrieval**: Provides access to all registered oracle addresses

## Resolution Process

1. The oracle waits until the `earliest_resolution_date`
2. Resolution can be triggered by providing evidence URLs (if configured) or using predefined resolution URLs
3. The system:
   - Fetches and validates web content
   - Processes data using LLMs
   - Analyzes multiple sources if available
   - Determines the final outcome
   - Updates the contract state

## Status States

- `ACTIVE`: Oracle is active but not yet resolved
- `RESOLVED`: Oracle has successfully determined an outcome
- `ERROR`: Resolution failed or produced invalid outcome

## Technical Notes

- The system uses GenLayer for contract execution
- Global imports are currently handled in specific ways due to simulator limitations
- Contract deployment is direct rather than using a factory pattern due to current platform constraints
