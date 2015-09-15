__author__ = 'VHLAND002'

import lex
import sys
import errors_ula

tokens = ('ID', 'FLOAT_LITERAL', 'ADD', 'SUB', 'MULT', 'DIV', 'EQUAL', 'OBRACKET', 'CBRACKET', 'WHITESPACE', 'COMMENT')


# Regular expression rules for simple tokens

t_ADD = r'\@'
t_SUB = r'\$'
t_MULT = r'\#'
t_DIV = r'\&'
t_EQUAL = r'\='
t_OBRACKET = r'\('
t_CBRACKET = r'\)'

# regular expressions

# def t_ID(self,t)
def t_ID(t):
    r'[a-zA-Z_][a-zA-Z_0-9]*'
    return t


# def t_FLOAT_LITERAL(self,t)
def t_FLOAT_LITERAL(t):
    #if we find a digit and can have 1 or more iterations of digits
    r'[+-]?\d+(\.\d+)?([eE][+-]?\d+)?'
    return t


# def t_SLCOMMENT(self,t):
def t_COMMENT(t):
    #means we check for // and go up until the end of the line ie \n (specified by the .) and then have 0 or more iterations of this (*)
    r'//.* | \/\*+[^*/]*\*+\/'
    t.value = "COMMENT"
    return t

# def t_WHITESPACE(self,t):
def t_WHITESPACE(t):
    #check for either of the characters and mark them as whitespace
    r'[ \t\r\n]+'
    if t.value == '\n':
        t.lexer.lineno += len(t.value)
    t.value = 'WHITESPACE'
    return t


#def t_NEWLINE(t):
    #r'[\n]'
    #t.value = 'WHITESPACE'
    #t.lexer.lineno += 1
    #return t



# def t_error(self,t):
def t_error(t):
    print("lexical error on line " + str(t.lineno))
    errors_ula.errors.append("lexical error on line " + str(t.lineno) + "\n")
    t.lexer.skip(len(t.value))

# imports a file and based on the boolean outputs a token file or not
def importFile(fileName, write):
    # we open the ula file for reading
    inFile = open(fileName, 'r')
    # we read all the data in one go
    data = inFile.read()
    # we close the ula file
    inFile.close()
    # we pass the file contents to the lexer
    lexer.input(data)

    # if we want to write out a token file
    if write:
        # we make a new filename from the old one to change the extension from .ula to .tkn
        fileName = fileName[0:-4] + '.tkn'
        # we open the file for writing
        outFile = open(fileName, 'w')
        # we process in data while there is data to process
        while True:
            # we get the next token
            tok = lexer.token()
            # if null we break, no more tokens
            if not tok:
                break
            # we handle float literals and ID's specifically to output both the type and value
            if tok.type == 'FLOAT_LITERAL' or tok.type == 'ID':
                # we write it out to our file
                outFile.write(tok.type + "," + str(tok.value) + '\n')
                # printing output
                #print(tok.type + "," + str(tok.value))
            # for anything else we just want the value
            else:
                outFile.write(str(tok.value) + '\n')
                #print(str(tok.value))

        # close the output file
        outFile.close()

# this starts the lexer
lexer = lex.lex()


def main():
    importFile(str(sys.argv[1]), True)

if __name__ == "__main__":
    main()






