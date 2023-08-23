import sys
import os
import random
import string

from stack import exec_stack
from cmd.cmd import cmds_single
from cmd.cmd import cmds_block

stdp = "std/"

filen = ""
if len(sys.argv) > 1:
  filen = sys.argv[1]
  with open(sys.argv[1], "r") as f:
    txt = f.read()
  if len(sys.argv) > 2:
    stdp = sys.argv[2]
else:
  txt = sys.stdin.read()

vars = {}
funs = {} # dict<name: string, tuple<args: int, type: string, block: list<string>>>
consts = {}

consts["__stdlib_path"] = stdp
consts["__path"] = [filen]
consts["__env"] = "I"

is_float = lambda s: s.replace(".", "").isnumeric()

proci = []

pval = lambda s: float(s) if is_float(s) else (vars[s] if s in vars.keys() else (consts[s] if s in consts.keys() else sys.float_info.min))

gen_anon_name = lambda: "__anonymus_" + ''.join(random.sample(string.ascii_lowercase, 8))

def exec(last_ind, lines):
  global vars
  global funs

  block = []
  last = ""
  for i, line in enumerate(lines):
    if line.strip().startswith(">>"):
      continue
    line = line.split(">>")[0]
    if len(line.strip()) == 0:
      continue
    ind = len(line) - len(line.lstrip())
    if ind > last_ind:
      block.append(line)
      continue

    if len(block) > 0:
      blocki = len(block[0]) - len(block[0].lstrip())
      cmd = last.strip().split(" ")
      args = cmd[1:]
      cmd = cmd[0]

      block = list(map(lambda x: x[blocki:], block))

      if cmd in cmds_block.keys():
        r = cmds_block[cmd](cmd, args, block[:], funs, vars, consts, exec_stack, exec, pval)
      else:
        if len(args) > 0 and cmd in cmds_single.keys():
          c = cmds_single[cmd]
          name = gen_anon_name()
          funs[name] = (-1, args[-1], block[:])
          c(cmd, args[:-1] + [name], funs, vars, consts, exec_stack, exec, pval)
        else:
          print("Command / function \"" + cmd + "\" not found!")

      block.clear()

    line = line.strip()
    last = line
    last_ind = ind

    cmd = line.split(" ")
    args = cmd[1:]
    cmd = cmd[0]


    if i+1 < len(lines):
      nl = lines[i+1]
      nind = len(nl) - len(nl.lstrip())

      if nind != ind and len(nl.strip()) > 0:
        continue

    if cmd in cmds_single.keys():
      r = cmds_single[cmd](cmd, args, funs, vars, consts, exec_stack, exec, pval)
      continue

    if cmd in funs.keys():
      nargs = []
      outs = []
      for arg in args:
        if arg.startswith(">"):
          outs.append(arg[1:])
          continue
        nargs.append(arg)
      args = nargs

      fun = funs[cmd]
      if fun[0] != len(args):
        print("Invalid arguments for function call " + cmd + "!")
        continue
      if fun[1] == "!":
        stack = exec_stack(fun[2], list(map(lambda x: vars[x] if x in vars.keys() else float(x), args)), pval, exec, funs, vars, consts)
        sp = len(stack) - 1
        for o in outs:
          if not o in vars.keys():
            print("cannot pop into variable: undefined variable: " + o + "!")
            continue
          if sp < 0:
            print("cannot pop into variable: stack underflow!")
            continue
          vars[o] = stack[sp]
          sp -= 1
        continue
      if fun[1] == "%":
        oldr = vars["R"] if "R" in vars.keys() else False
        vars["R"] = 0.0
        for i, arg in enumerate(args):
          vars["A"+str(i)] = pval(arg)
        exec(0, fun[2])
        if len(outs) > 0:
          if len(outs) != 1:
            print("percent functions cannot return more than one value!")
            continue
          if not outs[0] in vars.keys():
            print("cannot pop into variable: undefined variable: " + outs[0] + "!")
            continue
          vars[outs[0]] = vars["R"]
        if oldr == False:
          del vars["R"]
        else:
          vars["R"] = oldr
        continue
      print("Invalid code block type " + fun[1] + " of function " + cmd + "!")

    print("Command not found: " + cmd + "!")

  if len(block) > 0:
    blocki = len(block[0]) - len(block[0].lstrip())
    cmd = last.strip().split(" ")
    args = cmd[1:]
    cmd = cmd[0]

    block = list(map(lambda x: x[blocki:], block))

    if cmd in cmds_block.keys():
      r = cmds_block[cmd](cmd, args, block[:], funs, vars, consts, exec_stack, exec, pval)
    else:
      if len(args) > 0 and cmd in cmds_single.keys():
        c = cmds_single[cmd]
        name = gen_anon_name()
        funs[name] = (-1, args[-1], block[:])
        c(cmd, args[:-1] + [name], funs, vars, consts, exec_stack, exec, pval)
      else:
        print("Command / function \"" + cmd + "\" not found!")

    block.clear()

exec(0, txt.split("\n"))
