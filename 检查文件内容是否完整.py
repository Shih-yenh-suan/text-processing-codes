import os
import shutil
import re
from concurrent.futures import ThreadPoolExecutor


def clean_text(text):
    return re.sub(r"[^\u4e00-\u9fa5a-zA-Z]", "", text)


def process_file(file_path, output_folder):
    try:
        with open(file_path, 'r', encoding='utf-8', errors='ignore') as file:
            content = file.read()

        len_original = len(re.sub(r"\s", "", content))
        cleaned_content = clean_text(content)
        len_cleaned = len(re.sub(r"\s", "", cleaned_content))

        if (len_cleaned < 0.6 * len_original) or (len_original <= 10000):
            shutil.move(file_path, os.path.join(
                output_folder, os.path.basename(file_path)))
            print(f"{file_path}已移动, {len_cleaned}, {len_original}")
        else:
            print(
                f"{file_path[29:40]}保留, {len_cleaned}, {len_original}, {len_cleaned/len_original}")
    except Exception as e:
        print(f"处理文件 '{file_path}' 时发生错误: {e}")


def main(input_folder, output_folder):
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    # 获取文件列表并根据大小进行排序
    txt_files = [(os.path.join(input_folder, f), os.path.getsize(os.path.join(input_folder, f)))
                 for f in os.listdir(input_folder) if f.endswith('.txt')]
    txt_files.sort(key=lambda x: x[1])

    with ThreadPoolExecutor() as executor:
        # 处理排序后的文件
        executor.map(lambda file: process_file(
            file[0], output_folder), txt_files)


if __name__ == "__main__":
    input_folder_path = r"E:\Downloads\港股年报\港股年报英文版TXT"
    output_folder_path = r"E:\Downloads\港股年报\港股年报英文版TXT2"
    main(input_folder_path, output_folder_path)
