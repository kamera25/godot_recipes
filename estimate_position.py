import argparse
import re

def heuristic_estimate(text):
    text_lower = text.lower()

    # "座標" を示唆するキーワード群
    coord_keywords = [" x ", " y ", " z ", "vector", "vector2", "vector3", "axis", "axes", "pixel", "grid", "offset", "value", "(", ",", ")"]

    # "位置" を示唆するキーワード群
    location_keywords = ["start", "target", "relative", "where", "place", "move", "update", "change", "node", "object"]

    coord_score = sum(1 for kw in coord_keywords if kw in text_lower)
    location_score = sum(1 for kw in location_keywords if kw in text_lower)

    # positionという単語そのものがどう使われているか
    # e.g., position property -> 座標
    if "position property" in text_lower or "position properties" in text_lower:
        coord_score += 2

    if "position of" in text_lower:
        location_score += 1

    if coord_score > location_score:
        return "座標"
    elif location_score > coord_score:
        return "位置"
    else:
        return "位置 (デフォルト/判別困難)"

def estimate_translation(po_file):
    try:
        with open(po_file, "r", encoding="utf-8") as f:
            content = f.read()
    except FileNotFoundError:
        print(f"Error: File '{po_file}' not found.")
        return

    blocks = content.split("\n\n")
    results = []

    for b in blocks:
        if "msgid" in b and "msgstr" in b:
            lines = b.split('\n')
            msgid_lines = []
            state = None
            for line in lines:
                if line.startswith('msgid '):
                    state = 'msgid'
                    msgid_lines.append(line[6:].strip().strip('"'))
                elif line.startswith('msgstr '):
                    state = 'msgstr'
                elif line.startswith('"') and state == 'msgid':
                    msgid_lines.append(line.strip().strip('"'))

            en = "".join(msgid_lines)

            if "position" in en.lower():
                estimation = heuristic_estimate(en)
                results.append((en, estimation))

    print("--- 英文のヒューリスティック分析による「position」の訳語推定 ---\n")

    z_count = 0
    i_count = 0
    u_count = 0

    for en, est in results:
        print(f"原文: {en}")
        print(f"推定: {est}")
        print("-" * 40)

        if est == "座標":
            z_count += 1
        elif est.startswith("位置"):
            if "デフォルト" in est:
                u_count += 1
            else:
                i_count += 1

    total = len(results)
    print(f"\n【総括】")
    print(f"「position」を含む文節数: {total}")
    print(f"「座標」と推定された数: {z_count}")
    print(f"「位置」と推定された数: {i_count}")
    print(f" 判別困難(デフォルト「位置」)の数: {u_count}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Estimate translation for 'position' based on English heuristics.")
    parser.add_argument("file", help="PO file to analyze", nargs="?", default="output.po")
    args = parser.parse_args()
    estimate_translation(args.file)
