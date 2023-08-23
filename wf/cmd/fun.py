def block(cmd, args, block, funs, vars, consts, exec_stack, exec, pval):
  if len(args) != 3:
    print("Invalid arguments for \"fun\" command!")
    return False

  name = args[0]
  argl = args[1]

  if name in funs.keys():
    print("Function \"" + name + "\" is already defined!")
    return False

  if not argl.isnumeric():
    print("Function argument length needs to be number!")
    return False

  ind0 = len(block[0]) - len(block[0].lstrip())

  funs[args[0]] = (int(argl), args[2], list(map(lambda x: x[ind0:], block)))

  return True
