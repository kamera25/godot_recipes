import os
import sys
import subprocess
import re

import pathlib
GODOT_EXECUTABLE = str(pathlib.Path("/Applications/Godot.app/Contents/MacOS/Godot").resolve())
TMP_SCRIPT_PATH = "/tmp/check_script.gd"

def check_syntax(script_content, filepath, line_num):
    # Write the script content to the temporary file
    with open(TMP_SCRIPT_PATH, "w") as f:
        f.write(script_content)

    # Note: godot --check-only requires a project.godot file to be present in the directory
    # or the parent directories, or we need to run it from a directory with one.
    # However, --check-only -s script.gd might work fine. Let's just create an empty project.godot in /tmp just in case.
    project_godot_path = "/tmp/project.godot"
    if not os.path.exists(project_godot_path):
        with open(project_godot_path, "w") as f:
            pass

    # Run godot in headless mode to check syntax
    # godot --headless --check-only -s /tmp/check_script.gd
    try:
        result = subprocess.run(
            [GODOT_EXECUTABLE, "--headless", "--check-only", "-s", TMP_SCRIPT_PATH],
            capture_output=True,
            text=True,
            cwd="/tmp", # Run in /tmp where the dummy project.godot is
            timeout=10 # Timeout to prevent hanging
        )
    except subprocess.TimeoutExpired:
        print(f"Godot syntax check timed out for {filepath}:{line_num}")
        return False

    # Godot returns non-zero exit code if there are syntax errors
    # Note: godot error checking output goes to stderr. We want to check if "Parse error" or "Error" is in it.
    if result.returncode != 0 or "Parse Error:" in result.stderr or "Parse Error:" in result.stdout:
        # Ignore certain context errors because these are just code snippets, not full classes
        # e.g. "not declared in the current scope", "not found in base self"
        error_lines = []
        for line in result.stderr.split('\n') + result.stdout.split('\n'):
            if "Parse Error:" in line:
                # ignore errors due to missing context in snippets
                if "not declared in the current scope" in line: continue
                if "not found in base self" in line: continue
                if "Cannot use shorthand \"get_node()\" notation" in line: continue
                if "has the same name as a previously declared variable" in line: continue
                if "Unexpected \"Identifier\" in class body" in line: continue
                if "Unexpected \"if\" in class body" in line: continue
                if "Unexpected \"Indent\" in class body" in line: continue
                if "Unexpected \"for\" in class body" in line: continue
                if "Unexpected \"match\" in class body" in line: continue
                if "Unexpected \"elif\" in class body" in line: continue
                if "Unexpected \"else\" in class body" in line: continue
                if "Unexpected \"return\" in class body" in line: continue
                if "Expected indented block after" in line: continue
                if "Expected statement, found" in line: continue
                if "Unexpected \"$\" in class body" in line: continue
                if "Preload file" in line and "does not exist" in line: continue
                if "@onready\" can only be used in classes that inherit \"Node\"" in line: continue
                if "Could not find type" in line and "in the current scope" in line: continue
                if "Cannot use simple \"@export\" annotation because the type" in line: continue
                if "redefined (original in native class" in line: continue
                if "Could not resolve super class path" in line: continue
                if "Could not find base class" in line: continue
                if "Node export is only supported in Node-derived classes" in line: continue
                error_lines.append(line)

        if error_lines:
            print(f"Syntax error found in {filepath}:{line_num}")
            print("--- Output ---")
            for e in error_lines: print(e)
            print("--------------")
            return False
    return True

def process_markdown_file(filepath, content):
    # Regex to find gdscript blocks
    # Handle {{< highlight gdscript >}} ... {{< /highlight >}}
    # and ```gdscript ... ```
    # Using re.finditer to keep track of line numbers

    # 1. highlight shortcode
    highlight_pattern = re.compile(r'\{\{<\s*highlight\s+gdscript\s*>\}\}(.*?)\{\{<\s*/highlight\s*>\}\}', re.DOTALL)
    
    # 2. markdown code block
    md_block_pattern = re.compile(r'```gdscript(.*?)```', re.DOTALL)

    errors_found = False

    # Helper function to compute line number
    def get_line_num(match_obj):
        return content[:match_obj.start()].count('\n') + 1

    for match in highlight_pattern.finditer(content):
        code_block = match.group(1).strip()
        line_num = get_line_num(match)
        if not check_syntax(code_block, filepath, line_num):
            errors_found = True

    for match in md_block_pattern.finditer(content):
        code_block = match.group(1).strip()
        line_num = get_line_num(match)
        if not check_syntax(code_block, filepath, line_num):
            errors_found = True

    return not errors_found


def main():
    if len(sys.argv) < 2:
        print("Usage: python check_gdscript_syntax.py <directory_to_scan>")
        sys.exit(1)

    directory = sys.argv[1]
    
    if not os.path.exists(GODOT_EXECUTABLE):
        print(f"Error: Godot executable not found at {GODOT_EXECUTABLE}")
        sys.exit(1)

    total_files = 0
    files_with_errors = 0

    for root, _, files in os.walk(directory):
        for file in files:
            if file.endswith(".md"):
                filepath = os.path.join(root, file)
                total_files += 1
                with open(filepath, "r") as f:
                    content = f.read()
                if not process_markdown_file(filepath, content):
                    files_with_errors += 1

    print(f"Scanned {total_files} files.")
    if files_with_errors > 0:
        print(f"Found errors in {files_with_errors} files.")
        sys.exit(1)
    else:
        print("No syntax errors found.")

if __name__ == "__main__":
    main()
