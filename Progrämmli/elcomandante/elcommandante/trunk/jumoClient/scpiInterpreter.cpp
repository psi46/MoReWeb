/*
 * scpiInterpreter.cpp
 *
 *  Created on: 30.03.2012
 *      Author: Felix Bachmair
 */

#include "scpiInterpreter.h"
using namespace std;
scpiInterpreter::scpiInterpreter() {
	// TODO Auto-generated constructor stub

	directory.insert("HELP");//HELP

	directory.insert("PROG");//PROGram

	directory.insert("STAT");//STATus STATe
	directory.insert("SET"); //SET
	directory.insert("STAR");//STARt
	directory.insert("NEXT");//NEXT
	directory.insert("STOP");//STOP
	directory.insert("CANCEL");//CANCEL
	directory.insert("RANG");
	directory.insert("NUM");//NUMber
	directory.insert("TARGETTEMP");//TargetTemperature
	directory.insert("SEC");//SECtion
    directory.insert("EXIT");

	directory.insert("CLIENT");//CLIENT
	directory.insert("OUT");//OUTput

	directory.insert("MEAS");//MEASure
	directory.insert("TEMP");//TEMPerature
	directory.insert("HUM");//HUMidity
	directory.insert("MAX");//MAXimum
	directory.insert("DELTA");//DELTA
	directory.insert("TIME");
	directory.insert("CYCLE");
	directory.insert("LOWTEMP");
	directory.insert("HIGHTEMP");
	directory.insert("HEAT");
	verbosity=false;
}

scpiInterpreter::~scpiInterpreter() {
	// TODO Auto-generated destructor stub
}


std::string scpiInterpreter::toHigher(std::string in){
    transform(in.begin(), in.end(), in.begin(), (int(*)(int))toupper);
//	std::transform(in.begin(),in.end(),in.begin(),std::toupper);
	return in;
}
std::vector<std::string> scpiInterpreter::interpretePath(std::string data){//,commandType &type,std::string &command){
	size_t found;
	vector<string> output;
	found = data.find_first_of(":");
	bool foundLast=false;
	bool isValid =true;
	while (found!=string::npos&&!foundLast){
		size_t foundNext = data.find_first_of(":",found+1);
		if(foundNext!=string::npos){
			string out = data.substr(found+1,foundNext-found-1);
			out = interpreteWord(out);
			if(verbosity)cout<<out<<endl;
			if(out!=""){
				output.push_back(out);
				if(verbosity)cout<<output.size()<<" "<<out<<endl;
			}
			else
				isValid =false;
		}
		else{
			size_t foundNext = data.find_first_of(" ?!",found+1);
			foundLast=true;
			string out = data.substr(found+1,foundNext-found-1);
			out = interpreteWord(out);
			if(out!="")
				output.push_back(out);
			else
				isValid =false;
		}
		found=foundNext;
	}
	if(!isValid||output.size()==0)
		output.push_back("");
	return output;
}
scpiInterpreter::scpiPacket scpiInterpreter::interpreteData(std::string data){//,commandType &type,std::string &command){

	scpiPacket packet;
	packet.valid=false;
	if(data.size()==0)
		return packet;
	size_t found;
	vector<string> output;
	data = data +" ";
	found = data.find_first_of(" !?");
	output = interpretePath(data.substr(0,found));
	string type = data.substr(found,1);
	packet.type = interpreteType(type);
	found++;
	if(found!=string::npos)
		packet.command=data.substr(found);
	else packet.command="";
	if (packet.command==" ")packet.command="";
	if(verbosity)std::cout<<"COMMAND"<<packet.command<<" "<<flush;
	packet.path=output;
	packet.valid = !(output.back()=="");
	if(verbosity)packet.Print();

	if(verbosity)cout<<"return packet"<<endl;
	currentPacket = packet;
	return currentPacket;
}

std::string scpiInterpreter::interpreteWord(std::string word)
{
//	cout<<"interprete word: \""<<word<<"\"->\""<<flush;
	word = toHigher(word);
//	cout<<word<<"\""<<endl;
	bool found =false;
	size_t pos=0;
	set<string>::iterator it;
	while (!found && pos<=word.size()){
		string 	wanted = toHigher(word.substr(0,pos));
		it=directory.find(wanted);
//		cout<<"search for: "<<wanted<<endl;
		if(it!=directory.end())
			found=true;
		else
			pos++;
	}
	if(found){
		if(verbosity)cout<<word<<"-->"<<*it<<endl;
		return *it;
	}
	else
		if(verbosity)cout<<word<<" not found in directory"<<endl;
	return "";
}


scpiInterpreter::comandType scpiInterpreter::interpreteType(std::string type){
	if(verbosity)	cout<<"interpreteType: \""<<type<<"\""<<endl;
	if(type=="?")
		return CMD_QUESTION;
	else if(type=="!")
		return CMD_ANSWER;
	else
		return CMD_COMMAND;
}

bool scpiInterpreter::hasCommandOnPlace(std::string command, unsigned int place){
	if (currentPacket.path.size()>place){
		if(interpreteWord(command)==currentPacket.path.at(place))
			return true;
		else return false;
	}
	return false;
}


bool scpiInterpreter::getFloat(float &answer){
	if(isEmptyCommand())
		return false;
	float value = atof(this->getComand().c_str());
	//cout<<"Interprete "<<getComand()<<" as a Float: "<<value;
	answer =value;
	return true;//todo check if value is reasonable...
}

bool scpiInterpreter::getInteger(int &answer){
	if(isEmptyCommand())
		return false;
	float value = atoi(this->getComand().c_str());
	//cout<<"Interprete "<<getComand()<<" as a Float: "<<value;
	answer =value;
	return true;//todo check if value is reasonable...
}
