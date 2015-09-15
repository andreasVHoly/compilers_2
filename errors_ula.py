__author__ = 'VHLAND002'


import sys
import parse_ula
import lex_ula




# array that will hold all variables that have been defined
definedVars = []






# traverses the tuples to create the AST recursively
# @param: tree- this is the tuple list we get
# @param: value- this is the indentation value for the tab chars
def traverseTree(tree):
    # if we have a tuple list with only 2 elements we have 2 leaves or the parent of a 2 leaves
    #print(tree)
    if tree[0] == 'IdentifierExpression':
        if not checkVariable(tree[1][1]):
            print("Error: unknown variable " + str(tree[1][1]))
        else:
            print(str(tree[1][1]) + " found")
        for k in range(2, len(tree)):
            traverseTree(tree[k])
        return
    elif tree[0] == 'ID':
        if checkVariable(tree[1]):
            print("Error: duplicate variable")
        else:
            print(str(tree[1]) + " added to the list")
            definedVars.append(tree[1])
        return

    for q in range(1, len(tree)):
        traverseTree(tree[q])


# checks if the parsed variable is in the defined list
def checkVariable(var):
    if var in definedVars:
        return True
    else:
        return False






def main():
    #importUlaFile("ula_samples/comments.ast")
    name = "ula_samples/complex.ula"
    lex_ula.importFile(name, True)
    parse_ula.buildParser(name)
    for r in parse_ula.mainTree:
        traverseTree(r)
    #print(definedVars)

if __name__ == "__main__":
    main()