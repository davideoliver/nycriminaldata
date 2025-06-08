/*
Prompt: I'd like to create a doubly linked list with the data from datasets\NYPD_Complaint_Data_Historic.csv
and basing on the header doubly_linkedlist.h and doubly_linkedlist.cpp
*/

#include <iostream>
#include <fstream>
#include <sstream>
#include <string>
#include "doubly_linkedlist.h"
#include <cctype>
#include "hash_table.h"

int i = 0;

bool isInteger(const std::string& s) {
    if (s.empty()) return false;
    size_t i = 0;
    if (s[0] == '-' || s[0] == '+') i = 1;
    for (; i < s.size(); ++i) {
        if (!std::isdigit(s[i])) return false;
    }
    return true;
}

bool isFloat(const std::string& s) {
    std::istringstream iss(s);
    float f;
    iss >> std::noskipws >> f;
    return iss.eof() && !iss.fail();
}

ComplaintData parseCSVLine(const std::string& line) {
    ComplaintData data;
    std::stringstream ss(line);
    std::string field;

    std::getline(ss, data.CMPLNT_NUM, ',');
    std::getline(ss, data.CMPLNT_FR_DT, ',');
    std::getline(ss, data.CMPLNT_FR_TM, ',');
    std::getline(ss, data.CMPLNT_TO_DT, ',');
    std::getline(ss, data.CMPLNT_TO_TM, ',');

    std::getline(ss, field, ','); data.ADDR_PCT_CD = isInteger(field) ? std::stoi(field) : 0;
    std::getline(ss, data.RPT_DT, ',');

    std::getline(ss, field, ','); data.KY_CD = isInteger(field) ? std::stoi(field) : 0;
    std::getline(ss, data.OFNS_DESC, ',');

    std::getline(ss, field, ','); data.PD_CD = isInteger(field) ? std::stoi(field) : 0;
    std::getline(ss, field, ','); data.PD_DESC = isInteger(field) ? std::stoi(field) : 0;

    std::getline(ss, data.CRM_ATPT_CPTD_CD, ',');
    std::getline(ss, data.LAW_CAT_CD, ',');
    std::getline(ss, data.BORO_NM, ',');
    std::getline(ss, data.LOC_OF_OCCUR_DESC, ',');
    std::getline(ss, data.PREM_TYP_DESC, ',');
    std::getline(ss, data.JURIS_DESC, ',');

    std::getline(ss, field, ','); data.JURISDICTION_CODE = isInteger(field) ? std::stoi(field) : 0;
    std::getline(ss, field, ','); data.PARKS_NM = isInteger(field) ? std::stoi(field) : 0;
    std::getline(ss, field, ','); data.HADEVELOPT = isInteger(field) ? std::stoi(field) : 0;
    std::getline(ss, field, ','); data.HOUSING_PSA = isInteger(field) ? std::stoi(field) : 0;
    std::getline(ss, field, ','); data.X_COORD_CD = isInteger(field) ? std::stoi(field) : 0;
    std::getline(ss, field, ','); data.Y_COORD_CD = isInteger(field) ? std::stoi(field) : 0;

    std::getline(ss, data.SUSP_AGE_GROUP, ',');
    std::getline(ss, data.SUSP_RACE, ',');
    std::getline(ss, field, ','); data.SUSP_SEX = field.empty() ? ' ' : field[0];

    std::getline(ss, field, ','); data.TRANSIT_DISTRICT = isInteger(field) ? std::stoi(field) : 0;
    std::getline(ss, field, ','); data.Latitude = isFloat(field) ? std::stof(field) : 0.0f;
    std::getline(ss, field, ','); data.Longitude = isFloat(field) ? std::stof(field) : 0.0f;

    std::getline(ss, data.Lat_Lon, ',');
    std::getline(ss, data.PATROL_BORO, ',');
    std::getline(ss, data.STATION_NAME, ',');
    std::getline(ss, data.VIC_AGE_GROUP, ',');
    std::getline(ss, data.VIC_RACE, ',');
    std::getline(ss, field, ','); data.VIC_SEX = field.empty() ? ' ' : field[0];

    return data;
}

int main() {
    DoublyLinkedList list;
    HashTable hashTable;
    std::ifstream file("../../../datasets/NYPD_Complaint_Data_Historic.csv");
    // Check if the file opened successfully
    if (!file.is_open()) {
        // Prompt: Substitute the if with a exception
        throw std::runtime_error("Failed to open file!");
    }
    std::string line;
    // Skip header line
    std::getline(file, line);

    // Read each line and parse it into ComplaintData
    while (std::getline(file, line)) {
        ComplaintData data = parseCSVLine(line);
        list.append(data);
        /*
        hashTable.insert(data);
        i++;
        if(i == 5){
            break;
        }
            */// eu usei esse código pra testar o hashing, se for testar outra estrutura so mudar o "hashTable" dali
    }
    std::cout << list.size() << " Reclamações foram adicionadas a lista." << std::endl;

    hashTable.print();
    file.close(); 
}
