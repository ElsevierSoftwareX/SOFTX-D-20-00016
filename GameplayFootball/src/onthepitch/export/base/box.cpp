#ifdef _MSC_VER
#define _CRT_SECURE_NO_WARNINGS
#endif

#include <fstream>
#include <iostream>
#include <boost/archive/xml_iarchive.hpp>
#include <boost/archive/xml_oarchive.hpp>
#include "box.hpp"

using namespace std;

Box::Box() {}
Box::Box(long frame, double xtl, double ytl, double xbr,
            double ybr, int outside, int occluded,
            int keyframe) {

    this->frame = frame;
    this->xtl = xtl;
    this->ytl = ytl;
    this->xbr = xbr;
    this->ybr = ybr;
    this->outside = outside;
    this->occluded = occluded;
    this->keyframe = keyframe;
}