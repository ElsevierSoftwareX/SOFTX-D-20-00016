#ifdef _MSC_VER
#define _CRT_SECURE_NO_WARNINGS
#endif

#include <fstream>
#include <iostream>
#include <boost/archive/xml_iarchive.hpp>
#include <boost/archive/xml_oarchive.hpp>
#include "owner.hpp"

using namespace std;

Owner::Owner() {}
Owner::Owner(string username, string email) {

    this->username = username;
    this->email = email;   
}