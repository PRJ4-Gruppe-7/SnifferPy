SOURCES=shared.cpp main.cpp
# Added a "Addprefix" to relocate our .o files in the right directory
OBJECTS=$(addprefix ${BUILD_DIR}/,$(SOURCES:.cpp=.o))
# Added a "Addprefix" to relocate our .o files in the right directory
DEPS=$(addprefix ${BUILD_DIR}/,$(SOURCES:.cpp=.d))
EXE=prog
CXXFLAGS=-I.
LIBS=-lpthread

#Default target is host
ARCH ?= host

# Making for host
# > make ARCH=host
ifeq (${ARCH},host)
CXX=g++
BUILD_DIR=build/host
# Making a directory for our .o files called OBJ/host
OBJ_DIR =obj/host
endif

# Making for target
# > make ARCH=target
ifeq (${ARCH},target)
CXX=arm-rpizw-g++
BUILD_DIR=build/target
# Making a directory for our .o files called OBJ/target
OBJ_DIR = obj/target
endif


# Creating the directory /obj/target and host.
# Placing target in the directory /ocj
${OBJ_DIR}/$(EXE): $(DEPS) $(OBJECTS)
	mkdir -p ${OBJ_DIR}
	$(CXX) $(CXXFLAGS) -o $@ $(OBJECTS) ${LIBS}


# Rule that describes how a .d (dependency) file is created from a .cpp file
# Similar to the assigment that you just completed %.cpp -> %.o

${BUILD_DIR}/%.d: %.cpp
	mkdir -p ${BUILD_DIR}
	$(CXX) -MT$@ -MM $(CXXFLAGS) $< > $@
	$(CXX) -MT$(@:.d=.o) -MM $(CXXFLAGS) $< >> $@

${BUILD_DIR}/%.o: %.cpp ${BUILD_DIR}/%.d
	${CXX} ${CXXFLAGS} -c -o $@ $<

ifneq ($(filter -out clean format tidy ,$(MAKECMDGOALS)) ,)
-include $(DEPS)
endif


# Removes directories created earlier.
.PHONY: clean format tidy
clean:
	rm -rf obj build *.format *.tidy

format: $(SOURCES:.cpp=.format)
%.format: %.cpp
	@echo "Formatting file '$<'"...
	@clang-format -i $<
	@echo "" > $@

tidy: $(SOURCES:.cpp=.tidy)
%.tidy: %.cpp
	@echo "Tidying file '$<'"...
	@clang-tidy $< -- $(CXXFLAGS)
	@echo "" > $@
