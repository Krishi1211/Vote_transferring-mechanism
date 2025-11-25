#ifndef VOTER_CLIENT_H
#define VOTER_CLIENT_H

#include <string>
#include "core/SecurePacket.h"

class VoterClient {
public:
    SecurePacket generate_vote(const std::string& vote_content);
};

#endif // VOTER_CLIENT_H
