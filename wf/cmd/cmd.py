import cmd.stack_exec
import cmd.fun
import cmd.undef
import cmd.use
import cmd.var
import cmd.const

cmds_single = {
  "!":      cmd.stack_exec.single,
  "undef":  cmd.undef.single,
  "use":    cmd.use.single,
  "var":    cmd.var.single,
  "const":  cmd.const.single
}

cmds_block = {
  "!":      cmd.stack_exec.block,
  "fun":    cmd.fun.block
}
