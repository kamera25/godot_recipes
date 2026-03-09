import os
import re
import glob

def unescape_po_string(s):
    return s.replace('\\n', '\n').replace('\\"', '"').replace('\\\\', '\\')

def load_po(file_path):
    translations = {}
    if not os.path.exists(file_path):
        return translations
        
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
        
    # Split by double newline to get entries
    entries = re.split(r'\n\n(?=#:|\nmsgid)', content)
    for entry in entries:
        msgid_match = re.search(r'msgid\s+(.*)\nmsgstr', entry, flags=re.DOTALL)
        msgstr_match = re.search(r'msgstr\s+(.*)', entry, flags=re.DOTALL)
        
        if msgid_match and msgstr_match:
            msgid_raw = msgid_match.group(1)
            msgstr_raw = msgstr_match.group(1)
            
            msgid = "".join(re.findall(r'"([^"]*)"', msgid_raw))
            msgstr = "".join(re.findall(r'"([^"]*)"', msgstr_raw))
            
            if msgid and msgstr:
                translations[unescape_po_string(msgid)] = unescape_po_string(msgstr)
    return translations

def translate_content(content, translations):
    # Sort translations by length descending
    sorted_keys = sorted(translations.keys(), key=len, reverse=True)
    
    # We need to be careful with how md_gettext.py extracts blocks.
    # It removes YAML frontmatter and code blocks, then splits by \n\n.
    # Here we just do a direct replacement of known strings.
    
    # One issue is that the strings in PO might have been normalized or have diff line breaks.
    # But based on output.po view, they seem to match the literal content but with \n.
    
    for msgid in sorted_keys:
        if msgid in content:
            content = content.replace(msgid, translations[msgid])
        else:
            # Try matching with normalized whitespace if direct match fails?
            # Actually, let's see why it failed for the notice block.
            # The msgid in PO: 
            # "{{% notice style=\"tip\" title=\"Godot 4.0\"%}}\n**Godot 4.0 has been released!**<br>\n..."
            # The md content:
            # "{{% notice style=\"tip\" title=\"Godot 4.0\"%}}\n**Godot 4.0 has been released!**<br>\n..."
            pass
            
    return content

def main():
    po_file = '/Users/kamera25/godot_recipes/output.po'
    content_dir = '/Users/kamera25/godot_recipes/src-4/content'
    
    print(f"Loading translations from {po_file}...")
    translations = load_po(po_file)
    print(f"Loaded {len(translations)} entries.")
    
    md_files = glob.glob(os.path.join(content_dir, '**', '*.md'), recursive=True)
    md_files = [f for f in md_files if not f.endswith('.ja.md')]
    
    print(f"Processing {len(md_files)} markdown files...")
    files_created = 0
    
    for file_path in md_files:
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            translated = translate_content(content, translations)
            
            base, ext = os.path.splitext(file_path)
            ja_file_path = f"{base}.ja{ext}"
            
            with open(ja_file_path, 'w', encoding='utf-8') as f:
                f.write(translated)
            
            files_created += 1
            
        except Exception as e:
            print(f"Error processing {file_path}: {e}")
            
    print(f"Successfully created {files_created} Japanese markdown files.")

if __name__ == '__main__':
    main()
