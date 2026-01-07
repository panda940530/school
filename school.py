import os
import requests
from flask import Flask, request, render_template, make_response

USE_TEST = int(os.getenv("USE_TEST", "0"))  # 1: 測試路徑 /webhook-test/school, 0: 正式路徑 /webhook/school
BASE = os.getenv("N8N_BASE", "http://localhost:5679")  # 本機 n8n 預設，容器內可設為 http://n8n:5679
PATH = "/webhook-test/school" if USE_TEST else "/webhook/school"
N8N_WEBHOOK = f"{BASE}{PATH}"

DEFAULT_BAR_COLORS = ["#f57c00", "#2e7d32", "#1976d2", "#7b1fa2"]

app = Flask(__name__)

# 格式化欄位設定
PCT_FIELDS = {
    "project_growth_rate",
    "amount_growth_rate",
    "project_teacher_ratio",
}

MONEY_FIELDS = {
    "total_approved_amount",
    "executing_total_approved_amount",
    "approve_amount",
    "received_amount",
    "spent_amount",
    "refund_amount_raw",
    "manage_fee",
}

DECIMAL2_FIELDS = {
    "project_per_pi",
    "project_per_teacher",
}


def _get_bar_colors_from_form(form):
    colors = []
    for i in range(1, 5):
        c = (form.get(f"color{i}") or "").strip()
        if c:
            colors.append(c)
    return colors or DEFAULT_BAR_COLORS


def _to_float_or_none(v):
    if v is None or v == "":
        return None
    try:
        return float(v)
    except Exception:
        return None


def _fmt_pct(v, decimals=1):
    if v is None:
        return None
    return f"{v * 100:.{decimals}f}%"


def _fmt_money(v):
    fv = _to_float_or_none(v)
    if fv is None:
        return v
    if fv.is_integer():
        return f"{int(fv):,}"
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


@app.route("/", methods=["GET", "POST"])
def upload():
    # GET：回應查詢頁
    if request.method == "GET":
        return render_template(
            "school_upload.html",
            n8n_url=N8N_WEBHOOK,
            default_bar_colors=DEFAULT_BAR_COLORS,
        )

    # POST：接網頁表單的自然語言查詢
    query_text = (request.form.get("query") or "").strip()
    if not query_text:
        return "請輸入查詢內容", 400

    bar_colors = _get_bar_colors_from_form(request.form)

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

    rows_raw_for_chart = rows

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
        "close_date": "實結日期",
        "approve_amount": "計畫核定金額",
        "received_amount": "實收數",
        "spent_amount": "實支數",
        "refund_amount_raw": "餘額繳回",
        "manage_fee": "管理費",
        "college_name": "學院",
        "approve_year": "核定年度",
        "duration_days": "計畫期間天數",
        "project_count": "計畫件數",
        "total_approved_amount": "核定經費總額",
        "multi_year_project_count": "多年期計畫件數",
        "pi_count": "承接計畫教師人數",
        "project_growth_rate": "件數成長率",
        "amount_growth_rate": "金額成長率",
        "executing_project_count": "執行中計畫件數",
        "executing_total_approved_amount": "執行中計畫經費總額",
        "executing_now_project_count": "正在執行計畫件數",
        "executing_now_total_approved_amount": "正在執行計畫經費總額",
        "project_per_teacher": "人均計畫數",
        "project_teacher_ratio": "執行計畫之教師比例",
    }

    def localize_row(row):
        return {col_map.get(k, k): v for k, v in row.items()}

    localized_rows = [localize_row(transform_for_table(r)) for r in rows]

    return render_template(
        "school_result.html",
        rows=localized_rows,
        rows_raw=rows_raw_for_chart,
        chart=chart_spec,
        col_map=col_map,
        bar_colors=bar_colors,
        answer=answer,
        question=query_text,
    )


@app.route("/download_csv", methods=["POST"])
def download_csv():
    import csv
    import json
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

    resp = make_response("\ufeff" + csv_text)  # UTF-8-SIG
    resp.headers["Content-Type"] = "text/csv; charset=utf-8"
    resp.headers["Content-Disposition"] = "attachment; filename=school.csv"
    return resp


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
