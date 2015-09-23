__author__ = 'VHLAND002'
from llvmlite import ir

import parse_ula
import sys
import re

# where we keep all of our variables and their memory locations
variables = {}
# the last variable we encountered
last_var = ""
# the final tree we use for the IR code generation
convertedTree = ["Program"]


# we traverse the tree and build the IR code
def traverseTree(tree):
    global last_var
    # if we encounter the beginning of the list
    if tree[0] == 'Program':
        for i in tree[1:]: # traverse the rest of the tree
            traverseTree(i)
    elif tree[0] == '=':
        # access 0th element of 1, this will be the var name
        last_var = tree[1][0]
        # allocate a memory address
        variables[last_var] = builder.alloca(ir.FloatType())
        # store the rest of the tree in the memory location define for that variable
        builder.store(traverseTree(tree[2]), variables[last_var])

    # we handle all arithmatic operators
    elif tree[0] == '$': # subtract
        return builder.fsub(traverseTree(tree[1]), traverseTree(tree[2]))

    elif tree[0] == '&': # divide
        return builder.fdiv(traverseTree(tree[1]), traverseTree(tree[2]))

    elif tree[0] == '#': # multiply
        return builder.fmul(traverseTree(tree[1]), traverseTree(tree[2]))

    elif tree[0] == '@': # add
        return builder.fadd(traverseTree(tree[1]), traverseTree(tree[2]))

    # we check for integers and use a regular experssion to check for floats
    elif tree[0].isnumeric() or re.match("[+-]?\d+(\.\d+)?([eE][+-]?\d+)?", tree[0]):
        return ir.Constant(ir.FloatType(), float(tree[0]))
    # this should only ever catch variable names
    else:
        # we load the variables content based on the memory location from the builder
        return builder.load(variables[tree[0]])


# we make a new type
floattype = ir.FloatType()
# we create a new function that returns a float we define above and takes no args
functiontype = ir.FunctionType(floattype, ())
# we assign the module name as ula
module = ir.Module(name='ula')
# the function is called main
function = ir.Function(module, functiontype, name='main')
# we add an entry block
block = function.append_basic_block(name='entry')
# we build the IR code
builder = ir.IRBuilder(block)



def buildIRCode(name, print):

    # we generate the parser list
    parseTree = parse_ula.buildParser(name, False)
    for k in parseTree:
        convertedTree.append(k)
    traverseTree(convertedTree)
    # we build the IR code
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

