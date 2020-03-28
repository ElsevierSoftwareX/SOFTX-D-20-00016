#pragma once
#include <fstream>
#include <iostream>
#include <boost/archive/xml_iarchive.hpp>
#include <boost/archive/xml_oarchive.hpp>

using namespace std;

class Segment {

    private:

        friend class boost::serialization::access;
        template<class Archive> void serialize(Archive & ar,
            const unsigned int version) {
                
                ar & BOOST_SERIALIZATION_NVP(id);
                ar & BOOST_SERIALIZATION_NVP(start);
                ar & BOOST_SERIALIZATION_NVP(stop);
                ar & BOOST_SERIALIZATION_NVP(url);
            }

        int id;
        long start;
        long stop;
        string url;
        
    public:

        // Constructor
        Segment();
        Segment(int id, long start, long stop, string url);

};

// Order is important
BOOST_CLASS_IMPLEMENTATION(Segment, boost::serialization::object_serializable)
BOOST_CLASS_TRACKING(Segment, boost::serialization::track_never)