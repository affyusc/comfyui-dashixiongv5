import torch

class WUKONGRAGBDRGB:
    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "image": ("IMAGE",),
            },
        }

    RETURN_TYPES = ("IMAGE",)
    FUNCTION = "execute"
    CATEGORY = "WUKONG/图像"

    def execute(self, image):
        # 使用 rgba2rgb_tensor 函数转换图像
        out = self.rgba2rgb_tensor(image)       
        return (out,)

    # 将 RGBA 图像转换为 RGB
    def rgba2rgb_tensor(self, rgba):
        r = rgba[...,0]
        g = rgba[...,1]
        b = rgba[...,2]
        return torch.stack([r, g, b], dim=3)


# 节点注册
NODE_CLASS_MAPPINGS = {
    "WUKONGRAGBDRGB": WUKONGRAGBDRGB,
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "WUKONGRAGBDRGB": "WUKONGRAGBDRGB",
}
