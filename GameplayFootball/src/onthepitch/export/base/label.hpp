#pragma once
#include <fstream>
#include <iostream>
#include <boost/archive/xml_iarchive.hpp>
#include <boost/archive/xml_oarchive.hpp>
#include <boost/serialization/vector.hpp>

using namespace std;

class Label {

    private:

        friend class boost::serialization::access;
        template<class Archive> void serialize(Archive & ar,
            const unsigned int version) {
                
                ar & BOOST_SERIALIZATION_NVP(name);
                ar & BOOST_SERIALIZATION_NVP(attributes);
            }

        string name;
        vector<string> attributes;
        
    public:

        // Constructor
        Label();
        Label(string name);

        // Utility method
        void addAttribute(string a) { attributes.push_back(a); }

};

// Order is important
BOOST_CLASS_IMPLEMENTATION(Label, boost::serialization::object_serializable)
BOOST_CLASS_TRACKING(Label, boost::serialization::track_never)