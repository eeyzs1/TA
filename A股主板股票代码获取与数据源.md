---
AIGC:
  Label: "1"
  ContentProducer: "001191110108MA01KP2T5U00000"
  ProduceID: "undefined"
  ReservedCode1: "undefined"
  ContentPropagator: "001191110108MA01KP2T5U00000"
  PropagateID: "undefined"
  ReservedCode2: "undefined"
---

# A股主板股票代码获取完全指南

A股主板股票是指在上海证券交易所(上证)和深圳证券交易所(深证)主板市场上市的公司股票，具有较为成熟的公司规模和相对稳定的经营状况。获取这些股票的基础信息是投资研究和量化分析的第一步，本文将系统介绍获取A股主板股票代码的多种方法。

## 一、股票分类与命名规则

在深入获取方法之前，首先需要了解A股股票的分类体系：

### 1.1 A股股票板块分类

| 板块类型 | 代码前缀 | 交易所 | 特点 |
|---------|---------|-------|------|
| 上证主板 | 600、601、603、605 | 上海证券交易所 | 历史较悠久，多为大型企业 |
| 深证主板 | 000、002 | 深圳证券交易所 | 覆盖各行业，以制造业为主 |
| 创业板 | 300 | 深圳证券交易所 | 主要面向成长型创新创业企业 |
| 科创板 | 688 | 上海证券交易所 | 服务科技创新企业 |
| 北交所 | 433、432等 | 北京证券交易所 | 服务中小企业 |

根据([1†])、([11†])和([19†])的资料，这一分类体系是目前A股市场的基本架构。

### 1.2 主板股票识别

主板股票主要包括：
- 上证主板：代码以600、601、603、605开头
- 深证主板：代码以000、002开头

## 二、使用Python获取主板股票代码

### 2.1 Tushare库方法（推荐）

Tushare是国内最常用的金融数据接口库之一，特别适合量化投资和策略研究。

#### 2.1.1 安装与配置

```python
# 基础安装
pip install tushare

# Pro版本配置
import tushare as ts
ts.set_token('your_token_here')  # 需要注册Tushare账号获取token
pro = ts.pro_api()
```

根据([67†])和([76†])的说明，使用Tushare Pro版本功能更全面。

#### 2.1.2 获取主板股票列表

```python
import tushare as ts
import pandas as pd

# 设置API令牌
ts.set_token('your_token_here')
pro = ts.pro_api()

def get_mainboard_stocks():
    """获取所有主板股票列表"""
    # 获取上证主板股票（600、601、603、605开头）
    sha_mainboard = pro.stock_basic(exchange='SSE', market='主板', list_status='L',
                                   fields=['ts_code', 'symbol', 'name', 'area', 'industry', 'list_date'])
    
    # 获取深证主板股票（000、002开头）
    szse_mainboard = pro.stock_basic(exchange='SZSE', market='主板', list_status='L',
                                    fields=['ts_code', 'symbol', 'name', 'area', 'industry', 'list_date'])
    
    # 合并数据
    mainboard_stocks = pd.concat([sha_mainboard, szse_mainboard])
    
    return mainboard_stocks

# 获取并打印结果
mainboard_stocks = get_mainboard_stocks()
print(f"主板股票数量: {len(mainboard_stocks)}")
print(mainboard_stocks.head())
```

根据([29†])和([30†])，stock_basic是获取股票基础信息的核心接口，可以通过exchange和market参数精确筛选主板股票。

#### 2.1.3 数据导出

```python
# 保存为CSV文件
mainboard_stocks.to_csv('mainboard_stocks.csv', index=False, encoding='utf-8-sig')

# 保存为Excel文件
mainboard_stocks.to_excel('mainboard_stocks.xlsx', index=False)
```

([31†])和([37†])提供了将股票数据存储到本地文件的完整示例。

### 2.2 手动构建股票列表

如果无法使用Tushare或需要其他方式，可以手动构建股票列表：

```python
def create_mainboard_list():
    """手动创建主板股票代码列表"""
    # 上证主板范围（可根据需要调整范围）
    sha_codes = [f"600{i:03d}" for i in range(0, 700)] + [f"601{i:03d}" for i in range(0, 1000)] + \
                [f"603{i:03d}" for i in range(0, 1000)] + [f"605{i:03d}" for i in range(0, 200)]
    
    # 深证主板范围（可根据需要调整范围）
    szse_codes = [f"000{i:03d}" for i in range(1, 900)] + [f"002{i:03d}" for i in range(1, 500)]
    
    # 合并并去重
    all_mainboard_symbols = list(set(sha_codes + szse_codes))
    print(f"主板股票代码数量: {len(all_mainboard_symbols)}")
    return all_mainboard_symbols

# 获取股票代码列表
mainboard_symbols = create_mainboard_list()
```

这种方法简单直接，但可能包含已退市股票，需要结合其他数据进行过滤。

### 2.3 使用AkShare库

AkShare是另一个提供免费金融数据的Python库：

```python
import akshare as ak

def get_mainboard_stocks_ak():
    """使用akshare获取主板股票列表"""
    # 获取所有上市公司的基本信息
    stock_info = ak.stock_info_a_code_name()
    
    # 筛选主板股票
    mainboard_stocks = stock_info[stock_info['code'].str.startswith(('600', '601', '603', '605', '000', '002'))]
    
    return mainboard_stocks

# 获取主板股票
mainboard_stocks_ak = get_mainboard_stocks_ak()
print(mainboard_stocks_ak.head())
```

([14†])和([19†])提到AkShare提供了免费的股票数据接口，是Tushare的不错替代。

## 三、通过API接口获取股票数据

### 3.1 新浪财经API

新浪提供的免费股票数据API是获取A股数据的经典方式：

```python
import requests
import json
import pandas as pd
from tqdm import tqdm

def get_sina_stock_data():
    """通过新浪财经API获取所有股票数据"""
    # 获取股票列表
    mainboard_symbols = create_mainboard_list()
    
    # 分批次获取数据（避免请求超时）
    all_data = []
    batch_size = 100  # 每次请求的股票数量
    
    for i in tqdm(range(0, len(mainboard_symbols), batch_size)):
        symbol_batch = mainboard_symbols[i:i+batch_size]
        # 构建请求URL
        symbols_param = ','.join([f"sz{sym}" if sym.startswith(('000', '002')) else f"sh{sym}" for sym in symbol_batch])
        url = f"http://hq.sinajs.cn/list={symbols_param}"
        
        # 发送请求
        response = requests.get(url, timeout=10)
        if response.status_code == 200:
            # 解析数据
            data_list = response.text.split('\n')
            for data in data_list:
                if data.startswith("var"):
                    parts = data.split("=")
                    if len(parts) < 2:
                        continue
                    stock_data = parts[1].strip('";')
                    if stock_data == '':
                        continue
                    values = stock_data.split(",")
                    if len(values) <3:
                        continue
                    stock_info = {
                        'symbol': values[0],
                        'name': values[1],
                        'open': values[2],
                        'high': values[3],
                        'close': values[4],
                        'low': values[5],
                        'price': values[32],
                    }
                    all_data.append(stock_info)
    
    # 转换为DataFrame
    df = pd.DataFrame(all_data)
    return df

# 获取股票数据
sina_stock_data = get_sina_stock_data()
```

([10†])和([20†])详细介绍了新浪财经API的使用方法，这是一种免费且高效的数据获取方式。

### 3.2 其他免费API接口

根据([14†])和([21†])的整理，2025年仍可使用的免费股票API接口包括：

| API提供商 | 接口特点 | 适用场景 |
|----------|---------|---------|
| 麦蕊智数 | 支持沪深A股基础实时数据 | 实时行情获取 |
| 必盈数据 | Get方式请求，标准Json格式 | 简单集成 |
| 天聚数行 | 支持免费试用 | 有额度限制的场景 |
| 咕咕数据 | 支持所有A股实时交易数据 | 全面数据需求 |

## 四、数据准确性验证与处理

### 4.1 数据清洗与去重

获取的股票数据中可能包含重复或已退市的股票，需要进行数据清洗：

```python
def clean_stock_data(df):
    """清理和去重股票数据"""
    # 去重
    df_cleaned = df.drop_duplicates(subset='ts_code', keep='first')
    
    # 过滤无效数据
    df_cleaned = df_cleaned[df_cleaned['name'].notna()]
    
    # 重置索引
    df_cleaned = df_cleaned.reset_index(drop=True)
    
    return df_cleaned

# 清洗数据
cleaned_data = clean_stock_data(mainboard_stocks)
```

### 4.2 验证股票有效性

验证获取的股票代码是否有效：

```python
import requests

def validate_stock_codes(stock_list, batch_size=100):
    """验证股票代码是否有效"""
    valid_stocks = []
    
    for i in range(0, len(stock_list), batch_size):
        symbols_batch = stock_list[i:i+batch_size]
        symbols_param = ','.join([f"sz{sym}" if sym.startswith(('000', '002')) else f"sh{sym}" for sym in symbols_batch])
        
        url = f"http://hq.sinajs.cn/list={symbols_param}"
        response = requests.get(url, timeout=10)
        
        if response.status_code == 200:
            data_list = response.text.split('\n')
            for data in data_list:
                if data.startswith("var") and len(data) > 100:  # 简单判断是否有有效数据
                    symbol = data.split('=')[0].replace('var ', '')
                    valid_stocks.append(symbol[2:])  # 去掉sz/sh前缀
    
    return valid_stocks

# 验证股票代码有效性
valid_mainboard_stocks = validate_stock_codes(mainboard_symbols)
print(f"有效主板股票数量: {len(valid_mainboard_stocks)}")
```

## 五、数据更新与维护

### 5.1 定期更新机制

股票信息会发生变化（如新上市、退市等），需要建立数据更新机制：

```python
import schedule
import time
import datetime

def update_stock_data():
    """更新股票数据"""
    current_date = datetime.datetime.now().strftime("%Y-%m-%d")
    print(f"{current_date}: 开始更新股票数据")
    
    # 获取最新主板股票数据
    latest_data = get_mainboard_stocks()
    
    # 保存到文件
    filename = f"mainboard_stocks_{current_date}.csv"
    latest_data.to_csv(filename, index=False, encoding='utf-8-sig')
    print(f"数据更新完成，已保存至{filename}")

# 设置定时任务
schedule.every().monday.at("09:00").do(update_stock_data)  # 每周一上午9点更新

# 运行调度器
while True:
    schedule.run_pending()
    time.sleep(60)  # 每分钟检查一次
```

### 5.2 自动化数据维护

为避免数据重复和便于管理，可以建立自动化数据维护系统：

```python
import os
import glob

def manage_stock_data(data_directory):
    """管理股票数据文件"""
    # 获取目录下所有CSV文件
    csv_files = glob.glob(os.path.join(data_directory, "mainboard_stocks_*.csv"))
    
    # 按修改时间排序
    csv_files.sort(key=os.path.getmtime)
    
    # 保留最新的5份备份
    if len(csv_files) > 5:
        files_to_delete = csv_files[:-5]
        for f in files_to_delete:
            os.remove(f)
            print(f"已删除过期文件: {f}")
    
    # 检查最新文件是否完整
    if csv_files:
        latest_file = csv_files[-1]
        try:
            df = pd.read_csv(latest_file)
            if len(df) < 1000:  # 简单判断文件是否完整
                print(f"警告：最新文件可能不完整，股票数量: {len(df)}")
        except Exception as e:
            print(f"错误读取最新文件: {e}")
    
    print(f"数据管理完成，保留{min(5, len(csv_files))}个最新备份")

# 管理数据文件
manage_stock_data("./data")
```

## 六、不同方法比较与选择建议

根据([29†])、([19†])和([34†])的资料，我们可以对不同数据获取方法进行系统比较：

| 获取方法 | 优势 | 局限性 | 适用场景 | 成本 |
|---------|------|-------|---------|------|
| Tushare Pro | 数据准确、接口稳定、字段丰富 | 需要积分/付费 | 专业投资研究、量化交易 | 部分接口付费 |
| AkShare | 免费、接口简单 | 数据稳定性不如Tushare | 初级研究、学习 | 完全免费 |
| 新浪财经API | 免费、实时性强 | 需要解析JSON字符串 | 快速获取行情 | 完全免费 |
| 手动构建 | 灵活性高 | 数据准确性难以保证 | 特殊需求场景 | 完全免费 |

对于不同经验水平的用户，推荐选择如下：

- **Python初学者**：AkShare或手动构建列表
- **量化投资新手**：Tushare免费版+AkShare结合使用
- **专业投资者**：Tushare Pro版本

## 七、实践案例：主板股票基本面分析

获取股票代码后，可以进一步获取基本面数据进行分析：

```python
def analyze_mainboard_stocks():
    """分析主板股票基本面情况"""
    # 获取主板股票列表
    mainboard_stocks = get_mainboard_stocks()
    
    # 获取基本面数据（示例：市盈率、市值等）
    basic_data = []
    stock_list = mainboard_stocks['ts_code'].tolist()
    
    for i in range(0, len(stock_list), 100):
        batch = stock_list[i:i+100]
        df = pro.daily(batch)
        basic_data.append(df)
    
    # 合并数据
    all_data = pd.concat(basic_data)
    
    # 计算统计指标
    stats = {
        '股票数量': len(all_data),
        '平均市盈率': all_data['pe'].mean(),
        '平均市净率': all_data['pb'].mean(),
        '平均总市值': all_data['total_share'].mean() * all_data['close'].mean(),
    }
    
    return stats, all_data

# 分析主板股票基本面
stats, data = analyze_mainboard_stocks()
print(stats)
```

([29†])和([34†])提供了使用Tushare进行基本面分析的接口说明。

## 八、常见问题与解决方案

### 8.1 API请求限制

各大数据提供商都有请求频率限制，遇到此问题时：

1. **降低请求频率**：在请求间添加延时
2. **分批处理**：将大量请求分成小批次
3. **使用缓存**：本地存储已获取的数据

```python
import time

def throttled_request(url, params=None, delay=1):
    """带限流的请求函数"""
    response = requests.get(url, params=params)
    time.sleep(delay)  # 添加延迟避免频繁请求
    return response
```

### 8.2 数据格式处理

不同API返回的数据格式可能不同，需要进行格式转换：

```python
def standardize_stock_data(data, source='sina'):
    """统一不同来源股票数据的格式"""
    if source == 'sina':
        # 处理新浪财经数据格式
        pass
    elif source == 'tushare':
        # 处理Tushare数据格式
        pass
    # 添加更多数据源处理...
    
    return standardized_data
```

### 8.3 网络请求失败

网络不稳定可能导致请求失败，需要添加重试机制：

```python
def retry_request(func, *args, max_retries=3, retry_delay=5, **kwargs):
    """带重试功能的请求函数"""
    retries = 0
    while retries < max_retries:
        try:
            return func(*args, **kwargs)
        except Exception as e:
            retries += 1
            print(f"请求失败，重试次数: {retries}/{max_retries}")
            time.sleep(retry_delay)
    
    raise Exception(f"经过{max_retries}次尝试，请求仍失败")
```

## 总结

获取A股主板股票代码是投资研究和量化分析的基础环节。本文介绍了多种获取方法，从简单的代码列表构建到使用专业的数据API接口，能够满足不同用户的需求。在实际应用中，建议：

1. **优先使用Tushare**：数据准确、接口稳定，特别适合量化分析
2. **AkShare作为补充**：提供免费数据，适合预算有限的用户
3. **新浪财经API获取实时数据**：适合需要高频数据的场景
4. **建立数据维护机制**：确保数据的时效性和准确性

通过合理选择和组合这些方法，可以构建一个稳定可靠的A股主板股票数据获取和管理系统，为后续的投资研究和分析工作提供坚实的数据基础。

