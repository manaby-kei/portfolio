from flask import Flask, render_template, request

app = Flask(__name__)

# 四則演算のメインルート
@app.route("/", methods=["GET", "POST"])
def index():
    # 入力値を保持するためのデフォルト値
    num1_val = ""
    num2_val = ""
    result_message = "計算したい数値を入力し、演算子を選んでください"
    
    if request.method == "POST":
        try:
            # フォームデータから3つの値を取り出す
            num1_str = request.form['num1']
            num2_str = request.form['num2']
            operator = request.form['operator']

            # 入力値を保持
            num1_val = num1_str
            num2_val = num2_str
            
            # 文字列を数値に変換 (割り算対応のためfloatを使用)
            num1 = float(num1_str)
            num2 = float(num2_str)
            
            result = None
            
            # 演算子に応じて計算を分岐
            if operator == "+":
                result = num1 + num2
            elif operator == "-":
                result = num1 - num2
            elif operator == "*":
                result = num1 * num2
            elif operator == "/":
                # ゼロ除算エラーのチェック
                if num2 == 0:
                    result_message = "エラー：0で割ることはできません。"
                    # テンプレートを返して処理を終了
                    return render_template("flask_test.html", 
                                           message=result_message, 
                                           num1_val=num1_val, 
                                           num2_val=num2_val)
                result = num1 / num2
                
            # 結果メッセージを作成 (小数点以下2桁で表示)
            # 整数結果の場合、不要な .00 を表示しないように調整
            if result == int(result):
                result_message = f"{num1} {operator} {num2} = {int(result)} です！"
            else:
                result_message = f"{num1} {operator} {num2} = {result:.2f} です！"
                
        except ValueError:
            # 数値変換エラー
            result_message = "エラー：有効な数値を入力してください。"
        except Exception as e:
            # その他の予期せぬエラー
            result_message = f"予期せぬエラーが発生しました: {e}"
            
    # テンプレートをレンダリング
    return render_template("flask_test.html", 
                           message=result_message, 
                           num1_val=num1_val, 
                           num2_val=num2_val)

if __name__ == '__main__':
    # デバッグモードで実行
    app.run(debug=True)
