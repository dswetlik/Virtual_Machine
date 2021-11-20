import sys
from os.path import exists

memory = [] #[[0] * 16] * 65536
register = [] #[[0] * 16] * 8
instructionPointer = []
instructionRegister = []
nzpRegister = []


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
        if cmdIn.lower()[0:8] == "assemble":
            assemble(cmdIn)
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
        memory.append([0] * 16)

def initregisters():
    for x in range(8):
        register.append([0] * 16)

    for x in range(16):
        instructionPointer.append(0)
        instructionRegister.append(0)
    for x in range(3):
        nzpRegister.append(0)


def run():
    while True:
        fetch()
        cmds = decode(''.join(instructionRegister))
        print(list(cmds))
        execute(cmds)

        if (''.join(instructionRegister[0:4]) == '0000'):
            break


def fetch():
    num = ""
    for x in range(16):
        num += instructionPointer[x]
    num = int(num, base=2)

    for x in range(16):
        instructionRegister[x] = str(memory[num][x])

    num += 1
    for x in range(len(bin(num)[2:].zfill(16))):
        instructionPointer[x] = bin(num)[2:].zfill(16)[x]


def decode(strReg):

    retStrs = []
    opcode = ""
    registerA = ""
    registerB = ""
    destinationRegister = ""

    if strReg[0:4] == '0000':
        retStrs.append("HALT")
        return retStrs
    elif strReg[0:4] == '0001':
        retStrs.append("ADD")
        retStrs.append(translateregister(strReg[4:7]))
        retStrs.append(translateregister(strReg[7:10]))
        if strReg[10] == '0':
            retStrs.append("0")
            retStrs.append(translateregister(strReg[13:16]))
        else:
            retStrs.append("1")
            retStrs.append(strReg[11:16])
        return retStrs
    elif strReg[0:4] == '0010':
        retStrs.append("AND")
        retStrs.append(translateregister(strReg[4:7]))
        retStrs.append(translateregister(strReg[7:10]))
        if strReg[10] == '0':
            retStrs.append("0")
            retStrs.append(translateregister(strReg[13:16]))
        else:
            retStrs.append("1")
            retStrs.append(strReg[11:16])
        return retStrs
    elif strReg[0:4] == '0011':
        retStrs.append("NOT")
        retStrs.append(translateregister(strReg[4:7]))
        retStrs.append(translateregister(strReg[7:10]))
        return retStrs
    elif strReg[0:4] == '0100':
        retStrs.append("LD")
        retStrs.append(translateregister(strReg[4:7]))
        retStrs.append(strReg[7:16])
        return retStrs
    elif strReg[0:4] == '0101':
        retStrs.append("LDI")
        retStrs.append(translateregister(strReg[4:7]))
        retStrs.append(strReg[7:16])
        return retStrs
    elif strReg[0:4] == '0110':
        retStrs.append("LDR")
        retStrs.append(translateregister(strReg[4:7]))
        retStrs.append(translateregister(strReg[7:10]))
        retStrs.append(strReg[10:16])
        return retStrs
    elif strReg[0:4] == '0111':
        retStrs.append("ST")
        retStrs.append(translateregister(strReg[4:7]))
        retStrs.append(strReg[7:16])
        return retStrs
    elif strReg[0:4] == '1000':
        retStrs.append("STI")
        retStrs.append(translateregister(strReg[4:7]))
        retStrs.append(strReg[7:16])
        return retStrs
    elif strReg[0:4] == '1001':
        retStrs.append("STR")
        retStrs.append(translateregister(strReg[4:7]))
        retStrs.append(translateregister(strReg[7:10]))
        retStrs.append(strReg[10:16])
        return retStrs
    elif strReg[0:4] == '1010':
        retStrs.append("GET")
        retStrs.append(translateregister(strReg[4:7]))
        retStrs.append(strReg[7])
        return retStrs
    elif strReg[0:4] == '1011':
        retStrs.append("PUT")
        retStrs.append(translateregister(strReg[4:7]))
        retStrs.append(strReg[7])
        return retStrs
    elif strReg[0:4] == '1100':
        retStrs.append("BR")
        retStrs.append(strReg[4:7])
        retStrs.append(strReg[7:16])
        return retStrs
    elif strReg[0:4] == '1101':
        if strReg[4] == '0':
            retStrs.append("JMP")
            retStrs.append("0")
        else:
            retStrs.append("JSR")
            retStrs.append("1")
        retStrs.append(strReg[7:16])
        return retStrs
    elif strReg[0:4] == '1110':
        if strReg[4] == '0':
            retStrs.append("JMPR")
            retStrs.append("0")
        else:
            retStrs.append("JSRR")
            retStrs.append("1")
        retStrs.append(translateregister(strReg[7:10]))
        retStrs.append(strReg[10:16])
        return retStrs
    elif strReg[0:4] == '1111':
        retStrs.append("RET")
        return retStrs
    else:
        print("Invalid Command Exception: Given Command Is Not Valid")


def execute(cmds):
    if cmds[0] == "ADD":
        add(cmds)
    elif cmds[0] == "GET":
        if cmds[2] == "0":
            get(cmds)
        else:
            getc(cmds)
    elif cmds[0] == "PUT":
        if cmds[2] == "0":
            put(cmds)
        else:
            putc(cmds)
    elif cmds[0] == "AND":
        andN(cmds)
    elif cmds[0] == "NOT":
        notN(cmds)
    elif cmds[0] == "LD":
        ld(cmds)
    elif cmds[0] == "ST":
        st(cmds)
    elif cmds[0] == "LDI":
        ldi(cmds)
    elif cmds[0] == "STI":
        sti(cmds)
    elif cmds[0] == "BR":
        br(cmds)
    elif cmds[0] == "JMP":
        jmp(cmds)
    elif cmds[0] == "JSR":
        jsr(cmds)
    elif cmds[0] == "RET":
        ret(cmds)


def add(cmds):
    numA = ""
    numB = ""

    for x in range(16):
        numA += str(register[int(cmds[2][1])][x])

    if cmds[3] == '0':
        for x in range(16):
            numB += str(register[int(cmds[4][1])][x])
    else:
        numB = str(cmds[4][::-1])
        for x in range(11):
            numB += numB[4]
        numB = numB[::-1]

    numA = signedInt("0b" + numA)
    numB = signedInt("0b" + numB)
    numC = numA + numB

    updatenzp(numC)

    numC = signedBin(numC, 16)[2:].zfill(16)
    for x in range(16):
        register[int(cmds[1][1])][x] = numC[x]


def andN(cmds):
    numA = ""
    numB = ""

    for x in range(16):
        numA += str(register[int(cmds[2][1])][x])

    if cmds[3] == '0':
        for x in range(16):
            numB += str(register[int(cmds[4][1])][x])
    else:
        numB = str(cmds[4][::-1])
        for x in range(11):
            numB += numB[4]
        numB = numB[::-1]

    numA = signedInt("0b" + numA)
    numB = signedInt("0b" + numB)
    numC = numA & numB
    updatenzp(numC)
    numC = signedBin(numC, 16)[2:]
    for x in range(16):
        register[int(cmds[1][1])][x] = numC[x]


def notN(cmds):
    numA = ""

    for x in range(16):
        numA += str(register[int(cmds[2][1])][x])

    numA = ~signedInt("0b" + numA)
    updatenzp(numA)
    numA = signedBin(numA, 16)[2:]
    print(numA)
    for x in range(16):
        register[int(cmds[1][1])][x] = numA[x]


def ld(cmds):
    addr = int(''.join(str(x) for x in instructionPointer), base=2)
    minMem = (addr // 512) * 512
    maxMem = ((addr // 512) + 1) * 512
    reg = int(cmds[1][1])
    offset = ""
    for x in range(9):
        offset += cmds[2][x]
    offset = signedInt("0b" + offset)
    address = offset + minMem
    mem = ""
    for x in range(16):
        register[reg][x] = memory[address][x]
        mem += str(memory[address][x])
    updatenzp(signedInt("0b" + mem))


def st(cmds):
    addr = int(''.join(str(x) for x in instructionPointer), base=2)
    minMem = (addr // 512) * 512
    maxMem = ((addr // 512) + 1) * 512
    reg = int(cmds[1][1])
    offset = ""
    for x in range(9):
        offset += cmds[2][x]
    offset = signedInt("0b" + offset)
    address = offset + minMem
    mem = ""
    for x in range(16):
        memory[address][x] = register[reg][x]


def ldi(cmds):
    addr = int(''.join(str(x) for x in instructionPointer), base=2)
    minMem = (addr // 512) * 512
    maxMem = ((addr // 512) + 1) * 512
    reg = int(cmds[1][1])
    offset = ""
    for x in range(9):
        offset += cmds[2][x]
    offset = signedInt("0b" + offset)
    address = offset + minMem
    mem = 0
    memb = ""
    for x in range(16):
        mem += memory[address][x]
    for x in range(16):
        register[reg][x] = memory[mem][x]
        memb += memory[mem][x]

    updatenzp(signedInt("0b" + memb))


def sti(cmds):
    addr = int(''.join(str(x) for x in instructionPointer), base=2)
    minMem = (addr // 512) * 512
    maxMem = ((addr // 512) + 1) * 512
    reg = int(cmds[1][1])
    offset = ""
    for x in range(9):
        offset += cmds[2][x]
    offset = signedInt("0b" + offset)
    address = offset + minMem
    mem = 0
    for x in range(16):
        mem += memory[address][x]
    for x in range(16):
        memory[mem][x] = register[reg][x]


def br(cmds):
    addr = int(''.join(str(x) for x in instructionPointer), base=2)
    minMem = (addr // 512) * 512
    maxMem = ((addr // 512) + 1) * 512

    offset = ""
    for x in range(9):
        offset += cmds[2][x]
    offset = signedInt("0b" + offset)
    address = signedBin(offset + minMem, 16)[2:]

    if(cmds[1][0] == "1" and nzpRegister[0] == 1
    or cmds[1][1] == "1" and nzpRegister[1] == 1
    or cmds[1][2] == "1" and nzpRegister[2] == 1):
        for x in range(16):
            instructionPointer[x] = address[x]


def jmp(cmds):
    addr = int(''.join(str(x) for x in instructionPointer), base=2)
    minMem = (addr // 512) * 512
    maxMem = ((addr // 512) + 1) * 512

    offset = ""
    for x in range(9):
        offset += cmds[2][x]
    offset = signedInt("0b" + offset)
    address = signedBin(offset + minMem, 16)[2:]

    for x in range(16):
        instructionPointer[x] = address[x]


def jsr(cmds):
    addr = int(''.join(str(x) for x in instructionPointer), base=2)
    minMem = (addr // 512) * 512
    maxMem = ((addr // 512) + 1) * 512

    offset = ""
    for x in range(9):
        offset += cmds[2][x]
    offset = signedInt("0b" + offset)
    address = signedBin(offset + minMem, 16)[2:]

    for x in range(16):
        register[6][x] = instructionPointer[x]
    for x in range(16):
        instructionPointer[x] = address[x]


def ret(cmds):
    for x in range(16):
        instructionPointer[x] = register[6][x]


def get(cmds):
    val = input("Enter Integer: ")
    updatenzp(int(val))

    val = signedBin(int(val), 16)[2:].zfill(16)
    reg = int(cmds[1][1])

    for x in range(16):
        register[reg][x] = int(val[x])


def getc(cmds):
    val = input("Input Character: ")
    updatenzp(ord(val))

    val = bin(ord(val))[2:].zfill(16)
    reg = int(cmds[1][1])

    for x in range(16):
        register[reg][x] = int(val[x])


def put(cmds):
    val = ""
    for x in range(16):
        val += str(register[int(cmds[1][1])][x])
    print(signedInt("0b" + val),end='')


def putc(cmds):
    val = ""
    for x in range(16):
        val += str(register[int(cmds[1][1])][x])
    val = chr(int(val, base=2))
    print(val, end='')


def translateregister(regStr):
    regVal = "R" + str(int(regStr, base=2))
    return regVal


def assemble(string):
    args = string.split(" ")
    lineC = 0
    labels = []
    labelsLines = []
    opLabels = []
    opLabelsLines = []
    translation = []
    startLocation = 0

    if len(args) > 2:
        print("Argument Out-Of-Bounds Exception:\nToo Many Arguments")
    if len(args) < 2:
        print("Argument Out-Of-Bounds Exception:\nToo Few Arguments")
    if len(args[1]) < 5 or args[1][len(args[1]) - 4:len(args[1])] != ".asl":
        print("Invalid File Exception:\nFile is too small or has incorrect extension.")
    if exists(args[1]):
        file = open(args[1], "r")
        for line in file:
            if line[0] == ';':
                continue
            spl = line.strip("\n").split("\t")
            print(len(spl))
            print(line)
            if len(spl) == 3:
                label = str(spl[0])
                opcode = str(spl[1])
                operands = spl[2].split(" ")
            elif len(spl) == 2:
                label = str(spl[0])
                opcode = str(spl[1])
            elif len(spl) == 1:
                opcode = str(line[:len(line)]).strip("\n")
            else:
                break

            print("Label: " + label)
            print("Opcode: " + opcode)
            print(list(operands))

            if label != "":
                labels.append(label)
                labelsLines.append(lineC)

            val = ""

            if opcode == '.ORIG':
                startLocation = int('0' + operands[0], base=16)
                continue
            if opcode == '.END':
                val = "0000000000000000"
            if opcode == '.SET':
                num = signedBin(int(operands[0]), 16)[2:]
                val = num
            if opcode == '.FILL':
                num = int('0' + operands[0], base=16)
                print(num)
                val = signedBin(num, 17)[3:]
            if opcode == '.ASCII':
                for c in operands[0]:
                    num = bin(ord(c))[2:].zfill(16)
                    val = num
                val = "".zfill(16)
            if opcode == '.BLOCK':
                for x in range(int(operands[0])):
                    val = "0000000000000000"


            if opcode == 'ADD':
                val += "0001"
                val += signedBin(int(operands[0][1]), 4)[3:]
                if(operands[1][0] == '#'):
                    val += signedBin(int(operands[0][1]), 4)[3:]
                    val += "1"
                    val += signedBin(int(operands[1][1:]), 5)[2:]
                else:
                    val += signedBin(int(operands[1][1]), 4)[3:]
                    if operands[2][0] == '#':
                        val += "1"
                        val += signedBin(int(operands[2][1:]), 5)[2:]
                    else:
                        val += "000"
                        val += signedBin(int(operands[2][1]), 4)[3:]
            if opcode == "AND":
                val += "0010"
                val += signedBin(int(operands[0][1]), 4)[3:]
                val += signedBin(int(operands[1][1]), 4)[3:]
                if operands[2][0] == '#':
                    val += "1"
                    val += signedBin(int(operands[2][1:]), 5)[2:]
                else:
                    val += "000"
                    val += signedBin(int(operands[2][1]), 4)[3:]
            if opcode == "NOT":
                val += "0011"
                val += signedBin(int(operands[0][1]), 4)[3:]
                val += signedBin(int(operands[1][1]), 4)[3:]
                val += "111111"
            if opcode == "LD":
                val += "0100"
                val += signedBin(int(operands[0][1]), 4)[3:]
                if operands[1][0] == 'x':
                    val += signedBin(int('0' + operands[1], base=16), 16)[9:]
                else:
                    opLabels.append(str(operands[1]))
                    opLabelsLines.append(lineC)
            if opcode == "LDI":
                val += "0101"
                val += signedBin(int(operands[0][1]), 4)[3:]
                if operands[1][0] == 'x':
                    val += signedBin(int('0' + operands[1], base=16), 16)[9:]
                else:
                    opLabels.append(str(operands[1]))
                    opLabelsLines.append(lineC)
            if opcode == "ST":
                val += "0111"
                val += signedBin(int(operands[0][1]), 4)[3:]
                if operands[1][0] == 'x':
                    val += signedBin(int('0' + operands[1], base=16), 16)[9:]
                else:
                    opLabels.append(str(operands[1]))
                    opLabelsLines.append(lineC)
            if opcode == "STI":
                val += "1000"
                val += signedBin(int(operands[0][1]), 4)[3:]
                if operands[1][0] == 'x':
                    val += signedBin(int('0' + operands[1], base=16), 16)[9:]
                else:
                    opLabels.append(str(operands[1]))
                    opLabelsLines.append(lineC)
            if opcode == "GET":
                val += "1010"
                val += signedBin(int(operands[0][1]), 4)[3:]
                val += "011111111"
            if opcode == "GETC":
                val += "1010"
                val += signedBin(int(operands[0][1]), 4)[3:]
                val += "111111111"
            if opcode == "PUT":
                val += "1011"
                val += signedBin(int(operands[0][1]), 4)[3:]
                val += "011111111"
            if opcode == "PUTC":
                val += "1011"
                val += signedBin(int(operands[0][1]), 4)[3:]
                val += "111111111"
            if opcode == "BR":
                val += "1100"
                if operands[0] == "N":
                    val += "100"
                if operands[0] == "Z":
                    val += "010"
                if operands[0] == "P":
                    val += "001"
                if operands[0] == "NZ":
                    val += "110"
                if operands[0] == "ZP":
                    val += "011"
                if operands[0] == "NP":
                    val += "101"
                if operands[0] == "NZP":
                    val += "111"
                if operands[1][0] == 'x':
                    val += signedBin(int('0' + operands[1], base=16), 16)[9:]
                else:
                    opLabels.append(str(operands[1]))
                    opLabelsLines.append(lineC)
            if opcode == "JMP":
                val += "1101000"
                if operands[0][0] == 'x':
                    val += signedBin(int('0' + operands[0], base=16), 16)[9:]
                else:
                    opLabels.append(str(operands[0]))
                    opLabelsLines.append(lineC)
            if opcode == "JSR":
                val += "1101100"
                if operands[0][0] == 'x':
                    val += signedBin(int('0' + operands[0], base=16), 16)[9:]
                else:
                    opLabels.append(str(operands[0]))
                    opLabelsLines.append(lineC)
            if opcode == "RET":
                val += "1111000000000000"
            if opcode == "HALT":
                val += "0000000000000000"

            translation.append(val)
            lineC += 1

        for i in range(len(opLabels)):
            for j in range(len(labels)):
                if opLabels[i] == labels[j]:
                    addr = labelsLines[j]
                    translation[opLabelsLines[i]] += signedBin(addr, 16)[9:]
        print(str(startLocation))
        for line in translation:
            print(line)
        print("///")
        for x in range(16):
            instructionPointer[x] = bin(startLocation)[2:].zfill(16)[x]
        for line in translation:
            print(line)
            for x in range(16):
                memory[startLocation][x] = line[x]
            startLocation += 1



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


def updatenzp(num):
    if num > 0:
        nzpRegister[0] = 0
        nzpRegister[1] = 0
        nzpRegister[2] = 1
    elif num < 0:
        nzpRegister[0] = 1
        nzpRegister[1] = 0
        nzpRegister[2] = 0
    else:
        nzpRegister[0] = 0
        nzpRegister[1] = 1
        nzpRegister[2] = 0


def binNBits(num, bits):
    str = bin(num)

    if num >= 0:
        currentBits = len(str) - 2
        bin1 = str[2:len(str)]
        bin2 = "0b"
    else:
        currentBits = len(str) - 3
        bin1 = str[3:len(str)]
        bin2 = "-0b"

    if currentBits > bits:
        raise ValueError("Not Enough Bits")

    while currentBits < bits:
        bin2 += "0"
        currentBits += 1

    bin2 += bin1
    return bin2


def signedBin(num, bits):
    if num == 0:
        return binNBits(num, bits)
    elif num > 0:
        if num >= 2**(bits - 1):
            raise ValueError("Not Enough Bits")
        return binNBits(num, bits)
    else:
        if num <= -(2**(bits - 1)):
            raise ValueError("Not Enough Bits")
        return bin(num & (2**bits - 1))


def signedInt(binNum):
    if binNum[0:2] != "0b":
        raise TypeError
    total = 0
    bin = binNum[2:]
    revBin = bin[::-1]
    if revBin[len(revBin) - 1] == "0":
        for i in range(len(revBin) - 1):
            if revBin[i] == "1":
                total += 2**i
    elif revBin[len(revBin) - 1] == "1":
        total = -2**(len(revBin) - 1)
        for i in range(len(revBin) - 1):
            if revBin[i] == "1":
                total += 2**i
    return total


startmachine()

