import os
import re
import pandas as pd
from concurrent.futures import ProcessPoolExecutor, as_completed
from pathlib import Path
'''
输入：文本文件夹、关键词文本

统计文本文件夹中各个 .txt 文本的词频

输出到 excel 表格

待办：这是面向纯文本的计算代码，应当在分词后进行

'''


def count_keyword_frequency(filepath, keywords):
    with open(filepath, "r", encoding="utf-8") as f:
        content = f.read()
    count = {keyword: content.count(keyword) for keyword in keywords}
    count['文件名'] = Path(filepath).name
    return count


def countWordFrequency(folder_path, dict_path):
    # 读取词典
    with open(dict_path, "r", encoding="utf-8") as f:
        keywords = [line.strip() for line in f.readlines()]
        keywords = [re.sub(r'\t.*', r'', keyword) for keyword in keywords]
        keywords = [re.sub(r'\nTopic.*', r'', keyword) for keyword in keywords]

    # 获取所有txt文件的路径
    files = [os.path.join(folder_path, filename) for filename in os.listdir(
        folder_path) if filename.endswith(".txt")]
    file_count = len(files)
    print(f"Total files to process: {file_count}")

    # 创建一个进程池，并行处理文件
    results = []
    with ProcessPoolExecutor() as executor:
        future_to_file = {executor.submit(
            count_keyword_frequency, file, keywords): file for file in files}
        for future in as_completed(future_to_file):
            res = future.result()
            results.append(res)
            print(f"Files remaining: {file_count - len(results)}")

    # 将结果保存为CSV表格
    df = pd.DataFrame(results)
    csv_path = dict_path + "_result.csv"
    df.to_csv(csv_path, index=False, encoding="utf-8-sig")

    print("完成！！")
    return df


def main():

    # 输入文件夹路径和词典路径
    folder_path = r"E:\Source_for_sale\A股年报 PDF+TXT\A股年报TXT [56080份18.8GB]"
    dict_path = r"D:\ZZZMydocument\Academic_1101\230404_管理科学投稿\数据 tidy\[require]\数字化转型\许为宾\许为宾.txt"
    countWordFrequency(folder_path, dict_path)


if __name__ == '__main__':
    main()
