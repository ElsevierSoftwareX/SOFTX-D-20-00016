#ifdef _MSC_VER
#define _CRT_SECURE_NO_WARNINGS
#endif

#include <fstream>
#include <iostream>
#include <sstream>
#include <boost/archive/xml_iarchive.hpp>
#include <boost/archive/xml_oarchive.hpp>
#include "base/annotations.hpp"
#include "base/meta.hpp"
#include "base/track.hpp"
#include "base/task.hpp"
#include "base/original_size.hpp"
#include "base/label.hpp"
#include "base/owner.hpp"
#include "annotation.hpp"
#include "normalize.hpp"
#include "base/attribute.hpp"
#include <boost/geometry/geometries/point_xy.hpp>
#include <boost/geometry.hpp>
#include <time.h>

using namespace std;
using namespace boost::archive;
using namespace boost::geometry;

// Constructor
Annotation::Annotation() {

    string version = "1.1";
    Meta* meta = new Meta();

    Annotations* atomicEventsAnnotations = new Annotations(version, *meta);
    this->atomicEventsAnnotations = atomicEventsAnnotations;
    this->atomicEventsCounter = 1;

    Annotations* atomicEventsForCvatAnnotations = new Annotations(version, *meta);
    this->atomicEventsForCvatAnnotations = atomicEventsForCvatAnnotations;

    Annotations* atomicEventsForManualAnnotations = new Annotations(version, *meta);
    this->atomicEventsForManualAnnotations = atomicEventsForManualAnnotations;

    Annotations* complexEventsAnnotations = new Annotations(version, *meta);
    this->complexEventsAnnotations = complexEventsAnnotations;
    this->complexEventsCounter = 1;

}

void Annotation::AddMetadata() {

    int id = 8;
    string name = "Event Annotation";
    long size = 3000;
    string mode = "interpolation";
    int overlap = 5;
    string bugtracker = "";
    bool flipped = false;
    string created = "2018-11-07 12:46:32.600949+03:00";
    string updated = "2018-11-07 16:28:55.487507+03:00";
    
    // Set the labels
    string labelName = "Pass";
    Label* labelPass = new Label(labelName);
    string attribute = "@select=receiver:1,2,3,4,5,6,7,8,9,10,11,21,22,23,24,25,26,27,28,29,30,31";
    labelPass->addAttribute(attribute);
    attribute = "@select=sender:1,2,3,4,5,6,7,8,9,10,11,21,22,23,24,25,26,27,28,29,30,31";
    labelPass->addAttribute(attribute);

    labelName = "KickingTheBall";
    Label* labelKickingTheBall = new Label(labelName);
    attribute = "@select=player:1,2,3,4,5,6,7,8,9,10,11,21,22,23,24,25,26,27,28,29,30,31";
    labelKickingTheBall->addAttribute(attribute);

    // Set the segments
    string url = "http://localhost:8080/?id=7";
    Segment* segment = new Segment(7, 0, 2999, url);

    // Set the owner
    string username = "admin";
    string email = "giuseppecanto1993@gmail.com";
    Owner* owner = new Owner(username, email);

    // Set the original size
    OriginalSize* original_size = new OriginalSize(1280, 720);

    Task* task = new Task(
        id,
        name,
        size,
        mode,
        overlap,
        bugtracker,
        flipped,
        created,
        updated,
        *owner,
        *original_size);
    task->addLabel(*labelPass);
    task->addLabel(*labelKickingTheBall);
    task->addSegment(*segment);
    string dumped = "dumped_timestamp";
    Meta* meta = new Meta(*task, dumped);

    this->atomicEventsForCvatAnnotations->AddMetadata(*meta);
    this->complexEventsAnnotations->AddMetadata(*meta);
}

void Annotation::ExportAtomicEvents(string half) {

    // Declare variable(s)
    char* filename;
    unsigned int flags = no_header;
    Annotations* annotations;

    // It checks if fist-half or second-half
    if (half.compare("first") == 0) {
        filename = (char*) malloc(sizeof(char)*(40));
        filename = "Annotations_AtomicEvents_firstHalf.xml";
    } else if (half.compare("second") == 0) {
        filename = (char*) malloc(sizeof(char)*(41));
        filename = "Annotations_AtomicEvents_secondHalf.xml";
    } else {
        filename = (char*) malloc(sizeof(char)*(30));
        filename = "Annotations_AtomicEvents.xml";
    }

    // Export the data
    ofstream ofs(filename);
    xml_oarchive oa(ofs, flags);

    // Export annotation (with serialization)
    annotations = this->atomicEventsAnnotations;
    oa << BOOST_SERIALIZATION_NVP(annotations);
    ofs.close();

    // Normalize data with post-process
    AnnotationsLoader::Load(filename);

}

void Annotation::ExportAtomicEventsForCvatAnnotations(string half) {

    // Declare variable(s)
    char* filename;
    unsigned int flags = no_header;
    Annotations* annotations;

    // It checks if fist-half or second-half
    if (half.compare("first") == 0) {
        filename = (char*) malloc(sizeof(char)*(40));
        filename = "Annotations_AtomicEvents_Cvat_firstHalf.xml";
    } else if (half.compare("second") == 0) {
        filename = (char*) malloc(sizeof(char)*(41));
        filename = "Annotations_AtomicEvents_Cvat_secondHalf.xml";
    } else {
        filename = (char*) malloc(sizeof(char)*(30));
        filename = "Annotations_AtomicEvents_Cvat.xml";
    }

    // Export the data
    ofstream ofs(filename);
    xml_oarchive oa(ofs, flags);

    // Export annotation (with serialization)
    annotations = this->atomicEventsForCvatAnnotations;
    oa << BOOST_SERIALIZATION_NVP(annotations);
    ofs.close();

    // Normalize data with post-process
    AnnotationsLoader::Load(filename);

}

void Annotation::ExportAtomicEventsForManualAnnotations(string half) {

    // Declare variable(s)
    char* filename;
    unsigned int flags = no_header;
    Annotations* annotations;

    // It checks if fist-half or second-half
    if (half.compare("first") == 0) {
        filename = (char*) malloc(sizeof(char)*(40));
        filename = "Annotations_AtomicEvents_Manual_firstHalf.xml";
    } else if (half.compare("second") == 0) {
        filename = (char*) malloc(sizeof(char)*(41));
        filename = "Annotations_AtomicEvents_Manual_secondHalf.xml";
    } else {
        filename = (char*) malloc(sizeof(char)*(30));
        filename = "Annotations_AtomicEvents_Manual.xml";
    }

    // Export the data
    ofstream ofs(filename);
    xml_oarchive oa(ofs, flags);

    // Export annotation (with serialization)
    annotations = this->atomicEventsForManualAnnotations;
    oa << BOOST_SERIALIZATION_NVP(annotations);
    ofs.close();

    // Normalize data with post-process
    AnnotationsLoader::Load(filename);

}

void Annotation::ExportComplexEvents(string half) {

    // Declare variable(s)
    char* filename;
    unsigned int flags = no_header;
    Annotations* annotations;

    // It checks if fist-half or second-half
    if (half.compare("first") == 0) {
        filename = (char*) malloc(sizeof(char)*(40));
        filename = "Annotations_ComplexEvents_firstHalf.xml";
    } else if (half.compare("second") == 0) {
        filename = (char*) malloc(sizeof(char)*(41));
        filename = "Annotations_ComplexEvents_secondHalf.xml";
    } else {
        filename = (char*) malloc(sizeof(char)*(30));
        filename = "Annotations_ComplexEvents.xml";
    }

    // Export the data
    ofstream ofs(filename);
    xml_oarchive oa(ofs, flags);

    // Export annotation (with serialization)
    annotations = this->complexEventsAnnotations;
    oa << BOOST_SERIALIZATION_NVP(annotations);
    ofs.close();

    // Normalize data with post-process
    AnnotationsLoader::Load(filename);

}

void Annotation::Export(string half) {

   Annotation::ExportAtomicEvents(half);
   Annotation::ExportAtomicEventsForCvatAnnotations(half);
   Annotation::ExportAtomicEventsForManualAnnotations(half);
   Annotation::ExportComplexEvents(half);

}

void Annotation::KickingTheBall(int frame, string playerId, string teamId, double x, double y) {
    // TODO: the id of the event must be incremental, not always one
    // TODO: transform the playerPos 2D data to Bbox
    // =>
    // =>   from a 2d point which represent the position of the player
    // =>   build a rectangle with a fixed size and a center that
    // =>   corresponds to the the given 2d ponit.
    model::d2::point_xy<double> playerPos(x, y);

    // Create a track for the event
    Track* track = new Track(this->atomicEventsCounter, "KickingTheBall");

    // Add BBox for the event occurrence
    Box* b1 = new Box(frame, 1200.53, 91.79, 1241.58, 168.74, 0, 0, 1);
    string name = "playerId";
    Attribute* attribute = new Attribute(name, playerId);
    b1->addAttribute(*attribute);
    name = "teamId";
    attribute = new Attribute(name, teamId);
    b1->addAttribute(*attribute);
    track->addBox(*b1);

    // Add the tracked event to the annotation
    this->atomicEventsForCvatAnnotations->AddTrack(*track);

    // Create a track for the event
    track = new Track(this->atomicEventsCounter, "KickingTheBall");

    // Add BBox for the event occurrence
    b1 = new Box(frame, 1200.53, 91.79, 1241.58, 168.74, 0, 0, 1);
    name = "playerId";
    attribute = new Attribute(name, playerId);
    b1->addAttribute(*attribute);
    name = "teamId";
    attribute = new Attribute(name, teamId);
    b1->addAttribute(*attribute);
    name = "x";
    attribute = new Attribute(name, Annotation::DoubleToString(x));
    b1->addAttribute(*attribute);
    name = "y";
    attribute = new Attribute(name, Annotation::DoubleToString(y));
    b1->addAttribute(*attribute);
    track->addBox(*b1);

    // Add the tracked event to the annotation
    this->atomicEventsAnnotations->AddTrack(*track);

    // Increment counter
    this->atomicEventsCounter += 1;

}

void Annotation::BallPossession(int frame, string playerId, string teamId, double x, double y,
    string outermostOtherTeamDefensivePlayerId, string outermostOtherTeamDefensivePlayerTeamId,
    double outermostOtherTeamDefensivePlayerX, double outermostOtherTeamDefensivePlayerY) {

    // Create a track for the event
    Track* track = new Track(this->atomicEventsCounter, "BallPossession");

    // Add BBox for the event occurrence
    Box* b1 = new Box(frame, 1200.53, 91.79, 1241.58, 168.74, 0, 0, 1);
    string name = "playerId";
    Attribute* attribute = new Attribute(name, playerId);
    b1->addAttribute(*attribute);
    name = "teamId";
    attribute = new Attribute(name, teamId);
    b1->addAttribute(*attribute);
    name = "outermostOtherTeamDefensivePlayerId";
    attribute = new Attribute(name, outermostOtherTeamDefensivePlayerId);
    b1->addAttribute(*attribute);
    name = "outermostOtherTeamDefensivePlayerTeamId";
    attribute = new Attribute(name, outermostOtherTeamDefensivePlayerTeamId);
    b1->addAttribute(*attribute);
    track->addBox(*b1);

    // Add the tracked event to the annotation
    this->atomicEventsForCvatAnnotations->AddTrack(*track);

    // Create a track for the event
    track = new Track(this->atomicEventsCounter, "BallPossession");

    // Add BBox for the event occurrence
    b1 = new Box(frame, 1200.53, 91.79, 1241.58, 168.74, 0, 0, 1);
    name = "playerId";
    attribute = new Attribute(name, playerId);
    b1->addAttribute(*attribute);
    name = "teamId";
    attribute = new Attribute(name, teamId);
    b1->addAttribute(*attribute);
    name = "x";
    attribute = new Attribute(name, Annotation::DoubleToString(x));
    b1->addAttribute(*attribute);
    name = "y";
    attribute = new Attribute(name, Annotation::DoubleToString(y));
    b1->addAttribute(*attribute);
    name = "outermostOtherTeamDefensivePlayerId";
    attribute = new Attribute(name, outermostOtherTeamDefensivePlayerId);
    b1->addAttribute(*attribute);
    name = "outermostOtherTeamDefensivePlayerTeamId";
    attribute = new Attribute(name, outermostOtherTeamDefensivePlayerTeamId);
    b1->addAttribute(*attribute);
    name = "outermostOtherTeamDefensivePlayerX";
    attribute = new Attribute(name, Annotation::DoubleToString(outermostOtherTeamDefensivePlayerX));
    b1->addAttribute(*attribute);
    name = "outermostOtherTeamDefensivePlayerY";
    attribute = new Attribute(name, Annotation::DoubleToString(outermostOtherTeamDefensivePlayerY));
    b1->addAttribute(*attribute);
    track->addBox(*b1);

    // Add the tracked event to the annotation
    this->atomicEventsAnnotations->AddTrack(*track);

    // Increment counter
    this->atomicEventsCounter += 1;

}

void Annotation::Tackle(int frame, string player1Id, string team1Id, double x1, double y1,
    string player2Id, string team2Id, double x2, double y2) {

    // Create a track for the event
    Track* track = new Track(this->atomicEventsCounter, "Tackle");

    // Add BBox for the event occurrence
    Box* b1 = new Box(frame, 1200.53, 91.79, 1241.58, 168.74, 0, 0, 1);
    string name = "playerId";
    Attribute* attribute = new Attribute(name, player1Id);
    b1->addAttribute(*attribute);
    name = "teamId";
    attribute = new Attribute(name, team1Id);
    b1->addAttribute(*attribute);
    name = "tacklingPlayerId";
    attribute = new Attribute(name, player2Id);
    b1->addAttribute(*attribute);
    name = "tacklingPlayerTeamId";
    attribute = new Attribute(name, team2Id);
    b1->addAttribute(*attribute);
    track->addBox(*b1);

    // Add the tracked event to the annotation
    this->atomicEventsForCvatAnnotations->AddTrack(*track);

    // Create a track for the event
    track = new Track(this->atomicEventsCounter, "Tackle");

    // Add BBox for the event occurrence
    b1 = new Box(frame, 1200.53, 91.79, 1241.58, 168.74, 0, 0, 1);
    name = "playerId";
    attribute = new Attribute(name, player1Id);
    b1->addAttribute(*attribute);
    name = "teamId";
    attribute = new Attribute(name, team1Id);
    b1->addAttribute(*attribute);
    name = "x";
    attribute = new Attribute(name, Annotation::DoubleToString(x1));
    b1->addAttribute(*attribute);
    name = "y";
    attribute = new Attribute(name, Annotation::DoubleToString(y1));
    b1->addAttribute(*attribute);
    name = "tacklingPlayerId";
    attribute = new Attribute(name, player2Id);
    b1->addAttribute(*attribute);
    name = "tacklingPlayerTeamId";
    attribute = new Attribute(name, team2Id);
    b1->addAttribute(*attribute);
    name = "tacklingPlayerX";
    attribute = new Attribute(name, Annotation::DoubleToString(x2));
    b1->addAttribute(*attribute);
    name = "tacklingPlayerY";
    attribute = new Attribute(name, Annotation::DoubleToString(y2));
    b1->addAttribute(*attribute);
    track->addBox(*b1);

    // Add the tracked event to the annotation
    this->atomicEventsAnnotations->AddTrack(*track);

    // Increment counter
    this->atomicEventsCounter += 1;

}

void Annotation::BallDeflection(int frame, string playerId, string teamId, double x, double y) {

    // Create a track for the event
    Track* track = new Track(this->atomicEventsCounter, "BallDeflection");

    // Add BBox for the event occurrence
    Box* b1 = new Box(frame, 1200.53, 91.79, 1241.58, 168.74, 0, 0, 1);
    string name = "playerId";
    Attribute* attribute = new Attribute(name, playerId);
    b1->addAttribute(*attribute);
    name = "teamId";
    attribute = new Attribute(name, teamId);
    b1->addAttribute(*attribute);
    track->addBox(*b1);

    // Add the tracked event to the annotation
    this->atomicEventsForCvatAnnotations->AddTrack(*track);

    // Create a track for the event
    track = new Track(this->atomicEventsCounter, "BallDeflection");

    // Add BBox for the event occurrence
    b1 = new Box(frame, 1200.53, 91.79, 1241.58, 168.74, 0, 0, 1);
    name = "playerId";
    attribute = new Attribute(name, playerId);
    b1->addAttribute(*attribute);
    name = "teamId";
    attribute = new Attribute(name, teamId);
    b1->addAttribute(*attribute);
    name = "x";
    attribute = new Attribute(name, Annotation::DoubleToString(x));
    b1->addAttribute(*attribute);
    name = "y";
    attribute = new Attribute(name, Annotation::DoubleToString(y));
    b1->addAttribute(*attribute);
    track->addBox(*b1);

    // Add the tracked event to the annotation
    this->atomicEventsAnnotations->AddTrack(*track);

    // Increment counter
    this->atomicEventsCounter += 1;

}

void Annotation::BallOut(int frame) {

    // Create a track for the event
    Track* track = new Track(this->atomicEventsCounter, "BallOut");

    // Add BBox for the event occurrence
    Box* b = new Box(frame, 1200.53, 91.79, 1241.58, 168.74, 0, 0, 1);
    track->addBox(*b);

    // Add the tracked event to the annotation
    this->atomicEventsAnnotations->AddTrack(*track);
    this->atomicEventsForCvatAnnotations->AddTrack(*track);

    // Increment counter
    this->atomicEventsCounter += 1;

}

void Annotation::Goal(int frame, string scorerId, string teamId) {

    // Create a track for the event
    Track* track = new Track(this->atomicEventsCounter, "Goal");

    // Add BBox for the event occurrence
    Box* b1 = new Box(frame, 1200.53, 91.79, 1241.58, 168.74, 0, 0, 1);
    string name = "scorer";
    Attribute* attribute = new Attribute(name, scorerId);
    b1->addAttribute(*attribute);
    name = "team";
    attribute = new Attribute(name, teamId);
    b1->addAttribute(*attribute);
    track->addBox(*b1);

    // Add the tracked event to the annotation
    this->atomicEventsAnnotations->AddTrack(*track);
    this->atomicEventsForCvatAnnotations->AddTrack(*track);
    this->atomicEventsForManualAnnotations->AddTrack(*track);

    // Increment counter
    this->atomicEventsCounter += 1;

}

void Annotation::Foul(int frame, string scorerId, string teamId) {

    // Create a track for the event
    Track* track = new Track(this->atomicEventsCounter, "Foul");

    // Add BBox for the event occurrence
    Box* b1 = new Box(frame, 1200.53, 91.79, 1241.58, 168.74, 0, 0, 1);
    string name = "scorerId";
    Attribute* attribute = new Attribute(name, scorerId);
    b1->addAttribute(*attribute);
    name = "teamId";
    attribute = new Attribute(name, teamId);
    b1->addAttribute(*attribute);
    track->addBox(*b1);

    // Add the tracked event to the annotation
    this->atomicEventsAnnotations->AddTrack(*track);
    this->atomicEventsForCvatAnnotations->AddTrack(*track);
    this->atomicEventsForManualAnnotations->AddTrack(*track);

    // Increment counter
    this->atomicEventsCounter += 1;

}

void Annotation::Penalty(int frame, string scorerId, string teamId) {

    // Create a track for the event
    Track* track = new Track(this->atomicEventsCounter, "Penalty");

    // Add BBox for the event occurrence
    Box* b1 = new Box(frame, 1200.53, 91.79, 1241.58, 168.74, 0, 0, 1);
    string name = "scorerId";
    Attribute* attribute = new Attribute(name, scorerId);
    b1->addAttribute(*attribute);
    name = "teamId";
    attribute = new Attribute(name, teamId);
    b1->addAttribute(*attribute);
    track->addBox(*b1);

    // Add the tracked event to the annotation
    this->atomicEventsAnnotations->AddTrack(*track);
    this->atomicEventsForCvatAnnotations->AddTrack(*track);
    this->atomicEventsForManualAnnotations->AddTrack(*track);

    // Increment counter
    this->atomicEventsCounter += 1;

}

void Annotation::Pass(int startFrame, int endFrame, string senderId,
    string teamId, string receiverId) {

    Track* track = new Track(this->complexEventsCounter++, "Pass");

    Box* b;
    Attribute* attribute;
    string name;
    for (int f=startFrame; f<endFrame; f++) {

        // Is Keyframe or not?
        if (f == startFrame) {
            b = new Box(f, 1200.53, 91.79, 1241.58, 168.74, 0, 0, 1);
        } else {
            b = new Box(f, 1200.53, 91.79, 1241.58, 168.74, 0, 0, 0);
        }
        
        name = "sender";
        attribute = new Attribute(name, senderId);
        b->addAttribute(*attribute);

        name = "teamId";
        attribute = new Attribute(name, teamId);
        b->addAttribute(*attribute);

        name = "receiver";
        attribute = new Attribute(name, receiverId);
        b->addAttribute(*attribute);

        track->addBox(*b);
    }

    this->complexEventsAnnotations->AddTrack(*track);
}

void Annotation::PassThenGoal(int startFrame, int endFrame, string senderId,
    string teamId, string scorerId) {

    Track* track = new Track(this->complexEventsCounter++, "PassThenGoal");

    Box* b;
    Attribute* attribute;
    string name;
    for (int f=startFrame; f<endFrame; f++) {

        // Is Keyframe or not?
        if (f == startFrame) {
            b = new Box(f, 1200.53, 91.79, 1241.58, 168.74, 0, 0, 1);
        } else {
            b = new Box(f, 1200.53, 91.79, 1241.58, 168.74, 0, 0, 0);
        }
        
        name = "sender";
        attribute = new Attribute(name, senderId);
        b->addAttribute(*attribute);

        name = "teamId";
        attribute = new Attribute(name, teamId);
        b->addAttribute(*attribute);

        name = "scorer";
        attribute = new Attribute(name, scorerId);
        b->addAttribute(*attribute);

        track->addBox(*b);
    }

    this->complexEventsAnnotations->AddTrack(*track);
}

void Annotation::FilteringPass(int startFrame, int endFrame, string senderId,
    string teamId, string receiverId) {

    Track* track = new Track(this->complexEventsCounter++, "FilteringPass");

    Box* b;
    Attribute* attribute;
    string name;
    for (int f=startFrame; f<endFrame; f++) {

        // Is Keyframe or not?
        if (f == startFrame) {
            b = new Box(f, 1200.53, 91.79, 1241.58, 168.74, 0, 0, 1);
        } else {
            b = new Box(f, 1200.53, 91.79, 1241.58, 168.74, 0, 0, 0);
        }
        
        name = "sender";
        attribute = new Attribute(name, senderId);
        b->addAttribute(*attribute);

        name = "teamId";
        attribute = new Attribute(name, teamId);
        b->addAttribute(*attribute);

        name = "receiver";
        attribute = new Attribute(name, receiverId);
        b->addAttribute(*attribute);

        track->addBox(*b);
    }

    this->complexEventsAnnotations->AddTrack(*track);
}

void Annotation::FilteringPassThenGoal(int startFrame, int endFrame, string senderId,
    string teamId, string scorerId) {

    Track* track = new Track(this->complexEventsCounter++, "FilteringPassThenGoal");

    Box* b;
    Attribute* attribute;
    string name;
    for (int f=startFrame; f<endFrame; f++) {

        // Is Keyframe or not?
        if (f == startFrame) {
            b = new Box(f, 1200.53, 91.79, 1241.58, 168.74, 0, 0, 1);
        } else {
            b = new Box(f, 1200.53, 91.79, 1241.58, 168.74, 0, 0, 0);
        }
        
        name = "sender";
        attribute = new Attribute(name, senderId);
        b->addAttribute(*attribute);

        name = "teamId";
        attribute = new Attribute(name, teamId);
        b->addAttribute(*attribute);

        name = "scorer";
        attribute = new Attribute(name, scorerId);
        b->addAttribute(*attribute);

        track->addBox(*b);
    }

    this->complexEventsAnnotations->AddTrack(*track);
}

void Annotation::Cross(int startFrame, int endFrame, string senderId,
    string teamId, string receiverId, bool outcome) {

    Track* track = new Track(this->complexEventsCounter++, "Cross");

    Box* b;
    Attribute* attribute;
    string name;
    for (int f=startFrame; f<endFrame; f++) {

        // Is Keyframe or not?
        if (f == startFrame) {
            b = new Box(f, 1200.53, 91.79, 1241.58, 168.74, 0, 0, 1);
        } else {
            b = new Box(f, 1200.53, 91.79, 1241.58, 168.74, 0, 0, 0);
        }
        
        name = "sender";
        attribute = new Attribute(name, senderId);
        b->addAttribute(*attribute);

        name = "teamId";
        attribute = new Attribute(name, teamId);
        b->addAttribute(*attribute);

        name = "receiver";
        attribute = new Attribute(name, receiverId);
        b->addAttribute(*attribute);

        name = "outcome";
        string outcomeStr = outcome?"true":"false";
        attribute = new Attribute(name, outcomeStr);
        b->addAttribute(*attribute);

        track->addBox(*b);
    }

    this->complexEventsAnnotations->AddTrack(*track);
}

void Annotation::CrossThenGoal(int startFrame, int endFrame, string senderId,
    string teamId, string scorerId) {

    Track* track = new Track(this->complexEventsCounter++, "CrossThenGoal");

    Box* b;
    Attribute* attribute;
    string name;
    for (int f=startFrame; f<endFrame; f++) {

        // Is Keyframe or not?
        if (f == startFrame) {
            b = new Box(f, 1200.53, 91.79, 1241.58, 168.74, 0, 0, 1);
        } else {
            b = new Box(f, 1200.53, 91.79, 1241.58, 168.74, 0, 0, 0);
        }
        
        name = "sender";
        attribute = new Attribute(name, senderId);
        b->addAttribute(*attribute);

        name = "teamId";
        attribute = new Attribute(name, teamId);
        b->addAttribute(*attribute);

        name = "scorer";
        attribute = new Attribute(name, scorerId);
        b->addAttribute(*attribute);

        track->addBox(*b);
    }

    this->complexEventsAnnotations->AddTrack(*track);
}

void Annotation::Tackle(int startFrame, int endFrame, string victimId,
    string teamId, string tacklerId, bool outcome) {

    Track* track = new Track(this->complexEventsCounter++, "Tackle");

    Box* b;
    Attribute* attribute;
    string name;
    for (int f=startFrame; f<endFrame; f++) {

        // Is Keyframe or not?
        if (f == startFrame) {
            b = new Box(f, 1200.53, 91.79, 1241.58, 168.74, 0, 0, 1);
        } else {
            b = new Box(f, 1200.53, 91.79, 1241.58, 168.74, 0, 0, 0);
        }
        
        name = "victimId";
        attribute = new Attribute(name, victimId);
        b->addAttribute(*attribute);

        name = "teamId";
        attribute = new Attribute(name, teamId);
        b->addAttribute(*attribute);

        name = "tacklerId";
        attribute = new Attribute(name, tacklerId);
        b->addAttribute(*attribute);

        name = "outcome";
        string outcomeStr = outcome?"true":"false";
        attribute = new Attribute(name, outcomeStr);
        b->addAttribute(*attribute);

        track->addBox(*b);
    }

    this->complexEventsAnnotations->AddTrack(*track);
}

void Annotation::SlidingTackle(int startFrame, int endFrame, string victimId,
    string teamId, string tacklerId, bool outcome) {

    Track* track = new Track(this->complexEventsCounter++, "SlidingTackle");

    Box* b;
    Attribute* attribute;
    string name;
    for (int f=startFrame; f<endFrame; f++) {

        // Is Keyframe or not?
        if (f == startFrame) {
            b = new Box(f, 1200.53, 91.79, 1241.58, 168.74, 0, 0, 1);
        } else {
            b = new Box(f, 1200.53, 91.79, 1241.58, 168.74, 0, 0, 0);
        }
        
        name = "victimId";
        attribute = new Attribute(name, victimId);
        b->addAttribute(*attribute);

        name = "teamId";
        attribute = new Attribute(name, teamId);
        b->addAttribute(*attribute);

        name = "tacklerId";
        attribute = new Attribute(name, tacklerId);
        b->addAttribute(*attribute);

        name = "outcome";
        string outcomeStr = outcome ? "true":"false";
        attribute = new Attribute(name, outcomeStr);
        b->addAttribute(*attribute);

        track->addBox(*b);
    }

    this->complexEventsAnnotations->AddTrack(*track);
}

void Annotation::Shot(int startFrame, int endFrame, string shooterId,
    string teamId) {

    Track* track = new Track(this->complexEventsCounter++, "Shot");

    Box* b;
    Attribute* attribute;
    string name;
    for (int f=startFrame; f<endFrame; f++) {

        // Is Keyframe or not?
        if (f == startFrame) {
            b = new Box(f, 1200.53, 91.79, 1241.58, 168.74, 0, 0, 1);
        } else {
            b = new Box(f, 1200.53, 91.79, 1241.58, 168.74, 0, 0, 0);
        }
        
        name = "shooterId";
        attribute = new Attribute(name, shooterId);
        b->addAttribute(*attribute);

        name = "teamId";
        attribute = new Attribute(name, teamId);
        b->addAttribute(*attribute);

        track->addBox(*b);
    }

    this->complexEventsAnnotations->AddTrack(*track);
}


void Annotation::ShotOut(int startFrame, int endFrame, string shooterId,
    string teamId) {

    Track* track = new Track(this->complexEventsCounter++, "ShotOut");

    Box* b;
    Attribute* attribute;
    string name;
    for (int f=startFrame; f<endFrame; f++) {

        // Is Keyframe or not?
        if (f == startFrame) {
            b = new Box(f, 1200.53, 91.79, 1241.58, 168.74, 0, 0, 1);
        } else {
            b = new Box(f, 1200.53, 91.79, 1241.58, 168.74, 0, 0, 0);
        }
        
        name = "shooterId";
        attribute = new Attribute(name, shooterId);
        b->addAttribute(*attribute);

        name = "teamId";
        attribute = new Attribute(name, teamId);
        b->addAttribute(*attribute);

        track->addBox(*b);
    }

    this->complexEventsAnnotations->AddTrack(*track);
}

void Annotation::ShotThenGoal(int startFrame, int endFrame, string shooterId,
    string teamId) {

    Track* track = new Track(this->complexEventsCounter++, "ShotThenGoal");

    Box* b;
    Attribute* attribute;
    string name;
    for (int f=startFrame; f<endFrame; f++) {

        // Is Keyframe or not?
        if (f == startFrame) {
            b = new Box(f, 1200.53, 91.79, 1241.58, 168.74, 0, 0, 1);
        } else {
            b = new Box(f, 1200.53, 91.79, 1241.58, 168.74, 0, 0, 0);
        }
        
        name = "shooterId";
        attribute = new Attribute(name, shooterId);
        b->addAttribute(*attribute);

        name = "teamId";
        attribute = new Attribute(name, teamId);
        b->addAttribute(*attribute);

        track->addBox(*b);
    }

    this->complexEventsAnnotations->AddTrack(*track);
}

void Annotation::SavedShot(int startFrame, int endFrame, string shooterId,
    string teamId, string goalkeeperId, string team2Id, double x, double y,
    SavedShotCase sscase) {

    Track* track = new Track(this->complexEventsCounter++, "SavedShot");

    Box* b;
    Attribute* attribute;
    string name;
    for (int f=startFrame; f<endFrame; f++) {

        // Is Keyframe or not?
        if (f == startFrame) {
            b = new Box(f, 1200.53, 91.79, 1241.58, 168.74, 0, 0, 1);
        } else {
            b = new Box(f, 1200.53, 91.79, 1241.58, 168.74, 0, 0, 0);
        }
        
        name = "shooterId";
        attribute = new Attribute(name, shooterId);
        b->addAttribute(*attribute);

        name = "teamId";
        attribute = new Attribute(name, teamId);
        b->addAttribute(*attribute);

        name = "goalkeeperId";
        attribute = new Attribute(name, goalkeeperId);
        b->addAttribute(*attribute);

        name = "team2Id";
        attribute = new Attribute(name, team2Id);
        b->addAttribute(*attribute);

        name = "case";
        string sscaseStr = Annotation::SavedShotCaseToString(sscase);
        attribute = new Attribute(name, sscaseStr);
        b->addAttribute(*attribute);

        track->addBox(*b);
    }

    this->complexEventsAnnotations->AddTrack(*track);
}

void Annotation::SecondHalf(int frame) {

    // Create a track for the annotation
    Track* track = new Track(0, "SecondHalf");

    // Add BBox for the event occurrence
    Box* b1 = new Box(frame, 53.0, 38.0, 57.0, 34.0, 0, 0, 1);
    track->addBox(*b1);

    // Add the tracked event to the annotation
    this->atomicEventsForManualAnnotations->AddTrack(*track);

}

void Annotation::Goalkeeper(string goalKeeperId, string teamId) {

    // Create a track for the annotation
    Track* track = new Track(-1, "GoalKeeper");

    // Add BBox for the event occurrence
    Box* b1 = new Box(0, 53.0, 38.0, 57.0, 34.0, 0, 0, 1);
    
    string name = "goalKeeperId";
    Attribute* attribute = new Attribute(name, goalKeeperId);
    b1->addAttribute(*attribute);

    name = "teamId";
    attribute = new Attribute(name, teamId);
    b1->addAttribute(*attribute);

    track->addBox(*b1);

    // Add the tracked event to the annotation
    this->atomicEventsForManualAnnotations->AddTrack(*track);

}

string Annotation::SavedShotCaseToString(Annotation::SavedShotCase sscase) {

    switch(sscase) {
        case Annotation::OnPenalty:
            return "OnPenalty";
        case Annotation::OnFoul:
            return "OnFoul";
        case Annotation::InsideGoalArea:
            return "InsideGoalArea";
        case Annotation::InsidePenaltyArea:
            return "InsidePenaltyArea";
        case Annotation::FromOutsideArea:
            return "FromOutsideArea";
        default:
            return "No case";
    }

}

string Annotation::DoubleToString(double value) {

    // From StackOverflow:
    // https://stackoverflow.com/questions/332111/how-do-i-convert-a-double-into-a-string-in-c

    ostringstream strs;
    strs << value;
    string str = strs.str();

    return str;

}