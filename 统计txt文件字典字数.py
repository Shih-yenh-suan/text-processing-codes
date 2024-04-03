import os
import pandas as pd


def count_dictionary_words(folder_path, dictionary_path):
    # 读取词典
    with open(dictionary_path, 'r', encoding='utf-8') as f:
        dictionary = set(word.strip() for word in f.readlines())

    # 创建一个 DataFrame 用于存储结果
    result_data = []

    # 遍历文件夹中的每个文件
    for root, dirs, files in os.walk(folder_path):
        for filename in files:
            print(filename)
            if filename.endswith('.txt'):
                file_path = os.path.join(root, filename)
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                content_length = len(content)
                # 计算文件中包含的词典中的汉字数量
                dictionary_words_count = sum(
                    1 for word in dictionary if word in content)
                # 将每1千字所包含的字典字数计算出来
                per_thousand_words_count = (
                    dictionary_words_count / content_length) * 1000
                result_data.append(
                    {'文件名': filename, '词典字数': per_thousand_words_count})

    # 将结果转换为 DataFrame
    result_df = pd.DataFrame(result_data)

    # 保存结果到 stata 的 dta 文件
    result_df.to_stata('result.dta', version=118)


# 示例用法
count_dictionary_words(
    r"N:\Source_for_sale\A股年报【2024-03-27】\A股年报TXT",
    r"E:\Downloads\3500常用汉字.txt")
