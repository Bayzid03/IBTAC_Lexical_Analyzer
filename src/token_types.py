"""
Token Types for IBTAC Language Lexical Analyzer
Student ID: ***071 (identifiers must start with 071)
"""

from enum import Enum
from dataclasses import dataclass
from typing import Optional

class TokenType(Enum):
    # Literals
    IDENTIFIER = "IDENTIFIER"
    INTEGER = "INTEGER"
    FLOAT = "FLOAT"
    STRING = "STRING"
    
    # Keywords (only 5 keywords in IBTAC)
    IF = "IF"
    ELSE = "ELSE"
    WHILE = "WHILE"
    RETURN = "RETURN"
    FUNC = "FUNC"
    
    # Operators
    PLUS = "PLUS"                # +
    MINUS = "MINUS"              # -
    MULTIPLY = "MULTIPLY"        # *
    DIVIDE = "DIVIDE"            # /
    EQUAL = "EQUAL"              # ==
    NOT_EQUAL = "NOT_EQUAL"      # !=
    LESS_THAN = "LESS_THAN"      # <
    GREATER_THAN = "GREATER_THAN" # >
    LESS_EQUAL = "LESS_EQUAL"    # <=
    GREATER_EQUAL = "GREATER_EQUAL" # >=
    
    # Delimiters
    LPAREN = "LPAREN"            # (
    RPAREN = "RPAREN"            # )
    LBRACE = "LBRACE"            # {
    RBRACE = "RBRACE"            # }
    SEMICOLON = "SEMICOLON"      # ;
    COMMA = "COMMA"              # ,
    
    # Special
    COMMENT = "COMMENT"
    WHITESPACE = "WHITESPACE"
    NEWLINE = "NEWLINE"
    EOF = "EOF"
    
    # Error tokens
    ERROR = "ERROR"
    UNTERMINATED_STRING = "UNTERMINATED_STRING"
    INVALID_NUMBER = "INVALID_NUMBER"
    INVALID_SYMBOL = "INVALID_SYMBOL"

@dataclass
class Token:
    """Represents a token with its type, value, and position"""
    type: TokenType
    value: str
    line: int
    column: int
    error_msg: Optional[str] = None
    
    def __str__(self):
        if self.error_msg:
            return f"ERROR({self.type.value}): {self.error_msg} at line {self.line}, col {self.column}"
        return f"{self.type.value}({self.value}) at line {self.line}, col {self.column}"
    
    def is_error(self) -> bool:
        """Check if this token represents an error"""
        return self.type in [TokenType.ERROR, TokenType.UNTERMINATED_STRING, 
                           TokenType.INVALID_NUMBER, TokenType.INVALID_SYMBOL]

# Keywords mapping for IBTAC language
KEYWORDS = {
    'if': TokenType.IF,
    'else': TokenType.ELSE,
    'while': TokenType.WHILE,
    'return': TokenType.RETURN,
    'func': TokenType.FUNC  # Conflict: sometimes keyword, sometimes identifier
}

# Operator mappings
OPERATORS = {
    '+': TokenType.PLUS,
    '-': TokenType.MINUS,
    '*': TokenType.MULTIPLY,
    '/': TokenType.DIVIDE,
    '==': TokenType.EQUAL,
    '!=': TokenType.NOT_EQUAL,
    '<': TokenType.LESS_THAN,
    '>': TokenType.GREATER_THAN,
    '<=': TokenType.LESS_EQUAL,
    '>=': TokenType.GREATER_EQUAL,
}

# Single character delimiters
DELIMITERS = {
    '(': TokenType.LPAREN,
    ')': TokenType.RPAREN,
    '{': TokenType.LBRACE,
    '}': TokenType.RBRACE,
    ';': TokenType.SEMICOLON,
    ',': TokenType.COMMA,
}

def is_valid_identifier_start(char: str) -> bool:
    """
    Check if character can start an identifier
    Rule: Must start with '071' (last 3 digits of student ID)
    """
    return char == '0'  # First character of required prefix

def is_valid_identifier_char(char: str) -> bool:
    """Check if character can be part of identifier (letters, digits, underscore)"""
    return char.isalnum() or char == '_'

def is_digit(char: str) -> bool:
    """Check if character is a digit"""
    return char.isdigit()

def is_letter(char: str) -> bool:
    """Check if character is a letter"""
    return char.isalpha()

def is_whitespace(char: str) -> bool:
    """Check if character is whitespace (excluding newline)"""
    return char in ' \t\r'

def is_newline(char: str) -> bool:
    """Check if character is newline"""
    return char == '\n'
