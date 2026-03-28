import os
import glob
import re
import argparse
import datetime

def escape_po_string(s):
    return s.replace('\\', '\\\\').replace('"', '\\"').replace('\n', '\\n')

def unescape_po_string(s):
    return s.replace('\\n', '\n').replace('\\"', '"').replace('\\\\', '\\')

def extract_md_blocks(content):
    """Markdownからブロック要素を抽出し、翻訳可能なリストを返す"""
    texts = set()
    
    # フロントマターの抽出 (YAML: --- または TOML: +++)
    # より柔軟な正規表現: 行末のスペースや、様々な改行コードに対応
    frontmatter_match = re.match(r'^(---\s*\r?\n(.*?)\r?\n---\s*|\+\+\+\s*\r?\n(.*?)\r?\n\+\+\+\s*)(\r?\n|$)', content, flags=re.DOTALL)
    if frontmatter_match:
        frontmatter = frontmatter_match.group(2) or frontmatter_match.group(3)
        # title: "..." または title = "..." を抽出 (シングルクォート、ダブルクォート両対応)
        title_match = re.search(r'title\s*[:=]\s*["\'](.*?)["\']', frontmatter)
        if title_match:
            texts.add(title_match.group(1))

    # フロントマターを削除 (抽出時と同じ正規表現を使用)
    text_content = re.sub(r'^(---\s*\r?\n.*?\r?\n---\s*|\+\+\+\s*\r?\n.*?\r?\n\+\+\+\s*)(\r?\n|$)', '', content, flags=re.DOTALL)
    
    # コードブロックを抽出対象から外す
    text_content = re.sub(r'```.*?```', '', text_content, flags=re.DOTALL)
    text_content = re.sub(r'\{\{<\s*highlight.*?\{\{<\s*/highlight\s*>\}\}', '', text_content, flags=re.DOTALL)
    
    # アンダーバーで囲まれたテキストを抽出対象から外す
    text_content = re.sub(r'(^|\s|[^a-zA-Z0-9_])(_[^_]+_)([^a-zA-Z0-9_]|\s|$)', r'\1\3', text_content)

    # 段落ごとに分割 (改行2つ以上)
    blocks = re.split(r'\n\n+', text_content)
    
    for block in blocks:
        block = block.strip()
        
        # 空要素や短すぎるもの、数字だけの場合は無視
        if not block or len(block) <= 1 or block.isnumeric():
            continue
            
        # Hugoのショートコード単体 (例: {{% notice %}}) なら抽出をスキップ
        if re.match(r'^\{\{[%<].*?[%>]\}\}$', block):
            continue
            
        texts.add(block)
            
    return texts

def create_po(docs_dir, output_po_file):
    md_files = glob.glob(os.path.join(docs_dir, '**', '*.md'), recursive=True)
    # 翻訳済みファイル (*.ja.md) および隠しファイル (.*.md) を除外
    md_files = [f for f in md_files if not f.endswith('.ja.md') and not os.path.basename(f).startswith('.')]
    po_entries = {}
    
    print(f"Extraction: Found {len(md_files)} Markdown files in {docs_dir}")
    for file_path in md_files:
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            extracted = extract_md_blocks(content)
            rel_path = os.path.relpath(file_path, docs_dir)
            
            for text in extracted:
                if text not in po_entries:
                    po_entries[text] = set()
                po_entries[text].add(rel_path)
        except Exception as e:
            print(f"Error processing {file_path}: {e}")

    print(f"Writing {len(po_entries)} translation strings...（Markdownブロック）")
    with open(output_po_file, 'w', encoding='utf-8') as f:
        f.write('msgid ""\n')
        f.write('msgstr ""\n')
        f.write('"Project-Id-Version: Godot Recipes Content\\n"\n')
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

    print(f"Created: {output_po_file}")

def load_po(file_path):
    entries = {}
    if not os.path.exists(file_path):
        return entries
        
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
        
    blocks = content.split('\n\n')
    for block in blocks:
        # msgidとmsgstrのパターンを修正し、複数行の引用符を正しく処理する
        msgid_match = re.search(r'msgid\s*(?P<msgid_content>(?:"[^"]*"\s*)+)', block, flags=re.DOTALL)
        msgstr_match = re.search(r'msgstr\s*(?P<msgstr_content>(?:"[^"]*"\s*)+)', block, flags=re.DOTALL)
        
        if msgid_match and msgstr_match:
            # 各引用符で囲まれた部分を抽出し、結合する
            msgid_parts = re.findall(r'"([^"]*)"', msgid_match.group('msgid_content'))
            msgstr_parts = re.findall(r'"([^"]*)"', msgstr_match.group('msgstr_content'))
            
            msgid = "".join(msgid_parts)
            msgstr = "".join(msgstr_parts)
            
            if msgid and msgstr:
                entries[unescape_po_string(msgid)] = unescape_po_string(msgstr)
    return entries

def apply_translations(docs_dir, po_file):
    translations = load_po(po_file)
    if not translations:
        print("PO file is empty or missing.")
        return

    print(f"Loaded {len(translations)} translations from {po_file}")
    
    valid_translations = {k: v for k, v in translations.items() if v.strip()}
    if not valid_translations:
        print("No translated strings found in PO file.")
        return

    md_files = glob.glob(os.path.join(docs_dir, '**', '*.md'), recursive=True)
    files_modified = 0

    for file_path in md_files:
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()

            original_content = content
            
            # 各翻訳についてソースのテキストを置換
            # 長い文字列から先に置換する（部分一致による誤置換を防ぐため）
            sorted_keys = sorted(valid_translations.keys(), key=len, reverse=True)
            for msgid in sorted_keys:
                msgstr = valid_translations[msgid]
                if msgid in content:
                    content = content.replace(msgid, msgstr)
            
            if content != original_content:
                with open(file_path, 'w', encoding='utf-8') as f:
                    f.write(content)
                files_modified += 1
                
        except Exception as e:
            print(f"Error processing {file_path}: {e}")

    print(f"Translated {files_modified} Markdown files.")

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Markdown Gettext Tool")
    parser.add_argument('mode', choices=['extract', 'apply'], help="'extract' to create PO, 'apply' to translate Markdown")
    parser.add_argument('--dir', default='/app/src-4/content', help='Markdown directory')
    parser.add_argument('--po', default='/app/content_extracted.po', help='PO file path')
    
    args = parser.parse_args()
    
    if args.mode == 'extract':
        create_po(args.dir, args.po)
    elif args.mode == 'apply':
        apply_translations(args.dir, args.po)
