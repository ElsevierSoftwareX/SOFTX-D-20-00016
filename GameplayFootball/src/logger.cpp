#ifdef _MSC_VER
#define _CRT_SECURE_NO_WARNINGS
#endif

#include "logger.hpp"
#include <algorithm>
#include <iomanip>
#include <sstream>
#include <ctime>
#include <cstdio>

// Under comment for compilation error
// TODO: evaluate how to solve this
// #include <mutex>

using namespace std;

bool Logger::openFile(string filename) {
	ofstream* newFile = new ofstream(filename.c_str(), ios::out);
	if (newFile->is_open()) {
		openFiles[filename] = newFile;
		return true;
	}
	else
		return false;
}

bool Logger::closeFile(string filename) {
	map<string, ofstream*>::iterator  it = openFiles.find(filename);
	if (it != openFiles.end()) {
		it->second->close();
		openFiles.erase(it);
		RenameBeforeClosing(filename);
		return true;
	}
	else
		return false;
}

bool Logger::writeToFile(string filename, string line) {	
	map<string, ofstream*>::iterator it = openFiles.find(filename);
	if (it != openFiles.end()) {	

		// Under comment for compilation error
		// TODO: evaluate how to solve this
		// std::lock_guard<std::mutex> lock(m);
		
		*openFiles[filename] << line << endl;
		return true;
	}
	else
		return false;
}

void Logger::RenameBeforeClosing(string filename) {
	time_t currentTime = time(NULL);
	ostringstream oss;
	oss << ctime(&currentTime);
	string newFilename = filename + " "  + oss.str();
	rename(filename.c_str(), newFilename.c_str());
}