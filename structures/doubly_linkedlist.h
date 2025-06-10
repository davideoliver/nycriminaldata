// Prompt: I'd like to create a doubly linked list with the data from datasets\NYPD_Complaint_Data_Historic.csv
#pragma once
#include <string>
#include "complaint_data.h"

struct Node {
    ComplaintData data;
    Node* prev;
    Node* next;
    Node(const ComplaintData& d) : data(d), prev(nullptr), next(nullptr) {}
};

class DoublyLinkedList {
public:
    DoublyLinkedList();
    ~DoublyLinkedList();

    void append(const ComplaintData& data);
    void clear();
    size_t size() const;

    // Add more methods as needed (e.g., print, search, etc.)

    Node* head() const { return head_; }
    Node* tail() const { return tail_; }

private:
    Node* head_;
    Node* tail_;
    size_t size_;
};
