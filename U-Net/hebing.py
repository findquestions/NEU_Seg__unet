import os
import shutil

# 定义两个文件夹的路径
folder_training = r'D:\Download\赛题2-钢材表面缺陷检测与分割\数据集\NEU_Seg-main\annotations\training'
folder_test = r'D:\Download\赛题2-钢材表面缺陷检测与分割\数据集\NEU_Seg-main\annotations\test'

# 定义合并后的输出文件夹路径
output_folder = r'D:\Download\赛题2-钢材表面缺陷检测与分割\数据集\NEU_Seg-main\annotations\combined'
os.makedirs(output_folder, exist_ok=True)

# 获取训练文件夹和测试文件夹中的文件名
training_files = os.listdir(folder_training)
test_files = os.listdir(folder_test)

# 记录已经存在的文件名（不带扩展名）
existing_names = set()

# 处理训练文件夹中的文件
for filename in training_files:
    name, ext = os.path.splitext(filename)
    src_path = os.path.join(folder_training, filename)

    # 检查文件名是否已经存在
    if name in existing_names:
        # 如果重名，则添加后缀以避免冲突
        new_name = f"{name}_training{ext}"
    else:
        new_name = filename
        existing_names.add(name)

    dst_path = os.path.join(output_folder, new_name)
    shutil.copy(src_path, dst_path)

# 处理测试文件夹中的文件
for filename in test_files:
    name, ext = os.path.splitext(filename)
    src_path = os.path.join(folder_test, filename)

    # 检查文件名是否已经存在
    if name in existing_names:
        # 如果重名，则添加后缀以避免冲突
        new_name = f"{name}_test{ext}"
    else:
        new_name = filename
        existing_names.add(name)

    dst_path = os.path.join(output_folder, new_name)
    shutil.copy(src_path, dst_path)

print(f"图片已成功合并到 {output_folder} 文件夹，重名的文件已重命名。")
