from flask import Flask, render_template, request

app = Flask(__name__)

# 足し算計算機のメインルート
@app.route("/", methods=["GET", "POST"])
def index():
    # デフォルトのメッセージ
    result_message = "計算したい数値を入力してください"
    
    # POSTリクエスト（フォーム送信）があった場合の処理
    if request.method == "POST":
        try:
            # フォームデータから 'num1' と 'num2' の値を取り出す
            num1_str = request.form['num1']
            num2_str = request.form['num2']
            
            # 文字列を整数に変換
            num1 = int(num1_str)
            num2 = int(num2_str)
            
            # 計算の実行
            result = num1 + num2
            
            # 結果メッセージを作成
            result_message = f"{num1} + {num2} = {result} です！"
            
        except ValueError:
            # 数値変換エラー（整数以外の入力）
            result_message = "エラー：有効な整数を入力してください。"
        except Exception as e:
            # その他の予期せぬエラー
            result_message = f"予期せぬエラーが発生しました: {e}"
            
    # ★★★ 参照するテンプレートを 'flask_test.html' に変更 ★★★
    return render_template("flask_test.html", message=result_message)

if __name__ == '__main__':
    app.run(debug=True)
