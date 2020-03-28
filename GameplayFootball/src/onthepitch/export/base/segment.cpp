#ifdef _MSC_VER
#define _CRT_SECURE_NO_WARNINGS
#endif

#include <fstream>
#include <iostream>
#include <boost/archive/xml_iarchive.hpp>
#include <boost/archive/xml_oarchive.hpp>
#include "segment.hpp"

using namespace std;

Segment::Segment() {}
Segment::Segment(int id, long start, long stop, string url) {

    this->id = id;
    this->start = start;
    this->stop = stop;
    this->url = url;   
}