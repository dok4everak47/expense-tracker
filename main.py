"""
记账 API — V1 核心循环
用户：你自己
问题：每天花钱没概念，月底不知道钱去哪了
核心循环：记一笔 → 看全部 → 看汇总
"""

from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import sqlite3
import openpyxl
import io
from datetime import date

app = FastAPI(title="Expense Tracker")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)


# ============================================================
# 1. 数据库初始化（只有一个文件，零配置）
# ============================================================
def get_db():
    conn = sqlite3.connect("expenses.db")
    conn.row_factory = sqlite3.Row  # 让查询结果可以用字段名访问
    return conn


def init_db():
    with get_db() as conn:
        conn.execute("""
            CREATE TABLE IF NOT EXISTS expenses (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                amount REAL NOT NULL,
                category TEXT NOT NULL,
                note TEXT DEFAULT '',
                date TEXT NOT NULL
            )
        """)
        # 预算表
        conn.execute("""
            CREATE TABLE IF NOT EXISTS budgets (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                category TEXT NOT NULL,
                amount REAL NOT NULL,
                month TEXT NOT NULL,
                UNIQUE(category, month)
            )
        """)
        conn.commit()


init_db()


# ============================================================
# 2. 数据模型
# ============================================================
class ExpenseCreate(BaseModel):
    amount: float  # 金额，比如 35.5
    category: str  # 分类，比如 吃饭、交通、购物
    note: str = ""  # 备注，可选的
    date: str = str(date.today())  # 日期，默认今天


# ============================================================
# 3. V1 核心循环：三个接口，一个心跳
# ============================================================


# 接口 1：记一笔账
@app.post("/expenses")
def add_expense(expense: ExpenseCreate):
    """花了一笔钱，记下来"""
    with get_db() as conn:
        cursor = conn.execute(
            "INSERT INTO expenses (amount, category, note, date) VALUES (?, ?, ?, ?)",
            (expense.amount, expense.category, expense.note, expense.date),
        )
        conn.commit()
        new_id = cursor.lastrowid
    return {"message": "账已记好 ✅", "id": new_id}


# 接口 2：看所有账（支持按分类 + 日期 + 月份筛选）
@app.get("/expenses")
def list_expenses(category: str = "", date: str = "", month: str = ""):
    """看看我到底花了多少钱"""
    with get_db() as conn:
        conditions = []
        params = []
        if category:
            conditions.append("category = ?")
            params.append(category)
        if date:
            conditions.append("date = ?")
            params.append(date)
        if month:
            conditions.append("date LIKE ?")
            params.append(month + "%")
        where = " AND ".join(conditions)
        sql = "SELECT id, amount, category, note, date FROM expenses"
        if where:
            sql += " WHERE " + where
        sql += " ORDER BY date DESC"
        rows = conn.execute(sql, params).fetchall()
    return [dict(row) for row in rows]


# 接口 2.5：删一条帐
@app.delete("/expenses/{expense_id}")
def delete_expense(expense_id: int):
    with get_db() as conn:
        cursor = conn.execute(
            "DELETE FROM expenses WHERE id = ?",
            (expense_id,),
        )
        conn.commit()
        if cursor.rowcount == 0:
            return {"message": "没找到这条帐❌"}
    return {"message": f"第{expense_id}条已删✅"}


# 接口 2.6：改一条账
@app.put("/expenses/{expense_id}")
def update_expense(expense_id: int, expense: ExpenseCreate):
    with get_db() as conn:
        cursor = conn.execute(
            "UPDATE expenses SET amount = ?, category = ?, note = ?, date = ? WHERE id = ?",
            (expense.amount, expense.category, expense.note, expense.date, expense_id),
        )
        conn.commit()
        if cursor.rowcount == 0:
            return {"message": "没找到这条帐❌"}
    return {"message": f"第{expense_id}条已修改✅"}


# 接口 3：按分类汇总（支持按月份筛选）
@app.get("/expenses/summary")
def summary(month: str = ""):
    """我吃饭花了多少？交通花了多少？month 格式: 2026-05"""
    with get_db() as conn:
        if month:
            rows = conn.execute(
                "SELECT category, SUM(amount) as total, COUNT(*) as count FROM expenses WHERE date LIKE ? GROUP BY category ORDER BY total DESC",
                (month + "%",),
            ).fetchall()
        else:
            rows = conn.execute(
                "SELECT category, SUM(amount) as total, COUNT(*) as count FROM expenses GROUP BY category ORDER BY total DESC"
            ).fetchall()
    return [dict(row) for row in rows]


# 接口 3.5：按天统计（支持按月份筛选）
@app.get("/expenses/daily")
def daily(month: str = ""):
    """每天花了多少钱"""
    with get_db() as conn:
        if month:
            rows = conn.execute(
                "SELECT date, SUM(amount) as total, COUNT(*) as count FROM expenses WHERE date LIKE ? GROUP BY date ORDER BY date",
                (month + "%",),
            ).fetchall()
        else:
            rows = conn.execute(
                "SELECT date, SUM(amount) as total, COUNT(*) as count FROM expenses GROUP BY date ORDER BY date"
            ).fetchall()
    return [dict(row) for row in rows]


# 接口 3.6：列出所有有数据的月份
@app.get("/expenses/months")
def months():
    """返回所有有消费记录的月份"""
    with get_db() as conn:
        rows = conn.execute(
            "SELECT DISTINCT substr(date, 1, 7) as month FROM expenses ORDER BY month"
        ).fetchall()
    return [row["month"] for row in rows]


# ============================================================
# 接口 4：上传微信账单 Excel
# ============================================================


# ============================================================
# 接口 5：预算管理
# ============================================================
class BudgetSet(BaseModel):
    month: str    # 2026-05
    budgets: dict # {"吃饭": 1000, "交通": 200, ...}


@app.get("/budget")
def get_budget(month: str = ""):
    """获取某月的预算设置"""
    if not month:
        month = str(date.today())[:7]
    with get_db() as conn:
        rows = conn.execute(
            "SELECT category, amount FROM budgets WHERE month = ?", (month,)
        ).fetchall()
    result = {}
    for row in rows:
        result[row["category"]] = row["amount"]
    return {"month": month, "budgets": result}


@app.post("/budget")
def set_budget(data: BudgetSet):
    """设置月度预算"""
    with get_db() as conn:
        for category, amount in data.budgets.items():
            conn.execute(
                "INSERT INTO budgets (category, amount, month) VALUES (?, ?, ?) ON CONFLICT(category, month) DO UPDATE SET amount = ?",
                (category, amount, data.month, amount),
            )
        conn.commit()
    return {"message": "预算已保存 ✅"}


# ============================================================
# 接口 4：上传微信账单 Excel（旧接口，保留）
# ============================================================
CATEGORY_MAP = {
    "小笼包": "吃饭", "鸡爪": "吃饭", "蜜雪冰城": "吃饭",
    "luckin": "吃饭", "咖啡": "吃饭", "奶茶": "吃饭",
    "餐厅": "吃饭", "饭店": "吃饭", "粉": "吃饭",
    "面": "吃饭", "粥": "吃饭", "烧烤": "吃饭",
    "火锅": "吃饭", "包子": "吃饭", "饭": "吃饭",
    "超市": "吃饭", "赵一鸣": "吃饭", "喜茶": "吃饭",
    "全上品": "吃饭", "小汤总": "吃饭", "星巴克": "吃饭",
    "牛爷烧": "吃饭", "Cotti": "吃饭", "袁小饺": "吃饭",
    "云吞": "吃饭", "都市甜心": "吃饭", "汉堡": "吃饭",
    "朴大叔": "吃饭", "拌饭": "吃饭", "夏天": "吃饭",
    "玉小灶": "吃饭",
    "滴滴": "交通", "地铁": "交通", "公交": "交通",
    "铁路": "交通", "高铁": "交通", "打车": "交通",
    "停车": "交通", "加油站": "交通", "充电": "交通",
    "杭州青奇": "交通", "青桔": "交通", "美团单车": "交通",
    "淘宝": "购物", "京东": "购物", "拼多多": "购物",
    "天猫": "购物", "唯品会": "购物", "顺丰": "购物",
    "腾讯": "娱乐", "游戏": "娱乐", "视频": "娱乐",
    "音乐": "娱乐", "会员": "娱乐", "电影": "娱乐",
    "影院": "娱乐", "KTV": "娱乐", "优酷": "娱乐",
    "哔哩": "娱乐", "B站": "娱乐", "DP": "娱乐",
    "房租": "住房", "水电": "住房", "物业": "住房",
    "燃气": "住房", "宽带": "住房",
}


def guess_category(merchant, product):
    text = (merchant or "") + (product or "")
    for keyword, category in CATEGORY_MAP.items():
        if keyword in text:
            return category
    return "其他"


@app.post("/expenses/import")
async def import_wechat(file: UploadFile = File(...)):
    """上传微信账单 Excel 文件，自动导入支出记录"""
    if not file.filename.endswith(('.xlsx', '.xls')):
        return {"error": "请上传 .xlsx 或 .xls 文件"}

    contents = await file.read()
    wb = openpyxl.load_workbook(io.BytesIO(contents))
    ws = wb.active
    rows = list(ws.iter_rows(values_only=True))

    # 找表头
    header_row = 0
    for i, row in enumerate(rows):
        if row[0] and "交易时间" in str(row[0]):
            header_row = i
            break

    if header_row == 0:
        return {"error": "不是有效的微信账单文件"}

    imported, skipped = 0, 0
    with get_db() as conn:
        for row in rows[header_row + 1:]:
            trade_time = str(row[0]) if row[0] else ""
            merchant = str(row[2]) if row[2] else ""
            product = str(row[3]) if row[3] else ""
            direction = str(row[4]) if row[4] else ""
            amount_str = str(row[5]) if row[5] else "0"

            if not trade_time or trade_time == "None":
                continue
            if "支出" not in direction:
                skipped += 1
                continue

            expense_date = trade_time[:10]
            amount = float(amount_str.replace("¥", "").replace(",", ""))
            category = guess_category(merchant, product)
            note = merchant
            if product and product != "/":
                note += " - " + product
            note = note[:50]

            conn.execute(
                "INSERT INTO expenses (amount, category, note, date) VALUES (?, ?, ?, ?)",
                (amount, category, note, expense_date),
            )
            imported += 1
        conn.commit()

    return {"message": f"导入成功 ✅", "imported": imported, "skipped": skipped}


# ============================================================
# 4. 启动说明
# ============================================================
# 命令行输入：
#   cd expense-tracker
#   uvicorn main:app --reload
#
# 然后打开浏览器访问：
#   http://127.0.0.1:8000/docs  ← 自动生成的交互式 API 文档页面！
