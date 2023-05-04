# This program can be run as python2 or as python3
from __future__ import print_function

# Question 7 #########################################################
# tokens:
# Start with this tokens
EOI = 'EOI'  # end of input
Tr = 'True'  # Constant True - True
Fa = 'False'  # Constant False - False
LP = 'LP'  # Character (
RP = 'RP'  # Character )
ERR = 'ERR'  # Showing Error
And = 'And'
Or = 'Or'
Eq = '='
Var = 'Var'
Not = 'not'

# end of Question 7 ##################################################

# Question 8 - Grammar ###############################################
# statment -> Var Eq statement | expr
# expr -> neg tail | neg
# statment -> term | termTail
# termTail -> Succ term | Pred term | isZero term | ifThenElse term term term
# term -> Tr | Fa | Ze | (Add this later) LP statment RP
# end of Question 8 ##################################################


# Question 9 - recursive descent parser###############################
debug = False


def show(indent, name, s, spp):
    if debug:
        print(indent + name + '("', end='');
        j = len(s)
        for i in range(spp, j):
            print(s[i], sep="", end="")
        print('")', end='\n')
        return
    else:
        return


def EatWhiteSpace(s, spp):
    j = len(s)
    if spp >= j:
        return spp

    while s[spp] == ' ' or s[spp] == '\n':
        spp = spp + 1
        if spp >= j:
            break

    return spp
# end EatWhiteSpace


def Parse(s, indent):
    show(indent, 'Parse', s, 0)
    # Starting index
    spp = 0

    sppr = len(s) - 1
    # Keeping the tokens
    result = []

    indent1 = indent + ' '

    # Need to start reading the statments
    res, result, spp = statment(s, spp, indent, result)

    return res, result, spp


# statment -> Var Eq statement | expr
# statment -> term | termTail
def statment(s, spp, indent, result):
    show(indent, 'statment', s, spp)
    indent1 = indent + ' '

    # Keep the previous position saved
    previous_spp = spp

    # Let's read a token
    token, spp = NextTokenL(s, spp)

    #let's read the second token
    token_2, spp1 = NextTokenL(s, spp)

    if token == EOI or token == ERR:
        # Statement is a True term
        # Add the term to the list of tokens and return the statement
        result.append(token)
        return True, result, spp
    elif token == Var and token_2 == Eq:
        result.append(token)
        result.append(token_2)
        return statment(s, spp1, indent, result)
    else:
        return expr(s, previous_spp, indent, result)



# expr -> term or expr | term and expr | not term | term
def expr(s, spp, indent, result):
    show(indent, 'expr', s, spp)
    indent1 = indent + ' '

    # Keep the previous position saved
    previous_spp = spp

    # Let's read a token
    token, spp = NextTokenL(s, spp)
    if token == Not:
        result.append(token)
        return term(s, spp, indent, result)
    else:
        return term(s, previous_spp, indent, result)



def term(s, spp, indent, result):
    show(indent, 'term', s, spp)
    indent1 = indent + ' '

    # Keep the previous position saved
    previous_spp = spp

    # Let's read a token
    token, spp = NextTokenL(s, spp)

    token_2, spp1 = NextTokenL(s, spp)

    if token == Var or token == Tr or token == Fa:
        if token_2 == Or or token_2 == And:
            result.append(token)
            result.append(token_2)
            return expr(s, spp1, indent, result)
        elif token_2 == EOI:
            result.append(token)
            result.append(token_2)
            return True, result, spp
        else:
            result.append(token)
            return False, result, spp
    elif token == LP:
        result.append(token)
        return parenth(s, spp, indent, result)
    else:
        return False, result, spp

def parenth(s, spp, indent, result):
    show(indent, 'parenth', s, spp)
    indent1 = indent + ' '

    # Keep the previous position saved
    previous_spp = spp

    # Let's read a token
    res, result, spp = expr(s, spp, indent, result)

    if res:
        return False, result, spp

    token, spp = NextTokenL(s,spp)

    token_2, spp1 = NextTokenL(s, spp)

    if token == RP:
        result.append(token)
        if token_2 == Or or token_2 == And:
            result.append(token_2)
            return expr(s, spp1, indent, result) 
        elif token_2 == EOI:
            result.append(token_2)
            return True, result, spp
        else:
            return False, result, spp
    else:
        return False, result, spp
    
    


# function NextToken ---------------------------------------------
def NextTokenL(s, spp):
    spp1 = spp
    spp = EatWhiteSpace(s, spp)
    j = len(s)
    if spp >= j:
        return EOI, spp
    elif s[spp: spp + 3] == 'not':
        return Not, spp + 3
    elif s[spp] == "=":
        return Eq, spp + 1
    elif s[spp: spp + 3] == "Var":
        return Var, spp + 3
    elif s[spp: spp + 2] == "or":
        return Or, spp + 2
    elif s[spp: spp + 3] == "and":
        return And, spp + 3
    elif s[spp] == "(":
        return LP, spp + 1
    elif s[spp] == ")":
        return RP, spp + 1
    elif s[spp:spp + 4] == "True":
        return Tr, spp + 4
    elif s[spp:spp + 5] == "False":
        return Fa, spp + 5
    else:
        return ERR, spp1
# end NUM


# main section
s = "(Var = Var) = Var or not Var"
# What we expect

# I need a variable that keeps to index value. This will help
# me to figure out where in the string I am.
spp = 0  # Initial value will be zero since we are at index zero.
# Let's define a list that is going to keep the tokens

res, final_tokens_list, spp = Parse(s, "")

print(res, final_tokens_list)

# is there a leftover ?
if spp < len(s) - 1:
    print("parse Error")
else:
    print("parsing OK")
    print(' '.join(final_tokens_list))
# end main section

# end of Question 9 ########################################################
