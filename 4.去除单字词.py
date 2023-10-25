import os
'''
输入：输入文件夹、输出文件夹路径

遍历输入文件夹中的所有 .txt 文件。这些文件已经经过了 jieba 分词处理，每个词按照空格分隔

删除其中的单字词

输出：删除了单字词的 .txt 文件

'''


def remove_single_char_words(input_folder, output_folder):
    # 检查输出文件夹是否存在，如果不存在则创建
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    # 遍历输入文件夹中的所有文件
    for filename in os.listdir(input_folder):
        if filename.endswith(".txt"):
            input_file = os.path.join(input_folder, filename)
            output_file = os.path.join(output_folder, filename)

            # 打开输入文件
            with open(input_file, 'r', encoding='utf-8') as file:
                content = file.read()

            # 分割字符串为单词
            words = content.split()

            # 删除单个字母组成的单词
            filtered_words = [word for word in words if len(word) > 1]

            # 将修改后的内容写入输出文件
            with open(output_file, 'w', encoding='utf-8') as file:
                file.write(' '.join(filtered_words))

            print(f"处理完成: {filename}")


# 示例用法
input_folder = "D:\ZZZMydocument\Codes\LDA主题模型\csrReport3_jiebaDevide"
output_folder = "D:\ZZZMydocument\Codes\LDA主题模型\csrReport4_removeSingleWord"

remove_single_char_words(input_folder, output_folder)
