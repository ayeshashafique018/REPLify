import os
import re
from datetime import datetime
from colorama import Fore, Style, init


# Initialize colorama
init(autoreset=True)

# === Global Variables ===
global_env = {}
command_history = []
execution_count = 0

# === File Constants ===
HISTORY_FILE = "repl_history.txt"
TOKENS_FILE = "tokens.txt"
ERROR_TOKENS_FILE = "error_tokens.txt"

# === Input Handler ===
def get_user_input(prompt=">>> "):
    lines = []
    while True:
        line = input(prompt)
        if not line.strip():
            break
        lines.append(line)
    return "\n".join(lines)

# === Tokenization ===
def tokenize_code(code, is_error=False):
    pattern = r"\b\w+\b|[\+\-\*/=<>!&|;:(){}\[\],.]"
    tokens = re.findall(pattern, code)
    token_data = [(token, classify_token(token)) for token in tokens]

    append_tokens_to_file(token_data, ERROR_TOKENS_FILE if is_error else TOKENS_FILE)
    return token_data

def classify_token(token):
    keywords = {"def", "class", "return", "if", "else", "for", "while", "import", "from", "as", "with"}
    operators = {"+", "-", "*", "/", "=", "<", ">", "!", "&", "|"}
    if token in keywords:
        return "KEYWORD"
    elif token in operators:
        return "OPERATOR"
    elif re.match(r"^\d+$", token):
        return "NUMBER"
    elif re.match(r"^[a-zA-Z_]\w*$", token):
        return "IDENTIFIER"
    else:
        return "SYMBOL"

def append_tokens_to_file(token_data, file_name):
    try:
        with open(file_name, "a") as f:
            for token, token_type in token_data:
                f.write(f"{token}: {token_type}\n")
        # Removed noisy print here for cleaner REPL output
    except IOError as e:
        print(f"{Fore.RED}❌ Error saving tokens: {e}")

def show_tokens(file_name):
    if not os.path.exists(file_name):
        print(f"{Fore.RED}No tokens found in {file_name}.")
        return
    print(f"{Fore.MAGENTA}{Style.BRIGHT}📦 Tokens in {file_name}:")
    try:
        with open(file_name, "r") as f:
            for line in f:
                print(f"{Fore.CYAN}{line.strip()}")
    except IOError as e:
        print(f"{Fore.RED}❌ Error reading tokens: {e}")

# === Evaluation ===
def evaluate_code(code):
    global execution_count
    try:
        # If code contains assignment, function or class definition, use exec
        if any(kw in code for kw in ["=", "def ", "class "]):
            exec(code, global_env)
            execution_count += 1
            return None
        else:
            result = eval(code, global_env)
            execution_count += 1
            return result
    except Exception as e:
        # Save tokens from erroneous code
        tokenize_code(code, is_error=True)
        return f"{Fore.RED}{Style.BRIGHT}⚠ Error: {Style.RESET_ALL}{e}"

# === Output ===
def display_output(result):
    if result is not None:
        print(f"{Fore.GREEN}{Style.BRIGHT}🎯 Output:\n{Fore.CYAN}{result}")

# === History Handling ===
def add_to_history(command):
    timestamp = datetime.now().strftime("%H:%M:%S")
    command_history.append(f"[{timestamp}] {command}")

def show_history():
    if not command_history:
        print(f"{Fore.YELLOW}No commands in history yet.")
        return
    print(f"{Fore.MAGENTA}{Style.BRIGHT}🕓 Command History:")
    for idx, cmd in enumerate(command_history):
        print(f"{Fore.YELLOW}{idx + 1}: {Fore.RESET}{cmd}")

def save_history_to_file():
    try:
        with open(HISTORY_FILE, "w") as f:
            f.write("\n".join(command_history) + "\n")
        print(f"{Fore.GREEN}💾 History saved.")
    except IOError as e:
        print(f"{Fore.RED}❌ Error saving history: {e}")

def load_history_from_file():
    if not os.path.exists(HISTORY_FILE):
        print(f"{Fore.YELLOW}ℹ No history file found.")
        return
    try:
        with open(HISTORY_FILE, "r") as f:
            for line in f:
                stripped = line.strip()
                if stripped:
                    command_history.append(stripped)
        print(f"{Fore.GREEN}📂 History loaded.")
    except IOError as e:
        print(f"{Fore.RED}❌ Error loading history: {e}")

# === Utility Commands ===
def show_help():
    print(f"""{Fore.CYAN}{Style.BRIGHT}
📘 Available Commands:
──────────────────────────────
🔹 help         → Show this help menu
🔹 history      → Show command history
🔹 clear        → Clear the environment
🔹 tokens       → Show valid tokens
🔹 error_tokens → Show error tokens
🔹 env          → Show environment variables
🔹 stats        → Display usage statistics
🔹 debug        → Step-by-step code execution
🔹 exit()       → Exit the REPL
""")

def show_environment():
    if not global_env:
        print(f"{Fore.YELLOW}Environment is empty.")
        return
    print(f"{Fore.MAGENTA}{Style.BRIGHT}🌍 Current Environment:")
    for key, val in global_env.items():
        # Skip builtins to keep output clean
        if key.startswith("__") and key.endswith("__"):
            continue
        print(f"{Fore.YELLOW}{key}: {Fore.CYAN}{val}")

def show_stats():
    print(f"""{Fore.BLUE}{Style.BRIGHT}
📊 REPL Stats:
──────────────
{Fore.YELLOW}• Commands Executed: {execution_count}
• History Entries : {len(command_history)}""")

def debug_mode():
    print(f"{Fore.YELLOW}🐞 Debug mode: Enter lines one by one. Type 'done' to exit.\n")
    step = 1
    while True:
        line = input(f"{Fore.YELLOW}→ {Style.RESET_ALL}")
        if line.strip().lower() == "done":
            break

        # Show entered code
        print(f"{Fore.YELLOW}Debug Step {step}:")
        print(f">>> {line}")

        # Tokenize and show tokens (but do NOT save error tokens here to keep debug output clean)
        tokens = tokenize_code(line, is_error=False)
        if tokens:
            print("Tokens:")
            for token, token_type in tokens:
                print(f"  {token}: {token_type}")
        else:
            print("Tokens: (none)")

        # Evaluate code and show result or error
        result = evaluate_code(line)
        if result is None:
            print("Result: None")
        elif isinstance(result, str) and result.startswith(f"{Fore.RED}"):
            # This is an error message from evaluate_code
            print(result)
        else:
            print(f"Result:\n{Fore.CYAN}{result}")

        # Show environment snapshot (only user-defined keys, skip builtins and modules)
        print("Environment snapshot:")
        user_vars = {k: v for k, v in global_env.items() if not k.startswith("__") and not callable(v) and not isinstance(v, type(os))}
        if user_vars:
            for k, v in user_vars.items():
                print(f"  {k}: {v}")
        else:
            print("  (empty or builtins only)")

        print(f"{'-'*40}")
        step += 1

def clear_environment():
    global global_env
    global_env.clear()
    print(f"{Fore.YELLOW}🧹 Environment cleared.")

# === Main REPL Loop ===
def repl_loop():
    print(f"""{Fore.GREEN}{Style.BRIGHT}
╔════════════════════════════════════╗
║        🔁 PYTHON CUSTOM REPL       ║
╚════════════════════════════════════╝
{Fore.YELLOW}Type 'help' to view available commands.
""")
    load_history_from_file()

    while True:
        try:
            code = get_user_input(prompt_style)
            cmd = code.strip().lower()

            if cmd == "exit()":
                save_history_to_file()
                print(f"{Fore.CYAN}👋 Goodbye!")
                break
            elif cmd in commands:
                commands[cmd]()
            else:
                add_to_history(code)
                result = evaluate_code(code)
                # Tokenize on success or failure separately to avoid double writing
                if result is None or (isinstance(result, str) and not result.startswith(Fore.RED)):
                    tokenize_code(code)
                display_output(result)
        except KeyboardInterrupt:
            print(f"\n{Fore.RED}⛔ KeyboardInterrupt. Type 'exit()' to quit.")
            save_history_to_file()  # Save history before continuing or exit
        except EOFError:
            print(f"\n{Fore.RED}⛔ EOF received. Exiting...")
            save_history_to_file()  # Save history before exiting
            break

# === Command Dispatcher ===
commands = {
    "help": show_help,
    "history": show_history,
    "clear": clear_environment,
    "tokens": lambda: show_tokens(TOKENS_FILE),
    "error_tokens": lambda: show_tokens(ERROR_TOKENS_FILE),
    "env": show_environment,
    "stats": show_stats,
    "debug": debug_mode,
}

# === Prompt Style ===
prompt_style = f"{Fore.BLUE}>>> {Style.RESET_ALL}"

# === Entry Point ===
if __name__ == "__main__":
    repl_loop()
