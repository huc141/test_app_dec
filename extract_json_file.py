import json


def extract_and_write_jsons_by_client_type(file_path, client_type):
    with open(file_path, 'r') as file:
        lines = file.readlines()

    # 用于跟踪每个事件ID出现的次数
    event_id_counter = {}

    for line in lines:
        json_data = json.loads(line)
        print(json_data)
        if json_data.get('clientType') == client_type:
            events = json_data.get('events')
            if events and isinstance(events, list):
                for event in events:
                    event_id = event.get('id')
                    if event_id:
                        # 更新事件ID的计数器
                        event_id_counter[event_id] = event_id_counter.get(event_id, 0) + 1

                        # 生成带有顺序号的文件名
                        if event_id_counter[event_id] > 1:
                            new_file_name = f"{event_id}_{event_id_counter[event_id]}.json"
                        else:
                            new_file_name = f"{event_id}.json"

                        # 创建一个包含完整 events 列表的 JSON 数据
                        event_json_data = {**json_data}

                        # 写入新的JSON文件，使用格式化写入
                        with open(new_file_name, 'w') as new_file:
                            json.dump(event_json_data, new_file, indent=4)
                        print(f"Created file: {new_file_name}")


if __name__ == "__main__":
    ndjson_file_path = 'D:/1-原生-android/埋点测试/1/telemetric-app-events-1732777972054.ndjson'
    your_client_type = 'Android'
    extract_and_write_jsons_by_client_type(ndjson_file_path, your_client_type)
