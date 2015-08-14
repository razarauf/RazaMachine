#!/usr/bin/python

import sys, string, re

mem = [0]*300       # 300 words of main memory, up to a 1000 words can be allocated
mainReg = [0]*10    # 10 General registers (0-9)

def output():
  print "  PC %06.0f" % pcReg + "  Instr %06.0f" % instrReg
  for i in range(0, len(mainReg)/2):
    print "reg" + str(i) + " %06.0f" % mainReg[i] + "   reg" + str(i+5) + " %06.0f" % mainReg[i+5]

def readMem(filename):
  f = open(filename, 'r')
  for each_line in f:
    #(address,instruction, comment) = re.split(r'\s{3}', each_line)
    #addr_instr_array = re.split(r'\s{3}', each_line)
    addr_instr_array = each_line.split()
    mem[int(addr_instr_array[0])] = str(addr_instr_array[1]).strip()
  f.close()
  #mem[299] = "999999"

def cycle():
  global pcReg, mem, instrReg
  instrReg = pcReg
  #print str(instrReg) + str(mem[instrReg])
  pcReg += 1
  #if  instrReg < len(mem) and mem[instrReg] != 0:
  match = re.search(r'^(\d\d)(\d)(\d*)', mem[instrReg])
  if match:
    opCode = match.group(1)
    reg = int(match.group(2))
    memAddr = int(match.group(3))
    #print match.group(1) + ', ' + match.group(2) + ', ' + match.group(3)
    
    if opCode == "00":
      #000000  Halt
      #print "HALT! " + match.group()
      return 0
    elif opCode == '01':
      #01rmmm  Load register r with contents of address mmm.
      mainReg[reg] = mem[memAddr]
    elif opCode == '02':
      #02rmmm  Store the contents of register r at address mmm.
      mem[memAddr] = mainReg[reg]
    elif opCode == '03':
      #03rnnn  Load register r with the number nnn.
      mainReg[reg] = memAddr
    elif opCode == '04':
      #04r00s  Load register r with the memory word addressed by register s.
      mainReg[reg] = int(mem[mainReg[memAddr]])
    elif opCode == '05':
      #05r00s  Add contents of register s to register r
      mainReg[reg] = int(mainReg[reg]) + int(mainReg[memAddr])
    elif opCode == '06':
      #06r00s  Sub contents of register s from register r
      mainReg[reg] = int(mainReg[reg]) - int(mainReg[memAddr])
    elif opCode == '07':
      #07r00s  Mul contents of register s from register r
      mainReg[reg] = int(mainReg[reg]) * int(mainReg[memAddr])
    elif opCode == '08':
      #08r00s  Div contents of register s from register r
      mainReg[reg] = int(mainReg[reg]) / int(mainReg[memAddr])
    elif opCode == '10':
      #100mmm  Jump to location mmm
      pcReg = memAddr
    elif opCode == '11':
      #11rmmm  Jump to location mmm if register r is zero
      if mainReg[reg] == 0:
        pcReg = memAddr
  #print mainReg

def main():
  global pcReg, instrReg, mem, mainReg
  
  readMem(sys.argv[1])
  pcReg = 100
  instrReg = 0
  
  print "Initial:"
  
  output()
  
  for i in range(pcReg, len(mem)):
    if cycle() == 0:
      break
  
  print "\nFinal:"
  
  output()

# This is the standard boilerplate that calls the main() function.
if __name__ == '__main__':
  main()
