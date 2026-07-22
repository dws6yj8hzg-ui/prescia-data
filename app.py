from flask import Flask, request, jsonify
from flask_cors import CORS
import akshare as ak

app = Flask(__name__)
CORS(app)

@app.route("/kline")
def kline():
    code = request.args.get("code", "600519")
    period = request.args.get("period", "daily")
    try:
        df = ak.stock_zh_a_hist(symbol=code, period=period, adjust="qfq")
        df = df.rename(columns={
            "日期": "date", "开盘": "open", "收盘": "close",
            "最高": "high", "最低": "low", "成交量": "volume"
        })
        data = df[["date", "open", "close", "high", "low", "volume"]].to_dict(orient="records")
        return jsonify({"code": 0, "data": data})
    except Exception as e:
        return jsonify({"code": 1, "msg": str(e)}), 500

@app.route("/")
def home():
    return "Prescia AKShare service is running."

if __name__ == "__main__":
    import os
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
