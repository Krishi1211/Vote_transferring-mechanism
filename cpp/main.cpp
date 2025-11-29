#include <iostream>
#include <vector>
#include <string>
#include <random>
#include <chrono>
#include <iomanip>
#include <sstream>
#include <array>
#include <cstdint>
#include <functional>

using namespace std;

struct SecurePacket {
    array<char, 1024> data;

    SecurePacket(const string& vote_data) {
        if (vote_data.size() > 1024) {
            throw runtime_error("Vote data too large");
        }
        copy(vote_data.begin(), vote_data.end(), data.begin());
        
        random_device rd;
        mt19937 gen(rd());
        uniform_int_distribution<> dis(0, 61);
        const string charset = "0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz";

        for (size_t i = vote_data.size(); i < 1024; ++i) {
            data[i] = charset[dis(gen)];
        }
    }

    SecurePacket() : data{0} {}
};

struct Block {
    size_t previous_hash;
    int64_t timestamp;
    size_t data_hash;
    SecurePacket packet;
    size_t block_hash;

    size_t calculate_hash() const {
        stringstream ss;
        ss << previous_hash << timestamp << data_hash;
        for (char c : packet.data) {
            ss << c;
        }
        return hash<string>{}(ss.str());
    }
};

class BlockchainLedger {
private:
    vector<Block> chain;

public:
    BlockchainLedger() {
        Block genesis;
        genesis.previous_hash = 0;
        genesis.timestamp = chrono::system_clock::to_time_t(chrono::system_clock::now());
        genesis.data_hash = 0;
        genesis.packet = SecurePacket("GENESIS");
        genesis.block_hash = genesis.calculate_hash();
        chain.push_back(genesis);
    }

    void add_block(const SecurePacket& packet) {
        Block new_block;
        new_block.previous_hash = chain.back().block_hash;
        new_block.timestamp = chrono::system_clock::to_time_t(chrono::system_clock::now());
        
        stringstream ss;
        for (char c : packet.data) {
            ss << c;
        }
        new_block.data_hash = hash<string>{}(ss.str());
        new_block.packet = packet;
        new_block.block_hash = new_block.calculate_hash();
        
        chain.push_back(new_block);
    }

    size_t get_chain_size() const {
        return chain.size();
    }
};

class ShardController {
private:
    vector<BlockchainLedger> shards;
    int shard_count;

public:
    ShardController(int count) : shard_count(count) {
        for (int i = 0; i < count; ++i) {
            shards.emplace_back();
        }
    }

    void route_packet(int voter_id, const SecurePacket& packet) {
        size_t shard_id = hash<int>{}(voter_id) % shard_count;
        shards[shard_id].add_block(packet);
    }

    void print_status() const {
        for (int i = 0; i < shard_count; ++i) {
            cout << "Shard " << i << ": " << shards[i].get_chain_size() << " blocks" << endl;
        }
    }
};

class VoterClient {
public:
    SecurePacket generate_vote(const string& vote_content) {
        return SecurePacket(vote_content);
    }
};

int main() {
    ShardController controller(4);
    VoterClient client;

    vector<pair<int, string>> votes = {
        {101, "Vote A"},
        {102, "Vote B Long String"},
        {205, "Vote C"},
        {309, "Vote D"},
        {412, "Vote E"},
        {555, "Vote F"},
        {678, "Vote G"},
        {888, "Vote H"},
        {999, "Vote I"},
        {1000, "Vote J"}
    };

    cout << "Starting Simulation..." << endl;

    for (const auto& v : votes) {
        SecurePacket packet = client.generate_vote(v.second);
        controller.route_packet(v.first, packet);
        cout << "Processed vote from Voter ID: " << v.first << endl;
    }

    cout << "\nFinal Shard Status:" << endl;
    controller.print_status();

    return 0;
}
