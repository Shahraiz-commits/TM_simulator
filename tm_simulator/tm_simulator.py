class TuringMachine:
    def __init__(self, tm_definition, tm_input):
        self.states = []
        self.input_lines = []
        self.input_alphabet = []
        self.tape_alphabet = []
        self.initial_state = ''
        self.blank_symbol = ''
        self.final_states = []
        self.transitions = {}
        self.head_position = 0
        self.tape = []
        self.state = ''
        self.is_recognizer = False

        self.load_tm_definition(tm_definition)
        self.load_tm_input(tm_input)

    def load_tm_definition(self, tm_definition):
        with open(tm_definition, 'r') as f:
            lines = f.readlines()
        definition_started = False
        for line in lines:
            line = line.strip()
            
            # Find the line with "TM"
            if not definition_started:
                if line == "TM":
                    definition_started = True
                continue

            if definition_started:
                # Parsing the TM definition
                if len(self.states) == 0:
                    self.states = line.split(',')
                elif len(self.input_alphabet) == 0:
                    self.input_alphabet = line.split(',')
                elif len(self.tape_alphabet) == 0:
                    self.tape_alphabet = line.split(',')
                elif not self.initial_state:
                    self.initial_state = line
                elif not self.blank_symbol:
                    self.blank_symbol = line
                elif not self.final_states:
                    self.final_states = line.split(',')
                else:
                    # Parsing transitions (delta)
                    line = line.replace("(", "").replace(")", "").replace(" ", "")
                    parts = line.split(',')
                    if len(parts) == 5:
                        current_state, input_symbol, next_state, write_symbol, direction = parts
                        self.transitions[(current_state, input_symbol)] = (next_state, write_symbol, direction)
                    else:
                        print(f"Skipping malformed transition: {line}")

    def load_tm_input(self, tm_input):
        with open(tm_input, 'r') as f:
            # First line determines if it's a Recognizer or Transducer
            first_line = f.readline().strip()
            # Rest of the lines (input)
            for line in f:
                self.input_lines.append(line.strip())
        if first_line == "Recognizer":
            self.is_recognizer = True
        else:
            self.is_recognizer = False

    def step(self):
        current_symbol = self.tape[self.head_position]
        transition = self.transitions.get((self.state, current_symbol))
        if transition:
            next_state, write_symbol, direction = transition
            self.tape[self.head_position] = write_symbol
            self.state = next_state

            # Move the head
            if direction == 'R':
                self.head_position += 1
            elif direction == 'L':
                self.head_position -= 1

    def run(self, input_string):
        # Initialize the tape with the input string
        self.tape = list(input_string) + [self.blank_symbol] * 100  # Extra space for tape
        self.state = self.initial_state
        self.head_position = 0

        while self.state not in self.final_states:
            # if no transition exists for the current state-symbol pair, exit
            if not self.transitions.get((self.state, self.tape[self.head_position])):
                break
            self.step()

        # Handle the result
        if self.state in self.final_states:
            if self.is_recognizer:
                return f"{input_string} accepted"
            else:
                # For transducers, return the tape content excluding the blank symbol
                return ''.join(self.tape).strip(self.blank_symbol)
        else:
            return f"{input_string} rejected"


def simulate_tm(tm_definition, tm_input):
    tm = TuringMachine(tm_definition, tm_input)
    results = []

    for input_string in tm.input_lines:
        result = tm.run(input_string)
        results.append(result)
        # Clear the tape before moving to the next input string
        tm.tape = []
    return results


if __name__ == "__main__":
    tm_definition = "tm_definition.txt" 
    tm_input = "tm_input.txt" 

    results = simulate_tm(tm_definition, tm_input)
    for result in results:
        print(result)
