<img width="1524" height="884" alt="Screenshot (246)" src="https://github.com/user-attachments/assets/ceb49c69-8ac1-4d46-a522-3b84baf54150" /># 🔍 IBTAC Lexical Analyzer

[![Python](https://img.shields.io/badge/Python-3.8+-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://www.python.org/)
[![Gradio](https://img.shields.io/badge/Gradio-Web_UI-FF4B4B?style=for-the-badge&logo=gradio&logoColor=white)](https://gradio.app/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg?style=for-the-badge)](https://opensource.org/licenses/MIT)

> **Production-grade lexical analyzer for the IBTAC programming language with interactive web interface and automated test suite.**

---

## 🎯 Project Overview

Built a complete lexical analyzer (tokenizer) for a custom programming language with unique identifier rules, comprehensive error handling, and an interactive Gradio web interface. Includes automated test suite covering 7 edge cases.

**Key Achievements:**
- 🔧 Implemented **custom tokenization** with student ID-based identifier constraints
- ✅ Built **4 error token types** with panic-mode recovery
- 🌐 Created **Gradio web UI** with real-time analysis and visualization
- 🧪 Developed **7-test suite** with 100% pass rate

---

## 🏗️ Architecture

```
Input Code → Lexer → Token Stream → Error Handler → Web UI
                                                        ↓
                                            Token Table + Errors
```

| Component | Purpose | LOC |
|-----------|---------|-----|
| **Lexer** | Tokenization engine | ~350 |
| **Error Handler** | Detection & recovery | ~200 |
| **Web UI** | Interactive interface | ~400 |
| **Test Suite** | Validation | ~300 |

---

## ✨ Key Features

### 🔤 IBTAC Language Rules
- **Identifiers**: Must start with `071`, `070`, or `048` (e.g., `071name`, `070counter`)
- **Keywords**: `if`, `else`, `while`, `return`, `func`
- **Strings**: Delimited by `$` (e.g., `$Hello World$`)
- **Numbers**: Integers, floats, exponential (e.g., `123`, `.5`, `2.5e10`)
- **Operators**: `+ - * / == != < > <= >=`

### 🛡️ Error Handling
- 4 error types: `UNTERMINATED_STRING`, `INVALID_NUMBER`, `INVALID_SYMBOL`, `INVALID_IDENTIFIER`
- Line/column tracking for precise error reporting
- Panic-mode recovery on `;`, `}`, `\n`, `)`, `$`
- Suggestion engine for corrections

---

## 🧪 Test Suite

**7 Mandatory Tests (All Pass):**
1. Leading underscore validation
2. `func` keyword vs identifier
3. `.5` number format
4. Multi-line string errors
5. `<>` operator tokenization
6. Nested comment detection
7. Custom name/ID identifiers

```bash
python main.py              # Run all tests
python tests/run_tests.py   # Interactive mode
```

---

## 🚀 Quick Start

```bash
# Clone & install
git clone https://github.com/Bayzid03/IBTAC_Lexical_Analyzer.git
cd IBTAC_Lexical_Analyzer
pip install gradio pandas

# Launch web interface
python app.py
# Opens at http://127.0.0.1:7861
```

---

## 📊 Web Interface
<img width="1524" height="884" alt="Screenshot (246)" src="https://github.com/user-attachments/assets/0f7b18d8-784b-456e-a61c-d1116c4e48b5" />


**Features:**
- 📋 Load 10+ example test cases
- 🔍 Real-time token table generation
- ❌ Error panel with detailed messages
- 📊 Summary statistics & distribution

---

## 💻 Usage Example

```python
from src.lexer import IbtacLexer

# Tokenize code
code = "func 071main() { 071x = .5 }"
lexer = IbtacLexer(code)
tokens = lexer.tokenize()

# Print tokens
for token in tokens:
    print(f"{token.type.value}({token.value})")

# Check errors
if lexer.error_handler.has_errors():
    print(lexer.error_handler.get_error_summary())
```

---

## 📐 Design Decisions

1. Identifiers **MUST** start with `071`/`070`/`048`
2. `.5` format is **valid** (no leading zero required)
3. `func` alone is **keyword**, `071func` is identifier
4. Multi-line strings **NOT supported**
5. Nested comments **cause errors**
6. `<>` parsed as **separate tokens** (`<` `>`)

---

## 📁 Project Structure

```
IBTAC_Lexical_Analyzer/
├── src/
│   ├── lexer.py              # Main tokenizer
│   ├── token_types.py        # Token definitions
│   └── error_handler.py      # Error recovery
├── tests/run_tests.py        # Test runner
├── app.py                    # Gradio interface
├── main.py                   # Test suite
└── README.md
```

---

## 🎓 Skills Demonstrated

- **Compiler Design**: Lexical analysis, DFA implementation
- **Python**: OOP, dataclasses, type hints
- **Web Development**: Gradio framework, real-time UI
- **Testing**: Edge case coverage, automated validation
- **Error Handling**: Recovery strategies, contextual messages

---

## 📫 Contact

**Your Name**  
📧 Email: hossainbayzid011@gmail.com  
💼 LinkedIn: https://www.linkedin.com/in/bayzid-hossen-5b4739277/
🐙 GitHub: (https://github.com/Bayzid03)

---

## 📄 License

MIT License

---

<div align="center">

**⭐ Star this repo if you found it helpful!**

Built for Compiler Design Course

</div>
