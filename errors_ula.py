__author__ = 'VHLAND002'


import sys
import parse_ula




# array that will hold all variables that have been defined
definedVars = []
errors = []
fileName = str(sys.argv[1])[0:-4] + '_1.err'




# traverses the tuples to create the AST recursively
# @param: tree- this is the tuple list we get
# @param: value- this is the indentation value for the tab chars
def traverseTree(tree):
    # if we have a tuple list with only 2 elements we have 2 leaves or the parent of a 2 leaves

    if tree[0] is None:
        return
    #print(tree)
    if tree[0] == 'IdentifierExpression':
        if not checkVariable(tree[1][1]):
            #print("Error: unknown variable " + str(tree[1][1]))
            print("semantic error")
        #else:
            #print(str(tree[1][1]) + " found")
        for k in range(2, len(tree)):
            if k is not None:
                traverseTree(tree[k])
        return
    elif tree[0] == 'ID':
        if checkVariable(tree[1]):
            # print("Error: duplicate variable")
            print("semantic error")
        else:
            #print(str(tree[1]) + " added to the list")
            definedVars.append(tree[1])
        return

    for q in range(1, len(tree)):
        if q is not None:
            traverseTree(tree[q])


# checks if the parsed variable is in the defined list
def checkVariable(var):
    if var in definedVars:
        return True
    else:
        return False


def exportErrors(name):
    # export all errors here
    name = name[0:-4] + '_1.err'
    outFile = open(name, 'w')
    # we loop through the tree and write the output to the file
    outFile.write(errors[0])
    outFile.close()



def main():
    #importUlaFile("ula_samples/comments.ast")
    #name = "ula_error_samples/lerror1.ula"
    #name = "ula_error_samples/lerror2.ula"
    #name = "ula_error_samples/perror1.ula"
    #name = "ula_error_samples/perror2.ula"
    #name = "ula_error_samples/serror1.ula"
    #name = "ula_error_samples/serror2.ula"
    #lex_ula.importFile(name, True)
    #print(errors)
    parse_ula.buildParser(sys.argv[1])
    #print(errors)
    for r in parse_ula.mainTree:
        if r is not None:
            traverseTree(r)
    #print(definedVars)
    #print(errors)
    #exportErrors(sys.argv[1])


if __name__ == "__main__":
    main()