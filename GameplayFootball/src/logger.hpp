#pragma once
#include <iostream>
#include <fstream>
#include <map>
#include <string>

// Under comment for compilation error
// TODO: evaluate how to solve this
// #include <mutex>

class Logger
{
private:
	void RenameBeforeClosing(std::string);

	std::map<std::string, std::ofstream*> openFiles;
	
	// Under comment for compilation error
	// TODO: evaluate how to solve this
	// std::mutex m;

public:
	Logger() {}    
	Logger(Logger const&);
	void operator=(Logger const&);
	
	static Logger& getInstance()
	{
		static Logger instance; // Guaranteed to be destroyed.
								// Instantiated on first use.
		return instance;
	}

	bool openFile(std::string);
	bool closeFile(std::string);
	bool writeToFile(std::string, std::string);
};
