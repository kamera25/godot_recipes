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
    # Sort by length descending
    sorted_keys = sorted(translations.keys(), key=len, reverse=True)
    
    # We want to replace whole "blocks" to avoid partial match issues within words or code.
    # However, since we don't know the exact block boundaries used by the extractor,
    # we'll try to find the msgid as a distinct block.
    
    for msgid in sorted_keys:
        if msgid in content:
            # Check if this is a literal match. 
            # Given the previous failures, we'll try to be extremely specific.
            # If the msgid contains characters like '{{' or 'msgid' itself (somehow),
            # it might cause issues. 
            
            # Special case: don't replace if it looks like it's already translated or if it's a tiny string that might be inside a larger one already replaced.
            # But the 'sorted by length' should handle the latter.
            
            content = content.replace(msgid, translations[msgid])
            
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
            
            # Reset to original and re-translate to avoid accumulated errors
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
