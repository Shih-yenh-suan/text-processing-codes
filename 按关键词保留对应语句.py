import os
import re
import shutil
import threading
from pypinyin import lazy_pinyin
'''
输入：文本文件夹、输出文本文件夹、关键词词典

对于文本文件夹中所有的 .txt 文件，仅保留中文、英文、数字、重要标点
按照重要标点分行

保留包含关键词的行

保存并输出

'''


def read_keywords(keyword_path):
    """
    读取关键词文件并返回关键词列表
    """
    with open(keyword_path, 'r', encoding='ANSI') as file:
        keywords = file.read().strip().split('、')
        keywords = sorted(keywords, key=lambda x: "".join(lazy_pinyin(x)))
    return keywords


def remove_non_characters(input_path, output_path):
    # 创建输出文件夹
    os.makedirs(output_path, exist_ok=True)

    # 遍历输入文件夹中的所有文件
    for file_name in os.listdir(input_path):
        # 检查文件是否为txt文件
        if file_name.endswith(".txt"):
            input_file_path = os.path.join(input_path, file_name)
            output_file_path = os.path.join(output_path, file_name)

            # 打开输入文件
            with open(input_file_path, "r", encoding="utf-8") as input_file:
                # 读取文件内容
                content = input_file.read()

                # 去除中文、英文、数字、重要标点之外的，重要标点都分行
                useful_char = re.sub(
                    r"[^a-zA-Z\u4e00-\u9fa5\d!！.。?？……(..)]+", "", content)
                useful_char = re.sub(r"[!！.。?？……(..)]+", "\n", useful_char)

                # 创建输出文件并写入处理后的内容
                with open(output_file_path, "w", encoding="utf-8") as output_file:
                    output_file.write(useful_char)

            print(f"处理完成: {file_name}")

    print("所有文件处理完成！")


def keep_keyword_sentence(input_path, output_path, keywords_path):
    # 读取关键词
    keywords = read_keywords(keywords_path)

    # 遍历input_path文件夹下的所有txt文件
    for filename in os.listdir(input_path):
        if filename.endswith('.txt'):
            input_file_path = os.path.join(input_path, filename)
            output_file_path = os.path.join(output_path, filename)

            # 读取输入文件，保留包含关键词的句子
            with open(input_file_path, 'r', encoding='utf-8') as infile:
                sentences_to_keep = []
                for line in infile:
                    for keyword in keywords:
                        if keyword in line:
                            sentences_to_keep.append(line.strip())
                            break

            # 将保留的句子写入输出文件
            with open(output_file_path, 'w', encoding='utf-8') as outfile:
                outfile.write('\n'.join(sentences_to_keep))


def process_files(input_folder, output_folder, keywords_path):
    # Remove non-characters
    remove_non_characters(input_folder, output_folder)

    # Keep keyword sentences
    keep_keyword_sentence(output_folder, output_folder, keywords_path)


def main():
    input_folder = input("")
    output_folder = input("")
    keywords_path = input("")  # 关键词词典

    # Create a list of threads
    threads = []

    # Create two threads to process the files concurrently
    thread1 = threading.Thread(target=process_files, args=(
        input_folder, output_folder, keywords_path))
    thread2 = threading.Thread(target=process_files, args=(
        input_folder, output_folder, keywords_path))

    # Add threads to the list
    threads.append(thread1)
    threads.append(thread2)

    # Start both threads
    thread1.start()
    thread2.start()

    # Wait for both threads to finish
    thread1.join()
    thread2.join()


if __name__ == '__main__':
    main()
