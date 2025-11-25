#include "core/Blockchain.h"

#include "core/Blockchain.h"
#include <fstream>
#include <iostream>

Blockchain::Blockchain(int id) : difficulty(2), shard_id(id) {
    // Try to load from disk first
    load_from_disk();
    
    // If chain is empty (load failed or no file), create Genesis
    if (chain.empty()) {
        SecurePacket genesis_packet("GENESIS_BLOCK");
        Block genesis("0", genesis_packet);
        chain.push_back(genesis);
        save_to_disk();
    }
}

void Blockchain::add_block(const SecurePacket& packet) {
    Block new_block(chain.back().block_hash, packet);
    new_block.mine_block(difficulty);
    chain.push_back(new_block);
    save_to_disk(); // Auto-save on new block
}

std::string Blockchain::get_filename() const {
    return "shard_" + std::to_string(shard_id) + ".dat";
}

void Blockchain::save_to_disk() const {
    std::ofstream file(get_filename(), std::ios::binary);
    if (!file.is_open()) return;
    
    size_t size = chain.size();
    file.write(reinterpret_cast<const char*>(&size), sizeof(size));
    
    for (const auto& block : chain) {
        // Serialize block (simplified for this demo)
        // We only save the packet content for simplicity in this text-based format
        // In a real system, we'd serialize the whole struct
        std::string content = block.packet.get_content();
        size_t len = content.size();
        file.write(reinterpret_cast<const char*>(&len), sizeof(len));
        file.write(content.c_str(), len);
        
        // Save hashes
        size_t hash_len = block.block_hash.size();
        file.write(reinterpret_cast<const char*>(&hash_len), sizeof(hash_len));
        file.write(block.block_hash.c_str(), hash_len);
        
        hash_len = block.previous_hash.size();
        file.write(reinterpret_cast<const char*>(&hash_len), sizeof(hash_len));
        file.write(block.previous_hash.c_str(), hash_len);
    }
}

void Blockchain::load_from_disk() {
    std::ifstream file(get_filename(), std::ios::binary);
    if (!file.is_open()) return;
    
    size_t size;
    file.read(reinterpret_cast<char*>(&size), sizeof(size));
    
    chain.clear();
    for (size_t i = 0; i < size; ++i) {
        // Read content
        size_t len;
        file.read(reinterpret_cast<char*>(&len), sizeof(len));
        std::string content(len, ' ');
        file.read(&content[0], len);
        
        // Read hashes
        size_t hash_len;
        file.read(reinterpret_cast<char*>(&hash_len), sizeof(hash_len));
        std::string block_hash(hash_len, ' ');
        file.read(&block_hash[0], hash_len);
        
        file.read(reinterpret_cast<char*>(&hash_len), sizeof(hash_len));
        std::string prev_hash(hash_len, ' ');
        file.read(&prev_hash[0], hash_len);
        
        // Reconstruct block
        SecurePacket packet(content);
        Block b(prev_hash, packet);
        b.block_hash = block_hash; // Restore original hash
        // Timestamp and nonce are lost in this simplified serialization but that's ok for visual demo
        
        chain.push_back(b);
    }
}

bool Blockchain::is_chain_valid() const {
    for (size_t i = 1; i < chain.size(); ++i) {
        const Block& current = chain[i];
        const Block& previous = chain[i - 1];

        if (current.calculate_hash() != current.block_hash) {
            return false;
        }
        if (current.previous_hash != previous.block_hash) {
            return false;
        }
    }
    return true;
}

size_t Blockchain::get_size() const {
    return chain.size();
}

const std::vector<Block>& Blockchain::get_chain() const {
    return chain;
}
