import torch
from PIL import Image
import numpy as np
def tensor2pil(image):
    return Image.fromarray(np.clip(255. * image.cpu().numpy().squeeze(), 0, 255).astype(np.uint8))
def pil2tensor(image):
    return torch.from_numpy(np.array(image).astype(np.float32) / 255.0).unsqueeze(0)
def resize_mask(mask_pil, target_size):
    return mask_pil.resize(target_size, Image.LANCZOS)
def image2mask(image_pil):
    # Convert image to grayscale
    image_pil = image_pil.convert("L")
    # Convert grayscale image to binary mask
    threshold = 128
    mask_array = np.array(image_pil) > threshold
    return Image.fromarray((mask_array * 255).astype(np.uint8))
class WUKONGZHEZHAOCAIJIAN:
    def __init__(self):
        pass
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "模式": (["合并", "裁剪", "相交", "不相交"], {}),
            },
            "optional": {
                "底遮罩图": ("IMAGE", {}),
                "底遮罩": ("MASK", {}),
                "素材遮罩图": ("IMAGE", {}),
                "素材遮罩": ("MASK", {}),
            },
        }
    RETURN_TYPES = ("MASK", "IMAGE")
    RETURN_NAMES = ("合并遮罩", "合并遮罩图")
    FUNCTION = "mask_模式"
    CATEGORY = "WUKONG/其他"
    def mask_模式(self, 模式, 素材遮罩图=None, 底遮罩图=None, 素材遮罩=None, 底遮罩=None):
        # Convert source and target images to masks if provided
        if 素材遮罩图 is not None:
            素材遮罩_pil = tensor2pil(素材遮罩图)
            素材遮罩_pil = image2mask(素材遮罩_pil)
        else:
            素材遮罩_pil = tensor2pil(素材遮罩)
        if 底遮罩图 is not None:
            底遮罩_pil = tensor2pil(底遮罩图)
            底遮罩_pil = image2mask(底遮罩_pil)
        else:
            底遮罩_pil = tensor2pil(底遮罩)
        # Resize source mask to target mask size
        素材遮罩_pil = resize_mask(素材遮罩_pil, 底遮罩_pil.size)
        素材遮罩_array = np.array(素材遮罩_pil) > 0
        底遮罩_array = np.array(底遮罩_pil) > 0
        if 模式 == "合并":
            合并遮罩_array = np.logical_or(素材遮罩_array, 底遮罩_array)
        elif 模式 == "裁剪":
            合并遮罩_array = np.logical_and(底遮罩_array, np.logical_not(素材遮罩_array))
        elif 模式 == "相交":
            合并遮罩_array = np.logical_and(素材遮罩_array, 底遮罩_array)
        elif 模式 == "不相交":
            合并遮罩_array = np.logical_xor(素材遮罩_array, 底遮罩_array)
        else:
            raise ValueError("Invalid 模式 selected")
        合并遮罩 = Image.fromarray((合并遮罩_array * 255).astype(np.uint8))
        合并遮罩_tensor = pil2tensor(合并遮罩)
        合并遮罩图_tensor = pil2tensor(合并遮罩)
        return [合并遮罩_tensor, 合并遮罩图_tensor]


