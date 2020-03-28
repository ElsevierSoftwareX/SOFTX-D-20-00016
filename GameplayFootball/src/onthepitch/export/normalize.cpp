#include <stdlib.h> 
#include <iostream>
#include <fstream>
#include <sstream>
#include <string>
#include <cstring>
#include <map>
#include <list>
#include <pugixml.hpp>
#include "normalize.hpp"

using namespace std;
using namespace pugi;

AnnotationsLoader::AnnotationsLoader() {}
void AnnotationsLoader::Load(const char* filename) {

    // Open the input file
    xml_document document;
    xml_parse_result result = document.load_file(filename);
    if (result) {

        // Parse the file
        stringstream nodeName;
        xml_node annotations = document.child("annotations");

        // Remove all the attributes from the node
        AnnotationsProcessor::RemoveAttributes(annotations);
        
        for(xml_node_iterator it=annotations.begin(); it!=annotations.end(); ++it) {

            // Clear and set the node name
            nodeName.str("");
            nodeName << it->name();

            if (nodeName.str() == "track") {
                AnnotationsProcessor::ProcessTrack(*it);
            } else if (nodeName.str() == "meta") {

                stringstream childName;
                xml_node child;
                for (child = it->first_child(); child; child = child.next_sibling()) {
                    childName.str("");
                    childName << child.name();

                    if (childName.str() ==  "task") {
                        map<string, string> node_attributes;
                        list<xml_node> toRemove;

                        stringstream subChildName;
                        xml_node subChild;
                        for (subChild = child.first_child(); subChild; subChild = subChild.next_sibling()) {
                            subChildName.str("");
                            subChildName << subChild.name();

                            if (subChildName.str() ==  "labels") {
                                AnnotationsProcessor::ProcessLabel(subChild);
                            } else if (subChildName.str() == "segments") {
                                AnnotationsProcessor::ProcessSegment(subChild);

                            }
                        }

                    }


                }
                
            } else if (nodeName.str() == "XMLversion") {
                AnnotationsProcessor::ItemToVersion(*it);
            }

        }

        AnnotationsProcessor::MoveChildsToGrandparent(annotations, "track");

        // Close file and continue traversal
        document.save_file(filename);

    } else {}

}

void AnnotationsProcessor::MoveChildsToGrandparent(
    xml_node grandparent, const char* parentName) {

    // Defining variable(s)
    xml_node c, parent;

    // Select the parent node searching from grandparent
    parent = grandparent.child(parentName);

    // Iterate over the childs node of the parent
    for (c = parent.first_child(); c; c = c.next_sibling()) {
        grandparent.append_copy(c);    
    }

    // Remove the parent node from grandparent since empty
    grandparent.remove_child(parent);
}

void AnnotationsProcessor::ProcessTrack(xml_node track) {

    // Define variable(s)
    long int N = 0;

    // Remove all the attributes of the node
    AnnotationsProcessor::RemoveAttributes(track);

    // Get the count number (the cardinality of the array)
    xml_node count = track.child("count");
    N = atol(count.text().get());
    track.remove_child(count);

    // Remove the item_version
    xml_node item_version = track.child("item_version");
    track.remove_child(item_version);

    // Iterate over the item (the tracks) in the array
    for (int c = 1; c <= N; c++) {
        xml_node item = track.child("item");
        if (strcmp(item.name(), "item") == 0) {
            AnnotationsProcessor::ProcessItemTrack(item);
            AnnotationsProcessor::ItemToTrack(item);   
        }
    }    
}

void AnnotationsProcessor::ProcessBox(xml_node box) {

    // Define variable(s)
    long int N = 0;

    // Remove all the attributes of the node
    AnnotationsProcessor::RemoveAttributes(box);

    // Get the count number (the cardinality of the array)
    xml_node count = box.child("count");
    N = atol(count.text().get());
    box.remove_child(count);

    // Remove the item_version
    xml_node item_version = box.child("item_version");
    box.remove_child(item_version);

    // Iterate over the item (the boxes) in the array
    for (int c = 1; c <= N; c++) {
        xml_node item = box.child("item");
        if (strcmp(item.name(), "item") == 0) {
            AnnotationsProcessor::ProcessItemBox(item);
            AnnotationsProcessor::ItemToBox(item);
        }
    }    
}

void AnnotationsProcessor::ProcessLabel(xml_node label) {

    // Define variable(s)
    list<xml_node> labels;
    long int N = 0;

    // Remove all the attributes of the node
    AnnotationsProcessor::RemoveAttributes(label);

    // Get the count number (the cardinality of the array)
    xml_node count = label.child("count");
    N = atol(count.text().get());
    label.remove_child(count);

    // Remove the item_version
    xml_node item_version = label.child("item_version");
    label.remove_child(item_version);

    // Iterate over the item (the labels) in the array
    for (int c = 1; c <= N; c++) {
        xml_node item = label.child("item");
        if (strcmp(item.name(), "item") == 0) {
            AnnotationsProcessor::ItemToLabel(item);
            AnnotationsProcessor::ProcessItemLabel(item);
        }
    }    
}

void AnnotationsProcessor::ProcessSegment(xml_node segment) {

    // Define variable(s)
    list<xml_node> segments;
    long int N = 0;

    // Remove all the attributes of the node
    AnnotationsProcessor::RemoveAttributes(segment);

    // Get the count number (the cardinality of the array)
    xml_node count = segment.child("count");
    N = atol(count.text().get());
    segment.remove_child(count);

    // Remove the item_version
    xml_node item_version = segment.child("item_version");
    segment.remove_child(item_version);

    // Iterate over the item (the segments) in the array
    for (int c = 1; c <= N; c++) {
        xml_node item = segment.child("item");
        if (strcmp(item.name(), "item") == 0) {
            AnnotationsProcessor::ItemToSegment(item);
        }
    }    
}

void AnnotationsProcessor::ProcessBoxAttribute(xml_node attribute) {

    // Define variable(s)
    list<xml_node> attributes;
    long int N = 0;

    // Remove all the attributes of the node
    AnnotationsProcessor::RemoveAttributes(attribute);

    // Get the count number (the cardinality of the array)
    xml_node count = attribute.child("count");
    N = atol(count.text().get());
    attribute.remove_child(count);

    // Remove the item_version
    xml_node item_version = attribute.child("item_version");
    attribute.remove_child(item_version);

    // Iterate over the item (the attributes) in the array
    for (int c = 1; c <= N; c++) {
        xml_node item = attribute.child("item");
        if (strcmp(item.name(), "item") == 0) {
            AnnotationsProcessor::ItemToAttribute(item);
            AnnotationsProcessor::ProcessItemAttribute(item);
        }
    }    
}

xml_node AnnotationsProcessor::ItemToTrack(xml_node item) {
    item.set_name("track");
}

xml_node AnnotationsProcessor::ItemToBox(xml_node item) {
    item.set_name("box");
}

xml_node AnnotationsProcessor::ItemToLabel(xml_node item) {
    item.set_name("label");
}

xml_node AnnotationsProcessor::ItemToSegment(xml_node item) {
    item.set_name("segment");
}

xml_node AnnotationsProcessor::ItemToVersion(xml_node item) {
    item.set_name("version");
}

xml_node AnnotationsProcessor::ItemToAttribute(xml_node item) {
    item.set_name("attribute");
}

void AnnotationsProcessor::ProcessItemTrack(xml_node it) {

    map<string, string> node_attributes;
    list<xml_node> toRemove;

    stringstream childName;
    xml_node child;
    for (child = it.first_child(); child; child = child.next_sibling()) {
        childName.str("");
        childName << child.name();

        if (childName.str() ==  "box") {
            AnnotationsProcessor::ProcessBox(child);
        } else {
            node_attributes.insert(pair<string, string>(child.name(), child.text().get()));
            toRemove.push_back(child);
        }
    }

    // Remove the child nodes different from box
    list<xml_node>::iterator c;
    for (c = toRemove.begin(); c != toRemove.end(); c++) {
        if (strcmp((*c).name(), "box") != 0)
            it.remove_child(*c);
    }

    // Put the stored child nodes as attributes
    map<string, string>::iterator mapIt;
    for (mapIt = node_attributes.begin(); mapIt != node_attributes.end(); mapIt++) {
        it.append_attribute(mapIt->first.c_str()) = mapIt->second.c_str();
    }

    AnnotationsProcessor::MoveChildsToGrandparent(it, "box");
}

void AnnotationsProcessor::ProcessItemBox(xml_node item) {

    // Define variable(s)
    map<string, string> item_attributes;
    list<xml_node> toRemove;

    // Iterate over the child nodes (storing them)
    xml_node child;
    for (child = item.first_child(); child; child = child.next_sibling()) {
        if (strcmp(child.name(), "attributes") == 0) {
            AnnotationsProcessor::ProcessBoxAttribute(child);
            continue;
        }
        item_attributes.insert(pair<string, string>(child.name(), child.text().get()));
        toRemove.push_back(child);
    }
    
    // Remove the child nodes
    list<xml_node>::iterator c;
    for (c = toRemove.begin(); c != toRemove.end(); c++) {
        item.remove_child(*c);
    }

    // Put the stored child nodes as attributes
    map<string, string>::iterator mapIt;
    for (mapIt = item_attributes.begin(); mapIt != item_attributes.end(); mapIt++) {
        item.append_attribute(mapIt->first.c_str()) = mapIt->second.c_str();
    }

    AnnotationsProcessor::MoveChildsToGrandparent(item, "attributes");
}

void AnnotationsProcessor::ProcessItemLabel(xml_node item) {

    stringstream childName;
    xml_node child;
    for (child = item.first_child(); child; child = child.next_sibling()) {
        childName.str("");
        childName << child.name();

        if (childName.str() ==  "attributes") {


            // Define variable(s)
            list<xml_node> labels;
            long int N = 0;

            // Remove all the attributes of the node
            AnnotationsProcessor::RemoveAttributes(child);

            // Get the count number (the cardinality of the array)
            xml_node count = child.child("count");
            N = atol(count.text().get());
            child.remove_child(count);

            // Remove the item_version
            xml_node item_version = child.child("item_version");
            child.remove_child(item_version);

            // Iterate over the item (the labels) in the array
            for (int c = 1; c <= N; c++) {
                xml_node itemChild = child.child("item");
                if (strcmp(itemChild.name(), "item") == 0) {
                    AnnotationsProcessor::ItemToAttribute(itemChild);
                }
            }    
            
        }
    }

    
}

void AnnotationsProcessor::ProcessItemAttribute(xml_node item) {

    // Define variable(s)
    map<string, string> item_attributes;
    list<xml_node> toRemove;

    // Iterate over the child nodes (storing them)
    xml_node child;
    for (child = item.first_child(); child; child = child.next_sibling()) {
        item_attributes.insert(pair<string, string>(child.name(), child.text().get()));
        toRemove.push_back(child);
    }
    
    // Remove the child nodes
    list<xml_node>::iterator c;
    for (c = toRemove.begin(); c != toRemove.end(); c++) {
        item.remove_child(*c);
    }

    // Put the stored child nodes as attributes
    map<string, string>::iterator mapIt;
    for (mapIt = item_attributes.begin(); mapIt != item_attributes.end(); mapIt++) {
        if (strcmp(mapIt->first.c_str(), "value") == 0) {
            item.text().set(mapIt->second.c_str());
            continue;
        }
        item.append_attribute(mapIt->first.c_str()) = mapIt->second.c_str();
    }
    
}

void AnnotationsProcessor::RemoveAttributes(xml_node node) {

    // Define variable(s)
    list<xml_attribute> toRemove;

    // Iterate over the attributes of a node and
    // put them in the toRemove list
    xml_attribute_iterator i;
    for (i = node.attributes_begin(); i != node.attributes_end(); ++i) {
        toRemove.push_back(*i);
    }

    // Remove the attributes from the node
    list<xml_attribute>::iterator a;
    for (a = toRemove.begin(); a != toRemove.end(); ++a) {
        node.remove_attribute(*a);
    }
}