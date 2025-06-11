#include "chash_table.h"
#include <iostream>
#include <functional>

cHashTable::cHashTable(size_t size) : size_(size) {
    table_.resize(size_);
}

cHashTable::~cHashTable() {}

size_t cHashTable::hash(const std::string& key) const {
    std::hash<std::string> hasher;
    return hasher(key) % size_;
}

void cHashTable::insert(const ComplaintData& data) {
    size_t idx = hash(data.CMPLNT_NUM);
    for (auto& entry : table_[idx]) {
        if (entry.CMPLNT_NUM == data.CMPLNT_NUM) {
            entry = data; // Atualiza se já existir
            return;
        }
    }
    table_[idx].push_back(data);
}

ComplaintData* cHashTable::get(const std::string& complaintNumber) {
    size_t idx = hash(complaintNumber);
    for (auto& entry : table_[idx]) {
        if (entry.CMPLNT_NUM == complaintNumber) {
            return &entry;
        }
    }
    return nullptr;
}

bool cHashTable::remove(const std::string& complaintNumber) {
    size_t idx = hash(complaintNumber);
    auto& chain = table_[idx];
    for (auto it = chain.begin(); it != chain.end(); ++it) {
        if (it->CMPLNT_NUM == complaintNumber) {
            chain.erase(it);
            return true;
        }
    }
    return false;
}

void cHashTable::print() const {
    for (size_t i = 0; i < size_; ++i) {
        if (!table_[i].empty()) {
            std::cout << "Index " << i << ":\n";
            for (const auto& entry : table_[i]) {
                std::cout << "  Complaint #" << entry.CMPLNT_NUM 
                          << ", Offense: " << entry.OFNS_DESC
                          << ", Borough: " << entry.BORO_NM << '\n';
            }
        }
    }
}
