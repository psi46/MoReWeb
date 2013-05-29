LIBS = $(shell root-config --libs)
CFLAGS = $(shell root-config --cflags)
CXX = g++

TARGETS = $(basename $(shell ls *.C *.cpp *.cc *.c++ 2>/dev/null))

.PHONY: all

all: $(TARGETS)

%: %.C
	$(CXX) $(CFLAGS) -o $@ $< $(LIBS)
