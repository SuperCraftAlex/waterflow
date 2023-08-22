import sys
import os

stdp = ""

if len(sys.argv) > 1:
  with open(sys.argv[1], "r") as f:
    txt = f.read()
  if len(sys.argv) > 2:
    stdp = sys.argv[2]
else:
  txt = sys.stdin.read()

vars = {}
funs = {} # dict<name: string, tuple<args: int, type: string, block: list<string>>>

is_float = lambda s: s.replace(".", "").isnumeric()

proci = []

def pval(s):
  global vars

  if is_float(s):
    return float(s)

  if s in vars.keys():
    return vars[s]

  return sys.float_info.min

def exec_stack(block, stack):
  global vars
  global funs

  cond = 1.0

  # sp points to the current top element in the stack
  sp = len(stack) - 1

  stack += [0.0] * (255 - len(stack))

  for inst in block:
    inst = inst.strip().split(" ")
    args = inst[1:]
    inst = inst[0]

    if inst == "sec":
      if len(args) != 0:
        print("too many arguments for sec instruction!")
        continue
      cond = True
      continue

    if inst == "clc":
      if len(args) != 0:
        print("too many arguments for clc instruction!")
        continue
      cond = False
      continue

    if inst == "puc":
      if len(args) != 0:
        print("too many arguments for puc instruction!")
        continue
      sp += 1
      stack[sp] = cond
      continue

    if inst == "poc":
      if len(args) != 0:
        print("too many arguments for poc instruction!")
        continue
      if sp < 0:
        print("stack underflow! -> end stack-block")
        continue
      cond = float(stack[sp])
      sp -= 1
      continue

    if inst == "and":
      # cond = cond and stack
      if len(args) != 0:
        print("too many arguments for and instruction!")
        continue
      if sp < 0:
        print("stack underflow! -> end stack-block")
        continue
      cond = int(cond) == 1 and int(stack[sp]) == 1
      sp -= 1
      continue

    if inst == "or":
      # cond =q cond or stack
      if len(args) != 0:
        print("too many arguments for and instruction!")
        continue
      if sp < 0:
        print("stack underflow! -> end stack-block")
        continue
      cond = 1.0 if (int(cond) == 1 or int(stack[sp]) == 1) else 0.0
      sp -= 1
      continue

    if inst == "not":
      if len(args) != 0:
        print("too many arguments for not instruction!")
        continue
      cond = cond != 1
      continue

    if inst == "pass":
      if len(args) != 0:
        print("too many arguments for pass instruction!")
        continue
      return stack[:sp+1]

    if inst == "push":
      if len(args) != 1:
        print("invalid amount of arguments for push instruction!")
        continue
      sp += 1
      stack[sp] = pval(args[0])
      continue

    if inst == "pop":
      if len(args) != 1:
        print("invalid amount of arguments for pop instruction!")
        continue
      if not args[0] in vars.keys():
        print("cannot pop into non-existent variable: " + args[0] + "!")
        continue
      vars[args[0]] = stack[sp]
      sp -= 1
      if sp < -1:
        print("stack underflow! -> end stack-block")
        return stack[:sp+1]
      continue

    if inst == "swp":
      if len(args) != 0:
        print("too many arguments for swp instruction!")
        continue
      if sp < 1:
        print("stack underflow! -> end stack-block")
        return stack[:sp+1]
      (stack[sp-1], stack[sp]) = (stack[sp], stack[sp-1])
      continue

    if inst == "abs":
      if len(args) != 0:
        print("too many arguments for dup instruction!")
        continue
      if sp < 0:
        print("stack underflow! -> end stack-block")
        return stack[:sp+1]
      stack[sp] = abs(stack[sp])
      continue

    if inst == "dup":
      if len(args) != 0:
        print("too many arguments for dup instruction!")
        continue
      if sp < 0:
        print("stack underflow! -> end stack-block")
        return stack[:sp+1]
      stack[sp+1] = stack[sp]
      sp += 1
      continue

    if inst == "mod":
      if len(args) != 0:
        print("too many arguments for mod instruction!")
        continue
      if sp < 1:
        print("stack underflow! -> end stack-block")
        return stack[:sp+1]
      stack[sp-1] = int(stack[sp-1]) % int(stack[sp])
      sp -= 1
      continue

    if inst == "div":
      if len(args) != 0:
        print("too many arguments for div instruction!")
        continue
      if sp < 1:
        print("stack underflow! -> end stack-block")
        return stack[:sp+1]
      stack[sp-1] = int(stack[sp-1]) / int(stack[sp])
      sp -= 1
      continue

    if inst == "fdiv":
      if len(args) != 0:
        print("too many arguments for fdiv instruction!")
        continue
      if sp < 1:
        print("stack underflow! -> end stack-block")
        return stack[:sp+1]
      stack[sp-1] = stack[sp-1] / stack[sp]
      sp -= 1
      continue

    if inst == "mul":
      if len(args) != 0:
        print("too many arguments for mul instruction!")
        continue
      if sp < 1:
        print("stack underflow! -> end stack-block")
        return stack[:sp+1]
      stack[sp-1] = int(stack[sp-1]) * int(stack[sp])
      sp -= 1
      continue

    if inst == "fmul":
      if len(args) != 0:
        print("too many arguments for mul instruction!")
        continue
      if sp < 1:
        print("stack underflow! -> end stack-block")
        return stack[:sp+1]
      stack[sp-1] = stack[sp-1] * stack[sp]
      sp -= 1
      continue

    if inst == "fsub":
      if len(args) != 0:
        print("too many arguments for fsub instruction!")
        continue
      if sp < 1:
        print("stack underflow! -> end stack-block")
        return stack[:sp+1]
      stack[sp-1] = stack[sp-1] - stack[sp]
      sp -= 1
      continue

    if inst == "sub":
      if len(args) != 0:
        print("too many arguments for sub instruction!")
        continue
      if sp < 1:
        print("stack underflow! -> end stack-block")
        return stack[:sp+1]
      stack[sp-1] = int(int(stack[sp-1]) - int(stack[sp]))
      sp -= 1
      continue

    if inst == "add":
      if len(args) != 0:
        print("too many arguments for add instruction!")
        continue
      if sp < 1:
        print("stack underflow! -> end stack-block")
        return stack[:sp+1]
      stack[sp-1] = int(int(stack[sp-1]) + int(stack[sp]))
      sp -= 1
      continue

    if inst == "fadd":
      if len(args) != 0:
        print("too many arguments for fadd instruction!")
        continue
      if sp < 1:
        print("stack underflow! -> end stack-block")
        return stack[:sp+1]
      stack[sp-1] = stack[sp-1] + stack[sp]
      sp -= 1
      continue

    if inst == "call":
      if len(args) != 1:
        print("invalid amount of arguments for call instruction!")
        continue
      if not args[0] in funs.keys():
        print("cannot call undefined function!")
        continue
      if not cond == 1:
        continue
      fun = funs[args[0]]
      type = fun[1]
      if type == "!":
        stack = exec_stack(fun[2], stack[:sp+1])
        sp = len(stack) - 1
        stack += [0.0] * (255 - len(stack))
      elif type == "%":
        vars["R"] = "_"
        for i in range(fun[0]):
          if sp < 0:
            print("stack underflow! -> cant pass argument number " + str(i) + "!")
            continue
          vars["A"+str(i)] = stack[sp]
          sp -= 1
        exec(0, fun[2])
        if vars["R"] != "_":
          sp += 1
          stack[sp] = vars["R"]
      else:
        print("Unsupported function execution type!")
      continue

    if inst == "icv":
      if sp < 0:
        print("stack underflow! -> end of stack-block")
        return stack[:sp+1]
      stack[sp] = int(stack[sp])
      continue

    if inst == "fcv":
      if sp < 0:
        print("stack underflow! -> end of stack-block")
        return stack[:sp+1]
      stack[sp] = float(stack[sp])
      continue

    if inst == "dump":
      print("BOTTOM")
      for s in stack[:sp+1]:
        print(s)
      print("TOP")
      continue

    if inst == "magic":
      if len(args) != 1:
        print("invalid amount of arguments for magic instructuion!")
        continue
      val = int(args[0])
      if val == 0: # putchar
        sys.stdout.write(chr(int(stack[sp])))
        sp -= 1
      elif val == 1: # fush
        sys.stdout.flush()
      else:
        print("unimplemented magic number: " + str(val) + "!")
      continue

    print("instruction not found: " + inst + "!")

  return stack[:sp+1]

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

      if cmd == "!":
        if len(args) != 0:
          print("too many arguments for ! command!")
          continue
        exec_stack(block, [])
      elif cmd == "fun":
        if len(args) != 3:
          print("invalid amount of arguments for fun command!")
          continue
        ind0 = len(block[0]) - len(block[0].lstrip())
        funs[args[0]] = (int(args[1]), args[2], list(map(lambda x: x[ind0:], block)))
      else:
        print("command / function " + cmd + " not found!")

      block = []

    line = line.strip()
    last = line
    last_ind = ind

    cmd = last.split(" ")
    args = cmd[1:]
    cmd = cmd[0]

    if cmd == "use":
      if len(args) != 1:
        print("invalid´amount of arguments for use command!")
      qerr = args[0]
      if qerr.startswith("std/"):
        qerr = os.path.join(stdp, qerr[4:])
      if not os.path.isfile(qerr):
        print("cannot import library: " + qerr + "!")
        continue
      if not qerr in proci:
        with open(qerr, "r") as f:
          exec(0, f.read().split("\n"))
        proci.append(qerr)
      continue

    if cmd == "var":
      if len(args) != 2:
        print("invalid amount of arguments for var command!")
        continue
      if len(args[0]) < 3:
        print("variable names need to be at least 3 chars!")
        continue
      vars[args[0]] = int(args[1])
      continue

    if cmd == "while":
      # while the variable is > 0
      if len(args) != 2:
        print("invalid amount of arguments for while command!")
        continue
      if not args[0] in vars.keys():
        print("cannot execute while command with undefined variable!")
        continue
      if not args[1] in funs.keys():
        print("cannot execute while command with undefined function!")
        continue
      fun = funs[args[1]]
      if fun[0] > 0:
        print("can only use function with 0 arguments in while command!")
        continue
      if fun[1] != "!":
        print("can only use stack based functions in while command!")
        continue
      while True:
        if vars[args[0]] == 0:
          break
        stack = exec_stack(fun[2], [])
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
        stack = exec_stack(fun[2], [])
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
        stack = exec_stack(fun[2], list(map(lambda x: vars[x] if x in vars.keys() else float(x), args)))
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

    if i+1 < len(lines):
      nl = lines[i+1]
      nind = len(nl) - len(nl.lstrip())

      if nind == ind:
        print("command not found: " + cmd + "!")

  if len(block) > 0:
    blocki = len(block[0]) - len(block[0].lstrip())
    cmd = last.split(" ")
    args = cmd[1:]
    cmd = cmd[0]

    if cmd == "!":
      if len(args) != 0:
        print("too many arguments for ! command!")
        return
      exec_stack(block, [])
    elif cmd == "fun":
      if len(args) != 3:
        print("invalid amount of arguments for fun command!")
        return
      ind0 = len(block[0]) - len(block[0].lstrip())
      funs[args[0]] = (int(args[1]), args[2], list(map(lambda x: x[ind0:], block)))
    else:
      print("command / function " + cmd + " not found!")

    block = []

exec(0, txt.split("\n"))
