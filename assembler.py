#!/usr/bin/python

import sys, string, re

"""
--------------- Instruction Set for MM --------------
000000   hlt    Halt
01rmmm   ldr    Load register r with contents of address mmm.
02rmmm   sto    Store the contents of register r at address mmm.
03rnnn   ldn    Load register r with the number nnn.
04r00s   lfm    Load register r with the memory word addressed by register s.
05r00s   add    Add contents of register s to register r
06r00s   sub    Sub contents of register s from register r
07r00s   mul    Mul contents of register r by register s
08r00s   div    Div contents of register r by register s
100mmm   jmp    Jump to location mmm
11rmmm   jpz    Jump to location mmm if register r is zero
"""

opcodes={"hlt":"000", "ldr":"01", "sto":"02", "ldn":"03", "lfm":"04", "add":"05",
         "sub":"06", "mul":"07", "div":"08", "jmp":"100", "jpz":"11"}

registerLookup={"r0":"0","r1":"1","r2":"2","r3":"3","r4":"4","r5":"5","r6":"6",
                "r7":"7","r8":"8","r9":"9"}

keywords = ["go", "done", "loop"]

instructions = {}

memLabel = {}

hltAddr = 0

def readMem(filename, pcReg):
  global instructions, hltAddr, memLabel
  hltFlag = 0
  f = open(filename, 'r')
  for each_line in f:
    if not re.findall(r"^\s+$", each_line) :
      if hltFlag == 0: 
        tmp = processStr(each_line)
        instructions[pcReg] = tmp
        if not opcodes.get(str(tmp[0])) :
          #if label -> store in mem to address later
          memLabel[tmp[0]] = str(pcReg)
      elif hltFlag == 1:
        #end of instructions, now just memory, variable or array
        hltAddr = pcReg
        memLabel[processStr(each_line)] = str(pcReg)
      
      if each_line.strip() == "hlt" :
        hltFlag = 1
        instructions[pcReg] = processStr(each_line.strip())
      pcReg = pcReg + 1
  f.close()
  
def processStr(each_line):
  instruction = each_line.split("#")
  if "#" in each_line: tmp = instruction.pop()  
  clean_instruction = []
  instruction = " ".join(instruction).split()
  clean_instruction.extend(instruction)
  if "#" in each_line: clean_instruction.append("#"+tmp.strip())
  return clean_instruction

def analyzeInstr():
  output = []
  hltFlag = 0
  for key, value in instructions.items():
    if hltFlag == 0 :
      (hltFlag, tmp) = processEachValue(str(key), value)
      output.append(tmp)
    else:
      output.append(processMem(str(key), value))
  return output

def processEachValue(key, value):
  #getting the memory of the instruction as key and the instruction itself as the value
  #arg1[0:1]arg2[2]arg3[3:5] AKA 03 0 000
  arg1 = ""
  arg2n3 = ""
  label = ""
  comment = ""
  hltFlag = 0
   
  #print key + ": "
  
  for eachValue in value:
   #print "   " + eachValue
    if opcodes.get(eachValue):
      #opcode
      arg1 = opcodes.get(eachValue)
      if eachValue == "hlt" :
        #return (1, key + "\t" + "000000")
        hltFlag = 1
    elif eachValue.find("#") == -1:
      #not an opcode, label, or comment -> an argument or nothing...?
      arg2n3 = getArguments(eachValue)
    else:
      comment = "\t" + eachValue
      
  if label != "":
    return (hltFlag, key + "\t" + arg1+label+comment)
  else:
    return (hltFlag, key + "\t" + arg1+arg2n3+comment)
         
def getArguments (arguments):
  if arguments.find(',') != -1:
    #two arguments
    (arg1, arg2) = arguments.split(",")
    #args = arguments.split(",")
    realArg1 = getArgument(1, arg1.strip())
    realArg2 = getArgument(2, arg2.strip())
    return realArg1 + realArg2
  else:
    #one argument
    return getArgument(1, arguments)
  
def getArgument (argNum, argument):
  if registerLookup.get(argument) :
    #argument is a register
    if argNum == 1 : return registerLookup.get(argument)
    elif argNum == 2: return formatNumber(registerLookup.get(argument))
  elif argument.isdigit():
    #argument is just a number
    return formatNumber(argument)
  elif memLabel.get(argument):
    #argument is a label -> lookup in memory
    return memLabel.get(argument)    

def formatNumber (argument):
  if len(argument) == 1:
    return "00"+argument
  elif len(argument) == 2:
    return "0" + argument
  elif len(argument) == 3:
    return argument
  else:
    return "***"

def processMem(key, value):
  arg1 = ""
  arg2n3 = ""
  label = ""
  comment = ""
  hltFlag = 0
  
  for eachValue in value:
    if eachValue.isdigit():
      arg1 = eachValue
    elif eachValue.find("#") != -1 :
      comment = eachValue
    
  return key + "\t" +arg1 + "\t" + comment
    
def main():
  #global pcReg
  pcReg = 100
  
  #reading and splitting up each instruction
  readMem(sys.argv[1], pcReg)
  
  #for key,value in instructions.items():
  #  print str(key) + " " + str(value)
  
  output = analyzeInstr()
  
  for value in output:
    print value
  
# This is the standard boilerplate that calls the main() function.
if __name__ == '__main__':
  main()
