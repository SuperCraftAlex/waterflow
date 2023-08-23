import cmd.stack_exec
import cmd.fun
import cmd.undef
import cmd.use
import cmd.var
import cmd.const
import cmd.whil_e
import cmd.times
import cmd.asser_t

cmds_single = {
  "!":           cmd.stack_exec.single,
  "undef":       cmd.undef.single,
  "use":         cmd.use.single,
  "var":         cmd.var.single,
  "const":       cmd.const.single,
  "while":       cmd.whil_e.single,
  "times":       cmd.times.single,

  "assert":      cmd.asser_t.value,
  "assert_def":  cmd.asser_t.defined,
  "assert_ndef": cmd.asser_t.undefined
}

cmds_block = {
  "!":           cmd.stack_exec.block,
  "fun":         cmd.fun.block
}
