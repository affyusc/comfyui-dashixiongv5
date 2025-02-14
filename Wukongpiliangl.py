import os
from PIL import Image
import numpy as np
import torch

class Wukongpiliangshuchu:
    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "输入路径": ("STRING", {}),
                "输出格式": ("STRING", {"default": ".png", "choices": [".png", ".jpg", ".jpeg", ".webp"]}),  # 确保输出格式为字符串选择
            },
            "optional": {
                "seed": ("INT", {"default": 0, "min": 0, "max": 0xffffffffffffffff}),
                "切换随机输出": ("BOOLEAN", {"default": False}),
            }
        }
    RETURN_TYPES = ('IMAGE', 'STRING',)  # 增加STRING返回类型用于文件名
    FUNCTION = "get_transparent_image"
    CATEGORY = "WUKONG/图像"
    
    def __init__(self):
        self.current_index = 0

    def get_transparent_image(self, 输入路径, 输出格式, seed, 切换随机输出=False):
        try:
            if os.path.isdir(输入路径):
                images = []
                filenames = []
                for filename in os.listdir(输入路径):
                    if filename.lower().endswith(('.png', '.jpg', '.jpeg', '.webp')):
                        img_path = os.path.join(输入路径, filename)
                        image = Image.open(img_path).convert('RGBA')
                        images.append(image)
                        filenames.append(filename)  # 保存文件名
                if 切换随机输出:
                    import random
                    selected_image = random.choice(images)
                    selected_filename = random.choice(filenames)
                else:
                    selected_image = images[self.current_index % len(images)]
                    selected_filename = filenames[self.current_index % len(filenames)]
                    self.current_index += 1
                    
                # 将图像转换为Tensor
                image_rgba = selected_image
                image_np = np.array(image_rgba).astype(np.float32) / 255.0
                image_tensor = torch.from_numpy(image_np)[None, :, :, :]
                
                # 修改文件名后缀为用户指定的格式
                base_name, _ = os.path.splitext(selected_filename)
                new_filename = base_name + 输出格式
                
                return (image_tensor, new_filename)  # 返回图像和修改后的文件名
        
        except Exception as e:
            print(f"温馨提示处理图像时出错请重置节点：{e}")
        return None, "Unknown"  # 如果出错，返回默认值

# 注册节点
NODE_CLASS_MAPPINGS = {
    "Wukongpiliangshuchu": Wukongpiliangshuchu  # 将Wukongpiliang节点注册到NODE_CLASS_MAPPINGS中
}
