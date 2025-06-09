#include "b_tree.h"
#include <iostream>

BTreeNode::BTreeNode(int t, bool leaf) : t(t), leaf(leaf) {}

void BTree::destroyTree(BTreeNode* node) {
    if (node != nullptr) {
        for (auto child : node->children) {
            destroyTree(child);
        }
        delete node;
    }
}

BTree::~BTree() {
    destroyTree(root);
}

BTree::BTree(int t) : root(nullptr), t(t) {}

void BTree::insert(const ComplaintData& data) {
    if (!root) {
        root = new BTreeNode(t, true);
        root->keys.push_back(data);
    } else {
        if (root->keys.size() == 2 * t - 1) {
            BTreeNode* s = new BTreeNode(t, false);
            s->children.push_back(root);
            s->splitChild(0, root);
            int i = 0;
            if (s->keys[0].CMPLNT_NUM < data.CMPLNT_NUM) i++;
            s->children[i]->insertNonFull(data);
            root = s;
        } else {
            root->insertNonFull(data);
        }
    }
}

void BTreeNode::insertNonFull(const ComplaintData& data) {
    int i = keys.size() - 1;
    if (leaf) {
        keys.emplace_back(); // Espaço para a nova chave
        while (i >= 0 && keys[i].CMPLNT_NUM > data.CMPLNT_NUM) {
            keys[i + 1] = keys[i];
            i--;
        }
        keys[i + 1] = data;
    } else {
        while (i >= 0 && keys[i].CMPLNT_NUM > data.CMPLNT_NUM) {
            i--;
        }
        i++;
        if (children[i]->keys.size() == 2 * t - 1) {
            splitChild(i, children[i]);
            if (keys[i].CMPLNT_NUM < data.CMPLNT_NUM)
                i++;
        }
        children[i]->insertNonFull(data);
    }
}

void BTreeNode::splitChild(int i, BTreeNode* y) {
    BTreeNode* z = new BTreeNode(y->t, y->leaf);
    for (int j = 0; j < t - 1; j++) {
        z->keys.push_back(y->keys[j + t]);
    }

    if (!y->leaf) {
        for (int j = 0; j < t; j++) {
            z->children.push_back(y->children[j + t]);
        }
    }

    y->keys.resize(t - 1);
    y->children.resize(y->leaf ? 0 : t);

    children.insert(children.begin() + i + 1, z);
    keys.insert(keys.begin() + i, y->keys[t - 1]);
}

ComplaintData* BTree::search(const std::string& complaintNumber) {
    return root ? root->search(complaintNumber) : nullptr;
}

ComplaintData* BTreeNode::search(const std::string& complaintNumber) {
    int i = 0;
    while (i < keys.size() && complaintNumber > keys[i].CMPLNT_NUM)
        i++;

    if (i < keys.size() && keys[i].CMPLNT_NUM == complaintNumber)
        return &keys[i];

    if (leaf)
        return nullptr;

    return children[i]->search(complaintNumber);
}

void BTree::print() const {
    if (root) {
        root->print();
    } else {
        std::cout << "A árvore está vazia.\n";
    }
}

void BTreeNode::print(int indent) const {
    std::string indentStr(indent, ' ');
    std::cout << indentStr << "[";
    for (size_t i = 0; i < keys.size(); ++i) {
        std::cout << keys[i].CMPLNT_NUM;
        if (i != keys.size() - 1) std::cout << ", ";
    }
    std::cout << "]\n";

    // Recursivamente imprime os filhos com mais indentação
    for (auto child : children) {
        if (child) {
            child->print(indent + 4);
        }
    }
}

BTreeNode::~BTreeNode() {
    // Libera os filhos
    for (auto child : children) {
        delete child;
    }
}
