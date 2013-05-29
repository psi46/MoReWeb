/*
 * subClientHandler.h
 *
 *  Created on: 27.02.2012
 *      Author: Felix Bachmair
 */

#ifndef JUMOSUBCLIENTHANDLER_H_
#define JUMOSUBCLIENTHANDLER_H_
#include <vector>
#include <list>
#include <deque>
#include <set>
#include "subsystem/selectable_sclient.h"
#include "jumoInterface.h"
#include <stdio.h>
#include <stdlib.h>
#include <string>
#include <iostream>
#include <sstream>
#include <stdio.h>
#include <ios>      // ::std::scientific, ::std::ios::scientific
#include <iomanip>  // ::std::resetiosflags, ::std::setprecision
#include <iostream>
#include "subsystem/subClientHandler.h"
#include "scpiInterpreter.h"
//#include "subsystem/subClientHandler.h"
#include "jumoInterface.h"
#include <time.h>
#include <sys/time.h>
#include <math.h>


class 	jumoSubClientHandler: public subClientHandler{
	//todo constructor
	enum enumSTATUS{ WAITING=1, DRYING=2,COOLING=3,STABLE=4,HEATING=5,UNSTABLE=6,HEATING_FOR_COOLING=0,
					CYCLE_DRYING=7,CYCLE_COOLING=8,CYCLE_HEATING=9,CYCLE_RESTART=10,CYCLE_STABLE=11,CYCLE_UNSTABLE=12};
public:
	jumoSubClientHandler(std::string clientName="jumoClient",std::string address="");
	virtual ~jumoSubClientHandler();
	void setVerbosity(bool verb){verbosity=verb;}
	void CloseClient();
private:
	bool isCycleStatus(enumSTATUS status){return (!(status==WAITING||status==DRYING||status==STABLE||status==HEATING||status==UNSTABLE||status==COOLING||status==HEATING_FOR_COOLING));}
	void repeatedActions();
	void measureConditions();
	void checkIfTempStable(float temp);
	void checkHumidity(float hum);
	float meanTemp();
	void sendJumoStatus();
	void sendMaxHum();
	void sendMaxStartHum();
	void sendDeltaTMax();
	void sendHumidity();
	void sendTemperature();
	void sendProgramNumber();
	void sendTargetTemp();
	void sendTimeForStable();
	void stopAllMeasurments();
	void checkStatus();
	void analyseMeasure();
	void analyseClient();
	void analyseProgram();
	void startHeating();
	void startCycle(int nCylce);
	void setSetPointTemperature(float setPointTemp);
private:
	void setCycleHighTemp(float highTemp);
	void sendCycleHighTemp();
	void sendCycleLowTemp();
	void setCycleLowTemp(float lowTemp);
	void analyseCycleCommands();
	void sendSetPointTemp();

private:
	enumSTATUS status;
	float maxStartHum;
	jumoInterface jumo;
	scpiInterpreter interpret;

	std::deque<float> tempValues;
	unsigned int nMeanTemp;
	void printHelp();
	std::string getProgHelp(int i=0);
	std::string getMeasureHelp(int i=0);
	std::string getCycleHelp(int i=0);
	static std::string intend(int i=1);
	int extractProgramNumber(std::string data);
	void changeStatus(enumSTATUS newStatus);
    std::string getStatusString(enumSTATUS status);
	bool autoOutput;
	float currentHum;
	float targetTemp;
	float deltaTMax;
	float maxHum;
	long stableSince;
	int secondsForStable;
	int section;
	int nCycles;
	float cycleHighTemp;
	float cycleLowTemp;
	float MAXTEMP,MINTEMP;
	float setPointTemp;

private:
	bool isFirstTimeDry;
	bool isStable;
	bool isDry;
	bool isRunning;
	std::string sendAboName;
	bool verbosity;
public:
	bool analyseData(packetData_t data);
};

#endif /* JUMOSUBCLIENTHANDLER_H_ */
