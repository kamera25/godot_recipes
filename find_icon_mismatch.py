import sys
import re

def main():
    po_file = 'output.po'

    try:
        with open(po_file, 'r', encoding='utf-8') as f:
            lines = f.readlines()
    except FileNotFoundError:
        print(f"Error: {po_file} not found.")
        sys.exit(1)

    in_msgid = False
    in_msgstr = False

    msgid_icon_count = 0
    msgstr_icon_count = 0

    msgid_line_num = 0

    msgstr_text = ""

    for i, line in enumerate(lines):
        line_num = i + 1
        stripped = line.strip()

        if line.startswith('msgid '):
            # Check the previous block if we were in one
            if in_msgstr:
                if msgstr_text != '""' and msgstr_text != '' and msgid_icon_count != msgstr_icon_count:
                    print(f"Line {msgid_line_num}")

            in_msgid = True
            in_msgstr = False
            msgid_icon_count = line.count('{{< gd-icon')
            msgid_line_num = line_num
            msgstr_text = ""

        elif line.startswith('msgstr '):
            in_msgid = False
            in_msgstr = True
            msgstr_icon_count = line.count('{{< gd-icon')

            # Extract the actual text part
            match = re.match(r'msgstr\s+(.*)', stripped)
            if match:
                msgstr_text = match.group(1).strip()

        elif line.startswith('"'):
            if in_msgid:
                msgid_icon_count += line.count('{{< gd-icon')
            elif in_msgstr:
                msgstr_icon_count += line.count('{{< gd-icon')
                msgstr_text += stripped

        elif stripped == '':
            # End of a block
            if in_msgstr:
                if msgstr_text != '""' and msgstr_text != '' and msgid_icon_count != msgstr_icon_count:
                    print(f"Line {msgid_line_num}")

            in_msgid = False
            in_msgstr = False

    # Check the very last block
    if in_msgstr:
        if msgstr_text != '""' and msgstr_text != '' and msgid_icon_count != msgstr_icon_count:
            print(f"Line {msgid_line_num}")

if __name__ == '__main__':
    main()
