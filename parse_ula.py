__author__ = 'VHLAND002'

from lex_ula import tokens
import ply.yacc as yacc
import lex_ula
import sys  # for command line args

# we set the precendence of the operators
precedence = (
    ('left', 'ADD', 'SUB'),
    ('left', 'MULT', 'DIV'),
)


'''
#start -> program
def p_start(p):
    'start : program'
    p[0] = ("Start",p[1])

# program -> statement*
def p_program_statement(p):
    'program : statement'
    p[0] = ("Program",p[1])


start = 'start'
'''


# statement -> ID = expression
def p_statement_expression(p):
    'statement : ID EQUAL expression'
    p[0] = ('AssignStatement',('ID',p[1]),p[3])


# Expression -> Expression @ Term
def p_expression_add(p):
    'expression : expression ADD term'
    p[0] = ('AddExpression', p[1], p[3])


# Expression -> Expression $ Term
def p_expression_sub(p):
    'expression : expression SUB term'
    p[0] = ('SubExpression', p[1], p[3])


# Expression -> Term
def p_expression_term(p):
    'expression : term'
    p[0] = p[1]


# Term -> Term # Factor
def p_term_mult(p):
    'term : term MULT factor'
    p[0] = ('MulExpression', p[1], p[3])


# Term -> Term & Factor
def p_term_div(p):
    'term : term DIV factor'
    p[0] = ('DivExpression', p[1], p[3])

# Term -> Factor
def p_term_factor(p):
    'term : factor'
    p[0] = p[1]


# Factor -> (Expression)
def p_factor_expression(p):
    'factor : OBRACKET expression CBRACKET'
    p[0] = (p[2])


# Factor -> float
def p_factor_float_literal(p):
    'factor : FLOAT_LITERAL'
    p[0] = ('FloatExpression', ('FLOAT_LITERAL',p[1]))


# Factor -> identifier
def p_factor_id(p):
    'factor : ID'
    p[0] = ('IdentifierExpression', ('ID',p[1]))


# Error rule for syntax errors
def p_error(p):
    print("Syntax error in input!")


# converts the token file to a format we can work with and convert into an AST
def convertTokenFile():
    newData = []
    # we loop while we have data
    while True:
        # we get the next token
        tok = lex_ula.lexer.token()
        # if it is null, we break and add the statement we have accumulated
        if not tok:
            # we make up the statement from the contents of newData
            statement = ''
            for t in range(0, len(newData)):
                statement += str(newData[t])
            # we add this into the main array of perfect code
            content.append(str(statement))
            # break out of teh while loop
            break
        # if we are dealing with a type we want to ignore
        if tok.value == 'COMMENT' or tok.value == 'WHITESPACE':
            # continue to the next iteration
            continue
        # if we reach a = it means we have reached the next assignment statement
        elif tok.value == '=':
            statement = ''
            # we create the previous statement from everything but
            # the last element (this will be a variable name for the newly found assignment)
            for t in range(0,len(newData)-1):
                statement += str(newData[t])
            # we add the statement
            content.append(str(statement))
            # we reset everything to hold the new statement
            newData.clear()
            # we add the variable name
            newData.append(previous.value)
            # we add the new =
            newData.append(tok.value)
        else:
            # add whatever we encounter
            newData.append(tok.value)
        # make a backup of the token for the next assignment variable capturing
        previous = tok

    # we loop over what we found and add the output of the parser into an array
    for y in range(1, len(content)):
        mainTree.append(parser.parse(str(content[y]), lexer=lex_ula.lexer))


# traverses the tuples to create the AST recursively
# @param: tree- this is the tuple list we get
# @param: value- this is the indentation value for the tab chars
def traverseTree(tree, value):
    # if we have a tuple list with only 2 elements we have 2 leaves or the parent of a 2 leaves
    if len(tree) == 2:
        # when we have a parent
        if tree[0] == 'FloatExpression':
            # we append to the final string
            final.append('\n'+"\t"*value+ str(tree[0]))
            # we traverse the children
            traverseTree(tree[1],value+1)
        elif tree[0] == 'IdentifierExpression':
            # we append to the final string
            final.append('\n'+"\t"*value+ str(tree[0]))
            # we traverse the children
            traverseTree(tree[1],value+1)
        else:
            # we append to the final string
            final.append('\n'+"\t"*value+ str(tree[0]) + "," + str(tree[1]))
        return

    # we append the first element which is always a identifier
    final.append('\n'+"\t"*value+ str(tree[0]))
    # we loop over the rest and recursively assess them, incrementing the value to get the formatting right
    for q in range(1, len(tree)):
        traverseTree(tree[q], value+1)


# this creates the ast file from the final tree
# @param: name - the name of the file
# @param: tree - the tree to be written to the file
def createASTFile(name,tree):
    name = name[0:-4] + '.ast'
    outFile = open(name, 'w')
    # we loop through the tree and write the output to the file
    for p in tree:
        outFile.write(p)
    outFile.close()


# Build the parser
parser = yacc.yacc()
# the file name which is supplied via command line args
file = str(sys.argv[1])
# init of some variables
final = []
content = []
mainTree = []
# we import the file in the lexer without creating a token file
lex_ula.importFile(file, False)
# we convert the token stream
convertTokenFile()
# we append default strings for the AST
final.append("Start\n\tProgram")
# we go through the tree and traverse it
for r in mainTree:
    traverseTree(r, 2)
# now that the AST has been built we print it out
for i in final:
    print(i, end='')
# then we create the AST file
createASTFile(file, final)








