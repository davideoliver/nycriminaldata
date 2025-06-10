#pragma once
#include <vector>
#include <string>
#include "complaint_data.h"

class SkipListNode {
public:
    ComplaintData data;
    std::vector<SkipListNode*> forward;

    SkipListNode(const ComplaintData& data, int level);
};

class SkipList {
private:
    int maxLevel;
    float probability;
    SkipListNode* head;

    int randomLevel();

public:
    SkipList(int maxLevel = 16, float probability = 0.5f);
    ~SkipList();

    void insert(const ComplaintData& data);
    ComplaintData* search(const std::string& complaintNumber);
    bool remove(const std::string& complaintNumber);
    void print() const;
    void clear();
};
