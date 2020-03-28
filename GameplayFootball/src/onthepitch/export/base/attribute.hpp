#pragma once
#include <fstream>
#include <iostream>
#include <boost/archive/xml_iarchive.hpp>
#include <boost/archive/xml_oarchive.hpp>

using namespace std;

class Attribute {

    private:

        friend class boost::serialization::access;
        template<class Archive> void serialize(Archive & ar,
            const unsigned int version) {
                
                ar & BOOST_SERIALIZATION_NVP(name);
                ar & BOOST_SERIALIZATION_NVP(value);
            }

        string name;
        string value;
        
    public:

        // Constructor
        Attribute();
        Attribute(string name, string value);

};

// Order is important
BOOST_CLASS_IMPLEMENTATION(Attribute, boost::serialization::object_serializable)
BOOST_CLASS_TRACKING(Attribute, boost::serialization::track_never)