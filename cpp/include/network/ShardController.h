#ifndef SHARD_CONTROLLER_H
#define SHARD_CONTROLLER_H

#include <vector>
#include <memory>
#include <set>
#include <map>
#include "core/Blockchain.h"

class ShardController {
private:
    std::vector<std::unique_ptr<Blockchain>> shards;
    std::set<int> voted_ids; // Track who has voted
    int shard_count;

public:
    ShardController(int count);
    void route_packet(int voter_id, const SecurePacket& packet);
    void print_status() const;
    const Blockchain& get_shard(int index) const;
    
    // Manual JSON serialization for status
    std::string get_status_json() const {
        std::stringstream ss;
        ss << "{ \"shards\": [";
        for (int i = 0; i < shard_count; ++i) {
            ss << "{ \"id\": " << i << ", \"blocks\": " << shards[i]->get_size() << ", \"valid\": " << (shards[i]->is_chain_valid() ? "true" : "false") << " }";
            if (i < shard_count - 1) ss << ", ";
        }
        ss << "] }";
        return ss.str();
    }

    // Calculate vote tally
    std::string get_tally_json() const {
        std::map<std::string, int> tally;
        
        for (const auto& shard : shards) {
            const auto& chain = shard->get_chain();
            for (const auto& block : chain) {
                std::string content = block.packet.get_content();
                if (content == "GENESIS_BLOCK" || content == "GENESIS") continue;
                tally[content]++;
            }
        }

        std::stringstream ss;
        ss << "{ \"tally\": [";
        auto it = tally.begin();
        while (it != tally.end()) {
            ss << "{ \"candidate\": \"" << it->first << "\", \"count\": " << it->second << " }";
            if (++it != tally.end()) ss << ", ";
        }
        ss << "] }";
        return ss.str();
    }
};

#endif // SHARD_CONTROLLER_H
