import base64
import lzma
import os

# 读取当前的 __init__.py 文件
current_dir = os.path.dirname(os.path.abspath(__file__))
input_file = os.path.join(current_dir, '__init__.py')

# 读取文件内容
with open(input_file, "r", encoding='utf-8') as file:
    file_content = file.read()

# 进行 LZMA 压缩并进行 Base64 编码
encoded_content = base64.b64encode(lzma.compress(file_content.encode('utf-8')))

# 生成新的文件内容
new_content = f'''
import base64
import lzma

ENCODED = "{encoded_content.decode('utf-8')}"

def decrypt_and_run():
    try:
        decoded = lzma.decompress(base64.b64decode(ENCODED)).decode('utf-8')
        exec(decoded, globals())
    except Exception as e:
        print(f"Decryption failed: {{e}}")

decrypt_and_run()

if 'NODE_CLASS_MAPPINGS' not in globals():
    NODE_CLASS_MAPPINGS = {{}}
if 'NODE_DISPLAY_NAME_MAPPINGS' not in globals():
    NODE_DISPLAY_NAME_MAPPINGS = {{}}
'''

# 写入加密后的内容
with open(input_file, "w", encoding='utf-8') as file:
    file.write(new_content)

print("Encryption completed!")