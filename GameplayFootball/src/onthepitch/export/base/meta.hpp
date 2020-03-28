#pragma once
#include <fstream>
#include <iostream>
#include <boost/archive/xml_iarchive.hpp>
#include <boost/archive/xml_oarchive.hpp>
#include "task.hpp"

using namespace std;

class Meta {

    private:

        friend class boost::serialization::access;
        template<class Archive> void serialize(Archive & ar,
            const unsigned int version) {
                
                ar & BOOST_SERIALIZATION_NVP(task);
                ar & BOOST_SERIALIZATION_NVP(dumped);
            }

        Task task;
        string dumped;
        
    public:

        // Constructor
        Meta();
        Meta(Task task, string dumped);

};

// Order is important
BOOST_CLASS_IMPLEMENTATION(Meta, boost::serialization::object_serializable)
BOOST_CLASS_TRACKING(Meta, boost::serialization::track_never)