def block(cmd, args, block, funs, vars, consts, exec_stack, exec, pval):
  if len(args) != 3:
    print("Invalid arguments for \"fun\" command!")
    return False

  name = args[0]
  argl = args[1]

  if name in funs.keys():
    print("Function \"" + name + "\" is already defined!")
    return False

  if argl == "*":
    argl = "-1"

  if not argl.isnumeric():
    print("Function argument length needs to be number or a specifc argument length specifier!")
    return False

  funs[args[0]] = (int(argl), args[2], block)

  return True
