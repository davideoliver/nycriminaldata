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
#include "b_tree.h"
#include "skip_list.h"

int i = 0;

#include <thread>
#include <chrono>
#include <filesystem>

#include <thread>
#include <chrono>
#include <filesystem>

#include <thread>
#include <chrono>
#include <filesystem>

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

    std::string linedt; //Variable to hold each line of the dataset
    std::string lineda; // Variable to hold each line of the communication file
    
    DoublyLinkedList list;
    HashTable hashTable;
    BTree btree(3);
    SkipList skipList(16, 0.75f);
    std::ifstream dataset("../../../datasets/NYPD_Complaint_Data_Historic.csv");
    // Check if the file opened successfully
    if (!dataset.is_open()){
        std::ifstream dataset("../../../datasets/NYPD_Complaint_Data_Historic.csv");
    }
        // Check if the dataset opened successfully
    if (!dataset.is_open()){ // Prompt: Substitute the if with a exception 
        std::cout << "Failed to open the dataset file! Check if it exists and is accessible.";
    }
    // Skip header line
    std::getline(dataset, linedt);
    /*
    // Read each line and parse it into ComplaintData
    while (std::getline(dataset, linedt)) {
        ComplaintData data = parseCSVLine(linedt);
        list.append(data);
        hashTable.insert(data);
        btree.insert(data);
        skipList.insert(data);
        if (i < 5) {
         std::cout << "\n[Skip List apos inserir CMPLNT_NUM = " << data.CMPLNT_NUM << "]\n";
         skipList.print();
        }   
        i++;
        if(i == 5){
          break;
        }
*/
    // Use the same path as Python (relative to where Python launches the process)
    std::string comm_path = "datasets/communication.data";
    std::cout << "C++ communication file path: " << std::filesystem::absolute(comm_path) << std::endl;

    // Open communication file in read/write mode and keep it open
    std::fstream commFile(comm_path, std::ios::in | std::ios::out);
    if (!commFile.is_open()) {
        std::cout << "Failed to open the communication file! Check if it exists and is accessible.";
        return 1;
    }

    if (std::getline(commFile, lineda)) {
        int command = 0;
        try {
            command = std::stoi(lineda);
        } catch (const std::invalid_argument& e) {
            std::cout << "Invalid command! Structure not listed" << lineda << std::endl;
        } catch (const std::out_of_range& e) {
            std::cout << "Command out of range! Structure not listed" << lineda << std::endl;
        }
        switch(command) {
        case 0:
            while (std::getline(dataset, linedt)) {
                ComplaintData data = parseCSVLine(linedt);
                list.append(data);
            }
            break;
        case 1:
            while (std::getline(dataset, linedt)) {
                ComplaintData data = parseCSVLine(linedt);
                hashTable.insert(data);
            }
            break;
        default:
            std::cout << "Erro de Execução " << lineda << std::endl;
        }
        //Finished reading and creating the data structure
    }
    dataset.close();

    // Move file pointer to beginning and overwrite with 0
    commFile.clear();
    commFile.seekp(0, std::ios::beg);
    commFile << "0";
    commFile.flush();

    // Loop to constantly read the file and verify the number inside it
    while (true) {
        commFile.clear();
        commFile.seekg(0, std::ios::beg);
        std::string commandLine;
        if (std::getline(commFile, commandLine)) {
            int commandValue = 0;
            try {
                commandValue = std::stoi(commandLine);
            } catch (...) {
                commandValue = -1;
            }
            std::cout << "Current command value: " << commandValue << std::endl;
            if (commandValue != 0) {
                switch (commandValue) {
                    case 11:
                        std::cout << "List size: " << list.size() << std::endl;
                        // Move file pointer to beginning and overwrite with -11
                        commFile.clear();
                        commFile.seekp(0, std::ios::beg);
                        commFile << "-11";
                        commFile.flush();
                        break;
                    default:
                        std::cout << "Invalid command! Operation not Listened: " << commandValue << std::endl;
                        break;
                }
            }
        }
        std::this_thread::sleep_for(std::chrono::seconds(1));
    }

    commFile.close();
}
