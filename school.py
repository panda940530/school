import os, requests
from flask import Flask, request, render_template, make_response

USE_TEST = 1   # 1是測試用的Test URL, 0是正式用的Production URL
BASE     = os.getenv("N8N_BASE", "http://n8n:5679")  # n8n的主機位置 容器內:http://n8n:5679 外部: http://localhost:5679
PATH     = "/webhook-test/school" if USE_TEST else "/webhook/school"  # 測試跟正式用的不同URL路徑
N8N_WEBHOOK = f"{BASE}{PATH}"  # 兩者拼起來的完整 URL

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def upload():
    # GET：回查詢輸入頁
    if request.method == "GET":
        return render_template("school_upload.html", n8n_url=N8N_WEBHOOK)

    # POST：從網頁拿自然語言查詢
    query_text = (request.form.get("query") or "").strip()
    if not query_text:
        return "請輸入查詢內容", 400

    # 丟給 n8n
    payload = {"query": query_text}
    r = requests.post(N8N_WEBHOOK, json=payload, timeout=90)
    r.raise_for_status()

    raw = r.json()
    print("=== n8n raw ===")
    print(raw)

    rows, answer, chart_spec = [], "", {}
    if isinstance(raw, dict):
        rows = raw.get("rows", []) or []
        answer = raw.get("answer", "") or ""
        chart_spec = raw.get("chart", {}) or {}
    else:
        rows = raw or []
        answer = ""
        chart_spec = {}

    # 先保留英文字段 rows（給圖表用）
    rows_raw_for_chart = rows

    # ---- 成長率與金額轉字串：僅供表格顯示，用於 localized_rows ----

    # 需要轉成百分比字串的欄位（按需增減）
    PCT_FIELDS = {
        "project_growth_rate",       # 件數成長率 0.2111 -> 21.1%
        "amount_growth_rate",        # 金額成長率 0.1789 -> 17.9%
        "project_teacher_ratio",     # 例如 0.63 -> 63.0%（如果你有這欄）
    }

    # 需要加千分位的金額欄位（若 n8n 回來是字串也可直接保留）
    MONEY_FIELDS = {
        "total_approved_amount",
        "executing_total_approved_amount",
        "approve_amount",
        "received_amount",
        "refund_amount_raw",
        "manage_fee",
    }

    # 需要取到小數點第 2 位的欄位（數字型）
    DECIMAL2_FIELDS = {
        "project_per_pi",
        "project_per_teacher",
    }
    def _to_float_or_none(v):
        if v is None or v == "":
            return None
        try:
            # n8n 常把數字以字串回傳，這裡做安全轉型
            return float(v)
        except Exception:
            return None

    def _fmt_pct(v, decimals=1):
        if v is None:
            return None
        return f"{v * 100:.{decimals}f}%"

    def _fmt_money(v):
        # 允許 v 是字串或數字；若轉不出數字就原樣回傳
        fv = _to_float_or_none(v)
        if fv is None:
            return v
        # 無小數的整數金額：千分位
        if fv.is_integer():
            return f"{int(fv):,}"
        # 有小數就保留兩位
        return f"{fv:,.2f}"
    
    def _fmt_decimal2(v):
        fv = _to_float_or_none(v)
        if fv is None:
            return v
        return f"{fv:.2f}"

    def transform_for_table(row: dict) -> dict:
        out = {}
        for k, v in row.items():
            if k in PCT_FIELDS:
                out[k] = _fmt_pct(_to_float_or_none(v), decimals=1)
            elif k in MONEY_FIELDS:
                out[k] = _fmt_money(v)
            elif k in DECIMAL2_FIELDS:
                out[k] = _fmt_decimal2(v)
            else:
                out[k] = v
        return out

    # 英文→中文欄名（表格顯示用）
    col_map = {
        "project_code": "計畫代碼",
        "project_name": "計畫名稱",
        "exec_unit": "執行單位",
        "fund_source": "經費來源",
        "unit_category": "單位類別",
        "pi_code": "主持人代碼",
        "start_date": "起始日期",
        "end_date": "應結日期",
        "extend_date_raw": "延長日期",
        "close_date": "簽結日期",
        "approve_amount": "計畫核定金額",
        "received_amount": "實收數",
        "refund_amount_raw": "餘額繳回",
        "manage_fee": "管理費",
        "college_category": "學院",
        "approve_year": "核定年度",
        "duration_days": "計畫期間天數",
        "project_count": "計畫件數",
        "total_approved_amount": "核定經費總額",
        "multi_year_project_count": "多年期計畫件數",
        "pi_count": "承接計畫的教師人數",
        "project_growth_rate": "件數成長率",
        "amount_growth_rate": "金額成長率",
        "executing_project_count": "執行中計畫件數",
        "executing_total_approved_amount": "執行中計畫經費總額",
        "executing_now_project_count":"正在執行計畫件數",
        "executing_now_total_approved_amount":"正在執行計畫經費總額",
        "project_per_teacher": "人均計畫數",
        "project_teacher_ratio": "執行計畫之教師比例"
    }

    def localize_row(row):
        return {col_map.get(k, k): v for k, v in row.items()}

    # 轉好格式再做「英文→中文」對應，僅用於表格顯示
    localized_rows = [localize_row(transform_for_table(r)) for r in rows]

    return render_template(
        "school_result.html",
        rows=localized_rows,          # 中文表格
        rows_raw=rows_raw_for_chart,  # 給圖表用
        chart=chart_spec,             # n8n的 chart 規格
        col_map=col_map,              # ★ 新增：欄位英文→中文對照
        answer=answer,
        question=query_text
    )


@app.route("/download_csv", methods=["POST"])
def download_csv():
    import json, csv
    from io import StringIO

    rows = json.loads(request.form["rows"])

    all_cols = []
    for r in rows:
        for k in r.keys():
            if k not in all_cols:
                all_cols.append(k)

    buf = StringIO()
    writer = csv.writer(buf)
    writer.writerow(all_cols)
    for r in rows:
        writer.writerow([r.get(c, "") for c in all_cols])
    csv_text = buf.getvalue()

    resp = make_response(u'\ufeff' + csv_text)  # UTF-8-SIG
    resp.headers["Content-Type"] = "text/csv; charset=utf-8"
    resp.headers["Content-Disposition"] = "attachment; filename=merged.csv"
    return resp


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)