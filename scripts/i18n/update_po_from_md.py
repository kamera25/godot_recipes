import os
import glob
import re
import argparse
import datetime
import polib


COMMENT_PREFIXES = ('#', '//', ';', '--', '/*', '*', '<!--', '-->')
GDSCRIPT_FENCE = re.compile(r'^```(?:gdscript|gdscript[234])(?:\s|$)', re.IGNORECASE)


def _comment_from_line(line):
    """Return a full-line comment without indentation, or ``None``."""
    match = re.match(
        r'^[ \t]*(?P<comment>(?:#|//|;|--|/\*|\*|<!--|-->).*)[ \t]*$',
        line,
    )
    if not match:
        return None

    comment = match.group('comment').rstrip()
    prefix = next(
        (prefix for prefix in COMMENT_PREFIXES if comment.startswith(prefix)),
        None,
    )
    if prefix and comment[len(prefix):].strip(' \t*/'):
        return comment
    return None


def extract_gdscript_comments(content):
    """Extract standalone comments from GDScript fenced code blocks.

    Inline comments and ``#`` characters inside strings are intentionally not
    extracted. Indentation is not part of the msgid; it is restored when the
    translation is applied to the code block.
    """
    comments = set()
    in_gdscript = False

    for line in content.splitlines():
        if not in_gdscript:
            if GDSCRIPT_FENCE.match(line.strip()):
                in_gdscript = True
            continue

        if line.strip() == '```':
            in_gdscript = False
            continue

        comment = _comment_from_line(line)
        if comment:
            comments.add(comment)

    return comments


def extract_code_comments(content):
    """Backward-compatible alias for GDScript comment extraction."""
    return extract_gdscript_comments(content)


def collect_gdscript_comments(md_files, docs_dir):
    """Return ``msgid -> source Markdown paths`` for GDScript comments."""
    comments = {}
    for file_path in md_files:
        with open(file_path, 'r', encoding='utf-8') as file:
            file_comments = extract_gdscript_comments(file.read())
        rel_path = os.path.relpath(file_path, docs_dir).replace(os.sep, '/')
        for comment in file_comments:
            comments.setdefault(comment, set()).add(rel_path)
    return comments


def validate_gdscript_comments(po, comments_by_msgid):
    """Validate every extracted GDScript comment and its source reference."""
    missing = []
    missing_references = []

    for msgid, expected_paths in comments_by_msgid.items():
        entry = po.find(msgid)
        if entry is None or entry.obsolete:
            missing.append(msgid)
            continue

        actual_paths = {path.replace(os.sep, '/') for path, _ in entry.occurrences}
        for expected_path in expected_paths:
            if expected_path not in actual_paths:
                missing_references.append((msgid, expected_path))

    return missing, missing_references

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
    gdscript_comments_by_msgid = {} # comment msgid -> set of relative_paths
    
    print(f"Extracting strings from {len(md_files)} files...")
    for file_path in md_files:
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            blocks = extract_md_blocks(content)
            gdscript_comments = extract_gdscript_comments(content)
            blocks.update(gdscript_comments)
            rel_path = os.path.relpath(file_path, docs_dir).replace(os.sep, '/')

            for comment in gdscript_comments:
                gdscript_comments_by_msgid.setdefault(comment, set()).add(rel_path)
            
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

    # Comments inside protected code blocks need their own validation. This
    # confirms both the msgid and every Markdown source reference are present.
    missing_comments, missing_references = validate_gdscript_comments(
        po, gdscript_comments_by_msgid
    )
    if missing_comments or missing_references:
        print("GDScript comment validation failed:")
        for msgid in missing_comments:
            print(f"  Missing msgid: {msgid}")
        for msgid, path in missing_references:
            print(f"  Missing reference: {path}: {msgid}")
        raise RuntimeError("output.po does not contain all GDScript comments")

    print(f"  GDScript comments validated: {len(gdscript_comments_by_msgid)}")

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
