#include "core/SecurePacket.h"
#include <algorithm>
#include <random>

SecurePacket::SecurePacket() {
    data.fill(0);
}

SecurePacket::SecurePacket(const std::string& vote_data) {
    if (vote_data.size() > PACKET_SIZE) {
        throw std::runtime_error("Vote data exceeds packet size limit.");
    }

    // Copy vote data
    std::copy(vote_data.begin(), vote_data.end(), data.begin());
    
    // Add a delimiter to mark end of data (using null terminator or special char)
    if (vote_data.size() < PACKET_SIZE) {
        data[vote_data.size()] = '\0'; // Null terminator as delimiter
    }

    // Pad the rest with random noise
    for (size_t i = vote_data.size() + 1; i < PACKET_SIZE; ++i) {
        data[i] = CryptoUtils::generate_random_string(1)[0];
    }
}

std::string SecurePacket::get_content() const {
    // Return data up to the first null terminator
    return std::string(data.data());
}
