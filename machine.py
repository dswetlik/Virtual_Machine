import sys
from os.path import exists

memory = [[0] * 16] * 65536
register = [[0] * 16] * 8
instructionPointer = [0] * 16
instructionRegister = [0] * 16
nzpRegister = [0] * 3


def startmachine():
    initmemory()
    initregisters()
    cmd()


def cmd():
    runBool = 1
    while runBool == 1:
        cmdIn = input(":: ")
        if cmdIn.lower() == "break":
            runBool = 0
        if cmdIn.lower()[0:4] == "load":
            load(cmdIn)
        if cmdIn.lower() == "dump":
            dump()
        if cmdIn.lower() == "registers":
            registers()
        if cmdIn.lower() == "state":
            state()
        if cmdIn.lower() == "run":
            run()


def initmemory():
    for x in range(65536):
        for y in range(16):
            memory[x][y] = 0


def initregisters():
    for x in range(8):
        for y in range(16):
            register[x][y] = 0
    for x in range(16):
        instructionPointer[x] = 0
        instructionRegister[x] = 0
    for x in range(3):
        nzpRegister[x] = 0


def run():
    programCounter = 0
    num = ""
    for x in range(16):
        num += instructionPointer[x]
    num = int(num)
    maxCounter = ((num // 512) + 1) * 512
    fetch(num)

    while(''.join(instructionRegister[0:4]) != '0000'
          and programCounter <= maxCounter):

        print(''.join(instructionRegister))

        num += 1
        for x in range(len(bin(num)[2:].zfill(16))):
            instructionPointer[x] = bin(num)[2:].zfill(16)[x]
        fetch(num)
        programCounter += 1


def fetch(num):
    for x in range(16):
        instructionRegister[x] = memory[num][x]


def load(string):
    args = string.split(" ")
    if len(args) > 3:
        print("Argument Out-Of-Bounds Exception:\nToo Many Arguments")
    if len(args) < 3:
        print("Argument Out-Of-Bounds Exception:\nToo Few Arguments")
    if len(args[1]) < 5 or args[1][len(args[1]) - 4:len(args[1])] != ".eoc":
        print("Invalid File Exception:\nFile is too small or has incorrect extension.")
    if len(args[2]) != 4:
        print("Invalid Memory Location:\nPlease use 4 hexadecimal characters 0000-FFFF")
    if exists(args[1]):
        file = open(args[1], "r")
        addr = int('0x' + args[2], base=16)
        for x in range(len(bin(addr)[2:].zfill(16))):
            instructionPointer[x] = bin(addr)[2:].zfill(16)[x]
        for line in file:
            memory[addr] = line[:16]
            addr += 1
    else:
        print("Invalid File Exception: File Does Not Exist")


def dump():
    addr = int(''.join(str(x) for x in instructionPointer), base=2)
    minMem = (addr // 512) * 512
    maxMem = ((addr // 512) + 1) * 512

    for x in range(minMem, maxMem):
        output = ""
        output += "x" + hex(x)[2:].zfill(4) + ":"
        for y in range(16):
            if y % 4 == 0:
                output += " "
            output += str(memory[x][y])
        print(output)


def registers():
    for x in range(8):
        output = ""
        output += "x" + bin(x)[2:].zfill(3) + ":"
        for y in range(16):
            if y % 4 == 0:
                output += " "
            output += str(register[x][y])
        print(output)


def state():
    print("REGISTERS")
    registers()
    print("MEMORY DUMP")
    dump()
    print("NZP")
    output = " "
    for x in range(3):
        output += str(nzpRegister[x])
    print(output)
    output = ""
    print("INSTRUCTION POINTER")
    for x in range(16):
        if x % 4 == 0:
            output+= " "
        output += str(instructionPointer[x])
    print(output)
    output = ""
    print("INSTRUCTION REGISTER")
    for x in range(16):
        if x % 4 == 0:
            output+=" "
        output += str(instructionRegister[x])
    print(output)


startmachine()

