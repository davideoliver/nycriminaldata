/*
Prompt: I'd like to create a doubly linked list with the data from datasets\NYPD_Complaint_Data_Historic.csv
 and basing on the header doubly_linkedlist.h
*/
#include "doubly_linkedlist.h"

DoublyLinkedList::DoublyLinkedList() : head_(nullptr), tail_(nullptr), size_(0) {}

DoublyLinkedList::~DoublyLinkedList() {
    clear();
}

void DoublyLinkedList::append(const ComplaintData& data) {
    Node* newNode = new Node(data);
    if (!head_) {
        head_ = tail_ = newNode;
    } else {
        tail_->next = newNode;
        newNode->prev = tail_;
        tail_ = newNode;
    }
    ++size_;
}

void DoublyLinkedList::clear() {
    Node* current = head_;
    while (current) {
        Node* next = current->next;
        delete current;
        current = next;
    }
    head_ = tail_ = nullptr;
    size_ = 0;
}

size_t DoublyLinkedList::size() const {
    return size_;
}