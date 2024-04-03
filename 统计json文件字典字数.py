import json
import pandas as pd


def load_common_chinese_characters(txt_path):
    with open(txt_path, 'r', encoding='utf-8') as f:
        common_chinese_characters = set(word.strip() for word in f.readlines())
    return common_chinese_characters


def calculate_readability(json_path, common_characters_path):
    # 加载常用汉字集合
    common_chinese_characters = load_common_chinese_characters(
        common_characters_path)

    # 读取 JSON 文件
    with open(json_path, 'r', encoding='utf-8') as f:
        data = json.load(f)

    # 遍历每个条目，计算可读性
    for entry in data:
        print(entry["股票代码"])
        mda_text = ' '.join(entry["MDA"])  # 将多个MDA段落合并为一个字符串
        mda_length = len(mda_text)
        if mda_length > 0:
            common_chinese_count = sum(
                1 for char in mda_text if char in common_chinese_characters)
            readability = common_chinese_count / mda_length
        else:
            readability = 0
        entry["可读性"] = readability

    # 转换为 DataFrame
    df = pd.DataFrame(data)
    df.drop(columns=['MDA'], inplace=True)
    print(df)
    # 保存结果到 JSON 文件
    df.to_stata('result.dta', version=118)


# 示例用法
calculate_readability(r"D:\ZZZMydocument\Codes\实验\情感分析\MDA_提取环境语料.json",
                      r"E:\Downloads\3500常用汉字.txt")
