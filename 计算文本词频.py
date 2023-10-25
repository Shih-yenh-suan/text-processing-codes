import os
import re
import pandas as pd


def countWordFrequency(folder_path, dict_path):

    # 读取词典
    with open(dict_path, "r", encoding="utf-8") as f:
        keywords = [line.strip() for line in f.readlines()]
        keywords = [re.sub(r'\t.*', r'', keyword) for keyword in keywords]
        keywords = [re.sub(r'\nTopic.*', r'', keyword) for keyword in keywords]

    # 遍历文件夹，统计各个关键词出现的次数
    data = {}
    for filename in os.listdir(folder_path):
        if filename.endswith(".txt"):
            filepath = os.path.join(folder_path, filename)
            with open(filepath, "r", encoding="utf-8") as f:
                content = f.read()
                count = []
                for keyword in keywords:
                    count.append(content.count(keyword))
                data[filename] = count

    # 将结果保存为Excel表格
    df = pd.DataFrame.from_dict(data, orient="index", columns=keywords)
    df.index.name = "文件名"
    df.to_excel(dict_path + "_result.xlsx")

    print("完成！！")
    return df


def main():

    # 输入文件夹路径和词典路径
    folder_path = input("请输入文本文件夹：")
    dict_path = input("请输入包含关键词的文本，每行为一个关键词：")
    countWordFrequency(folder_path, dict_path)


if __name__ == '__main__':
    main()
