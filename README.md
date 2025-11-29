# Secure Vote-Transfer System

A blockchain-based voting system implementing secure vote transfer mechanisms with sharding, cryptographic packet protection, and real-time monitoring capabilities.

## 🎯 Overview

This project implements an end-to-end secure voting system that leverages blockchain technology and sharding to ensure vote integrity, anonymity, and scalability. The system features a dedicated voting interface for voters and a separate monitoring dashboard for administrators.

## ✨ Key Features

- **Blockchain-Based Ledger**: Immutable vote storage with cryptographic hashing
- **Sharding Architecture**: Distributed vote processing across multiple blockchain shards for scalability
- **Secure Packet Encryption**: 1024-byte secure packets with random padding for anonymity
- **Dual Interface Design**:
  - Clean voting booth interface for voters
  - Real-time monitoring dashboard for administrators
- **Vote Deduplication**: Prevents double-voting by tracking voter IDs
- **Persistent Storage**: Votes are saved to disk for reliability
- **Real-time Updates**: Live blockchain visualization and vote tallying

## 🏗️ Architecture

### Components

1. **Voting Node (Backend)** - `app.py`
   - Handles vote submission and validation
   - Routes votes to appropriate blockchain shards
   - Provides REST API endpoints

2. **Observer Node (Dashboard)** - `display_server.py`
   - Real-time monitoring interface
   - Displays blockchain shard status
   - Shows vote tallies and system statistics

3. **C++ Core Engine** - `src/` and `include/`
   - High-performance blockchain implementation
   - Cryptographic utilities
   - Shard controller and routing logic

### System Architecture

```
┌─────────────┐         ┌──────────────────┐         ┌─────────────────┐
│   Voter     │────────▶│  Voting Node     │────────▶│  Blockchain     │
│  Interface  │         │  (Flask Server)  │         │  Shards (0-3)   │
└─────────────┘         └──────────────────┘         └─────────────────┘
                                │                              │
                                │                              │
                                ▼                              ▼
                        ┌──────────────────┐         ┌─────────────────┐
                        │  Observer Node   │◀────────│  Vote Storage   │
                        │  (Dashboard)     │         │  (Persistent)   │
                        └──────────────────┘         └─────────────────┘
```

## 🚀 Getting Started

### Prerequisites

- **Python 3.7+** with Flask
- **CMake 3.10+**
- **C++ Compiler** with C++20 support (MSVC, GCC, or Clang)
- **Windows OS** (for batch script execution)

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/Krishi1211/Vote_transferring-mechanism.git
   cd Vote_transferring-mechanism
   ```

2. **Install Python dependencies**
   ```bash
   pip install flask
   ```

3. **Build the C++ components** (optional, pre-built executables included)
   ```bash
   mkdir build
   cd build
   cmake ..
   cmake --build .
   ```

### Running the System

#### Quick Start (Recommended)

Simply run the automated startup script:

```bash
run_system.bat
```

This will:
- Start the voting node on `http://localhost:5000`
- Start the observer dashboard on `http://localhost:5001`
- Automatically open both interfaces in your browser

#### Manual Start

If you prefer to start components individually:

1. **Start the Voting Node**
   ```bash
   python app.py
   ```

2. **Start the Observer Dashboard** (in a separate terminal)
   ```bash
   python display_server.py
   ```

3. **Access the interfaces**
   - Voter Booth: http://localhost:5000
   - Admin Dashboard: http://localhost:5001

## 📖 Usage

### Casting a Vote

1. Navigate to the **Voter Booth** (http://localhost:5000)
2. Enter your unique **Voter ID**
3. Select your preferred **Candidate** from the dropdown
4. Click **SUBMIT BALLOT**
5. Wait for confirmation message

### Monitoring the System

1. Navigate to the **Admin Dashboard** (http://localhost:5001)
2. View real-time blockchain shard status
3. Monitor vote distribution across shards
4. Track total votes and candidate tallies

## 🔒 Security Features

### Cryptographic Protection

- **SHA-256 Hashing**: Each block contains cryptographic hashes linking to previous blocks
- **Secure Packets**: 1024-byte packets with random padding to prevent traffic analysis
- **Immutable Ledger**: Once recorded, votes cannot be altered or deleted

### Privacy Measures

- **Anonymous Routing**: Votes are distributed across shards using hash-based routing
- **Packet Padding**: Random data fills unused packet space to obscure vote content
- **No Direct Linkage**: Voter IDs are hashed before shard assignment

### Integrity Verification

- **Chain Validation**: Each block references the previous block's hash
- **Timestamp Recording**: All votes include cryptographic timestamps
- **Duplicate Prevention**: System rejects votes from already-used voter IDs

## 📁 Project Structure

```
Vote_transferring-mechanism/
├── src/
│   ├── client/          # Voter client implementation
│   ├── core/            # Blockchain and shard logic
│   ├── crypto/          # Cryptographic utilities
│   └── network/         # Network communication
├── include/
│   ├── client/          # Client headers
│   ├── core/            # Core system headers
│   ├── crypto/          # Crypto headers
│   └── network/         # Network headers
├── app.py               # Voting node Flask server
├── display_server.py    # Observer node Flask server
├── index.html           # Voter booth interface
├── dashboard.html       # Admin monitoring interface
├── main.cpp             # C++ simulation entry point
├── CMakeLists.txt       # CMake build configuration
├── run_system.bat       # Automated startup script
└── README.md            # This file
```

## 🛠️ Technical Details

### Blockchain Implementation

- **Block Structure**:
  ```cpp
  struct Block {
      size_t previous_hash;    // Link to previous block
      int64_t timestamp;       // Block creation time
      size_t data_hash;        // Hash of vote data
      SecurePacket packet;     // Encrypted vote packet
      size_t block_hash;       // This block's hash
  };
  ```

- **Sharding Strategy**: Hash-based routing distributes votes evenly across 4 shards
- **Genesis Block**: Each shard initializes with a genesis block

### API Endpoints

#### Voting Node (Port 5000)

- `POST /vote` - Submit a vote
  ```json
  {
    "id": 1001,
    "content": "Candidate A"
  }
  ```

- `GET /status` - Get system status
  ```json
  {
    "shards": [2, 3, 1, 2],
    "total_votes": 8,
    "tallies": {
      "Candidate A": 3,
      "Candidate B": 2,
      ...
    }
  }
  ```

#### Observer Node (Port 5001)

- `GET /` - Dashboard interface
- `GET /data` - Real-time blockchain data (auto-refreshes)

## 🧪 Testing

### Running the C++ Simulation

```bash
# Build the project first
cd build
cmake --build .

# Run the simulation
./SecureVoteSystem
```

This will simulate 10 votes and display the shard distribution.

### Manual Testing

1. Submit votes with different voter IDs
2. Verify votes appear in the dashboard
3. Attempt to vote twice with the same ID (should be rejected)
4. Check vote tallies match submitted votes

## 📊 Performance

- **Throughput**: Handles hundreds of votes per second
- **Scalability**: Sharding allows horizontal scaling
- **Latency**: Sub-second vote confirmation
- **Storage**: Persistent disk storage for reliability

## 🤝 Contributing

This project was developed as part of ECS 235A coursework. For academic integrity, please do not copy directly for coursework submissions.

## 📄 License

This project is provided for educational purposes. Please check with the repository owner for usage rights.

## 👥 Authors

- **Krishi1211** - Initial development and implementation

## 📚 References

- [Blockchain Technology Overview](https://en.wikipedia.org/wiki/Blockchain)
- [Sharding in Distributed Systems](https://en.wikipedia.org/wiki/Shard_(database_architecture))
- ECS 235A Course Materials - UC Davis

## 🐛 Known Issues

- System currently runs on localhost only
- Limited to 4 shards (configurable in code)
- Requires manual voter ID management

## 🔮 Future Enhancements

- [ ] Multi-node distributed deployment
- [ ] Dynamic shard scaling
- [ ] Advanced cryptographic protocols (zero-knowledge proofs)
- [ ] Mobile application interface
- [ ] Automated voter authentication
- [ ] Result export and reporting tools

## 📞 Support

For questions or issues, please open an issue on the GitHub repository.

---

**Built with ❤️ for secure, transparent, and scalable voting systems**
