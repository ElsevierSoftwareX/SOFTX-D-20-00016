#pragma once

#include <fstream>
#include <iostream>
#include <boost/archive/xml_iarchive.hpp>
#include <boost/archive/xml_oarchive.hpp>
#include "base/annotations.hpp"
#include "base/meta.hpp"
#include "base/track.hpp"

using namespace std;

class Annotation {

    private:
        Annotations* atomicEventsAnnotations;
        Annotations* atomicEventsForCvatAnnotations;
        Annotations* atomicEventsForManualAnnotations;
        Annotations* complexEventsAnnotations;
        int atomicEventsCounter;
        int complexEventsCounter;

    public:

        enum SavedShotCase {
            InsideGoalArea,
            InsidePenaltyArea,
            FromOutsideArea,
            OnPenalty,
            OnFoul
        };

        // Constructor
        Annotation();

        void AddMetadata();
        void AddTrack(Track track);

        // Core method(s)
        void ExportAtomicEvents(string);
        void ExportAtomicEventsForCvatAnnotations(string);
        void ExportAtomicEventsForManualAnnotations(string);
        void ExportComplexEvents(string);
        void Export(string);

        // Interface for atomic events
        void KickingTheBall(int, string, string, double, double);
        void BallPossession(int, string, string, double, double, string, string, double, double);
        void Tackle(int, string, string, double, double, string, string, double, double);
        void BallDeflection(int, string, string, double, double);
        void BallOut(int);
        void Goal(int, string, string);
        void Foul(int, string, string);
        void Penalty(int, string, string);
        
        // Interface for complex events
        void Pass(int, int, string, string, string);
        void PassThenGoal(int, int, string, string, string);
        void FilteringPass(int, int, string, string, string);
        void FilteringPassThenGoal(int, int, string, string, string);
        void Cross(int, int, string, string, string, bool);
        void CrossThenGoal(int, int, string, string, string);
        void Tackle(int, int, string, string, string, bool);
        void SlidingTackle(int, int, string, string, string, bool);
        void Shot(int, int, string, string);
        void ShotOut(int, int, string, string);
        void ShotThenGoal(int, int, string, string);
        void SavedShot(int, int, string, string, string, string, double, double, SavedShotCase);

        // Interface for extra info
        void SecondHalf(int);
        void Goalkeeper(string, string);
        
        // Utility method(s)
        string SavedShotCaseToString(SavedShotCase sscase);
        string DoubleToString(double);
        
};