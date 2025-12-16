"""
IBTAC Lexical Analyzer - Gradio Web Interface
Interactive web UI for testing the lexical analyzer
"""

import gradio as gr
import pandas as pd
from src.lexer import IbtacLexer
from src.token_types import TokenType

class GradioLexerApp:
    def __init__(self):
        self.test_cases = {
            "Valid Identifiers (071)": "071name 071test_var 071student_id",
            "Valid Identifiers (070)": "070counter 070temp_val 070z",
            "Valid Identifiers (048)": "048_temp 048global 048a",
            "Invalid Identifiers": "name _071invalid 071 abc123",
            "Numbers": "123 .5 3.14 2.5e10 .invalid 0.123",
            "Keywords": "if else while return func 071func 070func 048func", # func is keyword, 07xfunc is identifier
            "String Literals": '$hello world$ $test$ $unterminated',
            "Operators": "+ - * / == != < > <= >= <>",
            "Comments": "// single line comment\n/* multi-line comment */",
            "Mixed Code": """// IBTAC sample
func 071main() {
    071x = .5 + 3.14
    070counter = 048_temp
    if 071x > 0 {
        071msg = $Hello IBTAC$
        return 071msg
    }
}""",
            "Error Cases": """_invalid 071name
$unterminated_string
/* unterminated comment
071x = .invalid.number""",
            "Assignment Test Cases": """// Test 1: Leading underscore
_071test 070valid _invalid

// Test 2: func keyword vs identifier (func is keyword, 07xfunc is identifier)
func 071func 070func 048func

// Test 3: .5 number format
.5 3.14 .0

// Test 4: Multi-line string (should error)
$single$ $multi
line$

// Test 5: <> operators
< > <> <= >=

// Test 6: Nested comments (should error)
/* outer /* inner */ */

// Test 7: Name and ID (customize this!)
071YourName 070YourID 048student"""
        }
    
    def analyze_code(self, input_code, show_whitespace=False, show_comments=True):
        """Analyze input code and return results"""
        if not input_code.strip():
            return "Please enter some IBTAC code to analyze.", "", ""
        
        try:
            lexer = IbtacLexer(input_code)
            tokens = lexer.tokenize()
            
            # Generate token table
            token_data = []
            error_data = []
            
            for i, token in enumerate(tokens):
                if token.type == TokenType.EOF:
                    break
                
                # Filter tokens based on settings
                if not show_whitespace and token.type in [TokenType.WHITESPACE, TokenType.NEWLINE]:
                    continue
                if not show_comments and token.type == TokenType.COMMENT:
                    continue
                
                if token.is_error():
                    error_data.append({
                        "Line": token.line,
                        "Column": token.column,
                        "Error Type": token.type.value,
                        "Value": token.value,
                        "Message": token.error_msg or "Unknown error"
                    })
                else:
                    token_data.append({
                        "Index": len(token_data) + 1,
                        "Token Type": token.type.value,
                        "Value": token.value,
                        "Line": token.line,
                        "Column": token.column
                    })
            
            # Create DataFrames
            tokens_df = pd.DataFrame(token_data)
            errors_df = pd.DataFrame(error_data)
            
            # Generate summary
            summary = self._generate_summary(tokens, lexer.error_handler)
            
            return summary, tokens_df, errors_df
            
        except Exception as e:
            return f"❌ **Error during analysis:** {str(e)}", pd.DataFrame(), pd.DataFrame()
    
    def _generate_summary(self, tokens, error_handler):
        """Generate analysis summary"""
        total_tokens = len([t for t in tokens if t.type != TokenType.EOF])
        meaningful_tokens = len([t for t in tokens if t.type not in [TokenType.WHITESPACE, TokenType.NEWLINE, TokenType.EOF]])
        errors = error_handler.error_count
        
        # Count token types
        token_counts = {}
        for token in tokens:
            if token.type == TokenType.EOF:
                continue
            if token.type in token_counts:
                token_counts[token.type] += 1
            else:
                token_counts[token.type] = 1
        
        # Generate summary text
        summary = f"""## 📊 **Analysis Summary**
        
**Total Tokens:** {total_tokens}  
**Meaningful Tokens:** {meaningful_tokens}  
**Errors Found:** {errors}  
**Status:** {'✅ Success' if errors == 0 else '⚠️ Errors Detected'}

### **Token Distribution:**
"""
        
        for token_type, count in sorted(token_counts.items(), key=lambda x: x[1], reverse=True):
            if token_type not in [TokenType.WHITESPACE, TokenType.NEWLINE]:
                summary += f"- **{token_type.value}:** {count}\n"
        
        if errors > 0:
            summary += f"\n### ⚠️ **Error Summary:**\n{error_handler.get_error_summary()}"
        
        return summary
    
    def load_example(self, example_name):
        """Load example code"""
        return self.test_cases.get(example_name, "")
    
    def run_assignment_tests(self):
        """Run all 7 assignment test cases"""
        test_results = []
        
        test_cases_data = [
            ("Leading underscore", " _071test _invalid 071valid"),
            ("func keyword/identifier", "func 071func 070func 048func"),
            ("Number .5 format", ".5 3.14 .0"),
            ("Multi-line strings", '$single$ $multi\nline$'),
            ("<> operators", "< > <> <= >="),
            ("Nested comments", "/* outer /* inner */ */"),
            ("Name & ID (Update Examples!)", "071Bayzid 070Shoaib 048Asif 0712025")
        ]
        
        for test_name, test_input in test_cases_data:
            lexer = IbtacLexer(test_input)
            tokens = lexer.tokenize()
            
            # Analyze results
            meaningful_tokens = [t for t in tokens if t.type not in [TokenType.WHITESPACE, TokenType.NEWLINE, TokenType.EOF]]
            errors = len([t for t in meaningful_tokens if t.is_error()])
            success_tokens = len([t for t in meaningful_tokens if not t.is_error()])
            
            # Determine expected vs actual
            if test_name == "Leading underscore":
                expected = "1 valid, 2 errors" # Only 071valid is valid now
                actual = f"{success_tokens} valid, {errors} errors"
                passed = success_tokens == 1 and errors == 2 # Assuming 071valid is the only valid one
            elif test_name == "func keyword/identifier":
                expected = "1 keyword, 3 identifiers" # func is keyword, 071func, 070func, 048func are identifiers
                actual = f"{success_tokens} tokens, {errors} errors"
                passed = success_tokens == 4 and errors == 0 # 1 keyword + 3 identifiers
            elif test_name == "Number .5 format":
                expected = "3 valid numbers"
                actual = f"{success_tokens} numbers, {errors} errors"
                passed = success_tokens >= 3
            elif test_name == "Multi-line strings":
                expected = "1 valid, 1 error" # $single$ is valid, multi-line part errors
                actual = f"{success_tokens} valid, {errors} errors"
                passed = errors >= 1  # Multi-line should error
            elif test_name == "<> operators":
                expected = "Separate < > tokens"
                actual = f"{success_tokens} operators"
                passed = success_tokens >= 5 # <, >, <, >, <=, >= (<> is two separate tokens)
            elif test_name == "Nested comments":
                expected = "Error (not supported)"
                actual = f"{errors} errors"
                passed = errors >= 1
            else:  # Name & ID - Note: This is the most flexible test
                # Expect at least 3 identifiers if the user customizes the input correctly
                expected = "At least 3 valid identifiers (customize input!)"
                actual = f"{success_tokens} identifiers"
                passed = success_tokens >= 3 # This is a flexible check; depends on user input

            # More specific check for Leading underscore test
            if test_name == "Leading underscore":
                 # Count identifiers starting with 071, 070, 048
                 valid_ident_count = len([t for t in meaningful_tokens if t.type == TokenType.IDENTIFIER and t.value.startswith(('071', '070', '048'))])
                 # Count errors (invalid identifiers like _071test, _invalid)
                 error_count = len([t for t in meaningful_tokens if t.is_error()])
                 # Expect 1 valid (071valid) and 2 errors (_071test, _invalid)
                 passed = valid_ident_count == 1 and error_count == 2


            test_results.append({
                "Test Case": test_name,
                "Input": test_input[:30] + "..." if len(test_input) > 30 else test_input,
                "Expected": expected,
                "Actual": actual,
                "Result": "✅ PASS" if passed else "❌ FAIL"
            })
        
        results_df = pd.DataFrame(test_results)
        
        passed_count = len([r for r in test_results if r["Result"].startswith("✅")])
        summary = f"""## 🧪 **Assignment Test Results**
        
**Tests Passed:** {passed_count}/7  
**Success Rate:** {(passed_count/7)*100:.1f}%  
**Status:** {'✅ All tests passed!' if passed_count == 7 else '⚠️ Some tests failed'}

### **Important Notes:**
- **Test 7** requires your actual name and ID as identifiers (e.g., 071Bayzid, 071888443).
- Failing tests may be intentional based on conflict resolutions (e.g., <> -> < >).
- Check individual test results below for details.
- **Test 1 (Leading underscore)**: Only identifiers starting with 071/070/048 are valid.
- **Test 2 (func)**: `func` is a keyword, `071func`, `070func`, `048func` are identifiers.
"""
        
        return summary, results_df

def create_interface():
    """Create and configure Gradio interface"""
    app = GradioLexerApp()
    
    with gr.Blocks(
        title="IBTAC Lexical Analyzer",
        theme=gr.themes.Soft(),
        css="""
        .gradio-container {
            max-width: 1200px;
            margin: auto;
        }
        .tab-nav button {
            font-size: 16px;
            font-weight: bold;
        }
        """
    ) as interface:
        
        gr.Markdown("""
        # 🔍 **IBTAC Lexical Analyzer**
        ### Interactive Web Interface for Compiler Design Assignment  
        """)
        
        with gr.Tabs():
            # Tab 1: Main Analyzer
            with gr.Tab("📝 Code Analyzer", elem_id="main-tab"):
                with gr.Row():
                    with gr.Column(scale=1):
                        gr.Markdown("### **Input IBTAC Code**")
                        
                        example_dropdown = gr.Dropdown(
                            choices=list(app.test_cases.keys()),
                            label="📋 Load Example",
                            value=None,
                            interactive=True
                        )
                        
                        input_code = gr.Textbox(
                            label="IBTAC Source Code",
                            placeholder="Enter your IBTAC code here...\n\nExample:\nfunc 071main() {\n    071x = .5\n    070counter = 048_temp\n    return $Hello IBTAC$\n}",
                            lines=10,
                            interactive=True
                        )
                        
                        with gr.Row():
                            analyze_btn = gr.Button("🔍 Analyze Code", variant="primary", size="lg")
                            clear_btn = gr.Button("🗑️ Clear", variant="secondary")
                        
                        with gr.Row():
                            show_whitespace = gr.Checkbox(label="Show Whitespace Tokens", value=False)
                            show_comments = gr.Checkbox(label="Show Comments", value=True)
                    
                    with gr.Column(scale=2):
                        summary_output = gr.Markdown("### Enter code and click 'Analyze' to see results")
                        
                        tokens_output = gr.Dataframe(
                            headers=["Index", "Token Type", "Value", "Line", "Column"],
                            label="🎯 Generated Tokens",
                            interactive=False,
                            wrap=True
                        )
                        
                        errors_output = gr.Dataframe(
                            headers=["Line", "Column", "Error Type", "Value", "Message"],
                            label="❌ Lexical Errors",
                            interactive=False,
                            wrap=True
                        )
            
            # Tab 2: Assignment Tests
            with gr.Tab("🧪 Assignment Tests", elem_id="test-tab"):
                gr.Markdown("""
                ### **Official Assignment Test Cases**
                These are the 7 mandatory test cases required by the assignment.
                """)
                
                test_btn = gr.Button("▶️ Run All Assignment Tests", variant="primary", size="lg")
                
                test_summary = gr.Markdown()
                test_results = gr.Dataframe(
                    headers=["Test Case", "Input", "Expected", "Actual", "Result"],
                    label="📊 Test Results Table",
                    interactive=False,
                    wrap=True
                )
            
            # Tab 3: Language Reference
            with gr.Tab("📖 IBTAC Reference", elem_id="reference-tab"):
                gr.Markdown("""
                ## **IBTAC Language Specification**
                
                ### **🔤 Identifiers**
                - **Must start with:** `071`, `070`, or `048`
                - **Can contain:** Letters, digits, underscores
                - **Valid:** `071name`, `071test_var`, `070counter`, `048_temp`
                - **Invalid:** `name`, `_071test`, `abc071`, `072var`
                
                ### **🔑 Keywords** (only 5)
                ```
                if    else    while    return    func
                ```
                
                ### **🔢 Numbers**
                - **Integers:** `123`, `0`, `999`
                - **Floats:** `3.14`, `.5`, `0.123`
                - **Exponential:** `1.5e10`, `2E-5`
                
                ### **📝 String Literals**
                - **Format:** Surrounded by `$` signs
                - **Example:** `$Hello World$`, `$test$`
                - **Multi-line:** Not supported (will error)
                
                ### **⚡ Operators**
                ```
                +  -  *  /  ==  !=  <  >  <=  >=
                ```
                - **Note:** `<>` treated as separate `<` and `>` tokens
                
                ### **💬 Comments**
                - **Single-line:** `// comment`
                - **Multi-line:** `/* comment */`
                - **Nested multi-line:** Not supported
                
                ### **🎯 Design Decisions (Conflicts Resolved)**
                1. **Identifiers must start with `071`, `070`, or `048`** (not underscore)
                2. **`.5` number format is valid** (no leading zero required)
                3. **`func` is keyword by default**, `071func`, `070func`, `048func` are identifiers.
                4. **Multi-line strings not supported**
                5. **Nested comments cause errors**
                6. **`<>` parsed as separate `<` `>` tokens**
                """)
        
        # Event handlers
        example_dropdown.change(
            fn=app.load_example,
            inputs=[example_dropdown],
            outputs=[input_code]
        )
        
        analyze_btn.click(
            fn=app.analyze_code,
            inputs=[input_code, show_whitespace, show_comments],
            outputs=[summary_output, tokens_output, errors_output]
        )
        
        clear_btn.click(
            fn=lambda: ("", None, pd.DataFrame(), pd.DataFrame()),
            inputs=[],
            outputs=[input_code, summary_output, tokens_output, errors_output]
        )
        
        test_btn.click(
            fn=app.run_assignment_tests,
            inputs=[],
            outputs=[test_summary, test_results]
        )
    
    return interface

if __name__ == "__main__":
    # Create and launch the interface
    app = create_interface()
    
    # Launch the app locally
    app.launch(
        server_name="127.0.0.1",  # Localhost only
        server_port=7861,         # Using port 7861 since 7860 is in use
        show_error=True           # Show detailed errors
    )
