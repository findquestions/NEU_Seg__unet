import os
import random

# 定义图片文件夹路径
image_folder = r'D:\Download\U-Net\U-Net\data_wenjian\JPEGImages'

# 获取所有图片名字（不带后缀）
image_names = [os.path.splitext(f)[0] for f in os.listdir(image_folder) if os.path.isfile(os.path.join(image_folder, f))]

# 随机打乱图片顺序
random.shuffle(image_names)

# 计算数量比例，按照 1:2:7 进行划分
total_images = len(image_names)
num_test = total_images // 10  # 1/10 的数据作为 test
num_val = (total_images * 2) // 10  # 2/10 的数据作为 val
num_train = total_images - num_test - num_val  # 剩下的 7/10 数据作为 train

# 划分数据集
test_images = image_names[:num_test]
val_images = image_names[num_test:num_test + num_val]
train_images = image_names[num_test + num_val:]

# 定义输出文件路径
test_txt_path = r'D:\Download\U-Net\U-Net\data_wenjian\test.txt'
val_txt_path = r'D:\Download\U-Net\U-Net\data_wenjian\val.txt'
train_txt_path = r'D:\Download\U-Net\U-Net\data_wenjian\train.txt'

# 将图片名字写入对应的 txt 文件
def write_to_txt(file_path, image_list):
    with open(file_path, 'w') as f:
        for image in image_list:
            f.write(image + '\n')

write_to_txt(test_txt_path, test_images)
write_to_txt(val_txt_path, val_images)
write_to_txt(train_txt_path, train_images)

print(f"Test, Val, and Train image names have been saved to:\n{test_txt_path}\n{val_txt_path}\n{train_txt_path}")
