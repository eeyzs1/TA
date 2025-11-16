# TA



## 准备/preparation
- 安装/install python3.12
- 切换到这个库的目录/cd to the directory of this repo
- pip install requirements.txt
- pip install ta_lib-0.6.6-cp312-cp312-win_amd64.whl
- 如果使用了其他版本的python，下载对应的talib的轮子/if using other python version, download corresponding talib whl file

## 使用/how to use
- 如果只是想选股，直接执行main.ipynb即可，如果因为没有jupyter的kernel而无法执行，vscode可以考虑安装python插件， 其他编辑器可以考虑以下步骤将文件转化为py执行/If you just want to select stocks, you can directly execute main.ipynb. If you cannot execute it because you do not have a Jupyter kernel, you can consider installing the Python extension in VSCode. For other editors, you can follow the steps below to convert the file to a .py executable file：
    - pip install nbconvert 
    - jupyter nbconvert --to script *.ipynb
    - after convert, you can find main.py file, then run "python main.py" should be fine
- 如果想要增加对talib的理解，可以阅读各个import talib的py文件，z针对每个函数都包含大量注释的为我对talib各个函数含义的解释，如想更进一步理解， 也可以阅读talib的源码，每个函数（XX）都为XX.c格式/If you want to enhance your understanding of talib, you can read the various py files that import talib. Each function contains extensive comments that explain the meaning of each talib function. If you want to further your understanding, you can also read the source code of talib, where each function (XX) is in the XX.c format
- run.py是老版的量化分析代码，不太好用，已弃用/"run.py" is an old version of quantitative analysis code, which is not very useful and has been deprecated
- main_hy_gn.ipynb是尝试用main的量化分析方法，regression.ipynb是用机器学习的方法尝试选出合适的行业或概念，目前看来并不合适，请按照需要修改后再使用...main_hy_gn.ipynb is an attempt to use the quantitative analysis method of main, while regression.ipynb is an attempt to select suitable industries or concepts using machine learning methods. Currently, it seems to be inappropriate. Please modify it as needed before using it...

## python update requirements.txt and update installed package/更新requirements.txt和已安装模块
pipreqsnb ./ --encoding=utf8 --force
pip-review --auto -v 
pip-review --auto -i https://pypi.tuna.tsinghua.edu.cn/simple  
pip-review --local --interactive 


# 股票投资评价体系
 
在股票投资中，一个完善的评价体系对于投资者来说至关重要。以下是一个基于巴菲特投资理念的股票评价体系的示例，它包含了多个关键因子。
 
## 市场因子
 
市场因子主要关注的是大盘的整体表现。当市场整体趋势向上时，个股通常会跟随上涨，为投资者带来收益。因此，在构建投资组合时，需要考虑市场整体趋势对个股价格的影响。
 
## 规模因子
 
规模因子主要考察的是公司的市值大小。研究表明，长期投资小市值公司的收益率往往高于长期投资大市值公司的收益率。这反映了小市值公司在成长潜力和市场表现上可能具有的优势。
 
## 价值因子
 
价值因子是巴菲特投资理念中的核心之一。它主要关注的是股票的估值情况，即交易价格与公允价值之间的关系。巴菲特强调购买具有“安全边际”的股票，即那些交易价格低于公允价值的股票。这可以通过市盈率（PE）、市净率（PB）等指标来衡量。
 
### 估值指标示例
 
- **市盈率（PE）**：衡量公司股价相对于每股收益的倍数。
- **市净率（PB）**：衡量公司股价相对于每股净资产的倍数。
 
## 动量因子
 
动量因子主要考察的是股票价格的短期变动趋势。如果一只股票的价格在近期内持续上涨，那么它可能会继续上涨；反之，如果价格下跌，则可能会继续下跌。这种趋势策略在巴菲特的投资实践中也得到了应用。
 
## 质量因子
 
质量因子主要关注的是公司的基本面情况，包括ROE（净资产收益率）、ROA（总资产收益率）、现金流、周转率、利润增长率、资产负债率等财务指标。这些指标能够反映公司的盈利能力和运营效率，是巴菲特选择优秀公司的重要依据。
 
### 关键财务指标示例
 
- **ROE（净资产收益率）**：衡量公司运用自有资本的效率。ROE衡量的是公司运用自有资本（即股东权益）的效率，反映了公司对股东投资的回报能力。计算公式为：ROE = 净利润 / 平均股东权益
- **ROA（总资产收益率）**：衡量公司运用全部资产的效率。ROA衡量的是公司运用全部资产（包括股东权益和负债）的效率，反映了公司整体资产的盈利能力。计算公式为：ROA = 净利润 / 平均总资产
- **现金流**：反映公司的现金流入和流出情况，是评估公司偿债能力的重要指标。
 
## 资金因子
 
资金因子主要考察的是投资者的资金来源和杠杆使用情况。巴菲特通过保险公司获得了源源不断的廉价资金，并给自己的投资加上了杠杆，从而提高了投资收益率。这种独特的商业模式和资金来源也是巴菲特成功的重要因素之一。
 


