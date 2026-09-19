import argparse
import re

def fix_links(input_path, output_path):
    with open(input_path, 'r', encoding='utf-8') as f:
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
            lines[i] = re.sub(r'/godot_recipes/3\.x', r'/godot_recipes/4.x/ja', lines[i])
            lines[i] = re.sub(r'http://kidscancode\.org/godot_recipes', r'/godot_recipes/4.x/ja', lines[i])

    with open(output_path, 'w', encoding='utf-8') as f:
        f.writelines(lines)

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Fix legacy links in PO translations.')
    parser.add_argument('input', nargs='?', default='output.po')
    parser.add_argument('-o', '--output', default='output.po')
    args = parser.parse_args()
    fix_links(args.input, args.output)
