"""
IBTAC Language Lexical Analyzer
Main lexer implementation
Supports identifiers starting with 071, 070, or 047
Student ID: ***071 (identifiers must start with 071, 070, or 047)
"""

from typing import List, Optional
from .token_types import *
from .error_handler import ErrorHandler

class IbtacLexer:
    """Main lexical analyzer for IBTAC language"""
    
    def __init__(self, source_code: str):
        self.source = source_code
        self.position = 0
        self.line = 1
        self.column = 1
        self.error_handler = ErrorHandler()
        self.tokens: List[Token] = []
    
    def current_char(self) -> str:
        """Get current character"""
        if self.position >= len(self.source):
            return '\0'
        return self.source[self.position]
    
    def peek_char(self, offset: int = 1) -> str:
        """Look ahead at character"""
        pos = self.position + offset
        if pos >= len(self.source):
            return '\0'
        return self.source[pos]
    
    def advance(self) -> str:
        """Move to next character and return the character that was current"""
        if self.position >= len(self.source):
            return '\0'
        
        char = self.source[self.position]
        self.position += 1
        
        if char == '\n':
            self.line += 1
            self.column = 1
        else:
            self.column += 1
        
        return char
    
    def tokenize(self) -> List[Token]:
        """Main tokenization method"""
        self.tokens.clear()
        
        while self.position < len(self.source):
            start_line = self.line
            start_col = self.column
            
            token = self._scan_token()
            if token:
                # Update token position to start position
                token.line = start_line
                token.column = start_col
                self.tokens.append(token)
        
        # Add EOF token
        self.tokens.append(Token(TokenType.EOF, "", self.line, self.column))
        return self.tokens
    
    def _scan_token(self) -> Optional[Token]:
        """Scan and return next token"""
        char = self.current_char()
        
        if char == '\0':
            return None
        
        # Skip whitespace
        if is_whitespace(char):
            self.advance()
            return None
        
        # Handle newlines
        if is_newline(char):
            self.advance()
            return Token(TokenType.NEWLINE, char, self.line, self.column)
        
        # Single-line comments
        if char == '/' and self.peek_char() == '/':
            return self._scan_single_line_comment()
        
        # Multi-line comments
        if char == '/' and self.peek_char() == '*':
            return self._scan_multi_line_comment()
        
        # String literals (surrounded by $)
        if char == '$':
            return self._scan_string()
            
        # Check for identifiers first (must start with 071, 070, or 048)
        if (char == '0' and 
            ((self.peek_char() == '7' and self.peek_char(2) in ('0', '1')) or
             (self.peek_char() == '4' and self.peek_char(2) == '8'))):
            return self._scan_identifier()
        
        # Numbers (but not 07x or 048 pattern)
        if is_digit(char) or (char == '.' and is_digit(self.peek_char())):
            return self._scan_number()
        
                # Identifiers cannot start with underscore
        if char == '_':
            start_line = self.line
            start_col = self.column
            value = self.advance()
            # consume rest of word (letters, digits, underscores)
            while is_valid_identifier_char(self.current_char()):
                value += self.advance()
            return Token(TokenType.ERROR, value, start_line, start_col,
                         error_msg=f"Invalid identifier: {value}")

        # Keywords that don't start with numbers
        if is_letter(char):
            return self._scan_keyword()
        
        # Operators (including multi-character)
        if char in '+-*/=!<>':
            return self._scan_operator()
        
        # Single-character delimiters
        if char in DELIMITERS:
            self.advance()
            return Token(DELIMITERS[char], char, self.line, self.column)
        
        # Invalid character
        self.advance()
        return self.error_handler.handle_invalid_symbol(
            self.line, self.column, char
        )
    
    def _scan_single_line_comment(self) -> Token:
        """Scan single-line comment (//)"""
        start_line = self.line
        start_col = self.column
        comment = ""
        comment += self.advance()  # First /
        comment += self.advance()  # Second /
        
        while self.current_char() != '\n' and self.current_char() != '\0':
            comment += self.advance()
        
        return Token(TokenType.COMMENT, comment, start_line, start_col)
    
    def _scan_multi_line_comment(self) -> Token:
        """Scan multi-line comment (/* */)"""
        start_line = self.line
        start_col = self.column
        comment = ""
        comment += self.advance()  # /
        comment += self.advance()  # *
        
        while self.current_char() != '\0':
            # Check for nested comments (not allowed)
            if self.current_char() == '/' and self.peek_char() == '*':
                return self.error_handler.handle_nested_comment_error(
                    self.line, self.column
                )
            
            if self.current_char() == '*' and self.peek_char() == '/':
                comment += self.advance()  # *
                comment += self.advance()  # /
                return Token(TokenType.COMMENT, comment, start_line, start_col)
            
            comment += self.advance()
        
        # Unterminated comment
        return self.error_handler.handle_unterminated_comment(
            start_line, start_col
        )
    
    def _scan_string(self) -> Token:
        """Scan string literal surrounded by $"""
        start_line = self.line
        start_col = self.column
        string_value = ""
        string_value += self.advance()  # Opening $
        
        while self.current_char() != '\0' and self.current_char() != '\n':
            char = self.advance()
            string_value += char
            if char == '$':  # Closing $
                return Token(TokenType.STRING, string_value, start_line, start_col)
        
        # Unterminated string
        return self.error_handler.handle_unterminated_string(
            start_line, start_col, string_value
        )
    
    def _scan_number(self) -> Token:
        """Scan numeric literals"""
        start_line = self.line
        start_col = self.column
        number = ""
        has_dot = False
        
        # Handle starting with dot (.5 case)
        if self.current_char() == '.':
            number += self.advance()
            has_dot = True
        
        # Scan digits
        while is_digit(self.current_char()):
            number += self.advance()
        
        # Handle decimal point
        if self.current_char() == '.' and not has_dot:
            number += self.advance()
            has_dot = True
            while is_digit(self.current_char()):
                number += self.advance()
        
        # Handle exponential notation
        if self.current_char().lower() == 'e':
            number += self.advance()
            if self.current_char() in '+-':
                number += self.advance()
            if not is_digit(self.current_char()):
                return self.error_handler.handle_invalid_number(
                    start_line, start_col, number
                )
            while is_digit(self.current_char()):
                number += self.advance()
        
        # Validate number format
        if not self.error_handler.validate_number_format(number):
            return self.error_handler.handle_invalid_number(
                start_line, start_col, number
            )
        
        # Determine token type
        token_type = TokenType.FLOAT if has_dot or 'e' in number.lower() else TokenType.INTEGER
        return Token(token_type, number, start_line, start_col)
    
    def _scan_identifier(self) -> Token:
        """Scan identifiers starting with 071, 070, or 047"""
        start_line = self.line
        start_col = self.column

        # Capture the prefix
        prefix = self.advance()  # '0'
        prefix += self.advance()  # '7' or '4'
        prefix += self.advance()  # '1', '0', or '7'

        identifier = prefix

        # Continue with letters, digits, underscores
        while is_valid_identifier_char(self.current_char()):
            identifier += self.advance()

        # Validate the prefix
        if prefix in ("071", "070", "048"):
            return Token(TokenType.IDENTIFIER, identifier, start_line, start_col)
        else:
            return Token(TokenType.ERROR, identifier, start_line, start_col,
                     error_msg=f"Invalid identifier: {identifier}")

    
    def _scan_keyword(self) -> Token:
        """Scan potential keywords"""
        start_line = self.line
        start_col = self.column
        word = ""
        while is_valid_identifier_char(self.current_char()):
            word += self.advance()
        
        # Check if it's a valid keyword
        if word.lower() in KEYWORDS:
            return Token(KEYWORDS[word.lower()], word, start_line, start_col)
        
        # Not a keyword and doesn't start with 071/070/048
        return self.error_handler.handle_invalid_identifier(
            start_line, start_col, word
        )
    
    def _scan_operator(self) -> Token:
        """Scan operators"""
        start_line = self.line
        start_col = self.column
        char = self.current_char()
        
        # Check for multi-character operators
        if char + self.peek_char() in OPERATORS:
            op = char + self.peek_char()
            self.advance()
            self.advance()
            return Token(OPERATORS[op], op, start_line, start_col)
        elif char in OPERATORS:
            self.advance()
            return Token(OPERATORS[char], char, start_line, start_col)
        
        # Invalid operator
        self.advance()
        return self.error_handler.handle_invalid_symbol(
            start_line, start_col, char
        )
    
    def print_tokens(self):
        """Print all tokens for debugging"""
        print("=== TOKENS ===")
        for token in self.tokens:
            if not token.is_error():
                print(token)
        
        if self.error_handler.has_errors():
            print("\n=== ERRORS ===")
            print(self.error_handler.get_error_summary())
    
    def get_error_summary(self) -> str:
        """Get error summary from error handler"""
        return self.error_handler.get_error_summary()


# Example usage and test
if __name__ == "__main__":
    # Test code with new identifier rules
    test_code = """
    // This is a comment
    if (071variable == 42) {
        $hello world$
        071another_var = 3.14;
        070counter = .5;
        048_temp = 2.5e10;
    }
    /* Multi-line
       comment */
    """
    
    lexer = IbtacLexer(test_code)
    tokens = lexer.tokenize()
    lexer.print_tokens()
