# -*- coding: utf-8 -*-
# Flaskと必要なライブラリのインポート
from flask import Flask, render_template, request, redirect, url_for, jsonify
import json
import os

# Firebase/Firestore接続用の設定（Canvas環境から自動で提供されるグローバル変数を使用）
# __app_id, __firebase_config, __initial_auth_token はCanvas実行環境で定義されています
app_id = os.environ.get('__app_id', 'default-app-id')
firebase_config = json.loads(os.environ.get('__firebase_config', '{}'))
initial_auth_token = os.environ.get('__initial_auth_token', '')

app = Flask(__name__)

# --- ▼ 共通ヘルパー関数 (今後のFirestore接続用) ▼ ---

# ToDoリスト機能のために、Firestoreの初期設定はテンプレートのJavaScriptで行います。
# Python側は、ルーティングとテンプレートのレンダリングに集中します。

# --- ▲ 共通ヘルパー関数 ▲ ---


# --- 1. 計算機機能のルーティング ---

@app.route('/calc', methods=['GET', 'POST'])
def calculator_index():
    # デフォルト値の設定
    result = None
    message = None
    num1_val = request.form.get('num1', '') # 値がなければ空文字
    num2_val = request.form.get('num2', '')
    operator_val = request.form.get('operator', '+')

    if request.method == 'POST':
        try:
            # フォームから数値と演算子を取得
            num1 = float(num1_val)
            num2 = float(num2_val)
            operator = operator_val

            # 四則演算の実行
            if operator == '+':
                result = num1 + num2
            elif operator == '-':
                result = num1 - num2
            elif operator == '*':
                result = num1 * num2
            elif operator == '/':
                if num2 == 0:
                    message = "エラー: ゼロで割ることはできません。"
                    result = None
                else:
                    result = num1 / num2
            else:
                message = "エラー: 無効な演算子が選択されました。"
                
            if result is not None:
                message = f"{num1} {operator} {num2} = {result:.2f}"
            
        except ValueError:
            message = "エラー: 無効な数値を入力しました。"
        except Exception as e:
            message = f"予期せぬエラーが発生しました: {e}"

    # 結果と入力値をテンプレートに渡す
    return render_template(
        "calculator.html", 
        message=message, 
        result=result, 
        num1_val=num1_val, 
        num2_val=num2_val,
        operator_val=operator_val
    )

# --- 2. ToDoリスト機能のルーティング ---

@app.route('/', methods=['GET'])
@app.route('/todo', methods=['GET'])
def todo_index():
    # ToDoリストのページを表示する
    # ユーザー認証情報はJavaScript側で処理するため、ここでは認証トークンを渡す
    return render_template(
        "todo.html",
        initial_auth_token=initial_auth_token,
        firebase_config=json.dumps(firebase_config),
        app_id=app_id
    )

if __name__ == '__main__':
    # 開発環境で実行
    app.run(debug=True)
