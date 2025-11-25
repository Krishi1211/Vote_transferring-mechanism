#include "client/VoterClient.h"

SecurePacket VoterClient::generate_vote(const std::string& vote_content) {
    // In a real system, this would sign the vote with a private key
    return SecurePacket(vote_content);
}
