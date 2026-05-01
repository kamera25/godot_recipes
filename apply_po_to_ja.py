import os
import re
import glob
import subprocess

def unescape_po_string(s):
    return s.replace('\\n', '\n').replace('\\"', '"').replace('\\\\', '\\')

def load_po(file_path):
    translations_by_file = {}
    if not os.path.exists(file_path):
        return translations_by_file
        
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
            
            msgid = "".join(re.findall(r'"((?:\\.|[^"\\])*)"', msgid_raw))
            msgstr = "".join(re.findall(r'"((?:\\.|[^"\\])*)"', msgstr_raw))
            
            if msgid and msgstr:
                unescaped_msgid = unescape_po_string(msgid)
                unescaped_msgstr = unescape_po_string(msgstr)

                # Extract file references
                ref_lines = re.findall(r'^#:\s*(.*)', entry, flags=re.MULTILINE)
                for line in ref_lines:
                    for ref in line.split():
                        file_ref = ref.split(':')[0]
                        if file_ref not in translations_by_file:
                            translations_by_file[file_ref] = {}
                        translations_by_file[file_ref][unescaped_msgid] = unescaped_msgstr

    return translations_by_file

def translate_content(content, translations):
    # Sort translations by length descending
    sorted_keys = sorted(translations.keys(), key=len, reverse=True)
    
    # Identify and protect frontmatter and code blocks
    protected_blocks = []
    
    def protect(match):
        block = match.group(0)
        # Apply translations to comments inside the code block before protecting it
        for msgid in sorted_keys:
            if msgid in block:
                block = block.replace(msgid, translations[msgid])

        placeholder = f"__PROTECTED_BLOCK_{len(protected_blocks)}__"
        protected_blocks.append(block)
        return placeholder

    # Protect code blocks (```)
    content = re.sub(r'```.*?```', protect, content, flags=re.DOTALL)
    
    # Protect Hugo highlight shortcode blocks
    content = re.sub(r'\{\{<\s*highlight.*?\{\{<\s*/highlight\s*>\}\}', protect, content, flags=re.DOTALL)

    # Perform translation replacement on the masked content
    for msgid in sorted_keys:
        # Check if msgid is essentially just a preserved word
        # (remove common markdown/HTML/spacing)
        clean_msgid = re.sub(r'<[^>]+>', '', msgid)
        clean_msgid = clean_msgid.replace('&nbsp;', '')
        clean_msgid = clean_msgid.strip('*# `\t\n')
            
        if msgid in content:
            content = content.replace(msgid, translations[msgid])
            
    # Restore protected blocks
    for i, block in enumerate(protected_blocks):
        content = content.replace(f"__PROTECTED_BLOCK_{i}__", block)
            
    return content

def main():
    po_file = './output.po'
    content_dir = './src-4/content'
    
    print(f"Loading translations from {po_file}...")
    translations_by_file = load_po(po_file)
    total_entries = sum(len(v) for v in translations_by_file.values())
    print(f"Loaded {total_entries} translations across {len(translations_by_file)} files.")
    
    md_files = glob.glob(os.path.join(content_dir, '**', '*.md'), recursive=True)
    md_files = [f for f in md_files if not f.endswith('.ja.md')]
    
    print(f"Processing {len(md_files)} markdown files...")
    files_created = 0
    
    for file_path in md_files:
        try:
            rel_path = os.path.relpath(file_path, content_dir)
            # Ensure forward slashes for matching with PO file keys
            rel_path = rel_path.replace(os.sep, '/')

            # Look up translations by matching the suffix of the reference
            file_translations = {}
            for po_ref, trans in translations_by_file.items():
                if po_ref == rel_path or po_ref.endswith('/' + rel_path):
                    # Merge dictionaries in case there are multiple matching refs
                    file_translations.update(trans)

            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            if file_translations:
                translated = translate_content(content, file_translations)
            else:
                translated = content
            
            base, ext = os.path.splitext(file_path)
            ja_file_path = f"{base}.ja{ext}"
            
            with open(ja_file_path, 'w', encoding='utf-8') as f:
                f.write(translated)
            
            files_created += 1
            
        except Exception as e:
            print(f"Error processing {file_path}: {e}")
            
    print(f"Successfully created {files_created} Japanese markdown files.")
    
    # Error checking for PO file
    print("Validating output.po...")
    try:
        # Format the PO file and check for errors
        subprocess.run(['msgcat', '--no-wrap', po_file, '-o', po_file], check=True, capture_output=True, text=True)
        # Check the PO file for syntax errors
        subprocess.run(['msgfmt', '-c', po_file], check=True, capture_output=True, text=True)
        print("PO file validation successful.")
    except subprocess.CalledProcessError as e:
        print(f"PO file validation failed:\n{e.stderr}")
        exit(1)

if __name__ == '__main__':
    main()
