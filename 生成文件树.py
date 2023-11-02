import os


def generate_file_tree(folder_path, prefix='', is_last=True):
    items = os.listdir(folder_path)
    print(prefix + ('└── ' if is_last else '├── ') +
          os.path.basename(folder_path))
    prefix += '    ' if is_last else '│   '

    files = [item for item in items if os.path.isfile(
        os.path.join(folder_path, item))]
    folders = [item for item in items if os.path.isdir(
        os.path.join(folder_path, item))]
    items = folders + files

    for i, item in enumerate(items):
        is_last = i == len(items) - 1
        path = os.path.join(folder_path, item)
        if os.path.isdir(path):
            generate_file_tree(path, prefix, is_last)
        else:
            print(prefix + ('└── ' if is_last else '├── ') + item)


if __name__ == '__main__':
    folder_path = input("请输入文件夹路径: ")
    generate_file_tree(folder_path)
