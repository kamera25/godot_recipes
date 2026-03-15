import re

def find_untranslated(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Entries are separated by blank lines
    entries = re.split(r'\n\n', content)
    untranslated = []
    
    for entry in entries:
        if 'msgstr ""' in entry:
            lines = entry.strip().split('\n')
            for i, line in enumerate(lines):
                if line.startswith('msgstr ""'):
                    # If this is the last line of the entry, or if the next line does not start with a quote
                    if i == len(lines) - 1:
                        if 'msgid ""' in entry and i == lines.index('msgstr ""'):
                             # Skip header
                             pass
                        else:
                            untranslated.append(entry)
                        break
                    elif not lines[i+1].strip().startswith('"'):
                         untranslated.append(entry)
                         break
    
    return untranslated

untranslated_entries = find_untranslated('/Users/kamera25/godot_recipes/output.po')
print(f"Found {len(untranslated_entries)} untranslated entries.")
for i, entry in enumerate(untranslated_entries[:20]):
    print(f"--- Entry {i+1} ---")
    print(entry)
