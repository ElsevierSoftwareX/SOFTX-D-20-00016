#pragma once
#include <fstream>
#include <iostream>
#include <boost/archive/xml_iarchive.hpp>
#include <boost/archive/xml_oarchive.hpp>
#include "attribute.hpp"

using namespace std;

class Box {

    private:

        friend class boost::serialization::access;
        template<class Archive> void serialize(Archive & ar,
            const unsigned int version) {
                
                ar & BOOST_SERIALIZATION_NVP(frame);
                ar & BOOST_SERIALIZATION_NVP(xtl);
                ar & BOOST_SERIALIZATION_NVP(ytl);
                ar & BOOST_SERIALIZATION_NVP(xbr);
                ar & BOOST_SERIALIZATION_NVP(ybr);
                ar & BOOST_SERIALIZATION_NVP(outside);
                ar & BOOST_SERIALIZATION_NVP(occluded);
                ar & BOOST_SERIALIZATION_NVP(keyframe);
                ar & BOOST_SERIALIZATION_NVP(attributes);
            }

        long frame;
        double xtl;
        double ytl;
        double xbr;
        double ybr;
        int outside;
        int occluded;
        int keyframe;
        vector<Attribute> attributes;
        
    public:

        // Constructor
        Box();
        Box(long frame, double xtl, double ytl, double xbr,
            double ybr, int outside, int occluded,
            int keyframe);

        // Utility method
        void addAttribute(Attribute a) { attributes.push_back(a); }
        

};

// Order is important
BOOST_CLASS_IMPLEMENTATION(Box, boost::serialization::object_serializable)
BOOST_CLASS_TRACKING(Box, boost::serialization::track_never)