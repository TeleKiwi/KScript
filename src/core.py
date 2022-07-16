#########################################
# TOKENS
#########################################

TT_INT = "int"
TT_FLOAT = "float"
TT_PLUS = "plus"
TT_MINUS = "minus"
TT_MUL = "mul"
TT_DIV = "div"
TT_LPAREN = "lparen"
TT_RPAREN = "rparen"

class Token:
    def __init__(self, type, value):
        self.type = type
        self.value = value

    def __repr__(self):
        if self.value:
            return f'{self.type}({self.value})'
        else: 
            return f'{self.type}'


#########################################
# LEXER
#########################################

class Lexer:
    def __init__(self, text):
        self.text = text
        self.pos = -1
        self.current_char = None
    