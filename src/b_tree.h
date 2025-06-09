#pragma once
#include <vector>
#include "complaint_data.h"

class BTreeNode {
public:
    bool leaf;
    std::vector<ComplaintData> keys;
    std::vector<BTreeNode*> children;
    int t; // grau mínimo

    BTreeNode(int t, bool leaf);

    void insertNonFull(const ComplaintData& data);
    void splitChild(int i, BTreeNode* y);
    ComplaintData* search(const std::string& complaintNumber);

    ~BTreeNode();

    void print(int indent = 0) const;
};

class BTree {
private:
    BTreeNode* root;
    int t;
public:
    BTree(int t);
    ~BTree();

    void insert(const ComplaintData& data);
    ComplaintData* search(const std::string& complaintNumber);

    void destroyTree(BTreeNode* node);

    void print() const;
};
