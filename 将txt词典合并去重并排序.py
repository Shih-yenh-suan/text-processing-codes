import os
from pypinyin import lazy_pinyin

script_directory = os.path.dirname(os.path.abspath(__file__))

file_paths = [r"D:\ZZZMydocument\Codes\实验\情感分析\关键词\原始关键词\1.txt",
              r"D:\ZZZMydocument\Codes\实验\情感分析\关键词\原始关键词\2.txt"]

file_paths = [os.path.join(script_directory, f) for f in file_paths]

stopwords = set()

# 读取关键词文件并添加到集合中
for file_path in file_paths:
    with open(file_path, "r", encoding="utf-8") as file:
        for line in file:
            stopwords.add(line.strip())

# 将关键词按拼音排序
sorted_stopwords = sorted(stopwords, key=lambda x: "".join(lazy_pinyin(x)))
sorted_stopwords = [item for item in sorted_stopwords if item.strip()]
# 删除被包含的词
final_stopwords = []
for word in sorted_stopwords:
    # 如果当前词语是被其他词语包含的部分，则跳过
    if any(w in word for w in final_stopwords):
        print(word)
        continue
    final_stopwords.append(word)

# 写入整合文档
integrated_file_path = r"D:\ZZZMydocument\Codes\实验\情感分析\关键词\整合.txt"
with open(integrated_file_path, "w", encoding="utf-8") as integrated_file:
    for word in final_stopwords:
        integrated_file.write(word + "\n")

print(f"整合文档已保存为 {integrated_file_path}")
