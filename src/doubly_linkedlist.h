// Prompt: I'd like to create a doubly linked list with the data from datasets\NYPD_Complaint_Data_Historic.csv
#pragma once
#include <string>
struct ComplaintData {
    std::string CMPLNT_NUM, CMPLNT_FR_DT, CMPLNT_FR_TM, CMPLNT_TO_DT, CMPLNT_TO_TM;
    int ADDR_PCT_CD;
    std::string RPT_DT; 
    int KY_CD;
    std::string OFNS_DESC;
    int PD_CD,PD_DESC;
    std::string CRM_ATPT_CPTD_CD, LAW_CAT_CD, BORO_NM, LOC_OF_OCCUR_DESC, PREM_TYP_DESC, JURIS_DESC;
    int JURISDICTION_CODE, PARKS_NM;
    int HADEVELOPT, HOUSING_PSA, X_COORD_CD, Y_COORD_CD;
    std::string SUSP_AGE_GROUP, SUSP_RACE;
    char SUSP_SEX;
    int TRANSIT_DISTRICT;
    float Latitude, Longitude;
    std::string Lat_Lon, PATROL_BORO, STATION_NAME, VIC_AGE_GROUP, VIC_RACE;
    char VIC_SEX;
};

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
