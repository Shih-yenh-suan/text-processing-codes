import os
import re


def remove_whitespace(input_path, output_path):
    # 创建输出文件夹
    os.makedirs(output_path, exist_ok=True)

    # 遍历输入文件夹中的所有文件
    for file_name in os.listdir(input_path):
        # 检查文件是否为txt文件
        if file_name.endswith(".txt"):
            input_file_path = os.path.join(input_path, file_name)
            output_file_path = os.path.join(output_path, file_name)

            # 打开输入文件
            with open(input_file_path, "r", encoding="utf-8") as input_file:
                # 读取文件内容
                content = input_file.read()

                # 删除空白字符
                no_whitespace_content = re.sub(r"[\t ]", "", content)

                # 创建输出文件并写入处理后的内容
                with open(output_file_path, "w", encoding="utf-8") as output_file:
                    output_file.write(no_whitespace_content)

            print(f"处理完成: {file_name}")

    print("所有文件处理完成！")


def main():
    # 输入文件夹路径和输出文件夹路径
    input_folder = input("请输入文本文件夹：")
    output_folder = input("请输入输出文本文件夹：")
    remove_whitespace(input_folder, output_folder)


if __name__ == '__main__':
    main()
