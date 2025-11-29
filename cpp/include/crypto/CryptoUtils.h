#ifndef CRYPTO_UTILS_H
#define CRYPTO_UTILS_H

#include <string>
#include <sstream>
#include <iomanip>
#include <functional>

namespace CryptoUtils {

    // Simple SHA-256 simulation using std::hash for demonstration purposes
    // In a real production system, use OpenSSL or a dedicated SHA256 library
    inline std::string sha256(const std::string& str) {
        std::hash<std::string> hasher;
        size_t hash_val = hasher(str);
        std::stringstream ss;
        ss << std::hex << std::setw(16) << std::setfill('0') << hash_val;
        return ss.str();
    }

    // Generate a random alphanumeric string of given length
    inline std::string generate_random_string(size_t length) {
        static const char charset[] =
            "0123456789"
            "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
            "abcdefghijklmnopqrstuvwxyz";
        std::string result;
        result.resize(length);
        for (size_t i = 0; i < length; ++i) {
            result[i] = charset[rand() % (sizeof(charset) - 1)];
        }
        return result;
    }
}

#endif // CRYPTO_UTILS_H
