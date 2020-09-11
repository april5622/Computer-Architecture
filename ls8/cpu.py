"""CPU functionality."""

import sys


HLT = 0b00000001
ADD = 0b10100000
MUL = 0b10100010
LDI = 0b10000010
PRN = 0b01000111
PUSH = 0b01000101
POP = 0b01000110
CALL = 0b01010000
RET = 0b00010001

class CPU:
    """Main CPU class."""

    def __init__(self):
        """Construct a new CPU."""
        self.ram = [0] * 256 
        self.registers = [0] * 8
        self.pc = 0
        self.running = True
        self.sp = 7
        self.brandtable = {}
        self.brandtable[HLT] = self.handle_HLT
        self.brandtable[LDI] = self.handle_LDI
        self.brandtable[PRN] = self.handle_PRN
        self.brandtable[ADD] = self.handle_ADD
        self.brandtable[MUL] = self.handle_MUL
        self.brandtable[PUSH] = self.handle_PUSH
        self.brandtable[POP] = self.handle_POP
        self.brandtable[CALL] = self.handle_CALL
        self.brandtable[RET] = self.handle_RET

    def ram_read(self, index):
        return self.ram[index]

    def ram_write(self, index, value):
        self.ram[index] = value

    def HLT(self): #HALT
        self.running = False
        self.pc += 1

    def load(self):
        """Load a program into memory."""
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


    def handle_HLT(self):
        self.running = False
        self.pc += 1
    
    def handle_LDI(self):
        register_info = self.ram_read(self.pc + 1)
        value = self.ram_read(self.pc + 2)
        self.registers[register_info] = value
        self.pc += 3

    def handle_PRN(self):
        register_info = self.ram_read(self.pc + 1)
        print(self.registers[register_info])
        self.pc += 2

    def handle_ADD(self):
        register_info1 = self.ram_read(self.pc + 1)
        register_info2 = self.ram_read(self.pc + 2)
        self.registers[register_info1] += self.registers[register_info2]
        self.pc += 3

    def handle_MUL(self):
        register_info1 = self.ram_read(self.pc + 1)
        register_info2 = self.ram_read(self.pc + 2)
        self.registers[register_info1] *= self.registers[register_info2]
        self.pc += 3

    def handle_PUSH(self):
        given_register = self.ram_read(self.pc + 1)
        value_in_register = self.registers[given_register]
        self.registers[self.sp] -= 1
        self.ram[self.registers[self.sp]] = value_in_register
        self.pc += 2

    def handle_POP(self):
        given_register = self.ram_read(self.pc + 1)
        value_in_ram = self.ram[self.registers[self.sp]]
        self.registers[given_register] = value_in_ram
        self.registers[self.sp] += 1
        self.pc += 2

    def handle_CALL(self):
        given_register = self.ram_read(self.pc + 1)
        self.registers[self.sp] -= 1
        self.ram[self.registers[self.sp]] = self.pc + 2
        self.pc = self.registers[given_register]

    def handle_RET(self):
        self.pc = self.ram[self.registers[self.sp]]
        self.registers[self.sp] += 1


    def run(self):
        """Run the CPU."""
        while self.running:
            instruction = self.ram_read(self.pc)

            if instruction in self.brandtable:
                ir = self.brandtable[instruction]
                ir()

            else:
                print(f"Unknown instruction {bin(instruction)}")
                sys.exit(1)

    