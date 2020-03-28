#ifdef _MSC_VER
#define _CRT_SECURE_NO_WARNINGS
#endif

#include <fstream>
#include <iostream>
#include <boost/archive/xml_iarchive.hpp>
#include <boost/archive/xml_oarchive.hpp>
#include "task.hpp"
#include "meta.hpp"
#include "track.hpp"
#include "annotations.hpp"

using namespace std;
using namespace boost::archive;

Annotations::Annotations() {}
Annotations::Annotations(string XMLversion, Meta meta) {

    this->XMLversion = XMLversion;
    this->meta = meta;
}

void Annotations::AddMetadata(Meta meta) {
    this->meta = meta;
}

void Annotations::AddTrack(Track t) {
    this->track.push_back(t); 
}