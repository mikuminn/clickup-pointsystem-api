import requests

# APIキー、タスクID、カスタムフィールドIDを設定
api_key = 'pk_89410085_ADBP0YVNIB91WAHA8W42LMZFX5DM7EWQ'
task_id = '86enq7ck1' 

# totalimportanceのカスタムフィールドID
total_importance_custom_field_id = 'df2fe57b-7678-4b44-971d-fe9acf87e8d1' 

# リクエストヘッダー
headers = {
    'Authorization': api_key
}

# タスクの詳細を取得するURL(include_subtasks=true によりサブタスクを含める)
tasks_url = f'https://api.clickup.com/api/v2/task/{task_id}?include_subtasks=true'

# タスクの詳細を取得
response = requests.get(tasks_url, headers=headers)
task_details = response.json()

total_importance = 0

# サブタスクが存在する場合
if 'subtasks' in task_details:
    subtasks = task_details['subtasks']
    # サブタスクの詳細を取得
    for subtask in subtasks:
        subtask_url = f'https://api.clickup.com/api/v2/task/{subtask["id"]}'
        subtask_response = requests.get(subtask_url, headers=headers)
        subtask_details = subtask_response.json()

        each_importance_custom_field_id = 'c195ffbd-6798-46d5-8792-122b1d9a3dbf'
        #  サブタスクのカスタムフィールドを取得
        if 'custom_fields' in subtask_details:
            custom_fields = subtask_details['custom_fields']
            for custom_field in custom_fields:
                # カスタムフィールドのIDがimportanceの場合、その値を合計する
                if custom_field['id'] == each_importance_custom_field_id:
                    total_importance += int(custom_field.get('value'))
else:
    print("No subtasks found or 'subtasks' key not present in response.")

# メインタスクのカスタムフィールドを更新するURL
update_url = f'https://api.clickup.com/api/v2/task/{task_id}/field/{total_importance_custom_field_id}'

# 更新するデータ
data = {
    "value": total_importance
}

# カスタムフィールドを更新
update_response = requests.post(update_url, headers=headers, json=data)

# 一応メッセージを表示させてるけど、ここは必要ですか？
if update_response.status_code == 200:
    print("カスタムフィールドを更新しました。")
else:
    print(f"エラーが発生しました: {update_response.text}")