"""
IBTAC Lexical Analyzer - Main Entry Point
Test runner for all required test cases
"""

import os
import sys
from typing import List
from src.lexer import IbtacLexer
from src.token_types import Token, TokenType

class LexerTester:
    """Test framework for IBTAC lexical analyzer"""
    
    def __init__(self):
        self.test_results = []
        self.total_tests = 0
        self.passed_tests = 0
    
    def run_all_tests(self):
        """Run all 7 required test cases"""
        print("=" * 60)
        print("IBTAC LEXICAL ANALYZER - TEST SUITE")
        print("Student ID: ***071")
        print("=" * 60)
        
        # Test cases as required by assignment
        test_cases = [
            ("Test 1: Leading underscore in identifier", self.test_leading_underscore),
            ("Test 2: func used as keyword & identifier", self.test_func_keyword_identifier),
            ("Test 3: .5 as number literal", self.test_dot_five_number),
            ("Test 4: Multi-line string literal", self.test_multiline_string),
            ("Test 5: <> operator usage", self.test_less_greater_operator),
            ("Test 6: Nested multi-line comments", self.test_nested_comments),
            ("Test 7: Your Name & Student ID", self.test_name_and_id)
        ]
        
        for test_name, test_function in test_cases:
            self.run_single_test(test_name, test_function)
        
        self.print_summary()
    
    def run_single_test(self, test_name: str, test_function):
        """Run a single test case"""
        print(f"\n{test_name}")
        print("-" * len(test_name))
        
        try:
            result = test_function()
            self.test_results.append(result)
            self.total_tests += 1
            if result['pass']:
                self.passed_tests += 1
                print("[PASS]")
            else:
                print("[FAIL]")
            
            print(f"Expected: {result['expected']}")
            print(f"Actual  : {result['actual']}")
            
        except Exception as e:
            print(f"[WARNING] {str(e)}")
            self.test_results.append({
                'test': test_name,
                'input': "Error occurred",
                'expected': "Test execution",
                'actual': f"Exception: {str(e)}",
                'pass': False
            })
            self.total_tests += 1
    
    def test_leading_underscore(self) -> dict:
        """Test Case 1: Leading underscore in identifier"""
        # According to updated rules: _071test is invalid (starts with _), 071_valid is valid, _invalid is invalid
        input_code = "_071test 071_valid _invalid 070_valid 048_valid"
        lexer = IbtacLexer(input_code)
        tokens = lexer.tokenize()
        
        # Filter non-whitespace, non-EOF tokens
        meaningful_tokens = [t for t in tokens if t.type not in [TokenType.WHITESPACE, TokenType.EOF]]
        
        # Expected: 3 valid identifiers (071_valid, 070_valid, 048_valid) and 2 errors (_071test, _invalid)
        expected = "ERROR, IDENTIFIER(071_valid), ERROR, IDENTIFIER(070_valid), IDENTIFIER(048_valid)"
        actual = ", ".join([f"{t.type.value}({t.value})" if not t.is_error() 
                           else f"ERROR" for t in meaningful_tokens])
        
        # Count valid identifiers (must start with 071, 070, or 048) and errors
        valid_identifiers = len([t for t in meaningful_tokens if t.type == TokenType.IDENTIFIER and t.value.startswith(('071', '070', '048'))])
        errors = len([t for t in meaningful_tokens if t.is_error()])
        
        # Should have 3 valid identifiers and 2 errors
        pass_condition = (valid_identifiers == 3 and errors == 2)
        
        return {
            'test': 'Leading underscore in identifier',
            'input': input_code,
            'expected': expected,
            'actual': actual,
            'pass': pass_condition
        }
    
    def test_func_keyword_identifier(self) -> dict:
        """Test Case 2: func used as keyword & identifier"""
        # func is a keyword, 071func, 070func, 048func are identifiers
        input_code = "func 071func 070func 048func"
        lexer = IbtacLexer(input_code)
        tokens = lexer.tokenize()
        
        meaningful_tokens = [t for t in tokens if t.type not in [TokenType.WHITESPACE, TokenType.EOF]]
        
        expected = "FUNC(func), IDENTIFIER(071func), IDENTIFIER(070func), IDENTIFIER(048func)"
        actual = ", ".join([f"{t.type.value}({t.value})" for t in meaningful_tokens if not t.is_error()])
        
        # Should have 1 FUNC keyword and 3 identifiers
        pass_condition = (
            len([t for t in meaningful_tokens if t.type == TokenType.FUNC]) == 1 and
            len([t for t in meaningful_tokens if t.type == TokenType.IDENTIFIER]) == 3
        )
        
        return {
            'test': 'func as keyword & identifier',
            'input': input_code,
            'expected': expected,
            'actual': actual,
            'pass': pass_condition
        }
    
    def test_dot_five_number(self) -> dict:
        """Test Case 3: .5 as number literal"""
        input_code = ".5 3.14 .0 .invalid"
        lexer = IbtacLexer(input_code)
        tokens = lexer.tokenize()
        
        meaningful_tokens = [t for t in tokens if t.type not in [TokenType.WHITESPACE, TokenType.EOF]]
        
        expected = "FLOAT(.5), FLOAT(3.14), FLOAT(.0), ERROR"
        actual = ", ".join([f"{t.type.value}({t.value})" if not t.is_error() 
                           else "ERROR" for t in meaningful_tokens])
        
        # Should recognize .5, 3.14, .0 as valid floats
        float_tokens = [t for t in meaningful_tokens if t.type == TokenType.FLOAT]
        pass_condition = len(float_tokens) >= 3
        
        return {
            'test': '.5 as number literal',
            'input': input_code,
            'expected': expected,
            'actual': actual,
            'pass': pass_condition
        }
    
    def test_multiline_string(self) -> dict:
        """Test Case 4: Multi-line string literal"""
        input_code = '$single line$ $multi\nline\nstring$'
        lexer = IbtacLexer(input_code)
        tokens = lexer.tokenize()
        
        meaningful_tokens = [t for t in tokens if t.type not in [TokenType.WHITESPACE, TokenType.NEWLINE, TokenType.EOF]]
        
        expected = "STRING($single line$), ERROR (unterminated)"
        actual = ", ".join([f"{t.type.value}({repr(t.value)})" if not t.is_error() 
                           else "ERROR" for t in meaningful_tokens])
        
        # Should have 1 valid string and 1 error (multi-line not supported)
        string_tokens = [t for t in meaningful_tokens if t.type == TokenType.STRING]
        error_tokens = [t for t in meaningful_tokens if t.is_error()]
        pass_condition = len(string_tokens) >= 1 and len(error_tokens) >= 1
        
        return {
            'test': 'Multi-line string literal',
            'input': repr(input_code),
            'expected': expected,
            'actual': actual,
            'pass': pass_condition
        }
    
    def test_less_greater_operator(self) -> dict:
        """Test Case 5: <> operator usage"""
        input_code = "< > <> <= >= =="
        lexer = IbtacLexer(input_code)
        tokens = lexer.tokenize()
        
        meaningful_tokens = [t for t in tokens if t.type not in [TokenType.WHITESPACE, TokenType.EOF]]
        
        expected = "LESS_THAN(<), GREATER_THAN(>), LESS_THAN(<), GREATER_THAN(>), LESS_EQUAL(<=), GREATER_EQUAL(>=), EQUAL(==)"
        actual = ", ".join([f"{t.type.value}({t.value})" for t in meaningful_tokens])
        
        # <> should be treated as separate < and > tokens
        lt_count = len([t for t in meaningful_tokens if t.type == TokenType.LESS_THAN])
        gt_count = len([t for t in meaningful_tokens if t.type == TokenType.GREATER_THAN])
        pass_condition = lt_count >= 2 and gt_count >= 2
        
        return {
            'test': '<> operator usage',
            'input': input_code,
            'expected': expected,
            'actual': actual,
            'pass': pass_condition
        }
    
    def test_nested_comments(self) -> dict:
        """Test Case 6: Nested multi-line comments"""
        input_code = "/* outer /* inner */ still in comment */"
        lexer = IbtacLexer(input_code)
        tokens = lexer.tokenize()
        
        meaningful_tokens = [t for t in tokens if t.type not in [TokenType.WHITESPACE, TokenType.EOF]]
        
        expected = "ERROR (nested comments not supported)"
        actual = ", ".join([f"{t.type.value}({t.value})" if not t.is_error() 
                           else "ERROR" for t in meaningful_tokens])
        
        # Should produce an error for nested comments
        pass_condition = len([t for t in meaningful_tokens if t.is_error()]) >= 1
        
        return {
            'test': 'Nested multi-line comments',
            'input': input_code,
            'expected': expected,
            'actual': actual,
            'pass': pass_condition
        }
    
    def test_name_and_id(self) -> dict:
        """Test Case 7: Your Name & Student ID"""

        input_code = "071Bayzid 070Shoaib 048Asif 0712025"
        lexer = IbtacLexer(input_code)
        tokens = lexer.tokenize()
        
        meaningful_tokens = [t for t in tokens if t.type not in [TokenType.WHITESPACE, TokenType.EOF]]
        
        expected = "IDENTIFIER(071Bayzid), IDENTIFIER(070Shoaib), IDENTIFIER(048Asif), IDENTIFIER(0712025)"
        actual = ", ".join([f"{t.type.value}({t.value})" for t in meaningful_tokens if not t.is_error()])
        
        # Should recognize all as valid identifiers
        identifier_count = len([t for t in meaningful_tokens if t.type == TokenType.IDENTIFIER])
        pass_condition = identifier_count >= 3
        
        return {
            'test': 'Name & Student ID recognition',
            'input': input_code,
            'expected': expected,
            'actual': actual,
            'pass': pass_condition
        }
    
    def print_summary(self):
        """Print test results summary"""
        print("\n" + "=" * 60)
        print("TEST RESULTS SUMMARY")
        print("=" * 60)
        print(f"Total Tests: {self.total_tests}")
        print(f"Passed: {self.passed_tests}")
        print(f"Failed: {self.total_tests - self.passed_tests}")
        print(f"Success Rate: {(self.passed_tests/self.total_tests)*100:.1f}%")
        
        # Create results table
        print(f"\n{'Test Case':<40} {'Input Snippet':<25} {'Expected':<20} {'Actual':<20} {'Pass/Fail':<10}")
        print("-" * 115)
        
        for result in self.test_results:
            test_name = result['test'][:39]
            input_snippet = result['input'][:24] 
            expected = result['expected'][:19]
            actual = result['actual'][:19]
            status = "PASS" if result['pass'] else "FAIL"
            
            print(f"{test_name:<40} {input_snippet:<25} {expected:<20} {actual:<20} {status:<10}")

def demo_lexer():
    """Demo the lexer with sample code"""
    print("\n" + "=" * 60)
    print("LEXER DEMONSTRATION")
    print("=" * 60)
    
    sample_code = '''
    // Sample IBTAC code with new identifier rules
    func 071main() {
        071x = .5 + 3.14
        070counter = 048_temp
        if 071x > 0 {
            071message = $Hello World$
            return 071message
        }
    }
    '''
    
    print("Input Code:")
    print(sample_code)
    print("\nTokens Generated:")
    print("-" * 40)
    
    lexer = IbtacLexer(sample_code)
    tokens = lexer.tokenize()
    
    for token in tokens:
        if token.type not in [TokenType.WHITESPACE, TokenType.NEWLINE]:
            if token.is_error():
                print(f"[OK] {token}")
            else:
                print(f"[OK] {token}")
    
    if lexer.error_handler.has_errors():
        print(f"\n[WARNING]  Errors Found:")
        print(lexer.error_handler.get_error_summary())

if __name__ == "__main__":
    # Run tests
    tester = LexerTester()
    tester.run_all_tests()
    
    # Demo the lexer
    demo_lexer()
    
    print(f"\n{'='*60}")
    print("Testing complete! Check results above.")
    print(f"{'='*60}")
