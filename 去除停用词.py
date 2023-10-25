import os
'''
输入：文本文件夹、停用词词典路径、输出文本文件夹

文本文件夹中有多个 .txt 文件
停用词词典中，每个停用词分行排列，一行一个

删除文本文件夹中 .txt 文件的停用词。

本步骤需要在分词之前进行。

'''


def remove_stopwords(input_folder, stopwords_file, output_folder):
    # 读取停用词文件
    with open(stopwords_file, 'r', encoding="utf-8") as f:
        stopwords = f.read().splitlines()

    # 根据停用词长度进行排序，以便尽量匹配更长的停用词
    stopwords.sort(key=len, reverse=True)

    # 遍历输入文件夹中的所有txt文件
    for filename in os.listdir(input_folder):
        if filename.endswith('.txt'):
            input_file = os.path.join(input_folder, filename)
            output_file = os.path.join(output_folder, filename)

            # 读取输入文件内容并删除停用词
            with open(input_file, 'r', encoding="utf-8") as f:
                content = f.read()
                for word in stopwords:
                    content = content.replace(word, '')

            # 将过滤后的内容保存到输出文件
            with open(output_file, 'w', encoding="utf-8") as f:
                f.writelines(content)

        print(f"处理完成: {filename}")


def main():

    # 获取用户输入
    input_folder = input("请输入文本文件夹：")
    stopwords_file = input("请输入停用词txt文件路径：")
    output_folder = input("请输入输出文本文件夹：")

    # 调用函数删除停用词并保存结果
    remove_stopwords(input_folder, stopwords_file, output_folder)


if __name__ == '__main__':
    main()
