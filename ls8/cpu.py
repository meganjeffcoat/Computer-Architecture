"""CPU functionality."""
#functionality, classes, constructor

import sys

class CPU:
    """Main CPU class."""

    def __init__(self):
        """Construct a new CPU."""
        self.ram = [0] * 256
        self.reg = [0] * 8
        self.pc = 0
        self.operations = {
            "LDI": 0b10000010,
            "HLT": 0b00000001,
            "PRN": 0b01000111,
            "ADD": 0b10100000,
        }


    # should accept the address to read and return the value stored there
    def ram_read(self, MAR): # MAR contains the address being read or written to
        return self.ram[MAR]


    # should accept a value to write, and the address to write it to
    def ram_write(self,MAR, MDR): # MDR contains the data that WAS read or the data to write
        self.ram[MAR] = MDR


    def load(self):
        """Load a program into memory."""

        address = 0

        # For now, we've just hardcoded a program:

        program = [
            # From print8.ls8
            0b10000010, # LDI R0,8
            0b00000000,
            0b00001000,
            0b01000111, # PRN R0
            0b00000000,
            0b00000001, # HLT
        ]

        for instruction in program:
            self.ram[address] = instruction
            address += 1


    def alu(self, op, reg_a, reg_b):
        """ALU operations."""

        if op == self.operations["ADD"]:
            self.reg[reg_a] += self.reg[reg_b]
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
            print(" %02X" % self.reg[i], end='')

        print()

    def run(self):
        """Run the CPU."""
        # needs to read memory address that's stored in register PC
        # need to store that result in IR
        # self.trace() #trace program execution
        # LDI = 0b10000010 # LDI R0,8 (register immediate, set the value of a register to an integer)
        # PRN = 0b01000111 # PRN R0 (pseudo-instruction, print numeric value stored in the given register)
        # HLT = 0b00000001 # HLT (halt the CPU, and exit the emulator)

        running = True
        while running:
            IR = self.ram[self.pc]

            operand_a = self.ram_read(self.pc + 1)
            operand_b = self.ram_read(self.pc + 2)

            if IR == self.operations["LDI"]:
                self.reg[operand_a] = operand_b
                self.pc += 3
            elif IR == self.operations["PRN"]:
                print(self.reg[operand_a])
                self.pc += 2
            elif IR == self.operations["HLT"]:
                running = False
            else:
                print(f"Unknown instruction: {self.ram[self.pc]}")
                sys.exit(1)
