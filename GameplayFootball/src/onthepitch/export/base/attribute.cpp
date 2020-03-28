#ifdef _MSC_VER
#define _CRT_SECURE_NO_WARNINGS
#endif

#include <fstream>
#include <iostream>
#include <boost/archive/xml_iarchive.hpp>
#include <boost/archive/xml_oarchive.hpp>
#include "attribute.hpp"

using namespace std;

Attribute::Attribute() {}
Attribute::Attribute(string name, string value) {

    this->name = name;
    this->value = value;
}