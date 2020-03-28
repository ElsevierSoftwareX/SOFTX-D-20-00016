#ifdef _MSC_VER
#define _CRT_SECURE_NO_WARNINGS
#endif

#include <fstream>
#include <iostream>
#include <boost/archive/xml_iarchive.hpp>
#include <boost/archive/xml_oarchive.hpp>
#include "meta.hpp"

using namespace std;

Meta::Meta() {}
Meta::Meta(Task task, string dumped) {

    this->task = task;
    this->dumped = dumped;
}