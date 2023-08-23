import sys

def exec_stack(block, stack, pval, exec, funs, vars, consts):
  cond = 1.0

  # sp points to the current top element in the stack
  sp = len(stack) - 1

  stack += [0.0] * (255 - len(stack))

  for inst in block:
    if len(inst.strip()) == 0:
      continue

    inst = inst.strip().split(" ")
    args = inst[1:]
    inst = inst[0]

    if inst == "sec":
      if len(args) != 0:
        err("too many arguments for sec instruction!")
        continue
      cond = True
      continue

    if inst == "clc":
      if len(args) != 0:
        err("too many arguments for clc instruction!")
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
        stack = exec_stack(fun[2], stack[:sp+1], pval, exec, funs, vars, consts)
        sp = len(stack) - 1
        stack += [0.0] * (255 - len(stack))
      elif type == "%":
        oldr = vars["R"] if "R" in vars.keys() else False
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
        if oldr == False:
          del vars["R"]
        else:
          vars["R"] = oldr
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
      val = int(pval(args[0]))
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
