#ifdef _MSC_VER
#define _CRT_SECURE_NO_WARNINGS
#endif

#include <fstream>
#include <iostream>
#include <boost/archive/xml_iarchive.hpp>
#include <boost/archive/xml_oarchive.hpp>
#include "task.hpp"
#include "original_size.hpp"

using namespace std;

Task::Task() {}
Task::Task(int id, string name, long size, string mode,
    int overlap, string bugtracker, bool flipped,
    string created, string updated, Owner owner,
    OriginalSize original_size) {

    this->id = id;
    this->name = name;
    this->size = size;
    this->mode = mode;
    this->overlap = overlap;
    this->bugtracker = bugtracker;
    this->flipped = flipped;
    this->created = created;
    this->updated = updated;
    this->owner = owner;
    this->original_size = original_size;
}