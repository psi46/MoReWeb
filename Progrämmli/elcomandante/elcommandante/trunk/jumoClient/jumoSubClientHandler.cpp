/*
 * subClientHandler.cpp
 *
 *  Created on: 27.02.2012
 *      Author: Felix Bachmair
 */

#include "jumoSubClientHandler.h"

using namespace std;

jumoSubClientHandler::jumoSubClientHandler(std::string name,std::string address):subClientHandler(name){
	jumo.setDevice(address);
	verbosity =false;
	setPointTemp = 17.;
	targetTemp=setPointTemp;
	//jumo.setTargetTemperature(targetTemp);
	deltaTMax=0.5;
	stableSince=2147483647;
	secondsForStable =30;
	nMeanTemp=5;
	maxHum = 30;
	autoOutput =false;//false;
	this->isStable=false;
	currentHum =100;
	isDry=false;
	isRunning=true;
	section=0;
	maxStartHum=10;
	status =WAITING;
	nCycles = 0;
	cycleHighTemp = 17.0;
	cycleLowTemp = -15.0;
	sendAboName="/jumo";
	MAXTEMP =30;
	MINTEMP = -25;
}

jumoSubClientHandler::~jumoSubClientHandler(){

}

bool jumoSubClientHandler::analyseData(packetData_t data)
{
	if(data.data.size()==0)
		return false;

	if(data.aboName.find(sendAboName)==string::npos)//todo allow other subscribtions?
		return (0);
	std::string command="";
	interpret.interpreteData(data.data);
	if (interpret.isAnswer())
		return (1);
	string aboData =data.data;

	/*
	 * CLIENT
	 */
	if(interpret.hasCommandOnPlace("CLIENT",0)){
		analyseClient();
	}
	/*
	 * PROGRam
	 */
	else if(interpret.hasCommandOnPlace("PROG",0)){
		analyseProgram();
	}
	/*
	 * MEASURE
	 */
	else if(interpret.hasCommandOnPlace("MEASURE",0)){
		analyseMeasure();
	}
	/*
	 * HELP
	 */
	else if(interpret.hasCommandOnPlace("HELP",0) && interpret.isQuestion() )
	{
		cout<<"HELP"<<endl;
		printHelp();
	}

	return 1;
}

void jumoSubClientHandler::analyseClient(){
	if(interpret.hasCommandOnPlace("OUTPUT",1)){
		if(interpret.isCommand()){
			if(interpret.checkComand("AUTO")){
				this->autoOutput=true;
			}
			else if(interpret.checkComand("MAN")){
				this->autoOutput=false;
			}
		}
	}
	stringstream out;
	out<<":CLIENT:OUTPUT! ";
	if(autoOutput)
		out<<"AUTO";
	else
		out<<"MANUAL";
	cout<<out.str()<<endl;
	this->sendToServer(sendAboName,out.str());
}

void jumoSubClientHandler::analyseCycleCommands(){
	cout<<"ANALYSE CYCLE COMMANDS "<<interpret.commandLength()<<endl;
	cout<<"  "<<interpret.getComand()<<endl;
	if (interpret.commandLength()==2&&interpret.isCommand()){
			cout<<"CYCLE"<<endl;
			nCycles = extractProgramNumber(interpret.getComand());
			startCycle(nCycles);
			cout<<"startstart"<<endl;
	}
	else if (interpret.hasCommandOnPlace("HIGHTEMP",2) && interpret.commandLength()==3){
		cout<<"HIGHTEMP"<<endl;
		cout<<"Question: "<<interpret.isQuestion()<<endl;
		cout<<"Answer: "<<interpret.isAnswer()<<endl;
		cout<<"command: "<<interpret.isCommand()<<endl;
		if(interpret.isCommand()){
			float highTemp;
			bool retVal=interpret.getFloat(highTemp);
			cout<<retVal<<" "<<highTemp<<"degC"<<endl;
			if(retVal)
				setCycleHighTemp(highTemp);
			else
				cout<<"HighTemp string could not be converted to float: "<<endl;
			cout<<"highhigh"<<endl;
		}
		sendCycleHighTemp();

	}
	else if (interpret.hasCommandOnPlace("LOWTEMP",2)){
		cout<<"LOWTEMP"<<endl;
		if(interpret.isQuestion()&&interpret.commandLength()==3){
			sendCycleLowTemp();
		}
		else if(interpret.isCommand()){
			float lowTemp;
			if(interpret.getFloat(lowTemp))
				setCycleLowTemp(lowTemp);
			else
				cout<<"LowTemp string could not be converted to float"<<endl;
			sendCycleLowTemp();
			cout<<"lowlow"<<endl;
		}
	}
}
void jumoSubClientHandler::analyseProgram(){

	if(interpret.hasCommandOnPlace("START",1)){
		int programNo=extractProgramNumber(interpret.getComand());
		cout<<"Start with ProgramNo "<<programNo<<endl;
		if(programNo<0||interpret.isEmptyCommand()){
			cout<<"start Last program"<<endl;
			jumo.startLastProgram();
		}
		else{
			cout<<"Start Program No "<<programNo<<endl;;
			jumo.startProgram(programNo);
		}
		sendJumoStatus();
		sendProgramNumber();
	}
	else if(interpret.hasCommandOnPlace("CYCLE",1))
		analyseCycleCommands();
	else if(interpret.hasCommandOnPlace("SEC",1)){
		if(interpret.hasCommandOnPlace("START",2)){
			int secNo = extractProgramNumber(interpret.getComand());
			jumo.startSection(secNo);
		}
	}
	else if(interpret.hasCommandOnPlace("CAT",1)){
		//todo
	}
	else if(interpret.hasCommandOnPlace("TEMP",1)){
		if(interpret.isCommand()){
			float temp;
			if(interpret.getFloat(temp)){
				setSetPointTemperature(temp);
			}
		}
		sendTargetTemp();
	}
	else if(interpret.hasCommandOnPlace("EXIT",1)){
		if(interpret.isCommand()){
			stopAllMeasurments();
		}
		this->killClient();
	}
	/*else{
		int programNumber=extractProgramNumber(interpret.getComand());
		if(programNumber >=0&&programNumber<=50)
		jumo.setProgramNumber(programNumber);
		sendProgramNumber();
		}*/
	else if(interpret.hasCommandOnPlace("NEXT",1)){
		jumo.nextStep();
		sleep(1);
	}
	else if(interpret.hasCommandOnPlace("PAUSE",1)){
		jumo.pauseProgram();
	}
	else if(interpret.hasCommandOnPlace("STOP",1)){
		changeStatus(WAITING);
		jumo.stopProgram();
	}
	else if(interpret.hasCommandOnPlace("CANCEL",1)){
		this->stopAllMeasurments();
	}
	else if(interpret.currentType(scpiInterpreter::CMD_QUESTION)){
		if (interpret.hasCommandOnPlace("STAT",1)){
			if(interpret.hasCommandOnPlace("TARGETTEMP",2))
				sendTargetTemp();
			sendJumoStatus();
		}
		else if(interpret.hasCommandOnPlace("HELP",1)){
			sendToServer(sendAboName,getProgHelp());
		}
		else if(interpret.hasCommandOnPlace("NUM",1)){
			sendProgramNumber();
		}
	}
	else if(interpret.hasCommandOnPlace("HEAT",1)){
		this->startHeating();
	}

}

void jumoSubClientHandler::analyseMeasure(){
	if(interpret.hasCommandOnPlace("HUMIDITY",1)){
		if(interpret.commandLength()==2&&interpret.isQuestion())
			sendHumidity();
		else{

			if (interpret.hasCommandOnPlace("START",2)){
				if(interpret.isCommand()){
					float maxStartHum;
					if(interpret.getFloat(maxStartHum))
						this->maxStartHum=maxStartHum;
				}
				sendMaxStartHum();
			}
			else if (interpret.hasCommandOnPlace("MAX",2)){
				if(interpret.isCommand()){
					float maxHum;
					if(interpret.getFloat(maxHum))
						this->maxHum=maxHum;
				}
				sendMaxHum();
			}
		}
	}
	else if(interpret.hasCommandOnPlace("TEMPERATURE",1)){
		if(interpret.commandLength()==2&&interpret.isQuestion())
			sendTemperature();
		else if(interpret.hasCommandOnPlace("DELTA",2)){
			if(interpret.isCommand()){
				float deltaTmax=1;
				if(interpret.getFloat(deltaTmax))
					this->deltaTMax=deltaTmax;
			}
			sendDeltaTMax();
		}
		else if(interpret.hasCommandOnPlace("DELTA",2)){
			if(interpret.isCommand()){
				int time=1;
				if(interpret.getInteger(time))
					this->secondsForStable=time;
			}
			sendTimeForStable();
		}
	}
}

int jumoSubClientHandler::extractProgramNumber(std::string data){
	if(data.size()==0||data==" "){
		return (-1);
	}
	int programNo = atoi(data.c_str());
	cout<<"Extract ProgramNo: "<<programNo<<endl;

	if(programNo>=0&&programNo<50)
		return (programNo);
	return (-1);
}

void jumoSubClientHandler::repeatedActions(){
	measureConditions();
	if(autoOutput) sendJumoStatus();
}

void jumoSubClientHandler::measureConditions(){
	float temp,hum,dewPoint;
	jumo.measure(temp,hum);
	dewPoint = jumo.calculateDewPoint(temp,hum);
	std::ostringstream out;
	out << temp;
	this->sendToServer("/temperature/jumo",out.str());
	out.clear();
	out.str("");
	out<<hum;
	currentHum = hum;
	this->sendToServer("/humidity",out.str());
	out.clear();
	out.str("");
	out<<dewPoint;
	this->sendToServer("/dewPoint",out.str());
	checkIfTempStable(temp);
	checkHumidity(hum);
	checkStatus();
}

void jumoSubClientHandler::checkHumidity(float hum){
	switch(status){
	case WAITING:isDry=false;break;
	case DRYING:if(hum<maxStartHum){changeStatus(COOLING);jumo.nextStep();cout<<"NEXT STEP"<<endl;sleep(1);changeStatus(COOLING);};break;
	case CYCLE_DRYING:if(hum<maxStartHum){changeStatus(CYCLE_COOLING);jumo.nextStep();cout<<"NEXT STEP"<<endl;sleep(1);changeStatus(CYCLE_COOLING);};break;
	case HEATING:break;
	default://COOLING,STABLE
		if(hum>maxHum){isDry=false;stopAllMeasurments();}
		break;
	}
}

void jumoSubClientHandler::checkIfTempStable(float temp){
	struct timeval tv;
	gettimeofday(&tv,NULL);
	long now = tv.tv_sec;
	long deltaTime = (long)now-(long)stableSince;
	//set temperature for channel 1
	if(isCycleStatus(status))
		targetTemp=cycleLowTemp;
	else
		targetTemp=setPointTemp;
    if(status==HEATING||status == CYCLE_HEATING||status==DRYING||status==CYCLE_DRYING||status==HEATING_FOR_COOLING){
        targetTemp = +40;
    }
	float deltaT =  fabs(temp-targetTemp);
	if(stableSince<0)deltaTime=0;
	switch(status){
		case WAITING:cout<<"waiting"<<endl;isStable=false;break;
		case DRYING :cout<<"drying"<<endl;isStable=false;break;
		case CYCLE_DRYING:cout<<"CycleDrying"<<endl;isStable=false;break;
		case HEATING:	cout<<"heating"<<endl;
				if(temp>18){jumo.nextStep();sleep(1);}
				isStable=false;break;
		case CYCLE_HEATING:	cout<<"CycleHeating"<<endl;
						if(temp>18){jumo.nextStep();sleep(1);(cout<<"end cycleHeating"<<endl);}
						isStable=false;break;
		case CYCLE_RESTART: break;//*/
		case STABLE:
			cout<<"stable"<<endl;
			this->tempValues.push_back(temp);
			if(tempValues.size()>nMeanTemp)
				tempValues.pop_front();
			if(fabs(meanTemp()-targetTemp)>deltaTMax)
				changeStatus(UNSTABLE);
			break;
		case CYCLE_STABLE:
					cout<<"Cycle stable"<<endl;
					this->tempValues.push_back(temp);
					if(tempValues.size()>nMeanTemp)
						tempValues.pop_front();
					if(fabs(meanTemp()-targetTemp)>deltaTMax)
						changeStatus(CYCLE_UNSTABLE);
					if(now-stableSince>60)
						changeStatus(CYCLE_HEATING);
					break;
		case HEATING_FOR_COOLING:
//				cout<<"Warming up for stablizing Temperature...currentTemp "<<temp<<", targetTemp: "<<setPointTemp<<endl;
				std::cout<<" coolingForHeating: ";
				std::cout<<std::setprecision(2)<<std::fixed<<std::showpos;
				std::cout<<std::setw(4)<<temp<<" - ";
				std::cout<<std::setw(4)<<setPointTemp<<" = ";
				std::cout<<std::setw(4)<<temp-setPointTemp<<" "<<std::endl;
				std::cout<<std::noshowpos;
				if(temp>setPointTemp-deltaTMax){
					cout<<"Temperature is high enough... Change to Cooling..."<<endl;
					jumo.stopProgram();
					jumo.startSection(1);
					sleep(1);
					changeStatus(COOLING);
				}
				break;
		default://COOLING,UNSTABLE
			std::cout<<" cooling / unstable: "<<setw(3)<<(int)(deltaTime<0?0:deltaTime)<<" ";
			std::cout<<std::setprecision(2)<<std::fixed<<std::showpos;
			std::cout<<std::setw(4)<<temp<<" - ";
			std::cout<<std::setw(4)<<targetTemp<<" = ";
			std::cout<<std::setw(4)<<deltaT<<" ";
			std::cout<<std::setw(4)<<deltaTMax<<std::endl;
			std::cout<<std::noshowpos;
			if ((temp < targetTemp-deltaTMax)&&!isCycleStatus(status)){
				cout<<"need to warm up for stabilzing temperature..."<<endl;
				changeStatus(HEATING_FOR_COOLING);
			}
			if(deltaT<deltaTMax){ //dry and deltaT<deltaTMax =>stableSince now/stillstable
				if(deltaTime<0||stableSince==-1){
					stableSince=now;
				}
			}
			else{//dry but temperature not small enough =>stableSince = -1
				stableSince =-1;
			}
			if(deltaTime>secondsForStable&&stableSince>0){
				if(status==COOLING||status==UNSTABLE)changeStatus(STABLE);
				else changeStatus(CYCLE_STABLE);
				sendJumoStatus();
			}
			break;
	}
}

float jumoSubClientHandler::meanTemp(){
	if(tempValues.size()<=0)
		return 99;
	float meanValue=0;
	for(unsigned int i=0;i<tempValues.size();i++)
		meanValue+=tempValues.at(i);
	meanValue/=(float)tempValues.size();
	return meanValue;
}


void jumoSubClientHandler::sendJumoStatus(){
	stringstream output;
	output<<":PROG:STAT! ";
	output<<getStatusString(status);
	this->sendToServer(sendAboName,output.str());
}

void jumoSubClientHandler::sendDeltaTMax(){
	stringstream output;
	output<<":MEASURE:TEMPERATURE:DELTA! ";
		output<<this->deltaTMax;
	this->sendToServer(sendAboName,output.str());
}

void jumoSubClientHandler::sendMaxHum(){
	stringstream output;
	output<<":MEASURE:HUMIDITY:MAX! ";
		output<<this->maxHum;
	this->sendToServer(sendAboName,output.str());
}

void jumoSubClientHandler::sendMaxStartHum(){
	stringstream output;
	output<<":MEASURE:HUMIDITY:START! ";
		output<<this->maxStartHum;
	this->sendToServer(sendAboName,output.str());
}
void jumoSubClientHandler::sendTemperature(){
	this->measureConditions();
	stringstream output;
	output<<":MEASURE:TEMPERATURE! ";
		output<<this->tempValues.front();
	this->sendToServer(sendAboName,output.str());

}

void jumoSubClientHandler::sendHumidity(){
	this->measureConditions();
	stringstream output;
	output<<":MEASURE:HUMIDITY! ";
		output<<currentHum;
	this->sendToServer(sendAboName,output.str());

}

void jumoSubClientHandler::stopAllMeasurments(){
	changeStatus(HEATING);
}

void jumoSubClientHandler::setCycleHighTemp(float highTemp){
	bool val = highTemp<MAXTEMP && highTemp>MINTEMP;
	cout<<"Set Cycle Temp HIGH : "<<highTemp<<" "<<MAXTEMP<<" "<<MINTEMP<<" "<<val<<endl;
	if(val)
		this->cycleHighTemp=highTemp;

}
void jumoSubClientHandler::setCycleLowTemp(float lowTemp){
	bool val = lowTemp<MAXTEMP && lowTemp>MINTEMP;
	cout<<"Set Cycle Temp Low : "<<lowTemp<<" "<<MAXTEMP<<" "<<MINTEMP<<" "<<val<<endl;
	if(val)
			this->cycleLowTemp=lowTemp;

}
void jumoSubClientHandler::sendCycleHighTemp(){
	stringstream output;
	output<<":PROG:CYCLE:HIGHTEMP! "<<cycleHighTemp;
	sendToServer(sendAboName,output.str());

}
void jumoSubClientHandler::sendCycleLowTemp(){
	stringstream output;
	output<<":PROG:CYCLE:LOWTEMP! "<<cycleLowTemp;
	sendToServer(sendAboName,output.str());
}

void jumoSubClientHandler::sendSetPointTemp(){
	sendTargetTemp();
}

void jumoSubClientHandler::checkStatus(){
	if(isCycleStatus(status)){
		targetTemp=cycleLowTemp;
		if(verbosity) cout<<getStatusString(status)<<" is a CycleStatus!"<<targetTemp<<endl;
	}
	else{
		targetTemp=setPointTemp;
		if(verbosity)cout<<getStatusString(status)<<" is a  normal Status!"<<targetTemp<<endl;
	}
	if (status==HEATING||status==CYCLE_HEATING){
		targetTemp=+40;
		jumo.setTargetTemperature(targetTemp);
	}
	if(status==COOLING||status==STABLE||status==CYCLE_COOLING||status==UNSTABLE){
		jumo.setTargetTemperature(targetTemp);
		if(verbosity)cout<<"Set new Temperature in Box to "<<targetTemp<<endl;
	}

	float jumoSetTemp;
	jumo.readTargetTemp(&jumoSetTemp);
	if(jumoSetTemp!=this->targetTemp){
		sendError("TargetTemp does not fit with jumo Set Temp");
	}
	int programNo;
	jumo.readProgramNo(&programNo);
	int sectionNo;
	jumo.readSectionNo(&sectionNo);
	section =sectionNo;
	if(verbosity) cout<<"SectionNo = "<<sectionNo<<endl;
	switch (sectionNo){
	case 0: 
		if(status==CYCLE_RESTART) break;
		else if(status==DRYING||status==COOLING||status==STABLE||status==UNSTABLE||status==HEATING)changeStatus(WAITING);
		else if(status==CYCLE_HEATING)changeStatus(CYCLE_RESTART);
		break;
	case 1: if(status==WAITING||status==HEATING||status==COOLING||status==STABLE||status==UNSTABLE) changeStatus(DRYING);
		if(status==CYCLE_RESTART||status==CYCLE_DRYING||status==CYCLE_STABLE||status==CYCLE_UNSTABLE||status==CYCLE_COOLING) changeStatus(CYCLE_DRYING);
		break;
	case 2: if(status==DRYING||status==WAITING)changeStatus(COOLING);
		else if(status==CYCLE_DRYING||status==CYCLE_RESTART)changeStatus(CYCLE_COOLING);
		else if(status==CYCLE_HEATING||status==HEATING||status==HEATING_FOR_COOLING){jumo.nextStep();sleep(1);}
		break;
	case 3: if(status==DRYING||status==COOLING||status==STABLE||status==UNSTABLE||status==WAITING)changeStatus(HEATING);
		else if(status==CYCLE_DRYING||status==CYCLE_COOLING||status==CYCLE_STABLE||status==CYCLE_UNSTABLE)changeStatus(CYCLE_HEATING);
		break;
	default: break;
	}
	if(status==CYCLE_RESTART){
		cout<<"STATUS == CYCLE_RESTART"<<endl;
		{
			if(nCycles>0){
				nCycles--;
				jumo.startLastProgram();
			}
			else{
				sendToServer(sendAboName,":PROG:CYCLE! FINISHED");
				changeStatus(WAITING);
			}
		}
	}

}


void jumoSubClientHandler::sendProgramNumber(){
	int programNo =-999;
	jumo.readProgramNo(&programNo);
	if(programNo>=0&&programNo<50){
		stringstream output;
		output<<":PROGRAM:NUMBER! "<<programNo;
		sendToServer(sendAboName,output.str());
	}

}

void jumoSubClientHandler::startHeating(){
	cout<<"start Heating"<<endl;
	if(status!=HEATING||status!=CYCLE_HEATING||status!=HEATING_FOR_COOLING){
		jumo.nextStep();
		sleep(1);
	}
}

void jumoSubClientHandler::setSetPointTemperature(float temp){

	if (setPointTemp-temp!=0){
		stableSince=-1;
		this->setPointTemp=temp;
		if(isCycleStatus(status))
			changeStatus(CYCLE_RESTART);
		else
			changeStatus(COOLING);
	}
	sendSetPointTemp();
}
void jumoSubClientHandler::sendTargetTemp(){
	stringstream out;
	out<<":PROG:STAT:TARGETTEMP! "<<this->setPointTemp;
	sendToServer(sendAboName,out.str());
}

void jumoSubClientHandler::sendTimeForStable(){
	stringstream out;
	out<<":MEAS:TEMP:TIME! "<<this->secondsForStable;
	sendToServer(sendAboName,out.str());
}

void jumoSubClientHandler::startCycle(int nCycle){
	nCycles=nCycle-1;
	cout<<"Start Cycle with "<<nCycles<<" Cylces"<<endl;
	changeStatus(CYCLE_RESTART);
}



/********************HELP********************************/
void jumoSubClientHandler::printHelp(){
	stringstream help;
	help<<"This is the JUMO Subsystem Client following commands are possible: \n";
	help<<getProgHelp(1)<<"\n";
	help<<getMeasureHelp(1)<<"\n";
	sendToServer(sendAboName,help.str());
	cout<<help.str()<<endl;
}
std::string jumoSubClientHandler::getProgHelp(int i){
	stringstream help;
	help<<intend(i)<<":PROG:NEXT          "<<"\n";
	help<<intend(i)<<":PROG:STARt (ProgNo)"<<"\n";
	help<<intend(i)<<":PROG:STATus?       "<<"\n";
	help<<intend(i)<<":PROG:NUMber?       "<<"\n";
	help<<intend(i)<<":PROG:PAUSe         "<<"\n";
	help<<intend(i)<<":PROG:CYCLE (nTimes)"<<"\n";
	help<<getCycleHelp(i);
	cout<<help.str()<<endl;
	return help.str();
}
std::string jumoSubClientHandler::getMeasureHelp(int i){
	stringstream help;
	help<<intend(i)<<":MEASure:TEMPerature?           "<<"\treturns current Jumo Temperature\n";
	help<<intend(i)<<":MEASure:TEMPerature:DELTA?     "<<"\treturn current MaxDeltaT for Jumo\n";
	help<<intend(i)<<":MEASure:TEMPerature:DELTA (VAL)"<<"\tsets deltaTmax to VAL\n";
	help<<intend(i)<<":MEASure:TEMPerature:TIME (VAL)"<<"\tsets time to VAL where deltaT < deltaTmax (in seconds)\n";
	help<<intend(i)<<":MEASure:TEMPerature:TIME?"<<"\treturns time where deltaT < deltaTmax (in seconds)\n";
	help<<intend(i)<<":MEASure:HUMidity?              "<<"\treturns current Jumo Humidity\n";
	help<<intend(i)<<":MEASure:HUMidity:MAX?          "<<"\treturns maximum allowed Humidtiy\n";
	help<<intend(i)<<":MEASure:HUMidity:MAX (VAL)     "<<"\tsets maximum allowed Humidtiy to VAL\n";
	cout<<help.str()<<endl;
	return help.str();
}
std::string jumoSubClientHandler::getCycleHelp(int i){
	stringstream help;
	help<<intend(i)<<":PROG:CYCLE:HIGHTEMP VAL        "<<"\tset cycle high temperature\n";
	help<<intend(i)<<":PROG:CYCLE:LOWTEMP  VAL        "<<"\tset cycle high temperature\n";
	cout<<help.str()<<endl;
	return help.str();
}
std::string jumoSubClientHandler::intend(int i){
	if(i==0)
 	       return "";
	else return"  "+intend(i-1);
}

void jumoSubClientHandler::changeStatus(jumoSubClientHandler::enumSTATUS newStatus) {
	if(this->status!=newStatus){
		cout<<" Change Status from "<<getStatusString(status)<<" to "<<getStatusString(newStatus)<<endl;
		status = newStatus;
		sendJumoStatus();
	}
}


std::string jumoSubClientHandler::getStatusString(jumoSubClientHandler::enumSTATUS status){
	stringstream output;
	switch(status){
		case WAITING:  output<<"WAITING"; break;
		case DRYING:   output<<"DRYING";  break;
		case COOLING:  output<<"COOLING"; break;
		case STABLE:   output<<"STABLE";  break;
		case UNSTABLE: output<<"UNSTABLE";break;
		case HEATING:  output<<"HEATING"; break;
		case HEATING_FOR_COOLING: output<<"HEATING_FOR_COOLING";break;
		case CYCLE_DRYING:   output<<"CYCLE_DRYING "<< nCycles;  break;
		case CYCLE_COOLING:  output<<"CYCLE_COOLING "<< nCycles; break;
		case CYCLE_STABLE:   output<<"CYCLE_STABLE "<< nCycles;  break;
		case CYCLE_UNSTABLE: output<<"CYCLE_UNSTABLE "<< nCycles;break;
		case CYCLE_HEATING:  output<<"CYCLE_HEATING "<< nCycles; break;
		case CYCLE_RESTART: output<<"CYCLE_RESTART "<< nCycles; break;
		default: 	   output<<"UNKNOWN";break;
		}
	return output.str();
}

void jumoSubClientHandler::CloseClient(){
	jumo.stopProgram();
}
