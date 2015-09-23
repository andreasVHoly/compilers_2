from __future__ import print_function
__author__ = 'VHLAND002'

import llvmlite.binding as llvm
import ir_ula
import sys


# initalize the llvm
llvm.initialize()
llvm.initialize_native_target()
llvm.initialize_native_asmprinter()


# we get the file name from command line
name = sys.argv[1]
# we get the output from our modified parser
llvm_ir = str(ir_ula.buildIRCode(name, False))

# creates the execution engine
def create_execution_engine():

    # create target machine
    target = llvm.Target.from_default_triple()
    target_machine = target.create_target_machine()
    # we create an empty backing module
    backing_mod = llvm.parse_assembly("")
    engine = llvm.create_mcjit_compiler(backing_mod, target_machine)
    return engine

# where we compile the ir code
def compile_ir(engine, llvm_ir):
    # we create a module from the str( parser output)
    mod = llvm.parse_assembly(llvm_ir)
    mod.verify()
    # we add the module
    engine.add_module(mod)
    engine.finalize_object()
    return mod

# we make a new engine
engine = create_execution_engine()
# we generate a mod from the engine and our parser code
mod = compile_ir(engine, llvm_ir)
# we create a new target machine with the new mod
target = llvm.Target.from_default_triple()
target_machine = target.create_target_machine()
# we generate the assembly code
code = target_machine.emit_assembly(mod)
# write out to the file
file = open(name[0:-4] + '.asm', 'w')
file.write(code)
file.close()

