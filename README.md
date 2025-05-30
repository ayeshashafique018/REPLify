# 🔁 Custom Python REPL (Read-Eval-Print Loop)

A customizable Python-based REPL (Read-Eval-Print Loop) environment built from scratch. This REPL goes beyond the default Python shell by offering helpful developer tools like tokenization, command history, debugging, environment visualization, and usage statistics.

---

## 🚀 Features

- 📦 **Tokenization**
  - Lexical analysis of user code
  - Separate tracking of valid and error tokens
  - Token classification (keywords, operators, identifiers, numbers)

- 📚 **Command History**
  - Tracks every input with timestamp
  - Saves and loads history from a file

- 🧠 **Environment Handling**
  - View user-defined variables in the current session
  - Option to clear/reset the environment

- 🐞 **Debug Mode**
  - Line-by-line debugging
  - See tokens, evaluation results, and environment state at each step

- 📊 **Stats**
  - Number of commands executed
  - Total history entries

- 🛠️ **Built-in Commands**
  - `help` – List available commands
  - `history` – Show previously executed commands
  - `tokens` – Display valid tokens
  - `error_tokens` – Display erroneous tokens
  - `env` – Show current environment variables
  - `stats` – View REPL statistics
  - `debug` – Step-by-step code execution
  - `clear` – Clear the current environment
  - `exit()` – Quit the REPL


---

## 🔧 Requirements

- Python 3.x
- `colorama` module  
  Install via:
  ```bash
  pip install colorama

