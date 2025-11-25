#ifndef BLOCK_H
#define BLOCK_H

#include <string>
#include <ctime>
#include "core/SecurePacket.h"

struct Block {
    std::string previous_hash;
    time_t timestamp;
    std::string data_hash;
    SecurePacket packet;
    std::string block_hash;
    uint64_t nonce;

    Block(std::string prev_hash, SecurePacket pkt);
    std::string calculate_hash() const;
    void mine_block(int difficulty);
};

#endif // BLOCK_H
