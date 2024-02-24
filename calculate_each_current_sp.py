import requests

# APIキー、タスクID
api_key = 'pk_89410085_ADBP0YVNIB91WAHA8W42LMZFX5DM7EWQ'
task_id = '86enq7ck1' 

# リクエストヘッダー
headers = {
    'Authorization': api_key
}

# タスクの詳細を取得するURL(include_subtasks=true によりサブタスクを含める)
tasks_url = f'https://api.clickup.com/api/v2/task/{task_id}?include_subtasks=true'

# タスクの詳細を取得
response = requests.get(tasks_url, headers=headers)
task_details = response.json()

# spoopoint per importanceを計算する
spoopoint_per_importance = 0

# totalspoopointの値を取得する
custom_fields = task_details['custom_fields']
totalspoopoint_id = '0d7a032b-6ccc-4633-934b-d7078c1ded9d' 
totalspoopoint = 0

for custom_field in custom_fields:
    if custom_field['id'] == totalspoopoint_id:
        totalspoopoint = int(custom_field.get('value'))
        break

# totaloimportanceの値を取得する
totalimportance_id = 'df2fe57b-7678-4b44-971d-fe9acf87e8d1' 
totalimportance = 0

for custom_field in custom_fields:
    if custom_field['id'] == totalimportance_id:
        totalimportance = int(custom_field.get('value'))
        break

spoopoint_per_importance = totalspoopoint / totalimportance

# サブタスクが存在する場合
if 'subtasks' in task_details:
    subtasks = task_details['subtasks']
    # サブタスクの詳細を取得
    for subtask in subtasks:
        subtask_url = f'https://api.clickup.com/api/v2/task/{subtask["id"]}'
        subtask_response = requests.get(subtask_url, headers=headers)
        subtask_details = subtask_response.json()

        importance_custom_field_id = 'c195ffbd-6798-46d5-8792-122b1d9a3dbf'
        each_importance = 0

        spoopoint_custom_field_id = '7c7d79c6-ac5a-40b2-81bb-185097a3c642' 
        each_spoopoint = 0

        subtask_status = 0

        progress_spoopoint = 0

        #  サブタスクのカスタムフィールドを取得
        if 'status' in subtask_details:
            subtask_status = subtask_details['status']['status']
            print(f"subtask_status: {subtask_status}")
        if 'custom_fields' in subtask_details:
            custom_fields = subtask_details['custom_fields']
            for custom_field in custom_fields:
                # importanceの値を取得
                if custom_field['id'] == importance_custom_field_id:
                    each_importance = int(custom_field.get('value'))
                    break
            each_spoopoint = each_importance * spoopoint_per_importance
            print(f"each_spoopoint: {each_spoopoint}")
        
        if subtask_status == 'to do':
            progress_spoopoint = 0
        elif subtask_status == 'in progress':
            progress_spoopoint = each_spoopoint * 0.1
        elif subtask_status == 'processed':
            progress_spoopoint = each_spoopoint * 0.5
        elif subtask_status == 'complete':
            progress_spoopoint = each_spoopoint

        print(f"進捗SP: {progress_spoopoint}")

else:
    print("No subtasks found or 'subtasks' key not present in response.")


