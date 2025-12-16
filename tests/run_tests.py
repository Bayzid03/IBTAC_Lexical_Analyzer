"""
Simple Test Runner for IBTAC Lexical Analyzer
Run individual tests or create custom test cases
"""
import os
import sys

# Add the project root to the Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.lexer import IbtacLexer
from src.token_types import TokenType

def test_single_input(code: str, description: str = "Custom Test"):
    """Test a single input string"""
    print(f"\n{'='*50}")
    print(f"TEST: {description}")
    print(f"{'='*50}")
    print(f"Input: {repr(code)}")
    print(f"{'-'*50}")
    
    lexer = IbtacLexer(code)
    tokens = lexer.tokenize()
    
    print("Tokens:")
    for i, token in enumerate(tokens):
        if token.type == TokenType.EOF:
            print(f"{i+1:2d}. EOF")
            break
        elif token.type in [TokenType.WHITESPACE, TokenType.NEWLINE]:
            continue  # Skip whitespace for cleaner output
        elif token.is_error():
            print(f"{i+1:2d}. ❌ ERROR: {token.error_msg} at line {token.line}")
        else:
            print(f"{i+1:2d}. ✅ {token.type.value}('{token.value}') at line {token.line}")
    
    if lexer.error_handler.has_errors():
        print(f"\n⚠️ Total Errors: {lexer.error_handler.error_count}")

def quick_tests():
    """Run some quick tests to verify basic functionality"""
    
    # Test 1: Valid identifiers (all three prefixes)
    test_single_input("071bayzid 071test_var 071x", "Valid Identifiers (071)")
    test_single_input("070shoaib 070temp_val 070z", "Valid Identifiers (070)")
    test_single_input("048_asif 048global 048a", "Valid Identifiers (048)")
    
    # Test 2: Invalid identifiers  
    test_single_input("name 071name _071invalid", "Invalid Identifiers")
    
    # Test 3: Numbers
    test_single_input("123 .5 3.14 2.5e10 .invalid", "Number Literals")
    
    # Test 4: Keywords
    test_single_input("if else while return func", "Keywords")
    
    # Test 5: Strings
    test_single_input('$hello$ $world$ $unterminated', "String Literals")
    
    # Test 6: Operators
    test_single_input("+ - * / == != < > <= >= <>", "Operators")
    
    # Test 7: Comments
    test_single_input("// single line\n/* multi line */", "Comments")

def interactive_test():
    """Interactive testing mode"""
    print("\n" + "="*50)
    print("INTERACTIVE TESTING MODE")
    print("="*50)
    print("Enter IBTAC code to tokenize (press Ctrl+C to exit)")
    print("Examples:")
    print("  071name = .5")  
    print("  func 071test() { return $hello$ }")
    print("  /* comment */ 071x + 070y + 048z")
    print("  070counter = 048_temp + 071value")
    
    while True:
        try:
            code = input("\n> ").strip()
            if not code:
                continue
            
            test_single_input(code, "Interactive Input")
            
        except KeyboardInterrupt:
            print("\n\nExiting interactive mode...")
            break
        except Exception as e:
            print(f"Error: {e}")

def test_your_details():
    """Test with your specific name and ID - CUSTOMIZE THIS!"""
    print("\n" + "="*50)
    print("PERSONAL VERIFICATION TEST")
    print("="*50)
    
    your_name_as_identifier = "071bayzid"
    another_valid_id = "070shoaib"
    another_valid_id2 = "048_asif" 
    your_id_as_identifier = "0712025"
    
    test_code = f"{your_name_as_identifier} {your_id_as_identifier} {another_valid_id} 048student"
    
    print(f"Testing your name as identifier: {your_name_as_identifier}")
    print(f"Testing your ID as identifier: {your_id_as_identifier}")
    print(f"Testing another valid ID: {another_valid_id}")
    print(f"Testing another valid ID: {another_valid_id2}")
    
    test_single_input(test_code, "Personal Details Verification (as identifiers)")

if __name__ == "__main__":
    import sys
    
    print("IBTAC Lexical Analyzer - Test Runner")
    print("Student ID: ***071")
    
    if len(sys.argv) > 1:
        mode = sys.argv[1].lower()
        
        if mode == "quick":
            quick_tests()
        elif mode == "interactive":
            interactive_test()
        elif mode == "personal":
            test_your_details()
        elif mode == "custom" and len(sys.argv) > 2:
            custom_code = " ".join(sys.argv[2:])
            test_single_input(custom_code, "Command Line Input")
        else:
            print("Usage:")
            print("  python run_tests.py quick       # Run quick tests")
            print("  python run_tests.py interactive # Interactive mode")
            print("  python run_tests.py personal    # Test your name/ID")
            print("  python run_tests.py custom <code> # Test custom code")
    else:
        # Default: run quick tests
        quick_tests()
        
        # Ask for interactive mode
        try:
            choice = input("\nRun interactive tests? (y/n): ").lower()
            if choice == 'y':
                interactive_test()
        except KeyboardInterrupt:
            print("\nExiting...")
