#!/usr/bin/env python3
import sys
import os
import argparse

def check_po_backticks(filepath, report_path=None):
    if not os.path.exists(filepath):
        print(f"Error: File not found: {filepath}")
        return

    print(f"Analyzing {filepath} ...")
    
    entries = []
    current_entry = None
    current_field = None
    
    with open(filepath, 'r', encoding='utf-8') as f:
        for line_num, line in enumerate(f, 1):
            line_str = line.strip()
            
            # 空行はエントリーの区切り
            if not line_str:
                if current_entry:
                    entries.append(current_entry)
                    current_entry = None
                current_field = None
                continue
            
            # コメント行はスキップ
            if line_str.startswith("#"):
                continue
                
            if line_str.startswith('msgid '):
                if current_entry:
                    entries.append(current_entry)
                current_entry = {
                    'msgid': '',
                    'msgstr': '',
                    'msgid_line': line_num,
                    'msgstr_line': None
                }
                current_field = 'msgid'
                content = line_str[6:].strip()
                if content.startswith('"') and content.endswith('"'):
                    current_entry['msgid'] += content[1:-1]
                    
            elif line_str.startswith('msgstr '):
                current_field = 'msgstr'
                if current_entry:
                    current_entry['msgstr_line'] = line_num
                content = line_str[7:].strip()
                if content.startswith('"') and content.endswith('"'):
                    if current_entry:
                        current_entry['msgstr'] += content[1:-1]
                        
            elif line_str.startswith('"') and line_str.endswith('"'):
                if current_entry:
                    val = line_str[1:-1]
                    if current_field == 'msgid':
                        current_entry['msgid'] += val
                    elif current_field == 'msgstr':
                        current_entry['msgstr'] += val
            else:
                # その他のフォーマット行（ヘッダー等）
                pass
                
        if current_entry:
            entries.append(current_entry)

    mismatches = []
    untranslated_count = 0
    
    for entry in entries:
        msgid = entry['msgid']
        msgstr = entry['msgstr']
        
        # msgidがヘッダー（空文字列）の場合はスキップ
        if not msgid and entry['msgid_line'] <= 5:
            continue
            
        # 翻訳が空のものは未翻訳としてカウント（比較からは除外する。未翻訳はバッククォート数が合わないのが当然のため）
        if not msgstr:
            untranslated_count += 1
            continue
            
        # エスケープされたバッククォート \` も考慮して、単純に ` をカウントする
        # （エスケープされていてもされていなくても、ペアになるはず）
        count_id = msgid.count('`')
        count_str = msgstr.count('`')
        
        if count_id != count_str:
            mismatches.append({
                'msgid_line': entry['msgid_line'],
                'msgstr_line': entry['msgstr_line'],
                'msgid': msgid,
                'msgstr': msgstr,
                'count_id': count_id,
                'count_str': count_str
            })
            
    print(f"Total entries processed: {len(entries)}")
    print(f"Untranslated entries skipped: {untranslated_count}")
    print(f"Mismatches found: {len(mismatches)}")
    print()
    
    if not mismatches:
        print("Success: All translated entries have matching backticks count!")
        return
        
    # レポートファイルの作成
    if report_path:
        with open(report_path, 'w', encoding='utf-8') as rf:
            rf.write(f"PO Backtick Match Report\n")
            rf.write(f"Target file: {filepath}\n")
            rf.write(f"Total entries processed: {len(entries)}\n")
            rf.write(f"Untranslated entries skipped: {untranslated_count}\n")
            rf.write(f"Mismatches found: {len(mismatches)}\n")
            rf.write("=" * 60 + "\n\n")
            
            for i, m in enumerate(mismatches, 1):
                rf.write(f"[{i}] Mismatch near line {m['msgid_line']}\n")
                rf.write(f"    Line (msgid) : {m['msgid_line']}\n")
                rf.write(f"    Line (msgstr): {m['msgstr_line']}\n")
                rf.write(f"    msgid  (` count: {m['count_id']}):\n")
                rf.write(f"      {m['msgid']}\n")
                rf.write(f"    msgstr (` count: {m['count_str']}):\n")
                rf.write(f"      {m['msgstr']}\n")
                rf.write("-" * 50 + "\n")
        print(f"Detailed report saved to: {report_path}")
        print()
        
    # 画面にはダイジェストを表示（最初の10件）
    print(f"--- Displaying first 10 mismatches ---")
    limit = min(10, len(mismatches))
    for i in range(limit):
        m = mismatches[i]
        print(f"[{i+1}] Mismatch near line {m['msgid_line']}")
        print(f"    Line (msgid) : {m['msgid_line']}")
        print(f"    Line (msgstr): {m['msgstr_line']}")
        print(f"    msgid  (` count: {m['count_id']}): {repr(m['msgid'])}")
        print(f"    msgstr (` count: {m['count_str']}): {repr(m['msgstr'])}")
        print("-" * 50)
    if len(mismatches) > 10:
        print(f"... and {len(mismatches) - 10} more mismatches. (Check '{report_path}' for all details)")

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Check msgid and msgstr backtick count consistency in PO files.")
    parser.add_argument('po_file', nargs='?', default='output.po', help="Path to the PO file to check (default: output.po)")
    parser.add_argument('-o', '--output', default='mismatch_report.txt', help="Path to save the detailed report (default: mismatch_report.txt)")
    
    args = parser.parse_args()
    check_po_backticks(args.po_file, args.output)
