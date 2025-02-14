from PIL import Image, ImageFilter
import torch
import numpy as np

def tensortopil(image):
    return Image.fromarray(np.clip(255. * image.cpu().numpy().squeeze(), 0, 255).astype(np.uint8))
def piltotensor(image):
    return torch.from_numpy(np.array(image).astype(np.float32) / 255.0).unsqueeze(0)

class WUKONGHTKSMH:
    @classmethod
    def INPUT_TYPES(s):
        return {
                "required": {
                                "mask": ("MASK",),
                                "模糊强度":("INT", {"default": 1, 
                                                        "min":0, 
                                                        "max": 150, 
                                                        "step": 1,
                                                        "display": "slider"})
                            }
            }
    
    RETURN_TYPES = ('MASK',)
    FUNCTION = "maskmohu"
    CATEGORY = "WUKONG/其他"
    INPUT_IS_LIST = False
    OUTPUT_IS_LIST = (False,)
    def maskmohu(self,mask,模糊强度):
        print('SmoothMask',mask.shape)
        mask=tensortopil(mask)
        feathered_image = mask.filter(ImageFilter.GaussianBlur(模糊强度))

        mask=piltotensor(feathered_image)
           
        return (mask,)


