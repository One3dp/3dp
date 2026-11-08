/* ============================================================
   One3DP · 3D PRINT WORKSTATION — 全站统一行为层
   为归档日报页等无导航页面补齐统一顶栏 / 页脚 / 主题切换 / 回到顶部
   不改动任何页面原有的业务逻辑
   ============================================================ */
(function () {
  'use strict';

  var me = document.currentScript;
  var src = (me && me.src) ? me.src : '';
  var match = src.match(/^(.*\/)assets\/site\.js(\?.*)?$/);
  var base = match ? match[1] : '';
  var THEME_KEY = 'one3dp_theme';

  function theme() {
    return document.body.getAttribute('data-theme') || 'light';
  }
  function setTheme(t) {
    document.body.setAttribute('data-theme', t);
    try { localStorage.setItem(THEME_KEY, t); } catch (e) {}
  }

  /* 归档页 / 跳转页没有主题脚本，这里统一补上持久化 */
  try {
    var saved = localStorage.getItem(THEME_KEY);
    if (!document.body.hasAttribute('data-theme') || !document.querySelector('.tbtn, .icon-btn')) {
      if (saved === 'dark' || saved === 'light') setTheme(saved);
      else if (!document.body.hasAttribute('data-theme')) setTheme('light');
    }
  } catch (e) {}

  function el(html) {
    var d = document.createElement('div');
    d.innerHTML = html;
    return d.firstElementChild;
  }

  /* ---------- 统一顶栏：仅当页面本身没有导航时注入 ---------- */
  if (!document.querySelector('.topnav, .masthead, .ws-masthead')) {
    var head = el(
      '<header class="ws-masthead">' +
        '<div class="ws-inner">' +
          '<a class="ws-brand" href="' + base + 'index.html">' +
            '<span class="ws-mark" aria-hidden="true"></span>一言智造' +
            '<span class="ws-en">ONE3DP</span>' +
          '</a>' +
          '<nav class="ws-nav" aria-label="主导航">' +
            '<a href="' + base + 'index.html#workspace">首页总览</a>' +
            '<a href="' + base + 'daily-hotspots.html">热点资讯</a>' +
            '<a href="' + base + 'weekly-trends.html">每周趋势</a>' +
            '<a href="' + base + 'history.html">历史归档</a>' +
            '<a href="' + base + 'price-calculator.html">报价计算器</a>' +
            '<a href="' + base + 'filament-guide.html">耗材资料</a>' +
          '</nav>' +
          '<div class="ws-actions">' +
            '<button class="ws-btn" id="wsThemeBtn" title="切换深浅色" aria-label="切换深浅色">◐</button>' +
            '<a class="ws-btn" href="' + base + 'index.html" title="返回首页" aria-label="返回首页">↗</a>' +
          '</div>' +
        '</div>' +
      '</header>'
    );
    document.body.insertBefore(head, document.body.firstChild);
    var tb = document.getElementById('wsThemeBtn');
    if (tb) tb.addEventListener('click', function () { setTheme(theme() === 'dark' ? 'light' : 'dark'); });
  }

  /* ---------- 统一页脚 ---------- */
  if (!document.querySelector('.ws-footer')) {
    var old = document.querySelector('.footer');
    if (old) old.style.display = 'none';
    var foot = el(
      '<footer class="ws-footer">' +
        '<div class="ws-wrap">' +
          '<div class="ws-footer-top">' +
            '<div class="ws-word">MAKE IT <span>REAL.</span></div>' +
            '<div class="ws-footer-links">' +
              '<a href="https://space.bilibili.com/1384210206" target="_blank" rel="noopener">B 站</a>' +
              '<a href="https://www.douyin.com/user/self" target="_blank" rel="noopener">抖音</a>' +
              '<a href="https://www.xiaohongshu.com/user/profile/5c9d41ed000000001102b987" target="_blank" rel="noopener">小红书</a>' +
              '<a href="https://github.com/One3dp/3dp" target="_blank" rel="noopener">GitHub</a>' +
              '<a href="' + base + 'history.html">历史归档</a>' +
            '</div>' +
          '</div>' +
          '<div class="ws-meta">' +
            '<span>© 2026 一言智造 One3DP · 3D PRINT WORKSTATION</span>' +
            '<a href="' + base + 'index.html">返回首页 ↑</a>' +
          '</div>' +
        '</div>' +
      '</footer>'
    );
    document.body.appendChild(foot);
  }

  /* ---------- 回到顶部 ---------- */
  if (!document.querySelector('.ws-to-top')) {
    var top = el('<button class="ws-to-top" title="回到顶部" aria-label="回到顶部">↑</button>');
    document.body.appendChild(top);
    window.addEventListener('scroll', function () {
      if (window.scrollY > 480) top.classList.add('show');
      else top.classList.remove('show');
    }, { passive: true });
    top.addEventListener('click', function () {
      window.scrollTo({ top: 0, behavior: 'smooth' });
    });
  }

  /* ---------- 当前栏目高亮 ---------- */
  var here = location.pathname.split('/').pop() || 'index.html';
  document.querySelectorAll('.topnav .navtabs a, .ws-nav a').forEach(function (a) {
    var href = a.getAttribute('href') || '';
    if (href.split('#')[0].split('/').pop() === here) a.classList.add('active');
  });
})();
