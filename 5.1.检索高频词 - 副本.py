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

            # 提取股票代码
            stock_code = re.findall(r"\d{6}", file_name)[0]

            # 读取文件内容
            with open(file_path, "r", encoding="utf-8") as txt_file:
                file_content = txt_file.read()

            # 将文件内容按空格分词
            words = file_content.split()

            # 记录每个单词在当前文档中的出现次数
            word_counts = defaultdict(int)
            for word in words:
                if word:
                    word_counts[word] += 1

            # 筛选只在当前股票代码中出现的单词
            unique_words = [word for word, count in word_counts.items() if count == 1]

            # 将当前股票代码的唯一单词添加到结果列表中
            content_list.extend([(stock_code, word) for word in unique_words])

    # 去重并写入txt文档
    unique_words = list(set(content_list))
    with open(output_file, 'w', encoding='utf-8') as f:
        for stock_code, word in unique_words:
            f.write(f"{stock_code}\t{word}\n")    

folder_path_A = "D:\ZZZMydocument\Codes\LDA主题模型\csrReport4_removeSingleWord"
output_file = 'D:\ZZZMydocument\Codes\LDA主题模型\csrReport5.1_removeMostCommonWord.txt'

process_table(folder_path_A)