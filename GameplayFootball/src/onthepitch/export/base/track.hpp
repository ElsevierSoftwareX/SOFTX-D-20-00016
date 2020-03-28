#pragma once
#include <fstream>
#include <iostream>
#include <boost/archive/xml_iarchive.hpp>
#include <boost/archive/xml_oarchive.hpp>
#include <boost/serialization/vector.hpp>
#include "track.hpp"
#include "box.hpp"

using namespace std;

class Track {

    private:

        friend class boost::serialization::access;
        template<class Archive> void serialize(Archive & ar,
            const unsigned int version) {
                
                ar & BOOST_SERIALIZATION_NVP(id);
                ar & BOOST_SERIALIZATION_NVP(label);
                ar & BOOST_SERIALIZATION_NVP(box);
            }

        long id;
        string label;
        vector<Box> box;
        
    public:

        // Constructor
        Track();
        Track(long id, string label);

        // Utility method
        void addBox(Box b) { box.push_back(b); }

};

// Order is important
BOOST_CLASS_IMPLEMENTATION(Track, boost::serialization::object_serializable)
BOOST_CLASS_TRACKING(Track, boost::serialization::track_never)