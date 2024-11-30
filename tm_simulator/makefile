# Define Python and script name
PYTHON = python3
SCRIPT = tm_simulator.py

# Input and definition files
TM_DEFINITION = tm_definition.txt
TM_INPUT = tm_input.txt

# Default target (runs the Python script with the tm_definition and tm_input)
all: run

# Run the tm_simulator.py script with the given tm_definition and tm_input files
run:
	$(PYTHON) $(SCRIPT) $(TM_DEFINITION) $(TM_INPUT)

# Clean target (optional, add any cleaning steps if needed, like removing output files)
clean:
	rm -f output.txt
