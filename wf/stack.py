import sys
import random

try:
    import msvcrt
    getch = msvcrt.getch
except:
    import sys, tty, termios
    def _unix_getch():
        """Get a single character from stdin, Unix version"""

        fd = sys.stdin.fileno()
        old_settings = termios.tcgetattr(fd)
        try:
            tty.setraw(sys.stdin.fileno())          # Raw read
            ch = sys.stdin.read(1)
        finally:
            termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
        return ch

    getch = _unix_getch

def exec_stack(block, stack, pval, exec, funs, vars, consts):
  err = print

  cond = 1.0

  # sp points to the current top element in the stack
  sp = len(stack) - 1

  stack += [0.0] * (255 - len(stack))

  labels = {}

  eblock = enumerate(block)
  for i, inst in eblock:
    inst = inst.strip()
    if len(inst) == 0:
      continue
    if inst[0] == ':':
      labels[inst[1:]] = i

  ci = 0
  while ci < len(block):
    inst = block[ci]
    ci += 1
    if len(inst.strip()) == 0 or inst.strip()[0] == ':':
      continue

    inst = inst.strip().split(" ")
    args = inst[1:]
    inst = inst[0]

    if inst == "jmc":
      if len(args) != 1:
        err("invalid arguments for jmc instruction!")
        continue
      if not args[0] in labels.keys():
        err("cannot jump to undefined label!")
        continue
      if int(cond) == 1:
        ci = labels[args[0]]
      continue

    if inst == "assert_sp":
      if len(args) != 1:
        err("invalid arguments for assert_sp instruction!")
        continue
      if sp != int(args[0]):
        err("assert_sp failed!")
      continue

    if inst == "assert_top":
      if len(args) != 1:
        err("invalid arguments for assert_top instruction!")
        continue
      if sp < 0:
        err("assert_top failed!")
        continue
      if float(stack[sp]) != float(args[0]):
        err("assert_top failed!")
      continue

    if inst == "sec":
      if len(args) != 0:
        err("too many arguments for sec instruction!")
        continue
      cond = 1
      continue

    if inst == "clc":
      if len(args) != 0:
        err("too many arguments for clc instruction!")
        continue
      cond = 0
      continue

    if inst == "puc":
      if len(args) != 0:
        err("too many arguments for puc instruction!")
        continue
      sp += 1
      stack[sp] = cond
      continue

    if inst == "poc":
      if len(args) != 0:
        err("too many arguments for poc instruction!")
        continue
      if sp < 0:
        err("stack underflow! -> end stack-block")
        continue
      cond = int(stack[sp])
      sp -= 1
      continue

    if inst == "and":
      # cond = cond and stack
      if len(args) != 0:
        err("too many arguments for and instruction!")
        continue
      if sp < 0:
        err("stack underflow! -> end stack-block")
        continue
      cond = int(int(cond) == 1 and int(stack[sp]) == 1)
      sp -= 1
      continue

    if inst == "or":
      # cond =q cond or stack
      if len(args) != 0:
        err("too many arguments for and instruction!")
        continue
      if sp < 0:
        err("stack underflow! -> end stack-block")
        continue
      cond = 1.0 if (int(cond) == 1 or int(stack[sp]) == 1) else 0.0
      sp -= 1
      continue

    if inst == "not":
      if len(args) != 0:
        err("too many arguments for not instruction!")
        continue
      cond = int(cond != 1)
      continue

    if inst == "pass":
      if len(args) != 0:
        err("too many arguments for pass instruction!")
        continue
      break

    if inst == "push":
      if len(args) != 1:
        err("invalid amount of arguments for push instruction!")
        continue
      sp += 1
      stack[sp] = pval(args[0])
      continue

    if inst == "pop":
      if len(args) != 1:
        err("invalid amount of arguments for pop instruction!")
        continue
      if not args[0] in vars.keys():
        err("cannot pop into non-existent variable: " + args[0] + "!")
        continue
      vars[args[0]] = stack[sp]
      sp -= 1
      if sp < -1:
        err("stack underflow! -> end stack-block")
        break
      continue

    if inst == "swp":
      if len(args) != 0:
        err("too many arguments for swp instruction!")
        continue
      if sp < 1:
        err("stack underflow! -> end stack-block")
        break
      (stack[sp-1], stack[sp]) = (stack[sp], stack[sp-1])
      continue

    if inst == "abs":
      if len(args) != 0:
        err("too many arguments for dup instruction!")
        continue
      if sp < 0:
        err("stack underflow! -> end stack-block")
        break
      stack[sp] = abs(stack[sp])
      continue

    if inst == "dup":
      if len(args) != 0:
        err("too many arguments for dup instruction!")
        continue
      if sp < 0:
        err("stack underflow! -> end stack-block")
        break
      stack[sp+1] = stack[sp]
      sp += 1
      continue

    if inst == "mod":
      if len(args) != 0:
        err("too many arguments for mod instruction!")
        continue
      if sp < 1:
        err("stack underflow! -> end stack-block")
        break
      stack[sp-1] = int(stack[sp-1]) % int(stack[sp])
      sp -= 1
      continue

    if inst == "div":
      if len(args) != 0:
        err("too many arguments for div instruction!")
        continue
      if sp < 1:
        err("stack underflow! -> end stack-block")
        break
      stack[sp-1] = int(stack[sp-1]) / int(stack[sp])
      sp -= 1
      continue

    if inst == "fdiv":
      if len(args) != 0:
        err("too many arguments for fdiv instruction!")
        continue
      if sp < 1:
        err("stack underflow! -> end stack-block")
        break
      stack[sp-1] = stack[sp-1] / stack[sp]
      sp -= 1
      continue

    if inst == "mul":
      if len(args) != 0:
        err("too many arguments for mul instruction!")
        continue
      if sp < 1:
        err("stack underflow! -> end stack-block")
        break
      stack[sp-1] = int(stack[sp-1]) * int(stack[sp])
      sp -= 1
      continue

    if inst == "fmul":
      if len(args) != 0:
        err("too many arguments for mul instruction!")
        continue
      if sp < 1:
        err("stack underflow! -> end stack-block")
        break
      stack[sp-1] = stack[sp-1] * stack[sp]
      sp -= 1
      continue

    if inst == "fsub":
      if len(args) != 0:
        err("too many arguments for fsub instruction!")
        continue
      if sp < 1:
        err("stack underflow! -> end stack-block")
        break
      stack[sp-1] = stack[sp-1] - stack[sp]
      sp -= 1
      continue

    if inst == "sub":
      if len(args) != 0:
        err("too many arguments for sub instruction!")
        continue
      if sp < 1:
        err("stack underflow! -> end stack-block")
        break
      stack[sp-1] = int(int(stack[sp-1]) - int(stack[sp]))
      sp -= 1
      continue

    if inst == "add":
      if len(args) != 0:
        err("too many arguments for add instruction!")
        continue
      if sp < 1:
        err("stack underflow! -> end stack-block")
        break
      stack[sp-1] = int(int(stack[sp-1]) + int(stack[sp]))
      sp -= 1
      continue

    if inst == "fadd":
      if len(args) != 0:
        err("too many arguments for fadd instruction!")
        continue
      if sp < 1:
        err("stack underflow! -> end stack-block")
        break
      stack[sp-1] = stack[sp-1] + stack[sp]
      sp -= 1
      continue

    if inst == "call":
      if len(args) != 1:
        err("invalid amount of arguments for call instruction!")
        continue
      if not args[0] in funs.keys():
        err("cannot call undefined function!")
        continue
      if not cond == 1:
        continue
      fun = funs[args[0]]
      type = fun[1]
      if type == "!":
        stack = exec_stack(fun[2], stack[:sp+1], pval, exec, funs, vars, consts)
        sp = len(stack) - 1
        stack += [0.0] * (255 - len(stack))
      elif type == "%":
        oldr = vars["R"] if "R" in vars.keys() else None
        vars["R"] = "_"
        for i in range(fun[0]):
          if sp < 0:
            err("stack underflow! -> cant pass argument number " + str(i) + "!")
            continue
          vars["A"+str(i)] = stack[sp]
          sp -= 1
        exec(0, fun[2])
        if vars["R"] != "_":
          sp += 1
          stack[sp] = vars["R"]
        if oldr == None:
          del vars["R"]
        else:
          vars["R"] = oldr
      else:
        err("Unsupported function execution type!")
      continue

    if inst == "icv":
      if len(args) != 0:
        err("too many arguments for icv instruction!")
        continue
      if sp < 0:
        err("stack underflow! -> end of stack-block")
        break
      stack[sp] = int(stack[sp])
      continue

    if inst == "fcv":
      if len(args) != 0:
        err("too many arguments for fcv instruction!")
        continue
      if sp < 0:
        err("stack underflow! -> end of stack-block")
        break
      stack[sp] = float(stack[sp])
      continue

    if inst == "dump":
      if len(args) != 0:
        err("too many arguments for dump instruction!")
        continue
      print("BOTTOM")
      for s in stack[:sp+1]:
        print(s)
      print("TOP")
      continue

    if inst == "magic":
      if len(args) != 1:
        err("invalid amount of arguments for magic instructuion!")
        continue
      val = int(pval(args[0]))
      if val == 10: # port write
        if sp < 1:
          err("stack underflow! -> end of stack-block")
          break
        port = int(stack[sp])
        value = stack[sp-1]
        sp -= 2
        if port == 0:
          sys.stdout.write(chr(int(value)))
        elif port == 1:
          sys.stdin.write(chr(int(value)))
      elif val == 11: # port read
        if sp < 0:
          err("stack underflow! -> end of stack-block")
          break
        port = int(stack[sp])
        sp -= 1
        if port == 0:
          err("port 0 is write only!")
          break
        if port == 1:
          sp += 1
          stack[sp] = ord(getch())
        else:
          sp += 1
          stack[sp] = random.uniform(sys.float_info.min, sys.float_info.max)
      elif val == 12: # port exists
        if sp < 0:
          err("stack underflow! -> end of stack-block")
          break
        port = int(stack[sp])
        sp -= 1
        cond = 1 if port in [0, 1] else 0
      elif val == 13: # port wait
        if sp < 0:
          err("stack underflow! -> end of stack-block")
          break
        port = int(stack[sp])
        sp -= 1
        if port == 0:
          sys.stdout.flush()
        elif port == 1:
          getch()
        else:
          while True:
            pass
      else:
        err("unimplemented magic number: " + str(val) + "!")
      continue

    err("instruction not found: " + inst + "!")

  return stack[:sp+1]
