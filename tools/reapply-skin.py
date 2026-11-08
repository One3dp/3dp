#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""全站皮肤复检 / 修复（幂等，可重复运行）。

背景：intl-report.html 等页面由「每周刷新」脚本用旧模板重新生成，会丢掉
统一皮肤的引用（site.css / site.js / favicon），并把主标题 emoji 带回来，
导致该页退回旧的蓝紫渐变配色。刷新完成后运行本脚本即可重新接回统一风格。

用法：python tools/reapply-skin.py
"""
import os
import re

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

FAVICON = (
    '<link rel="icon" href="data:image/svg+xml,'
    "%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 32 32'%3E"
    "%3Crect width='32' height='32' fill='%23141414'/%3E"
    "%3Cpath d='M16 6l9 5v10l-9 5-9-5V11z' fill='none' "
    "stroke='%23e64b23' stroke-width='2'/%3E%3C/svg%3E\">"
)

# 只清理主标题开头的装饰性 emoji，正文里的 emoji 不动
EMOJI_H1 = re.compile(
    r'(<h1[^>]*>)\s*[\U0001F300-\U0001FAFF\u2600-\u27BF]\s*'
)


def is_redirect(text):
    low = text.lower()
    return 'http-equiv="refresh"' in low or 'location.replace' in low


def main():
    changed = []
    for dirpath, dirnames, filenames in os.walk(ROOT):
        dirnames[:] = [d for d in dirnames
                       if d not in ('.git', 'assets', 'covers', 'tools')]
        for name in filenames:
            if not name.endswith('.html'):
                continue
            path = os.path.join(dirpath, name)
            rel = os.path.relpath(path, ROOT).replace('\\', '/')
            if rel == 'index.html':
                continue  # 首页样式自包含，不注入

            raw = open(path, 'rb').read()
            text = raw.decode('utf-8', 'surrogateescape')
            before = text
            base = '../' * rel.count('/')
            acts = []

            if 'rel="icon"' not in text:
                text = text.replace('</head>', FAVICON + '\n</head>', 1)
                acts.append('favicon')

            if 'assets/site.css' not in text:
                text = text.replace(
                    '</head>',
                    '<link rel="stylesheet" href="%sassets/site.css">\n</head>' % base,
                    1,
                )
                acts.append('css')

            if 'assets/site.js' not in text and not is_redirect(text):
                text = text.replace(
                    '</body>',
                    '<script src="%sassets/site.js"></script>\n</body>' % base,
                    1,
                )
                acts.append('js')

            stripped = EMOJI_H1.sub(r'\1', text)
            if stripped != text:
                text = stripped
                acts.append('h1-emoji')

            if text != before:
                open(path, 'wb').write(text.encode('utf-8', 'surrogateescape'))
                changed.append((rel, acts))

    print('检查完成：修复 %d 个页面' % len(changed))
    for rel, acts in changed:
        print('  %-52s %s' % (rel, ', '.join(acts)))
    if not changed:
        print('  全部页面皮肤完好，无需修复。')


if __name__ == '__main__':
    main()
