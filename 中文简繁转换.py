import os
import opencc
from langdetect import detect, lang_detect_exception
'''
输入：输入文件夹、输出文件夹路径

使用 langdetect 模块，检查输入文件夹中所有 .txt 的文本语言

对于繁体文件，将其转换为简体，用于文本分析

'''


def convert_files(input_folder, output_folder):
    # 创建输出文件夹
    os.makedirs(output_folder, exist_ok=True)

    # 创建OpenCC转换器
    converter = opencc.OpenCC('t2s.json')

    # 遍历输入文件夹中的所有文件
    for filename in os.listdir(input_folder):
        if filename.endswith('.txt'):
            input_path = os.path.join(input_folder, filename)
            output_path = os.path.join(output_folder, filename)

            # 打开输入文件
            with open(input_path, 'r', encoding='utf-8') as input_file:
                # 读取文件内容
                content = input_file.read()

                try:
                    # 使用langdetect库检测文档语言
                    lang = detect(content)
                except lang_detect_exception.LangDetectException:
                    # 如果遇到错误，跳过语言检测并继续处理下一个文件
                    print(f'文件 {filename} 无法检测，跳过处理。')
                    continue

                # 使用langdetect库检测文档语言
                lang = detect(content)

                # 判断文档是否为繁体文档
                if lang == 'ko':
                    # 将繁体字转换为简体字
                    converted_content = converter.convert(content)
                    print(f'文件 {filename} 转换完成！')
                else:
                    # 不需要转换，保持原文内容
                    converted_content = content
                    print(f'文件 {filename} 不是繁体文档，无需转换。')

                # 创建输出文件并写入转换后的内容
                with open(output_path, 'w', encoding='utf-8') as output_file:
                    output_file.write(converted_content)

    print('所有文件转换完成！')


def main():

    # 输入文件夹路径和词典路径
    input_folder = input("请输入文本文件夹：")
    output_folder = input("请输入输出文本文件夹：")
    convert_files(input_folder, output_folder)


if __name__ == '__main__':
    main()
