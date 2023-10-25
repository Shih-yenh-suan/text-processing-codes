import os
from concurrent.futures import ThreadPoolExecutor

class TrieNode:
    def __init__(self):
        self.children = {}
        self.is_word = False

class Trie:
    def __init__(self):
        self.root = TrieNode()

    def insert(self, word):
        node = self.root
        for char in word:
            if char not in node.children:
                node.children[char] = TrieNode()
            node = node.children[char]
        node.is_word = True

    def search(self, word):
        node = self.root
        for char in word:
            if char not in node.children:
                return False
            node = node.children[char]
        return node.is_word

def remove_words_in_file(file_path, output_path, trie):
    # 读取文件内容
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # 分割内容为单词列表
    word_list = content.split()

    # 删除词汇文件中出现的完整词汇
    word_list = [word for word in word_list if not trie.search(word)]

    # 将单词列表重新组合为字符串
    new_content = ' '.join(word_list)

    # 将修改后的内容写入新文件
    filename = os.path.basename(file_path)
    new_file_path = os.path.join(output_path, filename)
    with open(new_file_path, 'w', encoding='utf-8') as f:
        f.write(new_content)

    print(f"文件 {filename} 处理完成")

def remove_words_in_files(folder_path, output_path, words_file):
    # 读取词汇文件
    content_list = []
    for words_file in words_files:
        # 读取词汇文件
        with open(words_file, 'r', encoding='utf-8') as f:
            words = f.read().splitlines()
        content_list += words

    # 构建Trie树
    trie = Trie()
    for word in content_list:
        trie.insert(word)

    # 遍历文件夹中的所有文件
    with ThreadPoolExecutor() as executor:
        for filename in os.listdir(folder_path):
            file_path = os.path.join(folder_path, filename)
            if os.path.isfile(file_path) and filename.endswith('.txt'):
                executor.submit(remove_words_in_file, file_path, output_path, trie)

    print("所有文件处理完成")

# 示例用法
folder_path = "D:\ZZZMydocument\Codes\LDA主题模型\csrReport4_removeSingleWord"
output_path = "D:\ZZZMydocument\Codes\LDA主题模型\csrReport5.1_removeMostCommonWord"
words_files = ["D:\ZZZMydocument\Codes\LDA主题模型\csrReport5.1_removeMostCommonWord.txt",
               "D:\ZZZMydocument\Codes\LDA主题模型\csrReport5.2_dictionary.txt"]
remove_words_in_files(folder_path, output_path, words_files)