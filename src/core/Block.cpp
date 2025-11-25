#include "core/Block.h"
#include "crypto/CryptoUtils.h"
#include <iostream>

Block::Block(std::string prev_hash, SecurePacket pkt)
    : previous_hash(prev_hash), packet(pkt), nonce(0) {
    timestamp = std::time(nullptr);
    data_hash = CryptoUtils::sha256(std::string(packet.data.begin(), packet.data.end()));
    block_hash = calculate_hash();
}

std::string Block::calculate_hash() const {
    std::stringstream ss;
    ss << previous_hash << timestamp << data_hash << nonce;
    return CryptoUtils::sha256(ss.str());
}

void Block::mine_block(int difficulty) {
    std::string target(difficulty, '0');
    while (block_hash.substr(0, difficulty) != target) {
        nonce++;
        block_hash = calculate_hash();
    }
    // std::cout << "Block mined: " << block_hash << std::endl;
}
