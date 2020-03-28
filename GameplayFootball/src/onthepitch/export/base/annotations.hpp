#pragma once
#include <fstream>
#include <iostream>
#include <boost/archive/xml_iarchive.hpp>
#include <boost/archive/xml_oarchive.hpp>
#include "task.hpp"
#include "meta.hpp"
#include "track.hpp"

using namespace std;

class Annotations {

    private:

        friend class boost::serialization::access;
        template<class Archive> void serialize(Archive & ar,
            const unsigned int version) {
                
                ar & BOOST_SERIALIZATION_NVP(XMLversion);
                ar & BOOST_SERIALIZATION_NVP(meta);
                ar & BOOST_SERIALIZATION_NVP(track);
            }

        string XMLversion;
        Meta meta;
        vector<Track> track;

        // Utility member(s)
        ofstream ofs;
        
    public:

        // Constructor
        Annotations();
        Annotations(string XMLversion, Meta meta);

        // Core method(s)
        static void Export();

        // Utility method(s)
        void AddMetadata(Meta meta);
        void AddTrack(Track t);
        
};

// Order is important
BOOST_CLASS_IMPLEMENTATION(Annotations, boost::serialization::object_serializable)
BOOST_CLASS_TRACKING(Annotations, boost::serialization::track_never)
