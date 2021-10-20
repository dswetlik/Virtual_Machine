def decode(strReg):

    print(strReg)
    opcode = ""
    registerA = ""
    registerB = ""
    destinationRegister = ""

    if strReg[0:4] == '0000':
        opcode = "HALT"
    elif strReg[0:4] == '0001':
        opcode = "ADD"
        destinationRegister = translateregister(strReg[4:7])
        registerA = translateregister(strReg[7:10])
        if strReg[10] == '0':
            registerB = translateregister(strReg[13:16])
            print(opcode + " " + destinationRegister + " " + registerA + " " + registerB)
    elif strReg[0:4] == '0010':
        opcode = "AND"
    elif strReg[0:4] == '0011':
        opcode = "NOT"
    elif strReg[0:4] == '0100':
        opcode = "LD"
    elif strReg[0:4] == '0101':
        opcode = "LDI"
    elif strReg[0:4] == '0110':
        opcode = "LDR"
    elif strReg[0:4] == '0111':
        opcode = "ST"
    elif strReg[0:4] == '1000':
        opcode = "STI"
    elif strReg[0:4] == '1001':
        opcode = "STR"
    elif strReg[0:4] == '1010':
        opcode = "GET"
    elif strReg[0:4] == '1011':
        opcode = "PUT"
    elif strReg[0:4] == '1100':
        opcode = "BR"
    elif strReg[0:4] == '1101':
        opcode = "JMP"
    elif strReg[0:4] == '1110':
        opcode = "JMPR"
    elif strReg[0:4] == '1111':
        opcode = "RET"


def translateregister(regStr):
    regVal = "R" + str(int(regStr, base=2))
    return regVal


instructionRegister = [0,0,0,1,0,1,0,0,0,0,0,0,0,0,0,1]
strI = "".join([str(x) for x in instructionRegister])
decode(strI)
