import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA
import os
from datetime import datetime
import sys
def main():
    # 获取年份参数，默认为2023年
    year = 2023
    if len(sys.argv) > 1:
        try:
            year = int(sys.argv[1])
        except ValueError:
            print(f"警告：年份参数 '{sys.argv[1]}' 无效，将使用默认年份2023年")
    
    print(f'正在处理{year}年数据...')
    
    # 用户提供的技术关键词分类
    keyword_categories = {
        '人工智能': ['人工智能', '图像理解', '投资决策系统', '智能数据分析', '智能机器人', 
                   '机器学习', '深度学习', '语义搜索', '语言识别', '身份验证', '自动驾驶',
                   '自然语言处理', '神经网络', '卷积神经'],
        '大数据': ['大数据', '数据挖掘', '文本挖掘', '数据可视化', '异构数据'],
        '云计算': ['云计算', '流计算', '图计算', '内存计算', '安全计算',
                  '类脑计算认知计算', '融合架构', 'EB级存储'],
        '区块链': ['区块链', '分布式记账', '数字货币', '差分隐私技术', '智能金融合约', '加密货币'],
        '数字技术应用': ['增强现实', '混合现实', '虚拟现实', '图像识别', '机器视觉', '雷达点云',
                        '物联网', '信息物理系统', '机器通信', '移动互联网', '人工互联网', '无人工厂',
                        '互联网医疗', '电子商务', '移动支付', '第三方支付', 'NFC支付', '智能能源',
                        'B2B', 'B2C', 'C2B', 'C2C', 'O2O', '智能穿戴', '智慧农业', '智能交通',
                        '智慧医疗', '智慧客服', '智能家居', '智能文旅', '智能环保', '智能电网',
                        '智慧营销', '数字销售', '无人零售', '互联网金融', '数字金融', 'Fintech',
                        '金融科技', '量化金融', '开放银行']
    }
    
    # 读取数据文件
    file_path = f'{year}年年报技术关键词统计.xlsx'
    if not os.path.exists(file_path):
        print(f'错误：文件 {file_path} 不存在')
        return
    
    print(f'正在读取文件：{file_path}')
    df = pd.read_excel(file_path)
    
    # 检查必要的列
    required_columns = ['股票代码', '企业名称', '人工智能', '大数据', '云计算', '区块链', '物联网', '数字技术基础设施', '数字化应用场景']
    for col in required_columns:
        if col not in df.columns:
            print(f'错误：缺少列 {col}')
            return
    
    # 确保股票代码为6位数格式
    df['股票代码'] = df['股票代码'].apply(lambda x: str(x).zfill(6) if isinstance(x, (str, int)) and str(x) != '未知' and len(str(x)) < 6 else x)
    
    # 创建结果表结构
    result_columns = ['股票代码', '股票名称', '人工智能词频数', '大数据词频数', '云计算词频数', '区块链词频数', '数字技术应用词频数', '数字化转型指数']
    result_df = pd.DataFrame(columns=result_columns)
    
    # 填充股票代码和名称
    result_df['股票代码'] = df['股票代码']
    result_df['股票名称'] = df['企业名称']
    
    # 填充一级指标词频数
    result_df['人工智能词频数'] = df['人工智能'].fillna(0).astype(int)
    result_df['大数据词频数'] = df['大数据'].fillna(0).astype(int)
    result_df['云计算词频数'] = df['云计算'].fillna(0).astype(int)
    result_df['区块链词频数'] = df['区块链'].fillna(0).astype(int)
    
    # 数字技术应用 = 物联网 + 数字技术基础设施 + 数字化应用场景
    result_df['数字技术应用词频数'] = (df['物联网'].fillna(0) + df['数字技术基础设施'].fillna(0) + df['数字化应用场景'].fillna(0)).astype(int)
    
    # 计算数字化转型指数（使用PCA方法，与原有代码保持一致）
    # 用于计算的技术指标
    technical_columns = ['人工智能', '大数据', '云计算', '区块链', '物联网', '数字技术基础设施', '数字化应用场景']
    X = df[technical_columns].fillna(0).values
    
    # 数据标准化
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)
    
    # PCA分析
    pca = PCA()
    pca.fit(X_scaled)
    cumulative_variance = np.cumsum(pca.explained_variance_ratio_)
    n_components = np.argmax(cumulative_variance >= 0.85) + 1
    
    pca = PCA(n_components=n_components)
    principal_components = pca.fit_transform(X_scaled)
    weights = np.sum(np.abs(pca.components_), axis=0)
    weights = weights / np.sum(weights)
    
    # 计算指数值
    index_values = np.dot(X_scaled, weights)
    normalized_index = ((index_values - index_values.min()) / (index_values.max() - index_values.min()) * 100).round().astype(int)
    
    result_df['数字化转型指数'] = normalized_index
    
    # 保存结果
    output_file = f'{year}年一级指标词频与数字化转型指数.xlsx'
    with pd.ExcelWriter(output_file, engine='openpyxl') as writer:
        result_df.to_excel(writer, sheet_name='一级指标统计', index=False)
    
    print(f'\n结果已保存到：{output_file}')
    print('表结构：')
    print('股票代码, 股票名称, 人工智能词频数, 大数据词频数, 云计算词频数, 区块链词频数, 数字技术应用词频数, 数字化转型指数')

if __name__ == '__main__':
    main()