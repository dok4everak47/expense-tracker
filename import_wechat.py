"""
微信账单导入脚本
把微信导出的 Excel 账单批量导入你的记账 API
"""

import openpyxl
import requests

API = "http://127.0.0.1:8000"
FILENAME = "微信支付账单流水文件(20260501-20260530)_20260530235317.xlsx"

# ============================================================
# 1. 商户名 → 分类 的映射表（按你的消费习惯改）
# ============================================================
CATEGORY_MAP = {
    # 吃饭
    "小笼包": "吃饭",
    "鸡爪": "吃饭",
    "蜜雪冰城": "吃饭",
    "luckin": "吃饭",
    "咖啡": "吃饭",
    "奶茶": "吃饭",
    "餐厅": "吃饭",
    "饭店": "吃饭",
    "粉": "吃饭",
    "面": "吃饭",
    "粥": "吃饭",
    "烧烤": "吃饭",
    "火锅": "吃饭",
    "包子": "吃饭",
    "饭": "吃饭",
    "超市": "吃饭",
    "赵一鸣": "吃饭",
    "喜茶": "吃饭",
    "全上品": "吃饭",
    "小汤总": "吃饭",
    "星巴克": "吃饭",
    "牛爷烧": "吃饭",
    "Cotti": "吃饭",
    "袁小饺": "吃饭",
    "云吞": "吃饭",
    "都市甜心": "吃饭",
    "汉堡": "吃饭",
    "朴大叔": "吃饭",
    "拌饭": "吃饭",
    "夏天": "吃饭",
    "玉小灶": "吃饭",
    # 交通
    "滴滴": "交通",
    "地铁": "交通",
    "公交": "交通",
    "铁路": "交通",
    "高铁": "交通",
    "打车": "交通",
    "停车": "交通",
    "加油站": "交通",
    "充电": "交通",
    "杭州青奇": "交通",
    "青桔": "交通",
    "美团单车": "交通",
    # 购物
    "淘宝": "购物",
    "京东": "购物",
    "拼多多": "购物",
    "天猫": "购物",
    "唯品会": "购物",
    "顺丰": "购物",
    # 娱乐
    "腾讯": "娱乐",
    "游戏": "娱乐",
    "视频": "娱乐",
    "音乐": "娱乐",
    "会员": "娱乐",
    "电影": "娱乐",
    "影院": "娱乐",
    "KTV": "娱乐",
    "优酷": "娱乐",
    "哔哩": "娱乐",
    "B站": "娱乐",
    "DP": "娱乐",
    # 住房
    "房租": "住房",
    "水电": "住房",
    "物业": "住房",
    "燃气": "住房",
    "宽带": "住房",
}


def guess_category(merchant, product):
    """根据商户名和商品名猜分类"""
    text = merchant + product
    for keyword, category in CATEGORY_MAP.items():
        if keyword in text:
            return category
    return "其他"


# ============================================================
# 2. 读取 Excel
# ============================================================
wb = openpyxl.load_workbook(FILENAME)
ws = wb.active
rows = list(ws.iter_rows(values_only=True))

# 找到表头行
header_row = 0
for i, row in enumerate(rows):
    if row[0] and "交易时间" in str(row[0]):
        header_row = i
        break

if header_row == 0:
    print("❌ 没找到表头行")
    exit(1)

data_rows = rows[header_row + 1 :]
print(f"✅ 找到 {len(data_rows)} 条记录")

# ============================================================
# 3. 逐条导入（只导入支出）
# ============================================================
imported = 0
skipped = 0

for row in data_rows:
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

    date = trade_time[:10]
    amount = float(amount_str.replace("¥", "").replace(",", ""))
    category = guess_category(merchant, product)
    note = merchant
    if product and product != "/":
        note += " - " + product
    if len(note) > 50:
        note = note[:47] + "..."

    resp = requests.post(
        f"{API}/expenses",
        json={"amount": amount, "category": category, "note": note, "date": date},
    )

    if resp.status_code == 200:
        imported += 1
        print(f"  ✅ ¥{amount:.2f}  {category}  {note}")
    else:
        print(f"  ❌ 导入失败: {resp.text}")

print(f"\n🎉 完成！导入 {imported} 条，跳过 {skipped} 条（非支出）")

# ============================================================
# 4. 显示汇总
# ============================================================
resp = requests.get(f"{API}/expenses/summary")
if resp.status_code == 200:
    data = resp.json()
    total = sum(item["total"] for item in data)
    print(f"\n📊 30 天汇总：")
    for item in data:
        print(f"  {item['category']}: ¥{item['total']:.2f} ({item['count']}笔)")
    print(f"  合计: ¥{total:.2f}")
