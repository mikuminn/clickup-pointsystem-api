import requests

# APIキー、タスクID、カスタムフィールドIDを設定
api_key = 'pk_89410085_ADBP0YVNIB91WAHA8W42LMZFX5DM7EWQ'
task_id = '86enq7ck1' # TASKのIDは、個別タスクを表示してurlの/t/より後ろの英数字になります。と書いてあった
custom_field_id = '??????????????'  # 更新したいメインタスクのカスタムフィールドIDがわからない

# タスクの詳細を取得するためのヘッダー
headers = {
    'Authorization': api_key
}

# サブタスクを取得するURL
subtasks_url = f'https://api.clickup.com/api/v2/task/{task_id}/subtask'

# サブタスクを取得
response = requests.get(subtasks_url, headers=headers)
subtasks = response.json()['tasks']

# サブタスクのカスタムフィールドの値を集計
total_points = 0
for subtask in subtasks:
    # カスタムフィールドの値を取得し、total_pointsに加算
    for custom_field in subtask['custom_fields']:
        if custom_field['id'] == 'YOUR_SUBTASK_CUSTOM_FIELD_ID':  # サブタスクのカスタムフィールドIDもなに？
            try:
                total_points += int(custom_field['value'])
            except ValueError:
                # カスタムフィールドの値が数値でない場合はスキップ
                continue

# メインタスクのカスタムフィールドを更新するURL
update_url = f'https://api.clickup.com/api/v2/task/{task_id}/field/{custom_field_id}'

# 更新するデータ
data = {
    "value": total_points
}

# カスタムフィールドを更新
update_response = requests.post(update_url, headers=headers, json=data)

if update_response.status_code == 200:
    print("カスタムフィールドを更新しました。")
else:
    print(f"エラーが発生しました: {update_response.text}")
