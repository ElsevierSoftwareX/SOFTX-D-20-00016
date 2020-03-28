#pragma once

#include <pugixml.hpp>

using namespace pugi;
using namespace std;

class AnnotationsLoader {

  private:
    AnnotationsLoader();
  
  public:
    static void Load(const char* filename);

};

class AnnotationsProcessor {

  private:
    AnnotationsProcessor();

  public:
    static void ProcessTrack(xml_node track);
    static void ProcessBox(xml_node box);
    static void ProcessLabel(xml_node label);
    static void ProcessSegment(xml_node segment);
    static void ProcessBoxAttribute(xml_node attribute);
    static void RemoveAttributes(xml_node node);
    static void ProcessItemTrack(xml_node item);
    static void ProcessItemBox(xml_node item);
    static void ProcessItemLabel(xml_node item);
    static void ProcessItemAttribute(xml_node item);
    static xml_node ItemToTrack(xml_node);
    static xml_node ItemToBox(xml_node);
    static xml_node ItemToLabel(xml_node);
    static xml_node ItemToSegment(xml_node);
    static xml_node ItemToVersion(xml_node);
    static xml_node ItemToAttribute(xml_node);
    static void MoveChildsToGrandparent(xml_node, const char*);

};

class AnnotationsSaver {
  
  private:
    AnnotationsSaver();

  public:
    static void Save(string filename);

};