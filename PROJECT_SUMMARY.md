# Expense Tracker — 项目总结

> 项目地址：https://github.com/dok4everak47/expense-tracker  
> 启动命令：`cd /Users/dok4ever/expense-tracker && uv run uvicorn main:app --reload && open index.html`  
> 完成日期：2026-05-31

---

## 技术栈

| 层级 | 技术 |
|------|------|
| 后端 | Python 3.13 + FastAPI |
| 数据库 | SQLite（expenses 表 + budgets 表） |
| 前端 | Vanilla HTML/CSS/JS + ECharts 5.5（CDN） |
| 字体 | Inter（Google Fonts） |
| 包管理 | uv |
| 图表 | ECharts（环形图、柱状图+均线、分组柱状图） |

---

## API

| 方法 | 路径 | 功能 |
|------|------|------|
| POST | `/expenses` | 记一笔 |
| GET | `/expenses?category=&date=&month=` | 查账单 |
| PUT | `/expenses/{id}` | 改账单 |
| DELETE | `/expenses/{id}` | 删账单 |
| GET | `/expenses/summary?month=` | 分类汇总 |
| GET | `/expenses/daily?month=` | 按天统计 |
| GET | `/expenses/months` | 所有月份 |
| POST | `/expenses/import` | 上传微信 xlsx |
| GET/POST | `/budget` | 预算管理 |

---

## 前端页面

| 标签页 | 功能 |
|--------|------|
| 💰 记账 | 双列布局：左侧记账表单+汇总，右侧分类筛选+日期筛选+账单列表 |
| 📊 报表 | 月份选择器、KPI 卡片（月总/日均/吃饭占比/单日最高）、环形图、每日柱状图+7日均线、预算对比分组柱、点击弹明细弹窗 |
| ⚙️ 预算 | 每月每分类设置预算 |
| 📥 导入 | 上传微信 xlsx，智能分类 77+ 商户 |

---

## 智能分类映射

从微信商户名自动识别分类，覆盖：

- **吃饭：** 小笼包、鸡爪、蜜雪冰城、luckin、喜茶、全上品、小汤总、星巴克、牛爷烧、Cotti、袁小饺、云吞、都市甜心、朴大叔、夏天、玉小灶、赵一鸣、超市等
- **交通：** 滴滴、地铁、公交、高铁、杭州青奇、美团单车
- **购物：** 淘宝、京东、拼多多、顺丰
- **娱乐：** 腾讯、游戏、视频、音乐、DP、KTV、B站
- **住房：** 房租、水电、物业、燃气

---

## 图表

| 图表 | 类型 | 说明 |
|------|------|------|
| 环形图 | ECharts pie (doughnut) | 中间显示总金额，hover 显示百分比 |
| 每日趋势 | 柱状图 + 7日均线 | 蓝色柱（#818cf8），红色均线，hover 提示，点击弹日期明细 |
| 预算对比 | 分组柱状图 | 实际=彩色柱，预算=浅黄+橙边框，超预算变红，点击弹分类明细 |

---

## 对照视频 10 步框架

| 步骤 | 内容 | 状态 |
|------|------|------|
| 1 | 选一个客户 | ✅ 你自己，记账 |
| 2 | 定义用户 | ✅ |
| 3 | 选一个技术栈 | ✅ Python + FastAPI + SQLite |
| 4 | 100 法则 | ⬜ 持续中 |
| 5 | 核心循环 | ✅ 记→查→汇 |
| 6 | 公开贴出来 | ✅ GitHub |
| 7 | 建造者环境 | ⬜ |
| 8 | 干掉 ego | ✅ |
| 9 | "我能用吗？" | ⬜ |
| 10 | 选择 | ✅ 选了 B |

---

## 视频核心引用

- "Tech doesn't reward knowers. Tech rewards solvers."
- "AI writes code you don't understand → you own nothing. That's dependency with lipstick."
- "School is built for grades. Industry is built for shipping. Different game."
- "Waiting is the new quitting."
- "You are one working prototype away from changing your entire trajectory."

---

## 待做

- [ ] 每天记账（100 法则第 4 步）
- [ ] 前端加编辑入口（后端 PUT 已有）
- [ ] 导出 CSV
- [ ] 月度对比
- [ ] 搜索功能

---

## 项目文件

```
/Users/dok4ever/expense-tracker/
├── main.py              # FastAPI 后端
├── index.html           # 前端 SPA
├── import_wechat.py     # CLI 导入脚本
├── expenses.db          # SQLite（不上传 git）
├── pyproject.toml       # uv 配置
├── README.md            # 项目说明
└── .pi/skills/          # AI skill（项目记忆）
```
