import json
import os
from doctest import NORMALIZE_WHITESPACE


def extract_and_write_jsons_by_client_type(folder_path, client_type, output_folder, terminalModel=None):
    # 确保输出文件夹存在，如果不存在则创建
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    def extract_events():
        # 用于跟踪每个事件ID出现的次数
        event_id_counter = {}

        events = json_data.get('events')
        if events and isinstance(events, list):
            for event in events:
                # 生成带有事件ID的文件名
                event_id = event.get('id')
                if event_id:
                    # 更新事件ID的计数器
                    event_id_counter[event_id] = event_id_counter.get(event_id, 0) + 1

                    # 生成带有顺序号的文件名
                    # if event_id_counter[event_id] > 1:
                    #     new_file_name = f"{event_id}_{event_id_counter[event_id]}.json"
                    # else:
                    #     new_file_name = f"{event_id}.json"

                    # 生成带有顺序号的文件名
                    base_file_name = f"{event_id}.json"
                    new_file_name = base_file_name
                    counter = 1
                    while os.path.exists(os.path.join(output_folder, new_file_name)):
                        new_file_name = f"{event_id}_{counter}.json"
                        counter += 1

                    # 创建一个仅包含当前事件的JSON数据
                    event_json_data = {**json_data, 'events': [event]}

                    # 创建一个包含完整 events 列表的 JSON 数据
                    # event_json_data = {**json_data}

                    # 写入新的JSON文件，使用格式化写入
                    new_file_path = os.path.join(output_folder, new_file_name)
                    with open(new_file_path, 'w') as new_file:
                        json.dump(event_json_data, new_file, indent=4)
                    print(f"Created file: {new_file_path}")

    # 遍历文件夹中的所有文件
    for file_name in os.listdir(folder_path):
        if file_name.endswith('.ndjson'):
            file_path = os.path.join(folder_path, file_name)
            with open(file_path, 'r') as file:
                lines = file.readlines()

            # 用于跟踪每个事件ID出现的次数
            # event_id_counter = {}

            for line in lines:
                json_data = json.loads(line)
                if json_data.get('clientType') == client_type and json_data.get('terminalModel') == terminalModel:
                    extract_events()
                    # events = json_data.get('events')
                    # if events and isinstance(events, list):
                    #     for event in events:
                    #         # 生成带有事件ID的文件名
                    #         event_id = event.get('id')
                    #         if event_id:
                    #             # 更新事件ID的计数器
                    #             event_id_counter[event_id] = event_id_counter.get(event_id, 0) + 1
                    #
                    #             # 生成带有顺序号的文件名
                    #             # if event_id_counter[event_id] > 1:
                    #             #     new_file_name = f"{event_id}_{event_id_counter[event_id]}.json"
                    #             # else:
                    #             #     new_file_name = f"{event_id}.json"
                    #
                    #             # 生成带有顺序号的文件名
                    #             base_file_name = f"{event_id}.json"
                    #             new_file_name = base_file_name
                    #             counter = 1
                    #             while os.path.exists(os.path.join(output_folder, new_file_name)):
                    #                 new_file_name = f"{event_id}_{counter}.json"
                    #                 counter += 1
                    #
                    #             # 创建一个仅包含当前事件的JSON数据
                    #             event_json_data = {**json_data, 'events': [event]}
                    #
                    #             # 创建一个包含完整 events 列表的 JSON 数据
                    #             # event_json_data = {**json_data}
                    #
                    #             # 写入新的JSON文件，使用格式化写入
                    #             new_file_path = os.path.join(output_folder, new_file_name)
                    #             with open(new_file_path, 'w') as new_file:
                    #                 json.dump(event_json_data, new_file, indent=4)
                    #             print(f"Created file: {new_file_path}")

                elif json_data.get('clientType') == client_type and terminalModel is None:
                    extract_events()


def format_source_data_to_json(source_data_input_folder, source_data_output_folder):
    # 确保输出文件夹存在，如果不存在则创建
    if not os.path.exists(source_data_output_folder):
        os.makedirs(source_data_output_folder)

    # 遍历文件夹中的所有文件
    for file_name in os.listdir(source_data_input_folder):
        if file_name.endswith('.ndjson'):
            file_path = os.path.join(source_data_input_folder, file_name)
            with open(file_path, 'r') as file:
                lines = file.readlines()

            for line in lines:
                json_data = json.loads(line)

                # 创建一个包含完整 events 列表的 JSON 数据
                event_json_data = {**json_data}

                # 写入新的JSON文件，使用格式化写入
                new_file_path = os.path.join(source_data_output_folder, file_name)
                with open(new_file_path, 'w') as new_file:
                    json.dump(event_json_data, new_file, indent=4)
                print(f"源数据格式化完成: {new_file_path}")


if __name__ == "__main__":
    input_folder_path = '/test_app_dec/A1_S3_tar'  # 替换为你的ndjson文件所在的文件夹路径，或保持当前默认
    output_folder_path = '/test_app_dec/iOS'  # 替换为你的输出文件夹路径，或保持当前默认
    your_client_type = 'iOS'  # 替换你需要提取的客户端类型：iOS, Android
    your_terminalModel = 'iPhone14,2'  # 改成你的测试手机型号

    sd_output_folder_path = '/test_app_dec/A1_source_data'  # 替换为你的源数据格式化后的输出文件夹路径，或保持当前默认

    extract_and_write_jsons_by_client_type(folder_path=input_folder_path,
                                           client_type=your_client_type,
                                           output_folder=output_folder_path,
                                           terminalModel=your_terminalModel
                                           )

    format_source_data_to_json(source_data_input_folder=input_folder_path,
                               source_data_output_folder=sd_output_folder_path)

