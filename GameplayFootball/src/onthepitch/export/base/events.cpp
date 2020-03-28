#ifdef _MSC_VER
#define _CRT_SECURE_NO_WARNINGS
#endif

#include <fstream>
#include <iostream>
#include <boost/archive/xml_iarchive.hpp>
#include <boost/archive/xml_oarchive.hpp>
#include <boost/geometry/geometries/point_xy.hpp>
#include <boost/geometry.hpp>
#include "events.hpp"

using namespace std;
using namespace boost::geometry;
using namespace AtomicEvents;

KickingTheBall::KickingTheBall() {}
KickingTheBall::KickingTheBall(
    double timestamp,
    string playerId,
    model::d2::point_xy<double> playerPos) {

       this->timestamp = timestamp;
       this->playerId = playerId;
       this->playerPos = playerPos; 

}