import pandas as pd

# 读取每个工作表的股票数据

def read_stock_data():
    # 读取 Excel 文件
    file_path = 'a_stock_codes_by_concept.xlsx'
    concept_stock_data = {}
    # 获取所有工作表名称
    sheet_names = pd.ExcelFile(file_path).sheet_names

    for sheet_name in sheet_names:
        df = pd.read_excel(file_path, sheet_name=sheet_name, dtype={'code': str})
        concept_stock_data[sheet_name] = df

    return concept_stock_data


if __name__ == '__main__':
    stock_data = read_stock_data()
    for key in stock_data.keys():
        print(key)
        print(stock_data[key])
        print(stock_data[key]["code"])
        stock_data_ls = stock_data[key]["code"].tolist()
        print(stock_data_ls)
        chunked_list = [stock_data_ls[i:i + 3] for i in range(0, len(stock_data_ls), 3)]
        print(chunked_list)