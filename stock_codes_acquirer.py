import akshare as ak
import pandas as pd
# import numpy as np

# # 设置 NumPy 显示选项
# np.set_printoptions(threshold=np.inf)  # 显示所有内容，不截断

def acquire_stock_data():
    # 设置 Pandas 显示选项
    pd.set_option('display.max_colwidth', None)  # 不限制列宽
    pd.set_option('display.max_rows', None)      # 显示所有行
    pd.set_option('display.max_columns', None)   # 显示所有列
    # 获取A股股票列表
    stock_info_a_code_name_df = ak.stock_info_a_code_name()

    # 获取行业分类数据
    # sector_data = ak.stock_sector_spot(indicator="行业")
    # print(sector_data)
    # # 获取每个行业的股票代码
    # sector_stock_data = []
    # for label in sector_data['label']:
    #     try:
    #         sector_stocks = ak.stock_sector_detail(sector=f'"{label}"')
    #         sector_stocks['行业'] = label
    #         sector_stock_data.append(sector_stocks)
    #     except Exception as e:
    #         print(f"无法获取行业 {label} 的股票信息: {e}")
    # print(sector_stock_data)
    # # 合并所有行业股票数据
    # all_sector_stocks_df = pd.concat(sector_stock_data)

    # # 合并股票代码和行业信息
    # merged_df = pd.merge(stock_info_a_code_name_df, all_sector_stocks_df, left_on='code', right_on='代码', how='left')

    # # 按行业分类存储到Excel
    # with pd.ExcelWriter('a_stock_codes_by_sector.xlsx') as writer:
    #     for sector, group in merged_df.groupby('行业'):
    #         group[['code', 'name']].to_excel(writer, sheet_name=sector, index=False)

    # print("A股股票代码已按行业分类存储到 'a_stock_codes_by_sector.xlsx'")

    # 获取所有概念板块
    concept_list = ak.stock_board_concept_name_em()
    concept_stock_count_df = concept_list.sort_values(by='涨跌幅', ascending=False)

    # 输出热门板块（例如股票数量前 10 的板块）
    top_concepts = concept_stock_count_df.head(10)
    # print(top_concepts)
    # 获取每个概念板块的股票
    concept_stock_data = []
    for concept in top_concepts['板块名称']:
        try:
            concept_stocks = ak.stock_board_concept_cons_em(symbol=concept)
            concept_stocks['概念'] = concept
            concept_stock_data.append(concept_stocks)
        except Exception as e:
            print(f"无法获取概念板块 {concept} 的股票信息: {e}")
    # # 合并所有概念股票数据
    all_concept_stocks_df = pd.concat(concept_stock_data)

    # 合并股票代码和概念信息
    merged_df = pd.merge(stock_info_a_code_name_df, all_concept_stocks_df, left_on='code', right_on='代码', how='left')
    # print("merged_df")
    # print(merged_df)

    # 按概念分类存储到Excel
    with pd.ExcelWriter('a_stock_codes_by_concept.xlsx') as writer:
        for concept, group in merged_df.groupby('概念'):
            group[['code', 'name']].to_excel(writer, sheet_name=concept, index=False)

    print("A股股票代码已按概念分类存储到 'a_stock_codes_by_concept.xlsx'")

    # # 获取每只股票的地区信息
    # area_data = []
    # for code in stock_info_a_code_name_df['code']:
    #     try:
    #         stock_info = ak.stock_individual_info_em(symbol=code)
    #         area = stock_info.loc[stock_info['item'] == '公司地域', 'value'].values[0]
    #         area_data.append({'code': code, 'area': area})
    #     except Exception as e:
    #         print(f"无法获取股票 {code} 的地区信息: {e}")

    # # 将地区信息转换为DataFrame
    # area_df = pd.DataFrame(area_data)

    # # 合并股票代码和地区信息
    # merged_df = pd.merge(stock_info_a_code_name_df, area_df, on='code', how='left')

    # # 按地区分类存储到Excel
    # with pd.ExcelWriter('a_stock_codes_by_area.xlsx') as writer:
    #     for area, group in merged_df.groupby('area'):
    #         group[['code', 'name']].to_excel(writer, sheet_name=area, index=False)

    # print("A股股票代码已按地区分类存储到 'a_stock_codes_by_area.xlsx'")

if __name__ == '__main__':
    acquire_stock_data()
