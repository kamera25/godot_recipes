import polib
import re

def safe_rewrite(text):
    if "```" in text or "<" in text or "{{" in text or "[" in text:
        return text
    if text.startswith("> ") or text.startswith("- ") or text.startswith("* "):
        return text

    sentences = re.split(r'(?<=。)(?![\]\)\"\'」』])', text)
    new_sentences = []

    op_verbs = ["追加", "選択", "クリック", "設定", "入力", "変更", "作成", "保存", "移動", "ドラッグ", "ドロップ", "配置", "実行"]

    for sentence in sentences:
        if not sentence:
            continue

        parts = re.split(r'(して、|し、)', sentence)
        if len(parts) <= 1:
            new_sentences.append(sentence)
            continue

        steps = []
        current = ""
        for i in range(len(parts)):
            if parts[i] in ["して、", "し、"]:
                current += parts[i]
                # Is it a clear instruction?
                if any(verb in current for verb in op_verbs):
                    # Check for temporal clauses and avoid splitting
                    if "後に" in current or "前に" in current or "直後に" in current or "際に" in current or "時に" in current:
                        pass
                    else:
                        steps.append(current)
                        current = ""
            else:
                current += parts[i]

        if current:
            steps.append(current)

        if len(steps) < 2:
            new_sentences.append(sentence)
            continue

        cleaned_steps = []
        for i, step in enumerate(steps):
            if step.endswith("して、"):
                step = step[:-3] + "してください"
            elif step.endswith("し、"):
                step = step[:-2] + "してください"
            elif step.endswith("します。"):
                step = step[:-4] + "してください。"
            elif step.endswith("します"):
                step = step[:-3] + "してください"

            cleaned_steps.append(step)

        final_steps = []
        if len(cleaned_steps) >= 3:
            final_steps.append(cleaned_steps[0])
            final_steps.append("次に、" + cleaned_steps[1])
            for j in range(2, len(cleaned_steps)-1):
                final_steps.append("その後、" + cleaned_steps[j])
            final_steps.append("最後に、" + cleaned_steps[-1])
        else:
            final_steps = cleaned_steps # 2 steps -> No connecting words based on instructions

        for i, fs in enumerate(final_steps):
            if not fs.endswith("。") and not fs.endswith("！") and not fs.endswith("？") and not fs.endswith("：") and not fs.endswith(":"):
                if i == len(final_steps) - 1:
                    pass
                else:
                    fs += "。"
            final_steps[i] = fs

        rejoined = "".join(fs if fs.endswith("。") or fs.endswith("！") or fs.endswith("？") or fs.endswith("：") or fs.endswith(":") else fs + "。" for fs in final_steps)
        rejoined = rejoined.replace("。。", "。")
        new_sentences.append(rejoined)

    res = "".join(new_sentences)
    res = res.replace("。。", "。")
    return res

po = polib.pofile("output.po")
for entry in po:
    if "して、" in entry.msgstr or "し、" in entry.msgstr:
        new_str = safe_rewrite(entry.msgstr)
        if new_str != entry.msgstr:
            entry.msgstr = new_str

po.save("output_fixed.po")
