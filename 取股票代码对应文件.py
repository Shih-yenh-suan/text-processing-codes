import os
import shutil


def copy_stock_files(folder_path, stock_file, destination_folder):
    # 创建目标文件夹如果它不存在
    if not os.path.exists(destination_folder):
        os.makedirs(destination_folder)

    # 读取股票代码
    with open(stock_file, 'r') as file:
        stock_codes = {line.strip() for line in file}

    found_codes = set()

    # 遍历指定文件夹及其子文件夹
    for root, dirs, files in os.walk(folder_path):
        for file in files:
            # 检查文件名的前缀是否在任何一个股票代码中
            for code in stock_codes.copy():
                if file.startswith(code):
                    full_file_path = os.path.join(root, file)
                    shutil.copy(full_file_path, destination_folder)
                    print(f"Copied: {file}")
                    found_codes.add(code)

    # 检查未找到的股票代码
    not_found_codes = stock_codes - found_codes
    if not_found_codes:
        print("未找到以下股票代码对应的文件：")
        for code in not_found_codes:
            print(code)
    else:
        print("所有股票代码对应的文件都已找到并复制。")


# 使用示例
folder_path = r""  # 这里替换成你的文件夹路径
stock_file = r""  # 这里替换成你的股票代码文件路径
destination_folder = r""  # 这里替换成你想复制文件到的目标文件夹路径

copy_stock_files(folder_path, stock_file, destination_folder)
