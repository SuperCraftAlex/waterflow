def single(cmd, args, funs, vars, consts, exec_stack, exec, pval, err):
  if len(args) != 2:
    err("Invalid arguments for \"ifpath\" command!")
    return False

  fname = args[1]
  path = args[0]

  if not fname in funs.keys():
    err("Function given to \"ifpath\" command is not defined!")
    return False

  fun = funs[fname]

  if fun[0] > 0:
    err("Function given to \"ifpath\" command cannot have arguments!")
    return False

  ftype = fun[1]

  if path in consts["__path"]:
    if ftype == "!":
      exec_stack(fun[2], [], pval, exec, funs, vars, consts, err)

    elif ftype == "%":
      exec(0, fun[2], err)

    else:
      err("Type of function \"" + name + "\" is not implemented!")
      return False

  return True
