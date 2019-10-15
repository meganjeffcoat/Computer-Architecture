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
            "MUL": 0b10100010,
            "ADD": 0b10100000,
        }


    # should accept the address to read and return the value stored there
    def ram_read(self, MAR): # MAR contains the address being read or written to
        return self.ram[MAR]


    # should accept a value to write, and the address to write it to
    def ram_write(self,MAR, MDR): # MDR contains the data that WAS read or the data to write
        self.ram[MAR] = MDR


    def load(self, filename):
        """Load a program into memory."""

        # address = 0

        # with open(filename) as f:
        #     for line in f:
        #         comment_split = line.split("#")
        #         num = comment_split[0].strip()
        #         if num == '':
        #             continue
        #         elif (num[0] == '0') or (num[0] == '1'):
        #             self.ram[address] = int(num[:8], 2)
        #             address += 1
        try:
            address = 0

            with open(filename) as f:
                for line in f:
                    comment_split = line.split("#")
                    num = comment_split[0].strip()
                    try:
                        val =int(num, 2)
                    except ValueError:
                        continue

                    self.ram[address] = val
                    address +=1
        except FileNotFoundError:
            print(f"{sys.argv[0]}: {sys.argv[1]} not found")
            sys.exit(2)



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
