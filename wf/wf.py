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

pval = lambda s, err: float(s) if is_float(s) else (vars[s] if s in vars.keys() else (consts[s] if s in consts.keys() else err("Not a variable / local / constant / int / float: " + s + "!")))

gen_anon_name = lambda: "__anonymus_" + ''.join(random.sample(string.ascii_lowercase, 8))

def split_cmd(line):
  # splits into stuff like this: ["add"], ["(mul 1 2)"], ["3"]

  out = []
  p = ""
  ind = 0

  for c in line:
    if c == '(':
      ind += 1
    elif c == ')':
      ind -= 1
    elif c == ' ' and ind == 0:
      out.append(p[:])
      p = ""
      continue

    p += c

  out.append(p)

  return out

def exec_single(argl, blocks, err):
#  print(argl)

  # takes a list of split arguments
  # returns: (return_values: list)?

  global funs
  global vars
  global consts
  global cmds_single

  args = argl[1:]
  cmd = argl[0]

  if len(cmd) == 0:
    return None

  nargs = []
  anonc = 0
  for arg in args:
    arg = arg.strip()

    if len(arg) == 0:
      continue

    elif arg.startswith("(") or arg.startswith("-("):
      arg = arg[1:]
      skip_first = False
      if arg[0] == '(':
        skip_first = True
        arg = arg[1:]
      unpack = []
      for c in reversed(arg):
        if c in "-.":
          unpack.append(c)
        else:
          if c != ")":
            err("Inline function calls need to be enclosed in parentheses!")
            return None
          break
      v = exec_single(split_cmd(arg[:-(1+len(unpack))]), [], err)
      if v == None:
        err("Inline function calls need to return something!")
        return None
      unpack.append('-' if skip_first else '.')
      unpack = list(reversed(unpack))
      for i, u in enumerate(unpack):
        if len(v) == 0:
          err("Not enought return values to unpack!")
          return None
        if u == '.':
          nargs.append(str(v[-1]))
        v = v[:-1]

    else:
      nargs.append(arg)

  args = nargs[:]
  oargs = nargs[:]

  nargs = []
  anonc = 0
  for arg in args:
    if arg == "%" or arg == "!":
      anonc += 1
      if anonc > 1:
        err("Cannot have more than one anonymus function in function call!")
        continue

      fname = gen_anon_name()
      funs[fname] = (-1, arg, blocks[:])
      nargs.append(fname)

    else:
      nargs.append(arg)

  args = nargs[:]

  if ((not len(blocks) > 0) or anonc > 0) and cmd in cmds_single.keys():
    r = cmds_single[cmd](cmd, args, funs, vars, consts, exec_stack, exec, pval, err)
    return None

  if cmd in cmds_block.keys():
    r = cmds_block[cmd](cmd, oargs, blocks[:], funs, vars, consts, exec_stack, exec, pval, err)
    return None

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
      err("Invalid arguments for call of function: " + cmd + "!")
      return None

    if fun[1] == "!":
      stack = exec_stack(fun[2], list(map(lambda x: pval(x, err), args)), pval, exec, funs, vars, consts, err)
      sp = len(stack) - 1
      for o in outs:
        if not o in vars.keys():
          err("Cannot pop into variable: undefined variable: " + o + "!")
          continue
        if sp < 0:
          err("Cannot pop into variable: stack underflow!")
          continue
        vars[o] = stack[sp]
        sp -= 1
      if sp < 0:
        return None
      return stack[:sp+1]

    if fun[1] == "%":
      oldr = vars["R"] if "R" in vars.keys() else None
      vars["R"] = 0.0

      ovars = consts.copy()

      for i, arg in enumerate(args):
        consts["A"+str(i)] = pval(arg, err)

      exec(0, fun[2], err)

      for var in ovars.keys():
        if var[0] == 'A' and len(var) < 3:
          consts[var] = ovars[var]

      v = None

      if len(outs) > 0:
        if len(outs) != 1:
          err("Waterflow functions cannot return more than one value!")
          return None
        if not outs[0] in vars.keys():
          err("Cannot pop into variable: undefined variable: " + outs[0] + "!")
          return None
        vars[outs[0]] = vars["R"]

      else:
        v = [str(vars["R"])]

      if oldr == None:
        del vars["R"]

      else:
        vars["R"] = oldr

      return v

    err("Invalid code block type " + fun[1] + " of function " + cmd + "!")
    return None

  err("Command / Function " + cmd + " not found!")
  return None

def exec(last_ind, lines, err):
  global vars
  global consts
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
      block = list(map(lambda x: x[blocki:], block))

      argl = split_cmd(last.strip())
      exec_single(argl, block, err)

      block.clear()

    line = line.strip()
    last = line
    last_ind = ind

    exe = True
    for nl in lines[i+1:]:
      nl = nl.split(">>")[0].rstrip()
      if len(nl.strip()) == 0:
        continue
      nli = len(nl) - len(nl.lstrip())
      if nli > ind:
        exe = False
      break

    if exe:
      argl = split_cmd(line.strip())
      exec_single(argl, [], err)

  if len(block) > 0:
    blocki = len(block[0]) - len(block[0].lstrip())
    block = list(map(lambda x: x[blocki:], block))

    argl = split_cmd(last.strip())
    exec_single(argl, block, err)

    block.clear()

def error(x):
  sys.stderr.write(x)
  sys.stderr.flush()
  sys.exit(1)
#  return 0

exec(0, txt.split("\n"), error)
