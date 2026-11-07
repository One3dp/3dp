# 3D打印工作站

一言智造One3DP 的个人工作台导航：每日热点 / 报价计算器 / 耗材管理 / 耗材资料 / 模型比赛汇总。

部署：GitHub Pages（根目录，无构建）。

## 全站视觉规范

所有页面共用 `assets/site.css` + `assets/site.js`：纸白 / 墨黑 / 一抹朱橙，直角细线、无阴影，支持深浅主题（localStorage 键 `one3dp_theme`）。

新增页面时在 `</head>` 前引入 `assets/site.css`、在 `</body>` 前引入 `assets/site.js`（子目录用 `../assets/...`），即可自动获得统一顶栏、页脚、主题切换与回到顶部。首页 `index.html` 自带完整样式，不需要引入。
