import os
import re
import jieba
from concurrent.futures import ProcessPoolExecutor


def preprocess_file(input_file_path, output_file_path, stopwords, custom_dict_path=None):
    with open(input_file_path, "r", encoding="utf-8") as input_file:
        content = input_file.read()

        # 去除非中文字符
        chinese_content = re.sub(r"[^\u4e00-\u9fa5]+", "", content)

        # 使用jieba进行分词
        if custom_dict_path:
            jieba.load_userdict(custom_dict_path)
        seg_list = jieba.cut(chinese_content, cut_all=False)

        # 去除停用词
        seg_list = [word for word in seg_list if word not in stopwords]

        # 去除单字词
        seg_list = [word for word in seg_list if len(word) > 1]

        # 写入处理后的内容
        with open(output_file_path, "w", encoding="utf-8") as output_file:
            output_file.write(" ".join(seg_list))

        print(f"已处理文件：{input_file_path}")


def preprocess_folder(input_folder, output_folder, stopwords, custom_dict_path=None):
    with ProcessPoolExecutor() as executor:
        futures = []
        for file_name in os.listdir(input_folder):
            if file_name.endswith(".txt"):
                input_file_path = os.path.join(input_folder, file_name)
                output_file_path = os.path.join(output_folder, file_name)

                # 提交任务给进程池
                future = executor.submit(
                    preprocess_file, input_file_path, output_file_path, stopwords, custom_dict_path)
                futures.append(future)

        # 等待所有任务完成
        for future in futures:
            future.result()

    print("所有文件处理完成")


def main():
    input_folder = "E:\Downloads\下载2\暂存预处理文件\A股年报TXT"
    output_folder = "E:\Downloads\下载2\暂存预处理文件\A股年报TXT导出"
    stopwords_file = "E:\Downloads\下载2\暂存预处理文件\合并文档.txt"
    # custom_dict_path = input("输入自定义分词词典路径（可选，没有直接按enter）")

    # 读取停用词文件
    with open(stopwords_file, 'r', encoding="utf-8") as f:
        stopwords = set(f.read().splitlines())

    # 创建输出文件夹
    os.makedirs(output_folder, exist_ok=True)

    # 进行文本预处理
    preprocess_folder(input_folder, output_folder, stopwords)

    print("处理完成！")


if __name__ == '__main__':
    main()
