__author__ = 'VHLAND002'


import sys
import parse_ula

# array that will hold all variables that have been defined
definedVars = []
semantic_errors = []


# traverses the tuples to create the AST recursively
# @param: tree- this is the tuple list we get
# @param: value- this is the indentation value for the tab chars
def traverseTree(tree, lineno):
    # if we have a tuple list with only 2 elements we have 2 leaves or the parent of a 2 leaves
    if tree[0] is None:
        return
    if tree[0] == 'IdentifierExpression':
        if not checkVariable(tree[1][1]):
            semantic_errors.append("semantic error on line " + str(lineno))
        for k in range(2, len(tree)):
            if k is not None:
                traverseTree(tree[k],lineno)
        return
    elif tree[0] == 'ID':
        if checkVariable(tree[1]):
            semantic_errors.append("semantic error on line " + str(lineno))
        else:
            definedVars.append(tree[1])
        return

    for q in range(1, len(tree)):
        if q is not None:
            traverseTree(tree[q],lineno)


# checks if the parsed variable is in the defined list
def checkVariable(var):
    if var in definedVars:
        return True
    else:
        return False

# write errors out to a file
def exportErrors(name):
    # export all errors here
    name = name[0:-4] + '.err'
    outFile = open(name, 'w')
    # we loop through the tree and write the output to the file
    outFile.write(semantic_errors[0])
    print(semantic_errors[0])
    outFile.close()



def main():
    # we see if we have parser errors
    errors = parse_ula.buildParser(sys.argv[1], True)
    if errors:
        for i in errors:
            semantic_errors.append(i)

    lineno = 0
    # we check if we have semantic errors
    for r in parse_ula.mainTree:
        if r is not None:
            lineno += 1
            traverseTree(r,lineno)
    # we export all errors
    exportErrors(sys.argv[1])


if __name__ == "__main__":
    main()