#########################################
# CONSTANTS
#########################################

DIGITS = '0123456789'

#########################################
# ERRORS
#########################################

class Error:
    def __init__(self, pos_start, pos_end, error_name, details):
        self.pos_start = pos_start
        self.pos_end = pos_end
        self.error_name = error_name
        self.details = details
    
    def as_string(self):
        result = f'{self.error_name}: {self.details}'
        result += f'\n File {self.pos_start.fn}, line {self.pos_start.ln + 1}'
        return result

class IllegalCharacterError(Error):
    def __init__(self, pos_start, pos_end, details):
        super().__init__(pos_start, pos_end, 'Error: illegal character', details)

#########################################
# POSITION
#########################################

class Position:
    def __init__(self, idx, ln, col, fn, ftext):
        self.idx = idx
        self.ln = ln
        self.col = col
        self.fn = fn
        self.ftext = ftext
    
    def advance(self, current_char):
        self.idx += 1
        self.col += 1
        
        if current_char == '\n':
            self.ln += 1
            self.col = 0
        
        return self

    def copy(self):
        return Position(self.idx, self.ln, self.col, self.fn, self.ftext)
    
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
    def __init__(self, fn, text):
        self.fn = fn
        self.text = text
        self.pos = Position(-1, 0, -1, fn, text)
        self.current_char = None
        self.advance()
    
    def advance(self):
        self.pos.advance(self.current_char)
        self.current_char = self.text[self.pos.idx] if self.pos.idx < len(self.text) else None
        
        
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
                pos_start = self.pos.copy()
                char = self.current_char
                self.advance()
                return [], IllegalCharacterError(pos_start, self.pos.idx, f"'{char}'")          
            
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
# NODES
#########################################

class NumberNode:
    def __init__(self, tok):
        self.tok = tok
    
    def __repr__(self):
        return f'{self.tok}'
    
class BinOpNode:
    def __init__(self, left_node, op_tok, right_node):
        self.left_node = left_node
        self.op_tok = op_tok
        self.right_node = right_node
    
    def __repr__(self):
        return f'({self.left_node}, {self.op_tok}, {self.right_node})'
    
#########################################
# PARSER
#########################################

class Parser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.tok_idx = -1
        self.advance()

    def advance(self):
        self.tok_idx += 1
        if self.tok_idx < len(self.tokens):
            self.current_tok = self.tokens[self.tok_idx]
        
        return self.current_tok

    ############################################################3
    
    def parse(self):
        return self.expression()
    
    def factor(self):
        tok = self.current_tok
        if tok.type in (TT_INT, TT_FLOAT):
            self.advance()
            return NumberNode(tok)
    
    def term(self):
        return self.bin_op(self.factor, (TT_MUL, TT_DIV))
    
    def expression(self):
        return self.bin_op(self.term, (TT_PLUS, TT_MINUS))      
    
    def bin_op(self, func, ops):
        left = func()
        
        while self.current_tok.type in ops:
            op_tok = self.current_tok
            self.advance()
            right = func()
            left = BinOpNode(left, op_tok, right)
        
        return left 
#########################################
# RUN
#########################################

def run(fn, text):
    lexer = Lexer(fn, text)
    tokens, error = lexer.make_tokens()
    if error: return None, error
    
    parser = Parser(tokens)
    ast = parser.parse()
    return ast, None