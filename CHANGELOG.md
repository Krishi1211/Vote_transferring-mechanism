# Changelog

All notable changes to the Secure Vote-Transfer System will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [2.0.0] - 2025-11-29

### Added
- Professional folder structure with clear separation of concerns
- `cpp/` directory for all C++ core implementation
- `server/` directory with separate voting_node and observer_node subdirectories
- `web/` directory with separate voting_booth and dashboard subdirectories
- `docs/` directory for comprehensive documentation
- `scripts/` directory for utility scripts
- `research/` directory for academic materials
- `bin/` directory for compiled executables
- Linux/Mac startup script (`run_system.sh`)
- Python requirements.txt for dependency management
- CONTRIBUTING.md with coding standards and contribution guidelines
- LICENSE file (MIT License)
- Enhanced .gitignore with comprehensive exclusions
- This CHANGELOG.md file

### Changed
- Reorganized entire project structure for better maintainability
- Updated CMakeLists.txt to output executables to `bin/` directory
- Updated voting node server to use new path structure
- Updated observer node server to use new path structure
- Enhanced startup script with better user feedback
- Updated README.md to reflect new folder structure
- Bumped project version to 2.0.0

### Removed
- Old executables from root directory (SecureVoteSystem.exe, simulation.exe)
- Temporary utility script (extract_text.py)
- Old build directory contents
- Clutter from root directory

### Fixed
- Path references in all configuration files
- Build system to properly output to bin directory

## [1.0.0] - 2025-11-25

### Added
- Initial implementation of blockchain-based voting system
- Sharding architecture with 4 blockchain shards
- Secure packet encryption with 1024-byte packets
- Voting booth web interface
- Admin dashboard for monitoring
- Python Flask servers for voting and observation nodes
- C++ core implementation with cryptographic utilities
- Vote deduplication system
- Real-time blockchain visualization
- Persistent vote storage

### Features
- Blockchain ledger with cryptographic hashing
- Hash-based vote routing across shards
- Dual interface design (voter booth + admin dashboard)
- REST API for vote submission and status checking
- Real-time vote tallying
- Secure packet padding for anonymity

---

## Version History Summary

- **2.0.0** - Major reorganization into professional structure
- **1.0.0** - Initial release with core voting functionality
