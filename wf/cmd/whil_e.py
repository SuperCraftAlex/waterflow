def single(cmd, args, funs, vars, consts, exec_stack, exec, pval):
  if len(args) != 2:
    print("Invalid arguments for \"while\" command!")
    return False

  fname = args[1]
  var = args[0]

  if not fname in funs.keys():
    print("Function given to \"while\" command is not defined!")
    return False

  fun = funs[fname]

  if fun[0] > 0:
    print("Function given to \"while\" command cannot have arguments!")
    return False

  ftype = fun[1]

  while True:
    if not (var in vars.keys() or var in consts.keys()):
      print("Variable given to \"while\" command is not defined!")
      return False

    if pval(var) == 0:
      break

    if ftype == "!":
      exec_stack(fun[2], [], pval, exec, funs, vars, consts)

    elif ftype == "%":
      exec(0, fun[2])

    else:
      print("Type of function \"" + name + "\" is not implemented!")
      return False

  return True
