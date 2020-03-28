#pragma once
#include <fstream>
#include <iostream>
#include <boost/archive/xml_iarchive.hpp>
#include <boost/archive/xml_oarchive.hpp>

using namespace std;

class OriginalSize {

    private:

        friend class boost::serialization::access;
        template<class Archive> void serialize(Archive & ar,
            const unsigned int version) {
                
                ar & BOOST_SERIALIZATION_NVP(width);
                ar & BOOST_SERIALIZATION_NVP(height);
            }

        int width;
        int height;
        
    public:

        // Constructor
        OriginalSize();
        OriginalSize(int width, int height);

};

// Order is important
BOOST_CLASS_IMPLEMENTATION(OriginalSize, boost::serialization::object_serializable)
BOOST_CLASS_TRACKING(OriginalSize, boost::serialization::track_never)