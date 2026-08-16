#!/usr/bin/env python3
"""挑完配色後跑這支，確認可讀性。

用法:
    python3 check_palette.py '#B0175B' '#F2ECE3'          # 檢查單組 ink/paper
    python3 check_palette.py --file path/to/index.html    # 掃出檔案裡全部六組

為什麼要跑：整份手冊大量使用 --ink-60（備註、說明、eyebrow）與 --ink-38（次要拼音、
虛線），它們是 ink 對 paper 的半透明混色。base 對比不夠高的話，這些文字會糊掉——
而且是在手機上、在陽光下才發現。
"""
import re
import sys


def _lin(c):
    c /= 255
    return c / 12.92 if c <= 0.03928 else ((c + 0.055) / 1.055) ** 2.4


def luminance(hexcolor):
    h = hexcolor.lstrip('#')
    if len(h) == 3:
        h = ''.join(ch * 2 for ch in h)
    r, g, b = (int(h[i:i + 2], 16) for i in (0, 2, 4))
    return .2126 * _lin(r) + .7152 * _lin(g) + .0722 * _lin(b)


def contrast(a, b):
    la, lb = luminance(a), luminance(b)
    hi, lo = max(la, lb), min(la, lb)
    return (hi + .05) / (lo + .05)


def blend(ink, paper, alpha):
    """模擬 rgba(ink, alpha) 疊在 paper 上的實際顏色。"""
    ih, ph = ink.lstrip('#'), paper.lstrip('#')
    out = []
    for i in (0, 2, 4):
        iv, pv = int(ih[i:i + 2], 16), int(ph[i:i + 2], 16)
        out.append(round(iv * alpha + pv * (1 - alpha)))
    return '#%02X%02X%02X' % tuple(out)


# 門檻的來源，都是實測而非拍腦袋：
#   4.5 = WCAG AA 對一般字級的要求，正文（純 --ink）必須跨過，否則整頁吃力。
#   7.0 = 留給衍生層級的餘裕。base 到 7 時 ink-60 約 3.3 以上，備註文字還讀得動。
# 參考值：曼谷那三組實測 base 5.40–9.59、ink-60 2.50–4.12，在手機上實際使用沒問題，
# 所以 5.x 是「可用但要知道取捨」，不是壞掉。
BASE_GOOD = 7.0
BASE_MIN = 4.5


def report(label, ink, paper):
    base = contrast(ink, paper)
    tiers = {a: contrast(blend(ink, paper, a), paper) for a in (.85, .60, .38)}

    if base >= BASE_GOOD:
        mark, note = 'OK  ', ''
    elif base >= BASE_MIN:
        mark, note = 'WARN', '  ← 正文可讀，但次要層級會偏淡'
    else:
        mark, note = 'FAIL', '  ← 正文就未達 WCAG AA 4.5，換一組'

    print(f'{mark} {label:12} ink {ink}  paper {paper}')
    print(f'       base {base:5.2f}   ink-85 {tiers[.85]:5.2f}   '
          f'ink-60 {tiers[.60]:5.2f}   ink-38 {tiers[.38]:5.2f}{note}')
    if base >= BASE_MIN and tiers[.60] < 4.5:
        print(f'       ink-60 只有 {tiers[.60]:.2f}：硬底線、金額、警告這類資訊'
              f'不要只放在 .cost-note／.note 層級，要進 .alert 或用 <b>。')
    return base >= BASE_MIN


PALETTE_RE = re.compile(
    r'html\[data-theme="(?P<theme>[^"]+)"\]\[data-mode="(?P<mode>[^"]+)"\][^{]*\{'
    r'[^}]*--ink:\s*(?P<ink>#[0-9A-Fa-f]{3,6})'
    r'[^}]*--paper:\s*(?P<paper>#[0-9A-Fa-f]{3,6})')


def main():
    args = sys.argv[1:]
    if not args:
        print(__doc__)
        return 1

    if args[0] == '--file':
        text = open(args[1], encoding='utf-8').read()
        found = list(PALETTE_RE.finditer(text))
        if not found:
            print('在檔案裡找不到 html[data-theme][data-mode] 的配色宣告。')
            return 1
        ok = True
        for m in found:
            ok &= report(f"{m['theme']}/{m['mode']}", m['ink'], m['paper'])
        print()
        print('全部通過。' if ok else '有配色未達下限，請調整後重跑。')
        return 0 if ok else 1

    ink, paper = args[0], args[1]
    return 0 if report('custom', ink, paper) else 1


if __name__ == '__main__':
    sys.exit(main())
