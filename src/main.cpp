#include <iostream>
#include <vector>
#include <string>
#include <sstream>
#include "network/ShardController.h"
#include "client/VoterClient.h"

// Interactive mode for Web UI
void run_interactive_mode() {
    ShardController controller(4);
    VoterClient client;
    
    std::string line;
    while (std::getline(std::cin, line)) {
        std::stringstream ss(line);
        std::string command;
        ss >> command;
        
        if (command == "VOTE") {
            int id;
            std::string content;
            ss >> id;
            std::getline(ss, content); // Read rest of line
            
            // Trim leading space
            if (!content.empty() && content[0] == ' ') {
                content = content.substr(1);
            }
            
            SecurePacket packet = client.generate_vote(content);
            // Redirect cout to capture error message if any
            std::stringstream buffer;
            std::streambuf* old = std::cout.rdbuf(buffer.rdbuf());
            
            controller.route_packet(id, packet);
            
            std::cout.rdbuf(old); // Reset cout
            std::string output = buffer.str();
            
            if (output.find("ERROR") != std::string::npos) {
                std::cout << "ERROR Voter " << id << " has already voted" << std::endl;
            } else {
                std::cout << "SUCCESS Vote processed for ID " << id << std::endl;
            }
        } else if (command == "STATUS") {
            std::cout << controller.get_status_json() << std::endl;
        } else if (command == "TALLY") {
            std::cout << controller.get_tally_json() << std::endl;
        } else if (command == "EXIT") {
            break;
        } else {
            std::cout << "ERROR Unknown command" << std::endl;
        }
    }
}

int main(int argc, char* argv[]) {
    // If argument provided, run interactive mode
    if (argc > 1 && std::string(argv[1]) == "--interactive") {
        run_interactive_mode();
        return 0;
    }

    // Default simulation
    std::cout << "Initializing Secure Vote-Transfer System..." << std::endl;
    ShardController controller(4);
    VoterClient client;

    std::vector<std::pair<int, std::string>> votes;
    for (int i = 0; i < 20; ++i) {
        votes.push_back({1000 + i, "Vote_Option_" + std::to_string(i % 3)});
    }

    std::cout << "Processing " << votes.size() << " votes..." << std::endl;

    for (const auto& v : votes) {
        std::cout << "Processing Voter ID: " << v.first << " ... ";
        SecurePacket packet = client.generate_vote(v.second);
        controller.route_packet(v.first, packet);
        std::cout << "Routed to shard." << std::endl;
    }

    controller.print_status();
    return 0;
}
