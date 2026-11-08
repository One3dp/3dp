#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""全站皮肤 / 栏目文案复检（幂等，可重复运行）。

背景：intl-report.html 等页面由「每周刷新」脚本用旧模板重新生成，会丢掉
统一皮肤的引用（site.css / site.js / favicon），把主标题 emoji 带回来，
并把栏目名、时间口径退回旧版（国际3D打印热点 / 近 48 小时 / 每日日报）。
刷新完成后运行本脚本即可恢复统一风格与统一文案。

全站文案规范（2026-11-08 起）：
  栏目名   国内每周热点 / 国际每周热点
  时间标签 近一周（入口、导航、按钮、副标题统一）
  副标题   近一周 · 每周更新 · 北京时间 UTC+8 · 覆盖窗口：...
  功能名   常用功能列表与对应页面 h1 一律四个字
  顶部导航 一律四个字：首页总览 / 打印工具 / 资源中心 / 社区交流
  标题     <栏目名> · <日期> · 3D打印工作台

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

SUB_PREFIX = '近一周 · 每周更新 · 北京时间 UTC+8 · '

# 精确串替换：只改界面标签，不动正文新闻内容
RULES = [
    # ---- 顶部导航：四项一律四个字 ----
    ('>工作台</a>', '>首页总览</a>', '导航四字'),
    ('3D打印工具', '打印工具', '导航四字'),
    # ---- 首页 hero 两行：名称与时间标签统一 ----
    ('<span class="t">国际热点</span><small>全球动态</small>',
     '<span class="t">国际每周热点</span><small>近一周</small>', '首页国际栏目'),
    # ---- 首页常用功能：五个名称一律四个字 ----
    ('<div class="name">报价计算器</div>', '<div class="name">报价计算</div>', '功能名四字'),
    ('<div class="name">模型比赛汇总</div>', '<div class="name">模型比赛</div>', '功能名四字'),
    ('热点资讯、报价计算器、耗材管理、耗材资料与常用工具',
     '热点资讯、报价计算、耗材管理、耗材资料与常用工具', '首页描述'),
    # ---- 首页快捷子链接：四字 + 周口径 ----
    ('<a href="daily-hotspots.html">国内每周 →</a><a href="intl-report.html">国际热点 →</a><a href="daily-report.html">每日报告 →</a>',
     '<a href="daily-hotspots.html">国内周报 →</a><a href="intl-report.html">国际周报 →</a><a href="daily-report.html">完整周报 →</a>',
     '首页子链接'),
    # ---- 热点速览页 ----
    ('<div class="sub">每天 09:00 自动生成并同步，直达最新日报 / 国际版 / 历史归档</div>',
     '<div class="sub">近一周 · 每周更新 · 北京时间 UTC+8 · 直达国内 / 国际周报与历史归档</div>',
     '速览副标题'),
    ('<a class="pbtn" href="daily-report.html">→ 今日日报</a>',
     '<a class="pbtn" href="daily-report.html">→ 国内每周热点</a>', '速览按钮'),
    ('<a class="pbtn" href="intl-report.html">🌍 国际版</a>',
     '<a class="pbtn" href="intl-report.html">→ 国际每周热点</a>', '速览按钮'),
    ('<div class="qt">今日国内日报</div>', '<div class="qt">国内每周热点</div>', '速览卡片'),
    ('<div class="qt">🌍 国际版热点</div>', '<div class="qt">国际每周热点</div>', '速览卡片'),
    ('<div class="qt">🗂 历史归档</div>', '<div class="qt">历史周报</div>', '速览卡片'),
    ('覆盖近 48 小时窗口', '覆盖近一周窗口', '时间口径'),
    ('<div class="open">打开日报 ↗</div>', '<div class="open">打开周报 ↗</div>', '速览卡片'),
    ('<div class="open">打开国际版 ↗</div>', '<div class="open">打开国际周报 ↗</div>', '速览卡片'),
    ('全部历史日报列表', '全部历史周报列表', '归档口径'),
    ('<div class="at">📂 历史日报（10 期）</div>', '<div class="at">历史周报（10 期）</div>', '归档口径'),
    # ---- 历史归档页 ----
    ('<h1>3D打印动态日报 · 热点存档</h1>',
     '<h1>国内每周热点 · 历史存档</h1>', '归档页标题'),
    ('<div class="sub">所有历史版本均保留于 GitHub 仓库 archive/ 目录，不会被新版本覆盖 · 更新于 2026-10-09 07:50</div>',
     '<div class="sub">近一周 · 每周更新 · 北京时间 UTC+8 · 历史周报保留于 GitHub 仓库 archive/ 目录 · 更新于 2026-10-09 07:50</div>',
     '归档副标题'),
    ('<b>🖨️ 最新版（今日）</b>', '<b>最新版（本周）</b>', '归档口径'),
    ('<h2>历史版本（15 份）</h2>', '<h2>历史周报（15 份）</h2>', '归档口径'),
    # ---- 统计条 / 其它界面标签 ----
    ('B站 48h 热门视频', 'B站 近一周热门视频', '统计条时间'),
    ('抖音 48h 实测视频', '抖音 近一周实测视频', '统计条时间'),
    ('小红书 48h 实测视频', '小红书 近一周实测视频', '统计条时间'),
    # ---- 功能页 h1：与首页列表一致，四个字 ----
    ('<h1>3D打印报价计算器</h1>', '<h1>报价计算</h1>', '功能页 h1'),
    ('<h1>3D打印耗材管理</h1>', '<h1>耗材管理</h1>', '功能页 h1'),
    ('<h1>3D耗材资料</h1>', '<h1>耗材资料</h1>', '功能页 h1'),
    # ---- 旧栏目名兜底 ----
    ('国际3D打印热点', '国际每周热点', '栏目名'),
    ('3D打印动态日报', '国内每周热点', '栏目名'),
]

PAGE_TITLES = {
    'daily-hotspots.html': '国内每周热点 · 3D打印工作台',
    'history.html': '国内每周热点 · 历史存档 · 3D打印工作台',
    'price-calculator.html': '报价计算 · 3D打印工作台',
    'filament-manager.html': '耗材管理 · 3D打印工作台',
    'filament-guide.html': '耗材资料 · 3D打印工作台',
}


def is_redirect(text):
    low = text.lower()
    return 'http-equiv="refresh"' in low or 'location.replace' in low


def set_title(text, title):
    return re.sub(r'<title>.*?</title>', '<title>' + title + '</title>',
                  text, count=1, flags=re.S)


def unify_copy(text, rel):
    """把栏目名、时间口径、标题格式统一到全站规范。"""
    acts = []
    for old, new, tag in RULES:
        if old in text:
            text = text.replace(old, new)
            if tag not in acts:
                acts.append(tag)

    # 章节小标题里的「近 48h / 近 48 小时」→「近一周」
    def h2_fix(m):
        body = m.group(2).replace('近 48h', '近一周').replace('近 48 小时', '近一周')
        return m.group(1) + body + m.group(3)
    fixed = re.sub(r'(<h2[^>]*>)(.*?)(</h2>)', h2_fix, text, flags=re.S)
    if fixed != text:
        text = fixed
        acts.append('章节时间口径')

    # 标题统一格式：<栏目名> · <日期> · 3D打印工作台
    if rel in PAGE_TITLES:
        text = set_title(text, PAGE_TITLES[rel])
    elif rel == 'intl-report.html':
        # 优先用副标题里的快照日期（h1 里的生成起始日常与数据窗口不一致）
        m = (re.search(r'模型榜/视频快照 (20\d\d-\d\d-\d\d)', text)
             or re.search(r'<title>[^<]*?(20\d\d-\d\d-\d\d)[^<]*</title>', text))
        date = m.group(1) if m else ''
        text = set_title(text, '国际每周热点' + (' · ' + date if date else '') + ' · 3D打印工作台')
        text = re.sub(r'(<h1[^>]*>)\s*国际每周热点[^<]*</h1>',
                      r'\1国际每周热点</h1>', text, count=1)
    elif rel == 'daily-report.html' or rel.startswith('archive/'):
        m = re.search(r'<title>国内每周热点 · ([^<]+)</title>', text)
        if m:
            date = m.group(1).replace(' · 3D打印工作台', '').strip()
            text = set_title(text, '国内每周热点 · ' + date + ' · 3D打印工作台')

    # 副标题统一：近一周 · 每周更新 · 北京时间 UTC+8 · 覆盖窗口：...
    m = re.search(r'<div class="sub">([^<]*)</div>', text)
    if m and '覆盖窗口' in m.group(1) and SUB_PREFIX not in m.group(1):
        body = m.group(1)
        window = body[body.index('覆盖窗口'):]
        window = window.replace('（近 48 小时）', '').replace('（近 48h）', '').strip(' ·')
        new_sub = '<div class="sub">' + SUB_PREFIX + window + '</div>'
        text = text[:m.start()] + new_sub + text[m.end():]
        acts.append('副标题时间')

    return text, acts


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

            raw = open(path, 'rb').read()
            text = raw.decode('utf-8', 'surrogateescape')
            before = text
            base = '../' * rel.count('/')
            acts = []

            if rel != 'index.html':  # 首页样式自包含，不注入
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

            text, copy_acts = unify_copy(text, rel)
            acts.extend(copy_acts)

            if text != before:
                open(path, 'wb').write(text.encode('utf-8', 'surrogateescape'))
                changed.append((rel, acts))

    print('检查完成：更新 %d 个页面' % len(changed))
    for rel, acts in changed:
        print('  %-52s %s' % (rel, ', '.join(dict.fromkeys(acts))))
    if not changed:
        print('  全部页面皮肤与文案均已统一，无需修复。')


if __name__ == '__main__':
    main()
