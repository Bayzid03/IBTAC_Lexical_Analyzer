"""
Error Handler for IBTAC Language Lexical Analyzer
Handles lexical errors and recovery strategies
Supports identifiers starting with 071, 070, or 047
"""

from typing import List, Optional
from .token_types import Token, TokenType

class LexicalError(Exception):
    """Custom exception for lexical errors"""
    def __init__(self, message: str, line: int, column: int):
        self.message = message
        self.line = line
        self.column = column
        super().__init__(f"Lexical Error at line {line}, col {column}: {message}")

class ErrorHandler:
    """Handles lexical analysis errors and recovery"""
    
    def __init__(self):
        self.errors: List[Token] = []
        self.error_count = 0
    
    def report_error(self, error_type: TokenType, message: str, line: int, column: int, lexeme: str = "") -> Token:
        """Report a lexical error and create error token"""
        self.error_count += 1
        error_token = Token(
            type=error_type,
            value=lexeme,
            line=line,
            column=column,
            error_msg=message
        )
        self.errors.append(error_token)
        return error_token
    
    def handle_unterminated_string(self, line: int, column: int, partial_string: str) -> Token:
        """Handle unterminated string literals"""
        return self.report_error(
            TokenType.UNTERMINATED_STRING,
            f"Unterminated string literal: '{partial_string}'",
            line,
            column,
            partial_string
        )
    
    def handle_invalid_number(self, line: int, column: int, invalid_number: str) -> Token:
        """Handle malformed number literals"""
        return self.report_error(
            TokenType.INVALID_NUMBER,
            f"Invalid number format: '{invalid_number}'",
            line,
            column,
            invalid_number
        )
    
    def handle_invalid_symbol(self, line: int, column: int, symbol: str) -> Token:
        """Handle unrecognized symbols"""
        return self.report_error(
            TokenType.INVALID_SYMBOL,
            f"Invalid symbol: '{symbol}'",
            line,
            column,
            symbol
        )
    
    def handle_invalid_identifier(self, line: int, column: int, identifier: str) -> Token:
        """Handle identifiers that don't follow the 071/070/048 rule"""
        return self.report_error(
            TokenType.ERROR,
            f"Invalid identifier: '{identifier}' (must start with '071', '070', or '048')",
            line,
            column,
            identifier
        )
    
    def handle_nested_comment_error(self, line: int, column: int) -> Token:
        """Handle nested multi-line comment issues"""
        return self.report_error(
            TokenType.ERROR,
            "Nested multi-line comments are not supported",
            line,
            column,
            "/*"
        )
    
    def handle_unterminated_comment(self, line: int, column: int) -> Token:
        """Handle unterminated multi-line comments"""
        return self.report_error(
            TokenType.ERROR,
            "Unterminated multi-line comment",
            line,
            column,
            "/*"
        )
    
    def get_error_summary(self) -> str:
        """Get a summary of all errors encountered"""
        if self.error_count == 0:
            return "No lexical errors found."
        
        summary = f"Found {self.error_count} lexical error(s):\n"
        for i, error in enumerate(self.errors, 1):
            summary += f"{i}. {error}\n"
        return summary
    
    def has_errors(self) -> bool:
        """Check if any errors were encountered"""
        return self.error_count > 0
    
    def clear_errors(self):
        """Clear all recorded errors"""
        self.errors.clear()
        self.error_count = 0
    
    def panic_mode_recovery(self, current_char: str) -> bool:
        """
        Simple panic mode recovery strategy
        Skip characters until we find a synchronizing token
        """
        sync_chars = {';', '\n', '}', ')', '$'}  # Synchronizing characters
        return current_char in sync_chars
    
    def validate_identifier_format(self, identifier: str) -> bool:
        """
        Validate identifier according to IBTAC rules
        Must start with '071', '070', or '048' (student ID last 3 digits)
        """
        if len(identifier) < 3:
            return False
        return identifier.startswith(('071', '070', '048'))
    
    def validate_number_format(self, number_str: str) -> bool:
        """
        Validate number format for integers and floats
        Handles exponential notation and edge cases
        """
        try:
            # Handle different number formats
            if 'e' in number_str.lower() or 'E' in number_str:
                # Exponential notation
                float(number_str)
                return True
            elif '.' in number_str:
                # Float - check for edge case like .5
                if number_str.startswith('.'):
                    # Decision: Allow .5 format (conflict resolution)
                    float(number_str)
                    return True
                else:
                    float(number_str)
                    return True
            else:
                # Integer
                int(number_str)
                return True
        except ValueError:
            return False
    
    def suggest_correction(self, error_token: Token) -> Optional[str]:
        """Suggest possible corrections for common errors"""
        if error_token.type == TokenType.ERROR and "must start with" in error_token.error_msg:
            # Generic suggestion for identifier format
            return f"Try starting the identifier with '071', '070', or '048'."
        elif error_token.type == TokenType.UNTERMINATED_STRING:
            return f"Add closing '$' to complete string: '{error_token.value}$'"
        elif error_token.type == TokenType.INVALID_NUMBER:
            return "Check number format - use digits, decimal point, or exponential notation"
        return None 
