__author__ = 'VHLAND002'
from llvmlite import ir
from ctypes import CFUNCTYPE, c_float
import llvmlite.binding as llvm
import parse_ula
import sys
import re

variables = {}
last_var = ""
convertedTree = ["Program"]




def traverseTree(tree):
    global last_var

    #if str(tree[1]) in variables:
     #   tree[1] = variables[str(tree[1])]
    #elif str(tree[2]) in variables:
     #   tree[2] = variables[str(tree[2])]
    #print(tree)
    if tree[0] == 'Program':
        for i in tree[1:]: #traverse the rest of the tree
            traverseTree(i)
    elif tree[0] == '=':
        last_var = tree[1][0] # access 0th element of 1, this will be the var name
        variables[last_var] = builder.alloca(ir.FloatType()) # allocate a memory address
        builder.store(traverseTree(tree[2]), variables[last_var]) # store the rest of the tree as the variables after math

    elif tree[0] == '$': # subtract
        return(builder.fsub(traverseTree(tree[1]), traverseTree(tree[2])))

    elif tree[0] == '&': # divide
        return(builder.fdiv(traverseTree(tree[1]), traverseTree(tree[2])))

    elif tree[0] == '#': # multiply


        return(builder.fmul(traverseTree(tree[1]), traverseTree(tree[2])))

    elif tree[0] == '@': # add
        return(builder.fadd(traverseTree(tree[1]), traverseTree(tree[2])))

    elif tree[0].isnumeric() or re.match("[+-]?\d+(\.\d+)?([eE][+-]?\d+)?", tree[0]):
        return(ir.Constant(ir.FloatType(), float(tree[0])))

    else:
        #print(type(tree[0]))
        #(tree[0])
        #print(variables[tree[0]])
        #return(ir.Constant(ir.FloatType(), variables[tree[0]]))
        return(builder.load(variables[tree[0]]))

def checkVariable(name):
    global variables
    if name in variables:
        return

floattype = ir.FloatType()
functiontype = ir.FunctionType(floattype, ())
module = ir.Module(name='ula')
function = ir.Function(module, functiontype, name='main')
block = function.append_basic_block(name='entry')
builder = ir.IRBuilder(block)



def buildIRCode(name, print):
    #name =
    #name = "ula_irrun_samples/add.ula" #pass
    #name = "ula_irrun_samples/assign.ula" #pass
    #name = "ula_irrun_samples/circumference.ula" #pass
    #name = "ula_irrun_samples/expr.ula" #pass
    #name = "ula_irrun_samples/multi.ula" #pass

    parseTree = parse_ula.buildParser(name, False)
    #print(parseTree)
    for k in parseTree:
        convertedTree.append(k)

    #print(convertedTree)
    traverseTree(convertedTree)
    builder.ret(builder.load(variables[last_var]))
    if print:
        file = open(name[0:-4] + '.ir', 'w')
        file.write(str(module))
        file.close()
        print(str(module))
    return module


def main():
    buildIRCode(sys.argv[1], True)

if __name__ == "__main__":
    main()

