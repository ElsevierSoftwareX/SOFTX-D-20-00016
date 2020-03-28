#pragma once
#include <fstream>
#include <iostream>
#include <boost/archive/xml_iarchive.hpp>
#include <boost/archive/xml_oarchive.hpp>

using namespace std;

class Owner {

    private:

        friend class boost::serialization::access;
        template<class Archive> void serialize(Archive & ar,
            const unsigned int version) {
                
                ar & BOOST_SERIALIZATION_NVP(username);
                ar & BOOST_SERIALIZATION_NVP(email);
            }

        string username;
        string email;
        
    public:

        // Constructor
        Owner();
        Owner(string username, string email);

};

// Order is important
BOOST_CLASS_IMPLEMENTATION(Owner, boost::serialization::object_serializable)
BOOST_CLASS_TRACKING(Owner, boost::serialization::track_never)