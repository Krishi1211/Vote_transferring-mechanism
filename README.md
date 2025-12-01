# Secure Vote-Transfer System

[![Version](https://img.shields.io/badge/version-3.0.0-blue.svg)](CHANGELOG.md)
   - Shows vote tallies and system statistics

3. **C++ Core Engine** - `cpp/src/` and `cpp/include/`
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

- **Python 3.7+**
- **C++ Compiler** (GCC, MSVC, or Clang) with C++17+ support
- **Git** (for cloning)
- **pip** (Python package manager)

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/Krishi1211/Vote_transferring-mechanism.git
   cd Vote_transferring-mechanism
   ```

2. **Install Python dependencies**
   ```bash
   cd server/voting_node
   pip install -r requirements.txt
   ```

3. **Generate security keys**
   ```bash
   cd ../../scripts
   python generate_keys.py
   ```
   Copy the output to a new `.env` file in the project root.

4. **Build the C++ components** (if not already built)
   ```bash
   cd ../cpp
   g++ -std=c++17 -Iinclude -o ../bin/SecureVoteSystem.exe \
     src/main.cpp src/client/*.cpp src/core/*.cpp src/network/*.cpp
   ```

### Running the Secure System

#### Option 1: Manual Start (Recommended for Development)

1. **Start the Voting Node**
   ```bash
   cd server/voting_node
   python app.py
   ```
   Server will start on `http://localhost:5000`

2. **Access the voting interface**
   - Open browser: **http://localhost:5000**
   - Register a new account
   - Login and cast your vote!

#### Option 2: Automated Script

**Windows**:
```bash
cd scripts
run_system.bat
```

**Linux/Mac**:
```bash
cd scripts
chmod +x run_system.sh
./run_system.sh
```

This will:
- Start the voting node on `http://localhost:5000`
- Start the observer dashboard on `http://localhost:5001`
- Automatically open both interfaces in your browser

#### Manual Start

If you prefer to start components individually:

1. **Start the Voting Node**
   ```bash
   cd server/voting_node
   python app.py
   ```

2. **Start the Observer Dashboard** (in a separate terminal)
   ```bash
   cd server/observer_node
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
├── cpp/                          # C++ core implementation
│   ├── src/                      # Source files
│   │   ├── client/               # Voter client
│   │   ├── core/                 # Blockchain & sharding
│   │   ├── crypto/               # Cryptographic utilities
│   │   ├── network/              # Network communication
│   │   └── main.cpp              # Entry point
│   ├── include/                  # Header files
│   │   ├── client/
│   │   ├── core/
│   │   ├── crypto/
│   │   └── network/
│   └── CMakeLists.txt            # Build configuration
├── server/                       # Python backend
│   ├── voting_node/
│   │   ├── app.py                # Voting server
│   │   └── requirements.txt      # Dependencies
│   └── observer_node/
│       └── display_server.py     # Dashboard server
├── web/                          # Frontend interfaces
│   ├── voting_booth/
│   │   └── index.html            # Voter interface
│   └── dashboard/
│       └── dashboard.html        # Admin dashboard
├── docs/                         # Documentation
│   ├── ARCHITECTURE.md           # System architecture
│   ├── API.md                    # API documentation
│   └── SECURITY.md               # Security details
├── scripts/                      # Utility scripts
│   ├── run_system.bat            # Windows startup
│   └── run_system.sh             # Linux/Mac startup
├── research/                     # Academic materials
│   ├── ECS 235A Project Report-1.pdf
│   └── ECS235A_Progress Report Presentation(1).mp4
├── bin/                          # Compiled executables
├── .gitignore                    # Git ignore rules
├── README.md                     # This file
├── CONTRIBUTING.md               # Contribution guidelines
├── LICENSE                       # MIT License
└── CHANGELOG.md                  # Version history
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
cd cpp
mkdir build
cd build
cmake ..
cmake --build .

# Run the simulation
cd ../../bin
./SecureVoteSystem  # Linux/Mac
SecureVoteSystem.exe  # Windows
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

## 📚 Documentation

- **[Architecture Guide](docs/ARCHITECTURE.md)** - Detailed system architecture and component design
- **[API Reference](docs/API.md)** - Complete API documentation with examples
- **[Security Documentation](docs/SECURITY.md)** - Security features and threat model
- **[Contributing Guide](CONTRIBUTING.md)** - How to contribute to the project
- **[Changelog](CHANGELOG.md)** - Version history and release notes

## 🤝 About This Project

**Academic Project**: This system was developed as part of ECS 235A (Computer and Information Security) coursework at UC Davis.

**Purpose**: To demonstrate understanding of:
- Blockchain technology and cryptographic security
- Secure authentication and authorization
- Production-level security practices
- System architecture and design

**Academic Integrity Notice**: 
- ⚠️ **Do not copy this code for your own coursework submissions**
- ✅ Feel free to use as a learning reference
- ✅ Study the implementation for educational purposes
- ✅ Use concepts and ideas in your own original work

**For Contributions**: While this is primarily an academic project, suggestions and feedback are welcome for learning purposes.

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

**Note**: While the code is open source under MIT License, please respect academic integrity policies if you're a student.

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
