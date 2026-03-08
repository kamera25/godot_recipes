import os
import glob
import re
import argparse
import datetime

# 翻訳が必要なブロック要素
BLOCK_TAGS = r'p|h[1-6]|li|td|th|button|title|div|blockquote|article|section|caption|figcaption|label|legend|summary|dt|dd'

def escape_po_string(s):
    return s.replace('\\', '\\\\').replace('"', '\\"').replace('\n', '\\n')

def unescape_po_string(s):
    return s.replace('\\n', '\n').replace('\\"', '"').replace('\\\\', '\\')

def extract_html_blocks(html):
    """HTMLからブロック要素を抽出し、翻訳可能なリストを返す"""
    # scriptやstyle、preは無視
    html = re.sub(r'<script\b[^<]*(?:(?!<\/script>)<[^<]*)*<\/script>', '', html, flags=re.IGNORECASE)
    html = re.sub(r'<style\b[^<]*(?:(?!<\/style>)<[^<]*)*<\/style>', '', html, flags=re.IGNORECASE)
    html = re.sub(r'<code\b[^<]*(?:(?!<\/code>)<[^<]*)*<\/code>', '', html, flags=re.IGNORECASE)
    html = re.sub(r'<pre\b[^<]*(?:(?!<\/pre>)<[^<]*)*<\/pre>', '', html, flags=re.IGNORECASE)
    html = re.sub(r'<!--.*?-->', '', html, flags=re.DOTALL) # コメント削除
    
    # ブロック要素の中身を抽出する正規表現
    # 例: <p class="xxx">内容</p> の `内容` を取得
    pattern = fr'<({BLOCK_TAGS})\b[^>]*>(.*?)</\1>'
    
    texts = set()
    for match in re.finditer(pattern, html, flags=re.IGNORECASE | re.DOTALL):
        inner_html = match.group(2).strip()
        # 余分な空白・改行を整理
        inner_html = ' '.join(inner_html.split())
        
        # テキストがない場合や短すぎる、数字だけな場合は無視
        plain_text = re.sub(r'<[^>]+>', '', inner_html).strip()
        if plain_text and len(plain_text) > 1 and not plain_text.isnumeric():
            texts.add(inner_html)
            
    return texts

def create_po(docs_dir, output_po_file):
    html_files = glob.glob(os.path.join(docs_dir, '**', '*.html'), recursive=True)
    po_entries = {}
    
    print(f"Extraction: Found {len(html_files)} HTML files in {docs_dir}")
    for file_path in html_files:
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            extracted = extract_html_blocks(content)
            rel_path = os.path.relpath(file_path, docs_dir)
            
            for text in extracted:
                if text not in po_entries:
                    po_entries[text] = set()
                po_entries[text].add(rel_path)
        except Exception as e:
            print(f"Error processing {file_path}: {e}")

    print(f"Writing {len(po_entries)} translation strings...（HTMLタグを保持）")
    with open(output_po_file, 'w', encoding='utf-8') as f:
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

    print(f"Created: {output_po_file}")

def load_po(file_path):
    """POファイルを読み込んで {msgid: msgstr} の辞書を返す"""
    entries = {}
    if not os.path.exists(file_path):
        return entries
        
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
        
    # \n\n でブロックごとに分割
    blocks = content.split('\n\n')
    for block in blocks:
        # 複数行対応の簡易パース (シンプル化のため結合して検索)
        msgid_match = re.search(r'msgid\s+"(.*)"(?:\nmsgstr|$)', block, flags=re.DOTALL)
        msgstr_match = re.search(r'msgstr\s+"(.*)"', block, flags=re.DOTALL)
        
        if msgid_match and msgstr_match:
            # 複数行の "..."\n"..." を結合
            msgid = "".join(re.findall(r'"([^"]*)"', msgid_match.group(0)))
            msgstr = "".join(re.findall(r'"([^"]*)"', msgstr_match.group(0)))
            # msgidとmsgstrからそれぞれキーワードを除外
            msgid = msgid.replace('msgid', '', 1).strip()
            msgstr = msgstr.replace('msgstr', '', 1).strip()
            
            if msgid and msgstr:
                entries[unescape_po_string(msgid)] = unescape_po_string(msgstr)
    return entries

def apply_translations(docs_dir, po_file):
    translations = load_po(po_file)
    if not translations:
        print("PO file is empty or missing.")
        return

    print(f"Loaded {len(translations)} translations from {po_file}")
    
    # 翻訳が実際にあるものだけ処理
    valid_translations = {k: v for k, v in translations.items() if v.strip()}
    if not valid_translations:
        print("No translated strings found in PO file.")
        return

    html_files = glob.glob(os.path.join(docs_dir, '**', '*.html'), recursive=True)
    files_modified = 0

    for file_path in html_files:
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()

            original_content = content
            
            # 各翻訳について、HTMLソース内の元のインナーHTMLを置換する
            for msgid, msgstr in valid_translations.items():
                if msgid in content:
                    # 完全一致で置換 (単純な部分一致を避けるため)
                    content = content.replace(msgid, msgstr)
                else:
                    # ホワイトスペースの違いを吸収して置換を試みる
                    escaped_msgid = re.escape(msgid).replace(r'\ ', r'\s+')
                    content = re.sub(escaped_msgid, msgstr, content)
            
            if content != original_content:
                with open(file_path, 'w', encoding='utf-8') as f:
                    f.write(content)
                files_modified += 1
                
        except Exception as e:
            print(f"Error processing {file_path}: {e}")

    print(f"Translated {files_modified} HTML files.")

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="HTML Gettext Tool")
    parser.add_argument('mode', choices=['extract', 'apply'], help="'extract' to create PO, 'apply' to translate HTML")
    parser.add_argument('--dir', default='/Users/kamera25/godot_recipes/docs', help='HTML directory')
    parser.add_argument('--po', default='/Users/kamera25/godot_recipes/docs_extracted.po', help='PO file path')
    
    args = parser.parse_args()
    
    if args.mode == 'extract':
        create_po(args.dir, args.po)
    elif args.mode == 'apply':
        apply_translations(args.dir, args.po)
