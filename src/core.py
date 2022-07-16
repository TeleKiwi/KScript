#########################################
# CONSTANTS
#########################################

DIGITS = '0123456789'

#########################################
# ERRORS
#########################################

class Error:
    def __init__(self, error_name, details):
        self.error_name = error_name
        self.details = details
    
    def as_string(self):
        result = f'{self.error_name}: {self.details}'
        return result

class IllegalCharacterError(Error):
    def __init__(self, details):
        super().init('Error: illegal character', details)
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
    def __init__(self, type, value = None):
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
        self.advance()
    
    def advance(self):
        self.pos += 1
        self.current_char = self.text[self.pos] if self.pos < len(self.text) else None
        
        
    def make_tokens(self):
        tokens = []
        
        while self.current_char != None:
            if self.current_char in ' \t':
                self.advance()
            elif self.current_char in DIGITS:
                tokens.append(self.make_number())
            elif self.current_char == '+':
                tokens.append(Token(TT_PLUS))
                self.advance()
            elif self.current_char == '-':
                tokens.append(Token(TT_MINUS))
                self.advance()
            elif self.current_char == '*':
                tokens.append(Token(TT_MUL))
                self.advance()
            elif self.current_char == '/':
                tokens.append(Token(TT_DIV))
                self.advance()
            elif self.current_char == '(':
                tokens.append(Token(TT_LPAREN))
                self.advance()
            elif self.current_char == ')':
                tokens.append(Token(TT_RPAREN))
                self.advance()
            else:
                char = self.current_char
                self.advance()
                return [], IllegalCharacterError(f"'{char}'")          
            
        return tokens, None

    def make_number(self):
        num_as_string = ""
        dot_count = 0
        
        while self.current_char != None and self.current_char in DIGITS + '.':
            if self.current_char == '.':
                if dot_count == 1: break
                dot_count += 1
                num_as_string += '.'
            else:
                num_as_string += self.current_char
            self.advance()
        
        if dot_count == 0:
            return Token(TT_INT, int(num_as_string))
        else:
            return Token(TT_FLOAT, float(num_as_string))
        
        
#########################################
# RUN
#########################################

def run(text):
    lexer = Lexer(text)
    tokens, error = lexer.make_tokens()
    
    return tokens, error