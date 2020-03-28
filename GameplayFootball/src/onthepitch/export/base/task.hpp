#pragma once
#include <fstream>
#include <iostream>
#include <boost/archive/xml_iarchive.hpp>
#include <boost/archive/xml_oarchive.hpp>
#include "original_size.hpp"
#include "owner.hpp"
#include "label.hpp"
#include "segment.hpp"

using namespace std;

class Task {

    private:

        friend class boost::serialization::access;
        template<class Archive> void serialize(Archive & ar,
            const unsigned int version) {
                
                ar & BOOST_SERIALIZATION_NVP(id);
                ar & BOOST_SERIALIZATION_NVP(name);
                ar & BOOST_SERIALIZATION_NVP(size);
                ar & BOOST_SERIALIZATION_NVP(mode);
                ar & BOOST_SERIALIZATION_NVP(overlap);
                ar & BOOST_SERIALIZATION_NVP(bugtracker);
                ar & BOOST_SERIALIZATION_NVP(flipped);
                ar & BOOST_SERIALIZATION_NVP(created);
                ar & BOOST_SERIALIZATION_NVP(updated);
                ar & BOOST_SERIALIZATION_NVP(labels);
                ar & BOOST_SERIALIZATION_NVP(segments);
                ar & BOOST_SERIALIZATION_NVP(owner);
                ar & BOOST_SERIALIZATION_NVP(original_size);
            }

        int id;
        string name;
        long size;
        string mode;
        int overlap;
        string bugtracker;
        bool flipped;
        string created;
        string updated;
        vector<Label> labels;
        vector<Segment> segments;
        Owner owner;
        OriginalSize original_size;

    public:

        // Constructor(s)
        Task();
        Task(int id, string name, long size, string mode,
            int overlap, string bugtracker, bool flipped,
            string created, string updated, Owner owner,
            OriginalSize original_size);

        // Utility method
        void addLabel(Label l) { labels.push_back(l); }
        void addSegment(Segment s) { segments.push_back(s); }

};

// Order is important
BOOST_CLASS_IMPLEMENTATION(Task, boost::serialization::object_serializable)
BOOST_CLASS_TRACKING(Task, boost::serialization::track_never)