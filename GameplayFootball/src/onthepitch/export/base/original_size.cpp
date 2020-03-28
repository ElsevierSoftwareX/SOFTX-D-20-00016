#ifdef _MSC_VER
#define _CRT_SECURE_NO_WARNINGS
#endif

#include <fstream>
#include <iostream>
#include <boost/archive/xml_iarchive.hpp>
#include <boost/archive/xml_oarchive.hpp>
#include "original_size.hpp"

using namespace std;

OriginalSize::OriginalSize() {}
OriginalSize::OriginalSize(int width, int height) {

    this->width = width;
    this->height = height;
    
}