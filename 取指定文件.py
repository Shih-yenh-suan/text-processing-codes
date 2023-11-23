import os
import pandas as pd
from shutil import copyfile


def extract_reports(input_excel, report_folder):
    # 读取Excel文件
    df = pd.read_excel(input_excel, header=None, names=[
                       '股票代码', '年份', "类型",  "是否漂绿"])

    # 遍历Excel中的每一行
    for index, row in df.iterrows():
        stock_code = str(row['股票代码'])
        year = str(row['年份'])

        # 获取前两年的年份
        last_year = str(int(year) - 1)
        two_years_ago = str(int(year) - 2)

        # 递归地构建文件名列表
        file_names = get_report_files(
            report_folder, stock_code, year, last_year, two_years_ago)

        # 遍历文件名列表，如果文件存在，则复制到指定文件夹
        for file_name in file_names:
            source_path = os.path.join(report_folder, file_name)
            destination_path = os.path.join(direction, file_name)

            if os.path.exists(source_path):
                copyfile(source_path, destination_path)
                print(f"成功提取 {stock_code} {year} 年报告到 {destination_path}")
            else:
                print(f"{stock_code} {year} 年报告不存在于 {source_path}，跳过")


def get_report_files(folder, stock_code, year, last_year, two_years_ago):
    file_names = []
    for root, dirs, files in os.walk(folder):
        for file in files:
            if file.startswith(stock_code):
                file_year = file[7:10]
                if (file_year == year and year != '2016') or (file_year == '2016' and year == '2016') or \
                        file_year == last_year or file_year == two_years_ago:
                    file_names.append(file)
    print(file_names)
    return file_names


if __name__ == "__main__":
    # 输入Excel文件路径和报告文件夹路径
    excel_path = r"D:\ZZZMydocument\Academic_1101\231120_毕业论文\script\[GW-machine]\测试集.xlsx"
    folder_path = r"E:\Source_for_sale\A股社会责任报告 PDF+TXT\A股社会责任报告TXT [12364份78.7GB]"
    direction = r"D:\ZZZMydocument\Academic_1101\231120_毕业论文\script\[GW-machine]\测试集"
    # 调用函数提取报告
    extract_reports(excel_path, folder_path)
