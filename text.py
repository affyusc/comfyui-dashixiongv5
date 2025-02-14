import os
import csv

class WUKONGBAOCUNTEXT:
    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "multiline_text": ("STRING", {"multiline": True, "default": ""}),
                "output_file_path": ("STRING", {"multiline": False, "default": ""}),
                "file_name": ("STRING", {"multiline": False, "default": ""}),
                "file_extension": (["txt", "csv"],),
            }
        }

    RETURN_TYPES = ("STRING", )
    RETURN_NAMES = ("status_message", ) 
    OUTPUT_NODE = True
    FUNCTION = 'save_list'
    CATEGORY = "WUKONG/图像"

    def save_list(self, multiline_text, output_file_path, file_name, file_extension):
        filepath = os.path.join(output_file_path, f"{file_name}.{file_extension}")
        index = 1

        # 检查输出路径和文件名是否为空
        if not output_file_path or not file_name:
            print(f"[Warning] CR Save Text List. No file details found. No file output.") 
            return ("No file output due to missing file path or name", )

        # 检查文件是否已存在，防止覆盖，添加索引
        while os.path.exists(filepath):
            filepath = os.path.join(output_file_path, f"{file_name}_{index}.{file_extension}")
            index += 1
        
        print(f"[Info] CR Save Text List: Saving to {filepath}")

        # 保存为 CSV 文件
        if file_extension == "csv":
            text_list = [line.strip() for line in multiline_text.split("\n")]

            with open(filepath, "w", newline="") as csv_file:
                csv_writer = csv.writer(csv_file)
                for line in text_list:
                    csv_writer.writerow([line])
        # 保存为 TXT 文件
        else:
            with open(filepath, "w", newline="") as text_file:
                text_file.write(multiline_text)

        return (f"File saved successfully to {filepath}", )

# 节点注册
NODE_CLASS_MAPPINGS = {
    "WUKONGBAOCUNTEXT": WUKONGBAOCUNTEXT,
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "WUKONGBAOCUNTEXT": "WUKONGBAOCUNTEXT",
}
