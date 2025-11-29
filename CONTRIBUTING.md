# Contributing to Secure Vote-Transfer System

Thank you for your interest in contributing to the Secure Vote-Transfer System! This document provides guidelines for contributing to the project.

## Code of Conduct

- Be respectful and inclusive
- Focus on constructive feedback
- Help maintain a welcoming environment for all contributors

## How to Contribute

### Reporting Bugs

If you find a bug, please create an issue with:
- Clear description of the problem
- Steps to reproduce
- Expected vs actual behavior
- System information (OS, Python version, compiler version)

### Suggesting Enhancements

Enhancement suggestions are welcome! Please include:
- Clear description of the feature
- Use cases and benefits
- Potential implementation approach

### Pull Requests

1. **Fork the repository**
2. **Create a feature branch**
   ```bash
   git checkout -b feature/your-feature-name
   ```

3. **Make your changes**
   - Follow the coding standards below
   - Add tests if applicable
   - Update documentation

4. **Commit your changes**
   ```bash
   git commit -m "Add: Brief description of changes"
   ```
   Use conventional commit prefixes:
   - `Add:` for new features
   - `Fix:` for bug fixes
   - `Update:` for updates to existing features
   - `Refactor:` for code refactoring
   - `Docs:` for documentation changes

5. **Push to your fork**
   ```bash
   git push origin feature/your-feature-name
   ```

6. **Create a Pull Request**
   - Provide clear description of changes
   - Reference any related issues
   - Ensure all tests pass

## Coding Standards

### C++ Code

- **Standard**: C++20
- **Style**: 
  - Use 4 spaces for indentation
  - Class names in PascalCase
  - Function names in snake_case
  - Constants in UPPER_SNAKE_CASE
- **Comments**: Use clear, descriptive comments for complex logic
- **Headers**: Include guards in all header files

Example:
```cpp
class BlockchainLedger {
private:
    std::vector<Block> chain;
    
public:
    void add_block(const SecurePacket& packet);
    size_t get_chain_size() const;
};
```

### Python Code

- **Standard**: PEP 8
- **Style**:
  - Use 4 spaces for indentation
  - Class names in PascalCase
  - Function names in snake_case
  - Constants in UPPER_SNAKE_CASE
- **Type Hints**: Use type hints where appropriate
- **Docstrings**: Include docstrings for all public functions

Example:
```python
def send_command(self, command: str) -> str:
    """
    Send a command to the vote system process.
    
    Args:
        command: The command string to send
        
    Returns:
        The response from the process
    """
    # Implementation
```

### Web Code (HTML/CSS/JavaScript)

- **HTML**: Use semantic HTML5 elements
- **CSS**: 
  - Use CSS custom properties for theming
  - Mobile-first responsive design
- **JavaScript**:
  - Use modern ES6+ syntax
  - Async/await for asynchronous operations
  - Clear function and variable names

## Project Structure

When adding new files, follow the established structure:

```
cpp/          - C++ core implementation
server/       - Python backend servers
web/          - Frontend interfaces
docs/         - Documentation
scripts/      - Utility scripts
research/     - Academic materials
```

## Testing

- Test your changes locally before submitting
- Ensure the build system works: `cd cpp && mkdir build && cd build && cmake .. && cmake --build .`
- Test the full system: `cd scripts && ./run_system.bat` (or `.sh` on Linux/Mac)
- Verify both voting and dashboard interfaces work correctly

## Documentation

- Update README.md if you change functionality
- Add comments to complex code
- Update API documentation in `docs/API.md` if you modify endpoints
- Update CHANGELOG.md with your changes

## Questions?

If you have questions about contributing, feel free to:
- Open an issue for discussion
- Contact the maintainers

Thank you for contributing to making voting systems more secure!
