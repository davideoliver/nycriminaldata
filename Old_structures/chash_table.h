#pragma once
#include <string>
#include <vector>
#include <list>
#include "complaint_data.h"

class cHashTable {
public:
    cHashTable(size_t size = 10007);
    ~cHashTable();

    void insert(const ComplaintData& data);
    ComplaintData* get(const std::string& complaintNumber);
    bool remove(const std::string& complaintNumber);
    void print() const;

private:
    std::vector<std::list<ComplaintData>> table_;
    size_t hash(const std::string& key) const;
    size_t size_;
};