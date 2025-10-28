# -*- coding: utf-8 -*-
import os
from flask import Flask, render_template, request, redirect, url_for
from markupsafe import Markup
import json
import logging

# Flaskアプリケーションの初期化
# template_folder='templates', static_folder='static' は通常は不要ですが、環境に合わせ残します
app = Flask(__name__, template_folder='templates', static_folder='static')

# ----------------------------------------------------
# 必須のグローバル変数を安全に取得する
# ----------------------------------------------------

# Canvas環境の変数が取得できるか確認（ローカル実行時はNoneになる）
def get_global_var(key):
    """globals()から変数を安全に取得するヘルパー関数"""
    return globals().get(key, None)

# __app_id (string): アプリケーションの一意なID
app_id = get_global_var('__app_id') or "default-app-id"

# __firebase_config (string): Firebaseの設定JSON文字列
firebase_config = get_global_var('__firebase_config') or "{}"
try:
    # テンプレートに渡すためにJSON文字列であることを確認
    json.loads(firebase_config)
except json.JSONDecodeError:
    logging.error("Invalid JSON in __firebase_config. Using default empty JSON.")
    firebase_config = "{}"

# __initial_auth_token (string): ユーザー認証トークン
auth_token = get_global_var('__initial_auth_token')

# ----------------------------------------------------

# メインメニューのルート (/)
# メニューにアクセスしたら電卓ルートにリダイレクトするのが自然ですが、
# ユーザーが提供したメニューコードを保持し、`/calc`へのリンクとして機能させます。
@app.route('/')
def index():
    # シンプルなメニューを直接返す
    menu_html = """
    <!DOCTYPE html>
    <html lang="ja">
    <head>
        <meta charset="UTF-8">
        <title>アプリケーション メインメニュー</title>
        <style>
            body { font-family: sans-serif; text-align: center; margin-top: 100px; background-color: #f0f4f8; }
            .menu-container { background-color: white; padding: 30px; border-radius: 10px; box-shadow: 0 4px 8px rgba(0,0,0,0.1); display: inline-block; }
            h1 { color: #1a73e8; }
            a { display: block; margin: 15px 0; padding: 10px 20px; background-color: #e6e6e6; text-decoration: none; color: #333; border-radius: 5px; transition: background-color 0.3s; }
            a:hover { background-color: #ccc; }
        </style>
    </head>
    <body>
        <div class="menu-container">
            <h1>アプリケーション メインメニュー</h1>
            <p>アクセスしたい機能を選択してください。</p>
            <a href="/calc">電卓 🧮</a>
        </div>
    </body>
    </html>
    """
    return Markup(menu_html)


# 計算機用のルート
@app.route('/calc', methods=['GET', 'POST'])
def calculator_index():
    result = None
    num1_str = ""
    num2_str = ""
    operator = "+"
    message = "値を入力して「計算」を押してください" # 初期メッセージ

    if request.method == 'POST':
        try:
            num1_str = request.form.get('num1', "")
            num2_str = request.form.get('num2', "")
            operator = request.form.get('operator', "+")

            # フォームの入力値を保持
            num1 = float(num1_str)
            num2 = float(num2_str)

            if operator == '+':
                result = num1 + num2
            elif operator == '-':
                result = num1 - num2
            elif operator == '*':
                result = num1 * num2
            elif operator == '/':
                if num2 != 0:
                    result = num1 / num2
                else:
                    # ゼロ除算エラー
                    message = "エラー: ゼロで割ることはできません"
                    result = None 
            else:
                # 無効な演算子
                message = "エラー: 無効な演算子です"
                result = None

            if result is not None:
                # 計算成功メッセージ
                # 整数値であれば整数形式で表示
                if result == int(result):
                    result_display = int(result)
                else:
                    result_display = result

                message = f"計算結果: {result_display}"

        except ValueError:
            message = "エラー: 数値として無効な値が入力されました"
        except Exception as e:
            message = f"予期せぬエラーが発生しました: {e}"
            logging.error(f"Calculator Error: {e}")

    # 結果と入力値をテンプレートに渡す
    return render_template(
        "calculator.html",
        message=message, # HTMLが要求している変数
        num1_val=num1_str, # HTMLが要求している変数名に合わせて修正
        num2_val=num2_str, # HTMLが要求している変数名に合わせて修正
        operator=operator, # 選択された演算子を保持
    )

# デバッグモードでサーバーを起動
if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    # ローカル実行時に'templates'と'static'ディレクトリが存在することを確認してください
    app.run(debug=True, host='0.0.0.0', port=port)
