#include "network/ShardController.h"
#include <iostream>

ShardController::ShardController(int count) : shard_count(count) {
    for (int i = 0; i < count; ++i) {
        shards.push_back(std::make_unique<Blockchain>(i));
    }
}

#include "crypto/CryptoUtils.h"

void ShardController::route_packet(int voter_id, const SecurePacket& packet) {
    // Check for double voting
    if (voted_ids.find(voter_id) != voted_ids.end()) {
        std::cout << "ERROR: Voter " << voter_id << " has already voted!" << std::endl;
        return;
    }
    voted_ids.insert(voter_id);

    // Complex Hashing: Use a robust mixing algorithm to ensure distribution
    // This simulates a high-quality cryptographic hash distribution
    unsigned int x = voter_id;
    x = ((x >> 16) ^ x) * 0x45d9f3b;
    x = ((x >> 16) ^ x) * 0x45d9f3b;
    x = (x >> 16) ^ x;
    
    size_t shard_id = x % shard_count;
    
    shards[shard_id]->add_block(packet);
}

void ShardController::print_status() const {
    std::cout << "\n=== Network Status ===" << std::endl;
    for (int i = 0; i < shard_count; ++i) {
        std::cout << "Shard " << i << ": " << shards[i]->get_size() << " blocks" << std::endl;
        if (!shards[i]->is_chain_valid()) {
            std::cout << "  [WARNING] Shard " << i << " chain is invalid!" << std::endl;
        }
    }
    std::cout << "======================" << std::endl;
}

const Blockchain& ShardController::get_shard(int index) const {
    return *shards[index];
}
