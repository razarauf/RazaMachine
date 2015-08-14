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

codes={"hlt":"00", "ldr":"01", "sto":"02", "ldn":"03", "lfm":"04", "add":"05", "sub":"06", 
       "mul":"07", "div":"08", "jmp":"10", "jpz":"11"}

lookup={"r0":"0","r1":"1","r2":"2","r3":"3","r4":"4","r5":"5","r6":"6","r7":"7","r8":"8","r9":"9"}

all_instructions = []

def output():
  print "  PC %06.0f" % pcReg + "  Instr %06.0f" % instrReg
  for i in range(0, len(mainReg)/2):
    print "reg" + str(i) + " %06.0f" % mainReg[i] + "   reg" + str(i+5) + " %06.0f" % mainReg[i+5]

def readMem(filename):
  f = open(filename, 'r')
  for each_line in f:
    instruction = each_line.split("#")
    if "#" in each_line:
      instruction.pop()
      
    instruction = ''.join(instruction).strip()
    instruction = " ".join(instruction.split(',')).strip()
    instruction = " ".join(instruction.split())
    all_instructions.append(instruction)
  f.close()
  
#def processStr():
  #for each_instr in all_instructions:
    

def main():
  global all_instructions
  pcReg = 100
  
  readMem(sys.argv[1])
  
  for i in all_instructions:
    print i
  
  
# This is the standard boilerplate that calls the main() function.
if __name__ == '__main__':
  main()
