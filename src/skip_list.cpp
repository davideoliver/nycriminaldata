#include "skip_list.h"
#include <iostream>
#include <cstdlib>
#include <ctime>
#include <random>

SkipListNode::SkipListNode(const ComplaintData& data, int level)
    : data(data), forward(level + 1, nullptr) {}

SkipList::SkipList(int maxLevel, float probability)
    : maxLevel(maxLevel), probability(probability) {
    head = new SkipListNode(ComplaintData(), maxLevel);
    std::srand(std::time(nullptr));
}

SkipList::~SkipList() {
    clear();
    delete head;
}

std::default_random_engine engine(std::random_device{}());
std::uniform_real_distribution<float> distribution(0.0f, 1.0f);

int SkipList::randomLevel() {
    int level = 0;
    while (distribution(engine) < probability && level < maxLevel)
        level++;
    return level;
}

void SkipList::insert(const ComplaintData& data) {
    std::vector<SkipListNode*> update(maxLevel + 1);
    SkipListNode* current = head;

    for (int i = maxLevel; i >= 0; i--) {
        while (current->forward[i] && current->forward[i]->data.CMPLNT_NUM < data.CMPLNT_NUM) {
            current = current->forward[i];
        }
        update[i] = current;
    }

    current = current->forward[0];
    if (current && current->data.CMPLNT_NUM == data.CMPLNT_NUM) {
        current->data = data; // Update if already exists
        return;
    }

    int lvl = randomLevel();
    SkipListNode* newNode = new SkipListNode(data, lvl);
    for (int i = 0; i <= lvl; i++) {
        newNode->forward[i] = update[i]->forward[i];
        update[i]->forward[i] = newNode;
    }
}

ComplaintData* SkipList::search(const std::string& complaintNumber) {
    SkipListNode* current = head;
    for (int i = maxLevel; i >= 0; i--) {
        while (current->forward[i] && current->forward[i]->data.CMPLNT_NUM < complaintNumber) {
            current = current->forward[i];
        }
    }
    current = current->forward[0];
    if (current && current->data.CMPLNT_NUM == complaintNumber) {
        return &current->data;
    }
    return nullptr;
}

bool SkipList::remove(const std::string& complaintNumber) {
    std::vector<SkipListNode*> update(maxLevel + 1);
    SkipListNode* current = head;

    for (int i = maxLevel; i >= 0; i--) {
        while (current->forward[i] && current->forward[i]->data.CMPLNT_NUM < complaintNumber) {
            current = current->forward[i];
        }
        update[i] = current;
    }

    current = current->forward[0];
    if (!current || current->data.CMPLNT_NUM != complaintNumber) {
        return false;
    }

    for (int i = 0; i <= maxLevel; i++) {
        if (update[i]->forward[i] != current) break;
        update[i]->forward[i] = current->forward[i];
    }

    delete current;
    return true;
}

void SkipList::print() const {
    for (int i = maxLevel; i >= 0; --i) {
        SkipListNode* current = head->forward[i];
        std::cout << "Level " << i << ": ";
        while (current) {
            std::cout << current->data.CMPLNT_NUM << " -> ";
            current = current->forward[i];
        }
        std::cout << "nullptr\n";
    }
}

void SkipList::clear() {
    SkipListNode* current = head->forward[0];
    while (current) {
        SkipListNode* next = current->forward[0];
        delete current;
        current = next;
    }
    for (auto& ptr : head->forward) ptr = nullptr;
}
