import re

with open('output.po', 'r') as f:
    lines = f.readlines()

current_block = None

for i, line in enumerate(lines):
    if line.startswith('msgid'):
        current_block = 'msgid'
    elif line.startswith('msgstr'):
        current_block = 'msgstr'
    elif not line.startswith('"'):
        current_block = None

    if current_block == 'msgstr':
        # Apply substitutions only to the translation
        lines[i] = re.sub(r'/godot_recipes/3\.x', r'/godot_recipes/4.x/ja', lines[i])
        lines[i] = re.sub(r'http://kidscancode\.org/godot_recipes', r'/godot_recipes/4.x/ja', lines[i])

with open('output.po', 'w') as f:
    f.writelines(lines)
