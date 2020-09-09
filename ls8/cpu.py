"""CPU functionality."""

import sys


HLT = 0b00000001
MUL = 0b10100010
LDI = 0b10000010
PUSH = 0b01000101
POP = 0b01000110

class CPU:
    """Main CPU class."""

    def __init__(self):
        """Construct a new CPU."""
        self.ram = [0] * 256 
        self.registers = [0] * 8
        self.pc = 0
        self.running = True
        self.sp = 7

    def ram_read(self, index):
        return self.ram[index]

    def ram_write(self, index, value):
        self.ram[index] = value

    def HLT(self): #HALT
        self.running = False
        self.pc += 1

    def load(self):
        """Load a program into memory."""
        # if len(sys.argv) != 2:
        #     print("Usage: mult.ls8 filename")
        #     sys.exit(1)

        address = 0
        try:
            with open(sys.argv[1]) as f:
                for line in f:
                    # Split the current line on the # symbol
                    split_line = line.split('#')

                    code_value = split_line[0].strip() # removes whitespace and \n character
                    # Make sure that the value before the # symbol is not empty
                    if code_value == '':
                        continue

                    num = int(code_value, 2)
                    self.ram[address] = num
                    address += 1          

        except FileNotFoundError: 
            print(f"{sys.argv[1]} file not found")
            sys.exit(2)

    def alu(self, op, reg_a, reg_b):
        """ALU operations."""

        if op == "ADD":
            self.registers[reg_a] += self.registers[reg_b]
        elif op == "MUL":
            self.registers[reg_a] *= self.registers[reg_b]
        #elif op == "SUB": etc
        else:
            raise Exception("Unsupported ALU operation")

    def trace(self):
        """
        Handy function to print out the CPU state. You might want to call this
        from run() if you need help debugging.
        """

        print(f"TRACE: %02X | %02X %02X %02X |" % (
            self.pc,
            #self.fl,
            #self.ie,
            self.ram_read(self.pc),
            self.ram_read(self.pc + 1),
            self.ram_read(self.pc + 2)
        ), end='')

        for i in range(8):
            print(" %02X" % self.registers[i], end='')

        print()

    def run(self):
        """Run the CPU."""

        while self.running:
            instruction = self.ram_read(self.pc)

            if instruction == 0b10000010: # LDI R0,8, store a value in a register
                register_info = self.ram_read(self.pc + 1)
                value = self.ram_read(self.pc + 2)
                self.registers[register_info] = value
                self.pc += 3

            elif instruction == 0b01000111: # PRN R0, print register
                register_info = self.ram_read(self.pc + 1)
                print(self.registers[register_info])
                self.pc += 2

            elif instruction == 0b00000001: # HLT, HALT
                self.running = False
                self.pc += 1

            elif instruction == 10100000: # ADD
                register_info1 = self.ram_read(self.pc + 1)
                register_info2 = self.ram_read(self.pc + 2)
                self.registers[register_info1] += self.registers[register_info2]
                self.pc += 3

            elif instruction == 0b10100010: # MUL, multiply
                register_info1 = self.ram_read(self.pc + 1)
                register_info2 = self.ram_read(self.pc + 2)
                self.registers[register_info1] *= self.registers[register_info2]
                self.pc += 3

            elif instruction == 0b01000101: # PUSH
                given_register = self.ram_read(self.pc + 1)
                value_in_register = self.registers[given_register]
                self.registers[self.sp] -= 1
                self.ram[self.registers[self.sp]] = value_in_register
                self.pc += 2

            elif instruction == 0b01000110: # POP
                given_register = self.ram_read(self.pc + 1)
                value_in_ram = self.ram[self.registers[self.sp]]
                self.registers[given_register] = value_in_ram
                self.registers[self.sp] += 1
                self.pc += 2

            else:
                print(f"Unknown instruction {instruction}")
                sys.exit(1)


    