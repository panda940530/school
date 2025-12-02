# 1. 使用一個輕量級的 Python 基礎映像檔
FROM python:3.11-slim

# 2. 設定環境變數
# - 確保 Python 輸出立即顯示在日誌中
ENV PYTHONUNBUFFERED=1
# - 設定 UTF-8 編碼以正確處理主提示中的中文字元
ENV LANG=C.UTF-8

# 3. 設定工作目錄
WORKDIR /app

# 4. 複製並安裝依賴項
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 5. 複製應用程式程式碼到容器中
COPY . .

# 6. 設定容器啟動時要執行的預設命令
#    這將執行 agent.py 中的自主迴圈
CMD ["python", "school.py"]
