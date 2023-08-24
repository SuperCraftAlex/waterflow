def single(cmd, args, funs, vars, consts, exec_stack, exec, pval, err):
  if len(args) != 2:
    err("Invalid arguments for \"while\" command!")
    return False

  fname = args[1]
  var = args[0]

  if not fname in funs.keys():
    err("Function given to \"while\" command is not defined: " + fname + "!")
    return False

  fun = funs[fname]

  if fun[0] > 0:
    err("Function given to \"while\" command cannot have arguments " + fname + "!")
    return False

  ftype = fun[1]

  while True:
    if not (var in vars.keys() or var in consts.keys()):
      err("Variable given to \"while\" command is not defined: " + var + "!")
      return False

    if pval(var, err) == 0:
      break

    if ftype == "!":
      exec_stack(fun[2], [], pval, exec, funs, vars, consts, err)

    elif ftype == "%":
      exec(0, fun[2], err)

    else:
      err("Type of function \"" + name + "\" is not implemented!")
      return False

  return True
