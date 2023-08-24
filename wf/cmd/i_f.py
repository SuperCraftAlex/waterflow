def single(cmd, args, funs, vars, consts, exec_stack, exec, pval, err):
  if len(args) != 2:
    err("Invalid arguments for \"if\" command!")
    return False

  fname = args[1]
  a = int(pval(args[0], err))

  if not fname in funs.keys():
    err("Function given to \"if\" command is not defined!")
    return False

  fun = funs[fname]

  if fun[0] > 0:
    err("Function given to \"if\" command cannot have arguments!")
    return False

  ftype = fun[1]
  if int(a) == 1:
    if ftype == "!":
      exec_stack(fun[2], [], pval, exec, funs, vars, consts, err)

    elif ftype == "%":
      exec(0, fun[2], err)

    else:
      err("Type of function \"" + name + "\" is not implemented!")
      return False

  return True
