/*
 * scpiInterpreter.h
 *
 *  Created on: 30.03.2012
 *      Author: Felix Bachmair
 */

#ifndef SCPIINTERPRETER_H_
#define SCPIINTERPRETER_H_

#include <string>
#include <vector>
#include <set>
#include <iostream>
#include <stdio.h>
#include <stdlib.h>
#include <algorithm>
#include <stdio.h>
#include <ctype.h>
#include <cctype> // for toupper
class scpiInterpreter {
public:
	enum comandType{CMD_COMMAND =0,CMD_QUESTION = 1,CMD_ANSWER =2};
	struct scpiPacket{
		std::vector<std::string> path;
		comandType type;
		std::string command;
		bool valid;
		void Print(){
			std::cout<<"PRINT PACKET:"<<std::endl;
			for(unsigned int i=0;i<path.size();i++){
				std::cout<<i+1<<"\t"<<path.at(i)<<std::endl;
			}
			std::cout<<"command:"<<command<<std::endl;
			if(!valid) std::cout<<"Packet is NOT  Valid"<<std::endl;
			std::cout<<"DONE"<<std::endl;
		}
	};
	scpiInterpreter();
	virtual ~scpiInterpreter();
	scpiPacket interpreteData(std::string data);//,commandType &type,std::string &command);
private:
	std::vector<std::string> interpretePath(std::string data);//,commandType &type,std::string &command);
	std::string interpreteWord(std::string word);
	scpiInterpreter::comandType interpreteType(std::string type);
	std::string toHigher(std::string in);
	std::set<std::string> directory;
	bool verbosity;
	scpiPacket currentPacket;
public:
	bool hasCommandOnPlace(std::string cmd,unsigned int place);
	bool currentType(comandType type){return currentPacket.type==type;};
	bool isQuestion(){return currentPacket.type==CMD_QUESTION;}
	bool isAnswer(){return currentPacket.type ==CMD_ANSWER;}
	bool isCommand(){return currentPacket.type == CMD_COMMAND;}
	std::string getComand(){return currentPacket.command;};
	bool isEmptyCommand(){return currentPacket.command=="";}
	bool checkComand(std::string cmd){return getComand().find(cmd)!=std::string::npos;}
	bool getFloat(float &answer);
	bool getInteger(int &answer);
	unsigned int commandLength(){return (currentPacket.path.size());};
};

#endif /* SCPIINTERPRETER_H_ */
