"""CPU functionality."""

import sys

class CPU:
    """Main CPU class."""

    def __init__(self):
        """Construct a new CPU."""
        self.registers = [0,0,0,0,0,0,0,0]
        self.ram = [0] * 256
        self.fl = [0,0,0,0,0,0,0,0]

    def load(self):
        """Load a program into memory."""

        address = 0

        with open(sys.argv[1]) as f:
            for line in f:
                string_val = line.split("#")[0].strip()
                if string_val == '':
                    continue
                v = int(string_val, 2)
                #print(v)
                self.ram[address] = v
                address += 1

    def alu(self, op, reg_a, reg_b):
        """ALU operations."""

        if op == "ADD":
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
        halted = False
        pc = 0

        ADD = 0b10100000
        SUB = 0b10100001
        MUL = 0b10100010
        DIV = 0b10100011
        MOD = 0b10100100
        INC = 0b01100101
        DEC = 0b01100110
        CMP = 0b10100111
        AND = 0b10101000
        NOT = 0b01101001
        OR = 0b10101010
        XOR = 0b10101011
        SHL = 0b10101100
        SHR = 0b10101101
        NOP = 0b00000000
        HLT = 0b00000001
        LDI = 0b10000010
        LD = 0b10000011
        ST = 0b10000100
        PUSH = 0b01000101
        POP = 0b01000110
        PRN = 0b01000111
        PRA = 0b01001000
        CALL= 0b01010000
        RET = 0b00010001
        JMP = 0b01010100
        JEQ = 0b01010101
        JNE = 0b01010110
        JGT = 0b01010111
        JLT = 0b01011000
        JLE = 0b01011001
        JGE = 0b01011010

        SP =7
        L = 5
        G = 6
        E = 7

        while not halted:
            instruction = self.ram[pc]

            if instruction == LDI: #LDI
                reg_num = self.ram[pc + 1]
                value = self.ram[pc + 2]
                self.registers[reg_num] = value
                pc += 3
            elif instruction == PRN:
                reg_num = self.ram[pc + 1]
                print(self.registers[reg_num])
                pc += 2
            elif instruction == MUL:
                reg_num_a = self.ram[pc + 1]
                reg_num_b = self.ram[pc + 2]
                self.registers[reg_num_a] *= self.registers[reg_num_b]
                pc += 3
            elif instruction == ADD:
                reg_num_a = self.ram[pc + 1]
                reg_num_b = self.ram[pc + 2]
                self.registers[reg_num_a] += self.registers[reg_num_b]
                pc += 3
            elif instruction == PUSH:
                self.registers[SP] -= 1 # Decrement the SP
                reg_num = self.ram[pc+1] # get the register numer
                val = self.registers[reg_num] # get the value of the register
                top_of_stack_addr = self.registers[SP]
                self.ram[top_of_stack_addr] = val
                pc += 2
            elif instruction == POP:
                addr = self.registers[SP]
                val = self.ram[addr]
                reg_num = self.ram[pc+1]
                self.registers[reg_num] = val
                self.registers[SP] += 1
                pc += 2
            elif instruction == CALL:
                return_addr = pc + 2
                #Push it on the stack
                self.registers[SP] -= 1
                top_of_stack_addr = self.registers[SP]
                self.ram[top_of_stack_addr] = return_addr
                #Set the pc to the subroutine addr
                reg_num = self.ram[pc+1]
                subroutine_addr = self.registers[reg_num]
                pc = subroutine_addr
            elif instruction == RET:
                #pop the return addr off the stack
                top_of_stack_addr = self.registers[SP]
                return_addr = self.ram[top_of_stack_addr]
                self.registers[SP] += 1
                #store it in the PC
                pc = return_addr
            elif instruction == CMP:
                reg_num_a = self.ram[pc + 1]
                reg_num_b = self.ram[pc + 2]
                if self.registers[reg_num_a] == self.registers[reg_num_b]:
                    self.fl[E] = 1
                elif self.registers[reg_num_a] < self.registers[reg_num_b]:
                    self.fl[L] = 1
                else:
                    self.fl[G] = 1
                pc += 3
            elif instruction == JMP:
                reg_num = self.ram[pc + 1]
                val = self.registers[reg_num]
                pc = val
            elif instruction == JEQ:
                reg_num = self.ram[pc + 1]
                val = self.registers[reg_num]
                if self.fl[E] == 1:
                    pc = val
                else:
                    pc += 2
            elif instruction == JNE:
                reg_num = self.ram[pc + 1]
                val = self.registers[reg_num]
                if self.fl[E] == 0:
                    pc = val
                else:
                    pc += 2
            elif instruction == HLT:
                halted = True
            else:
                print(f'unknown instruction {instruction} at address {pc}')
                sys.exit(1)
