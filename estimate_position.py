import argparse

def estimate_translation(po_file):
    try:
        with open(po_file, "r", encoding="utf-8") as f:
            content = f.read()
    except FileNotFoundError:
        print(f"Error: File '{po_file}' not found.")
        return

    blocks = content.split("\n\n")
    z_count = 0
    i_count = 0
    for b in blocks:
        if "msgid" in b and "msgstr" in b:
            # Simple line parsing:
            lines = b.split('\n')
            msgid_lines = []
            msgstr_lines = []
            state = None
            for line in lines:
                if line.startswith('msgid '):
                    state = 'msgid'
                    msgid_lines.append(line[6:].strip().strip('"'))
                elif line.startswith('msgstr '):
                    state = 'msgstr'
                    msgstr_lines.append(line[7:].strip().strip('"'))
                elif line.startswith('"') and state == 'msgid':
                    msgid_lines.append(line.strip().strip('"'))
                elif line.startswith('"') and state == 'msgstr':
                    msgstr_lines.append(line.strip().strip('"'))

            en = "".join(msgid_lines).lower()
            ja = "".join(msgstr_lines)

            if "position" in en:
                if "座標" in ja:
                    z_count += 1
                if "位置" in ja:
                    i_count += 1

    print("--- 翻訳確率推定 ---")
    print(f"「position」の出現ブロックのうち:")
    print(f"「座標」が含まれるブロック数: {z_count}")
    print(f"「位置」が含まれるブロック数: {i_count}")

    total = z_count + i_count
    if total > 0:
        z_prob = z_count / total * 100
        i_prob = i_count / total * 100
        better_word = "座標" if z_count > i_count else "位置"
        better_prob = z_prob if z_count > i_count else i_prob
        print(f"推測: 「{better_word}」が適当である確率が {better_prob:.1f}% と推定されます。")
        print(f"結果: 「{better_word}」の方が多く使われています。")
    else:
        print("「position」という単語が含まれ、かつ「座標」か「位置」と訳されているブロックが見つかりませんでした。")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Estimate the translation for 'position'.")
    parser.add_argument("file", help="PO file to analyze", nargs="?", default="output.po")
    args = parser.parse_args()
    estimate_translation(args.file)
