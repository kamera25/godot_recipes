import os
import glob
import re
import argparse
import datetime
import polib

def extract_md_blocks(content):
    """Markdownからブロック要素を抽出し、翻訳可能なリストを返す。
    md_gettext.pyのロジックを流用。
    """
    texts = set()
    
    # フロントマターの抽出 (YAML: --- または TOML: +++)
    frontmatter_match = re.match(r'^(---\s*\r?\n(.*?)\r?\n---\s*|\+\+\+\s*\r?\n(.*?)\r?\n\+\+\+\s*)(\r?\n|$)', content, flags=re.DOTALL)
    if frontmatter_match:
        frontmatter = frontmatter_match.group(2) or frontmatter_match.group(3)
        # title: "..." または title = "..." 
        title_match = re.search(r'title\s*[:=]\s*["\'](.*?)["\']', frontmatter)
        if title_match:
            texts.add(title_match.group(1))

    # フロントマターを削除
    text_content = re.sub(r'^(---\s*\r?\n.*?\r?\n---\s*|\+\+\+\s*\r?\n.*?\r?\n\+\+\+\s*)(\r?\n|$)', '', content, flags=re.DOTALL)
    
    # コードブロック内のコメントを抽出対象に追加
    code_blocks = re.findall(r'```.*?```', text_content, flags=re.DOTALL)
    code_blocks += re.findall(r'\{\{<\s*highlight.*?\{\{<\s*/highlight\s*>\}\}', text_content, flags=re.DOTALL)
    for block in code_blocks:
        for line in block.split('\n'):
            m_full = re.match(r'^\s*(#|//)\s*(.+)$', line)
            if m_full:
                texts.add(line.strip())
            else:
                m_inline = re.search(r'\s+(#|//)\s*(.+)$', line)
                if m_inline:
                    texts.add(m_inline.group(0).strip())

    # コードブロックを抽出対象から外す
    text_content = re.sub(r'```.*?```', '', text_content, flags=re.DOTALL)
    text_content = re.sub(r'\{\{<\s*highlight.*?\{\{<\s*/highlight\s*>\}\}', '', text_content, flags=re.DOTALL)
    
    # 段落ごとに分割 (改行2つ以上)
    blocks = re.split(r'\n\n+', text_content)
    
    for block in blocks:
        block = block.strip()
        
        # 空要素や短すぎるもの、数字だけの場合は無視
        if not block or len(block) <= 1 or block.isnumeric():
            continue
            
        # Hugoのショートコード単体なら抽出をスキップ
        if re.match(r'^\{\{[%<].*?[%>]\}\}$', block):
            continue
            
        texts.add(block)
            
    return texts

def update_po_file(docs_dir, po_file_path, dry_run=False):
    # 1. すべてのMarkdownファイルを取得 (翻訳済みの .ja.md は除く)
    md_files = glob.glob(os.path.join(docs_dir, '**', '*.md'), recursive=True)
    md_files = [f for f in md_files if not f.endswith('.ja.md') and not os.path.basename(f).startswith('.')]
    
    # 2. 現存するPOファイルを読み込む（なければ新規作成）
    if os.path.exists(po_file_path):
        po = polib.pofile(po_file_path)
        print(f"Loaded existing PO file: {po_file_path} ({len(po)} entries)")
    else:
        po = polib.POFile()
        po.metadata = {
            'Project-Id-Version': 'Godot Recipes Content',
            'POT-Creation-Date': datetime.datetime.now().strftime('%Y-%m-%d %H:%M%z'),
            'MIME-Version': '1.0',
            'Content-Type': 'text/plain; charset=UTF-8',
            'Content-Transfer-Encoding': '8bit',
        }
        print(f"Creating new PO file: {po_file_path}")

    # 現在のMDファイルに含まれるすべてのテキストを抽出
    extracted_data = {} # msgid -> set of relative_paths
    
    print(f"Extracting strings from {len(md_files)} files...")
    for file_path in md_files:
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            blocks = extract_md_blocks(content)
            rel_path = os.path.relpath(file_path, docs_dir)
            
            for text in blocks:
                if text not in extracted_data:
                    extracted_data[text] = set()
                extracted_data[text].add(rel_path)
        except Exception as e:
            print(f"Error processing {file_path}: {e}")

    # 3. POファイルを更新
    new_entries_count = 0
    updated_entries_count = 0
    seen_msgids = set()

    for msgid, occurrences in extracted_data.items():
        seen_msgids.add(msgid)
        entry = po.find(msgid)
        
        # 出現場所をリスト化 (ファイル名のみ。polibの書式に合わせる)
        occ_list = [(occ, "") for occ in sorted(list(occurrences))]
        
        if entry:
            # 既存のエントリ：出現場所を更新し、obsoleteフラグがあれば解除
            entry.occurrences = occ_list
            if entry.obsolete:
                entry.obsolete = False
                print(f"Re-activated obsolete entry: {msgid[:50]}...")
            updated_entries_count += 1
        else:
            # 新規エントリを追加
            new_entry = polib.POEntry(
                msgid=msgid,
                msgstr='',
                occurrences=occ_list
            )
            po.append(new_entry)
            new_entries_count += 1
            # print(f"Added new entry: {msgid[:50]}...")

    # 4. 現在のMDファイルに存在しないエントリをobsoleteにする
    obsolete_count = 0
    for entry in po:
        if entry.msgid and entry.msgid not in seen_msgids and not entry.obsolete:
            entry.obsolete = True
            obsolete_count += 1
            # print(f"Marked as obsolete: {entry.msgid[:50]}...")

    # 5. 保存
    if not dry_run:
        po.save(po_file_path)
        print(f"Saved {po_file_path}.")
    else:
        print("Dry run: File not saved.")

    print(f"\nSummary:")
    print(f"  New strings added: {new_entries_count}")
    print(f"  Existing strings updated: {updated_entries_count}")
    print(f"  Strings marked as obsolete: {obsolete_count}")

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Update PO file from Markdown content")
    parser.add_argument('--dir', default='./src-4/content', help='Directory containing Markdown files')
    parser.add_argument('--po', default='./output.po', help='Path to the PO file to update')
    parser.add_argument('--dry-run', action='store_true', help='Do not save changes')
    
    args = parser.parse_args()
    
    # 絶対パスに変換
    docs_dir = os.path.abspath(args.dir)
    po_file = os.path.abspath(args.po)
    
    if not os.path.isdir(docs_dir):
        print(f"Error: Directory not found: {docs_dir}")
        exit(1)
        
    update_po_file(docs_dir, po_file, dry_run=args.dry_run)
