#ifndef BLOCKCHAIN_H
#define BLOCKCHAIN_H

#include <vector>
#include "core/Block.h"

class Blockchain {
private:
    std::vector<Block> chain;
    int difficulty;

public:
    Blockchain(int id); // Modified constructor to include ID
    void add_block(const SecurePacket& packet);
    bool is_chain_valid() const;
    size_t get_size() const;
    const std::vector<Block>& get_chain() const;
    
    // Persistence
    void save_to_disk() const;
    void load_from_disk();
    
private:
    int shard_id;
    std::string get_filename() const;
};

#endif // BLOCKCHAIN_H
