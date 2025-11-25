# Secure Vote-Transfer System - Walkthrough

## Overview
This project implements a secure, scalable vote-transfer mechanism using C++. It features:
- **SecurePacket**: Fixed-size padded packets (1024 bytes) to prevent traffic analysis.
- **Sharding**: A `ShardController` that distributes votes across multiple blockchains based on Voter ID.
- **Blockchain**: A Proof-of-Work blockchain implementation for data integrity.

## Project Structure
```
/src
  /core       - Block, Blockchain, SecurePacket
  /network    - ShardController
  /client     - VoterClient
  main.cpp    - Simulation entry point
/include      - Header files
```

## Compilation & Execution
Since CMake is not available, you can compile the project manually using `g++`.

### Command
Run the following command in the project root:
```bash
g++ -std=c++14 -I include src/main.cpp src/core/Block.cpp src/core/Blockchain.cpp src/core/SecurePacket.cpp src/network/ShardController.cpp src/client/VoterClient.cpp -o SecureVoteSystem.exe
```

### Running the Simulation
```bash
./SecureVoteSystem.exe
```

## Expected Output
The simulation initializes 4 shards and processes 20 votes. You should see output indicating votes being routed and a final status report:

```
Initializing Secure Vote-Transfer System...
Processing 20 votes...
Processing Voter ID: 1000 ... Routed to shard.
...
=== Network Status ===
Shard 0: 6 blocks
Shard 1: 6 blocks
Shard 2: 6 blocks
Shard 3: 6 blocks
======================
```
*Note: Block counts include the Genesis block.*

## Verification Results
- **Traffic Analysis Resistance**: All packets are padded to 1024 bytes (verified in `SecurePacket.cpp`).
- **Scalability**: Votes are evenly distributed across shards (verified in output).
- **Integrity**: Blockchain hash links are maintained (verified by `is_chain_valid()` check in `ShardController`).
