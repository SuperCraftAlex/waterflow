import sys
import os

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

def exec(last_ind, lines):
  global vars
  global funs

  block = []
  last = ""
  for i, line in enumerate(lines):
    if line.strip().startswith(">>"):
      continue
    if len(line.strip()) == 0:
      continue
    ind = len(line) - len(line.lstrip())
    if ind > last_ind:
      block.append(line)
      continue

    if len(block) > 0:
      blocki = len(block[0]) - len(block[0].lstrip())
      cmd = last.split(" ")
      args = cmd[1:]
      cmd = cmd[0]

      if cmd in cmds_block.keys():
        r = cmds_block[cmd](cmd, args, block, funs, vars, consts, exec_stack, exec, pval)
      else:
        print("Command / function \"" + cmd + "\" not found!")

      block = []

    line = line.strip()
    last = line
    last_ind = ind

    cmd = last.split(" ")
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

    if cmd == "const":
      if len(args) < 1 or len(args) > 2:
        print("invalid amount of arguments for const command!")
        continue
      if len(args[0]) < 3:
        print("constant names need to be at least 3 chars!")
        continue
      if args[0] in consts.keys():
        print("cannot redefine constants!")
        continue
      if len(args) == 2:
        consts[args[0]] = pval(args[1])
      else:
        consts[args[0]] = pval(args[1])
      continue

    if cmd == "while":
      # while the variable is > 0
      if len(args) != 2:
        print("invalid amount of arguments for while command!")
        continue
      if len(args[1]) == 1:
        continue
      if not args[1] in funs.keys():
        print("cannot execute while command with undefined function!")
        continue
      fun = funs[args[1]]
      if fun[0] > 0:
        print("can only use function with 0 arguments in while command!")
        continue
      if fun[1] == "!":
        while True:
          if pval(args[0]) == 0:
            break
          exec_stack(fun[2], [], pval, exec, funs, vars, consts)
      elif fun[1] == "%":
        while True:
          if pval(args[0]) == 0:
            break
          exec(0, fun[2])
      else:
        print("invalid function type for while command!")
      continue

    if cmd == "times":
      # if a true (=1) is on the stack, the loop breaks
      if len(args) != 2:
        print("invalid amount of arguments for times command!")
        continue
      if not args[0] in vars.keys():
        print("cannot execute times command with undefined variable!")
        continue
      if not args[1] in funs.keys():
        print("cannot execute times command with undefined function!")
        continue
      am = vars[args[0]]
      fun = funs[args[1]]
      if fun[0] > 0:
        print("can only use function with 0 arguments in times command!")
        continue
      if fun[1] != "!":
        print("can only use stack based functions in times command!")
        continue
      for i in range(int(am)):
        vars[args[0]] = i
        stack = exec_stack(fun[2], [], pval, exec, funs, vars, consts)
        if len(stack) > 0 and stack[-1] == 1:
          break
      vars[args[0]] = am
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
        continue
      print("Invalid code block type " + fun[1] + " of function " + cmd + "!")

    print("command not found: " + cmd + "!")

  if len(block) > 0:
    blocki = len(block[0]) - len(block[0].lstrip())
    cmd = last.split(" ")
    args = cmd[1:]
    cmd = cmd[0]

    if cmd in cmds_block.keys():
      r = cmds_block[cmd](cmd, args, block, funs, vars, consts, exec_stack, exec, pval)
    else:
      print("command / function " + cmd + " not found!")

    block = []

exec(0, txt.split("\n"))
