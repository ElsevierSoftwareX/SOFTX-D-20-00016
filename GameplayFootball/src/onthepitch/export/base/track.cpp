#ifdef _MSC_VER
#define _CRT_SECURE_NO_WARNINGS
#endif

#include <fstream>
#include <iostream>
#include <boost/archive/xml_iarchive.hpp>
#include <boost/archive/xml_oarchive.hpp>
#include "track.hpp"
#include "box.hpp"

using namespace std;

Track::Track() {}
Track::Track(long id, string label) {

    this->id = id;
    this->label = label;
}