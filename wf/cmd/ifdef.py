def defined(cmd, args, funs, vars, consts, exec_stack, exec, pval, err):
  if len(args) != 2:
    err("Invalid arguments for \"ifdef\" command!")
    return False

  fname = args[1]
  v = args[0]

  if not fname in funs.keys():
    err("Function given to \"ifdef\" command is not defined!")
    return False

  fun = funs[fname]

  if fun[0] > 0:
    err("Function given to \"ifdef\" command cannot have arguments!")
    return False

  ftype = fun[1]

  if v in funs.keys() or v in vars.keys() or v in consts.keys():
    if ftype == "!":
      exec_stack(fun[2], [], pval, exec, funs, vars, consts, err)

    elif ftype == "%":
      exec(0, fun[2], err)

    else:
      err("Type of function \"" + name + "\" is not implemented!")
      return False

  return True

def notdefined(cmd, args, funs, vars, consts, exec_stack, exec, pval, err):
  if len(args) != 2:
    err("Invalid arguments for \"ifndef\" command!")
    return False

  fname = args[1]
  v = args[0]

  if not fname in funs.keys():
    err("Function given to \"ifndef\" command is not defined!")
    return False

  fun = funs[fname]

  if fun[0] > 0:
    err("Function given to \"ifndef\" command cannot have arguments!")
    return False

  ftype = fun[1]

  if not (v in funs.keys() or v in vars.keys() or v in consts.keys()):
    if ftype == "!":
      exec_stack(fun[2], [], pval, exec, funs, vars, consts, err)

    elif ftype == "%":
      exec(0, fun[2], err)

    else:
      err("Type of function \"" + name + "\" is not implemented!")
      return False

  return True
