#ifndef SECURE_PACKET_H
#define SECURE_PACKET_H

#include <array>
#include <string>
#include <stdexcept>
#include <vector>
#include "crypto/CryptoUtils.h"

class SecurePacket {
public:
    static const size_t PACKET_SIZE = 1024;
    std::array<char, PACKET_SIZE> data;

    SecurePacket();
    SecurePacket(const std::string& vote_data);

    std::string get_content() const;
};

#endif // SECURE_PACKET_H
