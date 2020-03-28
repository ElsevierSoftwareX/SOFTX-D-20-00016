#pragma once
#include <fstream>
#include <iostream>
#include <boost/geometry/geometries/point_xy.hpp>
#include <boost/geometry.hpp>

using namespace std;
using namespace boost::geometry;

namespace AtomicEvents {

    class KickingTheBall {

        private:
            double timestamp;
            string playerId;
            model::d2::point_xy<double> playerPos;

        public:
            KickingTheBall();
            KickingTheBall(
                double timestamp,
                string playerId,
                model::d2::point_xy<double> playerPos);
    };

};

namespace ComplexEvents {};