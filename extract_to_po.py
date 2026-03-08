import os
import glob
import re
import datetime

def extract_text_from_html(html):
    # Remove scripts, styles, codes, and preformatted blocks entirely
    html = re.sub(r'<script\b[^<]*(?:(?!<\/script>)<[^<]*)*<\/script>', '', html, flags=re.IGNORECASE)
    html = re.sub(r'<style\b[^<]*(?:(?!<\/style>)<[^<]*)*<\/style>', '', html, flags=re.IGNORECASE)
    html = re.sub(r'<code\b[^<]*(?:(?!<\/code>)<[^<]*)*<\/code>', '', html, flags=re.IGNORECASE)
    html = re.sub(r'<pre\b[^<]*(?:(?!<\/pre>)<[^<]*)*<\/pre>', '', html, flags=re.IGNORECASE)
    html = re.sub(r'<!--.*?-->', '', html, flags=re.DOTALL) # Remove comments
    
    # Split by common block tags to avoid merging independent paragraphs
    block_tags = r'p|div|h[1-6]|li|td|th|ul|ol|table|blockquote|article|section|nav|header|footer|aside'
    blocks = re.split(fr'<(?:/)?(?:{block_tags})\b[^>]*>', html, flags=re.IGNORECASE)
    
    texts = set()
    for block in blocks:
        # Strip all remaining tags
        text = re.sub(r'<[^>]+>', ' ', block)
        # Normalize whitespace (also converts newlines into spaces)
        text = ' '.join(text.split())
        # Filter out empty or very short garbage
        if text and len(text) > 1 and not text.isnumeric():
            texts.add(text)
            
    return texts

def escape_po_string(s):
    s = s.replace('\\', '\\\\')
    s = s.replace('"', '\\"')
    return s

def main():
    docs_dir = '/Users/kamera25/godot_recipes/docs'
    output_po_file = '/Users/kamera25/godot_recipes/docs_extracted.po'
    
    html_files = glob.glob(os.path.join(docs_dir, '**', '*.html'), recursive=True)
    
    po_entries = {} # msgid -> set of file paths
    
    print(f"Found {len(html_files)} HTML files in {docs_dir}")
    
    for file_path in html_files:
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
                
            extracted_texts = extract_text_from_html(content)
            
            rel_path = os.path.relpath(file_path, docs_dir)
            
            for text in extracted_texts:
                if text not in po_entries:
                    po_entries[text] = set()
                po_entries[text].add(rel_path)
                
        except Exception as e:
            print(f"Error processing {file_path}: {e}")
            
    # Write PO file
    print(f"Writing {len(po_entries)} extracted strings to {output_po_file}...")
    with open(output_po_file, 'w', encoding='utf-8') as f:
        # Write PO header
        f.write('msgid ""\n')
        f.write('msgstr ""\n')
        f.write('"Project-Id-Version: Godot Recipes Docs\\n"\n')
        f.write(f'"POT-Creation-Date: {datetime.datetime.now().strftime("%Y-%m-%d %H:%M%z")}\\n"\n')
        f.write('"MIME-Version: 1.0\\n"\n')
        f.write('"Content-Type: text/plain; charset=UTF-8\\n"\n')
        f.write('"Content-Transfer-Encoding: 8bit\\n"\n')
        f.write('\n')
        
        for msgid, locations in po_entries.items():
            for loc in sorted(list(locations))[:5]:
                f.write(f'#: {loc}\n')
            f.write(f'msgid "{escape_po_string(msgid)}"\n')
            f.write(f'msgstr ""\n\n')

    print(f"Successfully created: {output_po_file}")

if __name__ == '__main__':
    main()
