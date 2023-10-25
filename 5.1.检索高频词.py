import os
import re
import pandas as pd
from collections import defaultdict

def process_table(folder_path_A):
    # 获取文件夹A中的所有txt文件
    file_list = os.listdir(folder_path_A)
    total_files = len(file_list)
    # 初始化content为空字符串
    content_list = []

    # 遍历文件夹A中的所有txt文件
    for i, file_name in enumerate(file_list):
        if file_name.endswith(".txt"):
            file_path = os.path.join(folder_path_A, file_name)

            # 读取文件内容
            with open(file_path, "r", encoding="utf-8") as txt_file:
                file_content = txt_file.read()

            # 将文件内容添加到content中，并在不同文件之间添加换行符
            content_list.append(file_content)

    # 将content写入输出文件
    with open(output_file, 'a', encoding='utf-8') as f:
        f.write("\n".join(content_list))

    # 统计每个词的出现次数
    word_counts = defaultdict(int)
    all_words = []
    lines = re.split(r'\n', "\n".join(content_list))
    
    for line in lines:
        words = line.split()
        all_words.extend(words)
        for word in words:
            if word:
                word_counts[word] += 1

    # 计算全部行中出现的词
    common_words = [word for word, count in word_counts.items() if count >= total_files * 1]  
    
    # 计算出现频率最高的前0.1%的词
    total_words = len(all_words)
    number_words = defaultdict(int)
    for word in all_words:
        number_words[word] += 1
    frequency_dict = {word: count/total_words for word, count in number_words.items()}
    sorted_dict = sorted(frequency_dict.items(), key=lambda x: x[1], reverse=True)
    top_words = [word for word, count in sorted_dict[:int(len(sorted_dict) * 0.001)]]

    # 计算仅在全部样本中出现过一次的单词
    unique_words_once = [word for word, count in number_words.items() if count == 1]

    # 去重并写入txt文档
    unique_words = list(set(common_words + unique_words_once + top_words))
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write('\n'.join(unique_words))    

folder_path_A = "D:\ZZZMydocument\Codes\LDA主题模型\csrReport4_removeSingleWord"
output_file = 'D:\ZZZMydocument\Codes\LDA主题模型\csrReport5.1_removeMostCommonWord.txt'

process_table(folder_path_A)