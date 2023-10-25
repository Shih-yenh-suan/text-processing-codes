import os
import jieba

def segment_files(folder_path_A, folder_path_B, custom_dict_path=None):
    # 检查文件夹B是否存在，如果不存在则创建
    if not os.path.exists(folder_path_B):
        os.makedirs(folder_path_B)

    # 加载自定义词典C
    if custom_dict_path:
        jieba.load_userdict(custom_dict_path)

    # 遍历文件夹A中的所有txt文件
    for file_name in os.listdir(folder_path_A):
        if file_name.endswith(".txt"):
            file_path_A = os.path.join(folder_path_A, file_name)
            file_path_B = os.path.join(folder_path_B, file_name)

            # 读取文件内容
            with open(file_path_A, "r", encoding="utf-8") as file_A:
                content = file_A.read()

            # 使用jieba进行分词
            seg_list = jieba.cut(content, cut_all=False)

            # 将分词结果写入文件夹B中的对应文件
            with open(file_path_B, "w", encoding="utf-8") as file_B:
                file_B.write(" ".join(seg_list))

            print(f"文件 {file_name} 分词完成")

    print("所有文件分词完成")

def main():
    
    input_folder = input("请输入文本文件夹：") # D:\ZZZMydocument\Codes\LDA主题模型\csrReport1.1_removeSpecialChar
    output_folder = input("请输入输出文本文件夹：") # D:\ZZZMydocument\Codes\LDA主题模型\csrReport1.2_cht2chs
    custom_dict_path = input("输入自定义词典路径（可选，没有直接按enter）")
    segment_files(input_folder, output_folder, custom_dict_path)
    
if __name__ == '__main__':
    main()
    