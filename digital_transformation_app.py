import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os
import numpy as np
import folium
from streamlit_folium import folium_static
import plotly.express as px
import io

# 设置页面配置
st.set_page_config(
    page_title="数字化转型指数分析平台",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# 设置中文字体
plt.rcParams['font.sans-serif'] = ['SimHei']  # 用来正常显示中文标签
plt.rcParams['axes.unicode_minus'] = False  # 用来正常显示负号

# 主题切换功能
if 'theme' not in st.session_state:
    st.session_state.theme = 'dark'  # 默认暗色主题

# 定义主题样式
# 删除浅色主题

dark_theme_css = """
<style>
    /* 粉色标题样式 */
    .pink-title {
        color: #FF1493 !important;
    }
    
    .stApp {
        background-color: #1e1e1e;
        color: #ffffff;
    }
    .stSidebar {
        background-color: #2d2d2d;
    }
    .stMarkdown {
        color: #ffffff;
    }
    .stMetric {
        background-color: #3d3d3d;
        color: #ffffff;
    }
    .stDataFrame, .stTable {
        background-color: #2d2d2d;
        color: #ffffff;
    }
    .stDataFrame th,
    .stTable th {
        background-color: #3d3d3d;
        color: #ffffff;
    }
    .stDataFrame td,
    .stTable td {
        background-color: #2d2d2d;
        color: #ffffff;
    }
    /* 添加更多组件的样式 */
    .stButton > button {
        color: #ffffff;
        background-color: #3d3d3d;
    }
    .stTextInput > div > div > input {
        color: #ffffff;
        background-color: #3d3d3d;
    }
    .stSelectbox > div > div > select {
        color: #ffffff;
        background-color: #3d3d3d;
    }
    .stCheckbox > div > label {
        color: #ffffff;
    }
    .stRadio > div > label {
        color: #ffffff;
    }
    .stSlider > div > div > div > div {
        color: #ffffff;
    }
    .stNumberInput > div > div > input {
        color: #ffffff;
        background-color: #3d3d3d;
    }
    .stDateInput > div > div > input {
        color: #ffffff;
        background-color: #3d3d3d;
    }
    .stTimeInput > div > div > input {
        color: #ffffff;
        background-color: #3d3d3d;
    }
    .stFileUploader > div > label {
        color: #ffffff;
    }
    .stTextArea > div > div > textarea {
        color: #ffffff;
        background-color: #3d3d3d;
    }
    .stCaption {
        color: #cccccc;
    }
    .stExpander > div > div > button {
        color: #ffffff;
    }
    /* 确保所有文本都可见 */
    * {
        color: #ffffff !important;
    }
</style>
"""

# 添加粉色主题
pink_theme_css = """
<style>
    /* 粉色标题样式 */
    .pink-title {
        color: #FF1493 !important;
    }
    
    .stApp {
        background-color: #fff0f5;
        color: #8b4513;
    }
    .stSidebar {
        background-color: #ffb6c1;
        color: #8b4513;
    }
    .stMarkdown {
        color: #8b4513;
    }
    .stMetric {
        background-color: #fff0f5;
        color: #8b4513;
    }
    .stDataFrame, .stTable {
        background-color: #ffffff;
        color: #8b4513;
    }
    .stDataFrame th,
    .stTable th {
        background-color: #ffb6c1;
        color: #8b4513;
    }
    .stDataFrame td,
    .stTable td {
        background-color: #ffffff;
        color: #8b4513;
    }
    /* 添加标题颜色设置 */
    h1, h2, h3, h4, h5, h6 {
        color: #8b4513 !important;
    }
</style>
"""

# 应用主题样式
if st.session_state.theme == 'dark':
    st.markdown(dark_theme_css, unsafe_allow_html=True)
else:  # pink theme
    st.markdown(pink_theme_css, unsafe_allow_html=True)

# 页面标题和主题切换
col1, col2 = st.columns([3, 1])
with col1:
    st.title("📊 数字化转型指数分析平台")
with col2:
    # 主题切换按钮
    if st.session_state.theme == 'dark':
        next_theme = "🌸 切换至粉色模式"
    else:  # pink theme
        next_theme = "🌙 切换至暗色模式"
    
    theme_button = st.button(next_theme, key="theme_switch")
    if theme_button:
        if st.session_state.theme == 'dark':
            st.session_state.theme = 'pink'
        else:  # pink theme
            st.session_state.theme = 'dark'
        # 刷新页面以应用新主题
        st.rerun()

# 构建文件路径
# 使用os.path.abspath和相对路径确保文件路径的正确性
file_path = os.path.abspath('1999-2023年数字化转型指数与行业合并表.xlsx')

# 添加调试信息
st.write(f"当前工作目录: {os.getcwd()}")
st.write(f"文件路径: {file_path}")
st.write(f"文件是否存在: {os.path.exists(file_path)}")

# 数据加载函数
@st.cache_data

def load_data():
    if os.path.exists(file_path):
        df = pd.read_excel(file_path)
        return df
    else:
        st.error("数据文件不存在，请检查文件路径是否正确")
        return None

# 加载数据
df = load_data()

# 中国省份、城市和简称映射
provinces_cities_mapping = {
    # 省份和直辖市
    '北京': '北京', '上海': '上海', '广东': '广东', '江苏': '江苏', '浙江': '浙江', '山东': '山东', 
    '福建': '福建', '河南': '河南', '湖北': '湖北', '湖南': '湖南', '四川': '四川', '河北': '河北', 
    '安徽': '安徽', '江西': '江西', '辽宁': '辽宁', '陕西': '陕西', '山西': '山西', '黑龙江': '黑龙江', 
    '吉林': '吉林', '云南': '云南', '贵州': '贵州', '广西': '广西', '天津': '天津', '重庆': '重庆', 
    '内蒙古': '内蒙古', '新疆': '新疆', '甘肃': '甘肃', '宁夏': '宁夏', '青海': '青海', '西藏': '西藏', 
    '海南': '海南', '香港': '香港', '澳门': '澳门', '台湾': '台湾',
    # 主要城市
    '深圳': '广东', '广州': '广东', '杭州': '浙江', '南京': '江苏', '青岛': '山东', '济南': '山东',
    '苏州': '江苏', '宁波': '浙江', '厦门': '福建', '福州': '福建', '成都': '四川', '武汉': '湖北',
    '长沙': '湖南', '西安': '陕西', '郑州': '河南', '沈阳': '辽宁', '大连': '辽宁', '长春': '吉林',
    '哈尔滨': '黑龙江', '合肥': '安徽', '南昌': '江西', '石家庄': '河北', '太原': '山西', '昆明': '云南',
    '贵阳': '贵州', '南宁': '广西', '乌鲁木齐': '新疆', '兰州': '甘肃', '银川': '宁夏', '西宁': '青海',
    '拉萨': '西藏', '海口': '海南', '三亚': '海南',
    # 新增城市（根据数据分析结果）
    '东莞': '广东', '佛山': '广东', '惠州': '广东', '中山': '广东', '珠海': '广东',
    '无锡': '江苏', '徐州': '江苏', '常州': '江苏', '南通': '江苏', '连云港': '江苏',
    '温州': '浙江', '绍兴': '浙江', '嘉兴': '浙江', '金华': '浙江', '台州': '浙江', '湖州': '浙江',
    '泉州': '福建', '漳州': '福建', '莆田': '福建', '宁德': '福建', '龙岩': '福建',
    '烟台': '山东', '潍坊': '山东', '淄博': '山东', '济宁': '山东', '泰安': '山东', '临沂': '山东',
    '岳阳': '湖南', '衡阳': '湖南', '株洲': '湖南', '湘潭': '湖南', '常德': '湖南',
    '沧州': '河北', '唐山': '河北', '保定': '河北', '廊坊': '河北', '承德': '河北',
    '大同': '山西', '阳泉': '山西', '长治': '山西', '晋城': '山西', '临汾': '山西',
    '乐山': '四川', '泸州': '四川', '德阳': '四川', '绵阳': '四川', '宜宾': '四川', '广安': '四川', '眉山': '四川',
    '襄阳': '湖北', '宜昌': '湖北', '荆州': '湖北', '黄冈': '湖北',
    '九江': '江西', '赣州': '江西', '上饶': '江西', '宜春': '江西',
    '包头': '内蒙古', '呼和浩特': '内蒙古',
    '洛阳': '河南', '开封': '河南', '新乡': '河南', '安阳': '河南',
    '锦州': '辽宁', '营口': '辽宁',
    '遵义': '贵州', '六盘水': '贵州',
    '柳州': '广西', '桂林': '广西',
    '曲靖': '云南', '玉溪': '云南',
    '咸阳': '陕西', '宝鸡': '陕西',
    '芜湖': '安徽', '马鞍山': '安徽',
    '大庆': '黑龙江', '齐齐哈尔': '黑龙江',
    '吉林': '吉林', '四平': '吉林'
}

# 从企业名称中提取省份信息
def extract_province(company_name):
    for city_province in provinces_cities_mapping:
        if city_province in company_name:
            return provinces_cities_mapping[city_province]
    # 如果无法提取省份信息，返回默认省份
    return '全国'

if df is not None:
    # 从企业名称中提取省份信息
    df['省份'] = df['企业名称'].apply(extract_province)
    
    # 侧边栏
    st.sidebar.header("🔍 数据筛选")
    
    # 年份选择器
    years = sorted(df['年份'].unique())
    selected_years = st.sidebar.multiselect(
        "选择年份",
        years,
        default=years[-5:],
        help="默认只显示最近5年数据，如需查询更早数据，请手动选择年份"
    )
    
    # 行业选择器
    industries = sorted(df['行业名称'].dropna().unique())
    selected_industries = st.sidebar.multiselect(
        "选择行业",
        industries,
        default=None
    )
    
    # 股票代码查询
    stock_codes = st.sidebar.text_input(
        "输入股票代码（多个代码用逗号分隔）",
        help="例如：600008,600223,600225"
    )
    
    # 企业名称查询
    company_names = st.sidebar.text_input(
        "输入企业名称（多个名称用逗号分隔）",
        help="支持模糊匹配，例如：首创,万杰,天香"
    )
    
    # 数据筛选 - 优化逻辑：如果有股票代码或企业名称输入但没有选择年份，则显示所有年份数据
    if not selected_years and (stock_codes or company_names):
        # 如果用户没有选择年份，但输入了股票代码或企业名称，显示所有年份数据
        filtered_df = df.copy()
    else:
        # 否则使用选择的年份筛选
        filtered_df = df[df['年份'].isin(selected_years)]
    
    if selected_industries:
        filtered_df = filtered_df[filtered_df['行业名称'].isin(selected_industries)]
    
    # 股票代码筛选
    if stock_codes:
        # 处理用户输入的股票代码，支持逗号分隔
        stock_code_list = [code.strip() for code in stock_codes.split(',') if code.strip()]
        # 筛选包含输入股票代码的行
        filtered_df = filtered_df[filtered_df['股票代码'].astype(str).isin(stock_code_list)]
    
    # 企业名称筛选
    if company_names:
        # 处理用户输入的企业名称，支持逗号分隔
        company_name_list = [name.strip() for name in company_names.split(',') if name.strip()]
        # 创建筛选条件
        filter_condition = pd.Series([False]*len(filtered_df), index=filtered_df.index)
        
        # 对每个输入的企业名称进行模糊匹配
        for name in company_name_list:
            if name:
                filter_condition = filter_condition | filtered_df['企业名称'].str.contains(name, case=False, na=False)
        
        # 应用筛选条件
        filtered_df = filtered_df[filter_condition]
    
    # 主内容区
    # 无数据提示
    if len(filtered_df) == 0:
        st.warning("⚠️  没有找到匹配的数据")
        
        # 分析可能的原因
        reasons = []
        if stock_codes:
            stock_code_list = [code.strip() for code in stock_codes.split(',') if code.strip()]
            # 检查股票代码是否在数据库中存在
            all_years_data = df[df['股票代码'].astype(str).isin(stock_code_list)]
            if len(all_years_data) > 0:
                # 检查是否是年份筛选的问题
                available_years = sorted(all_years_data['年份'].unique())
                reasons.append(f"输入的股票代码在所选年份范围内没有数据。该股票代码的可用年份为: {available_years}")
                reasons.append(f"建议尝试手动选择其他年份来查看数据")
            else:
                reasons.append("输入的股票代码在数据库中不存在")
                reasons.append("请检查股票代码是否正确")
        
        if company_names:
            company_name_list = [name.strip() for name in company_names.split(',') if name.strip()]
            # 检查企业名称是否在数据库中存在
            filter_condition = pd.Series([False]*len(df), index=df.index)
            for name in company_name_list:
                filter_condition |= df['企业名称'].str.contains(name, na=False)
            all_years_data = df[filter_condition]
            
            if len(all_years_data) > 0:
                # 检查是否是年份筛选的问题
                available_years = sorted(all_years_data['年份'].unique())
                reasons.append(f"输入的企业名称在所选年份范围内没有数据。该企业的可用年份为: {available_years}")
                reasons.append(f"建议尝试手动选择其他年份来查看数据")
            else:
                reasons.append("输入的企业名称在数据库中不存在或匹配度太低")
                reasons.append("请尝试使用更精确的企业名称或不同的关键词")
        
        if not stock_codes and not company_names:
            reasons.append("当前的筛选条件（年份、行业等）可能过于严格")
            reasons.append("建议尝试放宽筛选条件")
        
        # 显示可能的解决方法
        if reasons:
            st.info("### 可能的解决方法:")
            for i, reason in enumerate(reasons, 1):
                st.write(f"{i}. {reason}")
    
    # 调试信息（可选显示）
    if st.checkbox("显示调试信息"):
        st.subheader("调试信息")
        st.write(f"原始数据总行数: {len(df)}")
        st.write(f"筛选后数据行数: {len(filtered_df)}")
        st.write(f"当前选择的年份: {selected_years}")
        
        if stock_codes:
            stock_code_list = [code.strip() for code in stock_codes.split(',') if code.strip()]
            st.write(f"输入的股票代码: {stock_code_list}")
            st.write(f"匹配到的股票代码: {list(filtered_df['股票代码'].unique())}")
            
            # 检查股票代码在所有年份的数据情况
            all_years_data = df[df['股票代码'].astype(str).isin(stock_code_list)]
            if len(all_years_data) > 0:
                available_years = sorted(all_years_data['年份'].unique())
                st.write(f"股票代码在数据库中的可用年份: {available_years}")
                st.write(f"所选年份范围内的数据行数: {len(filtered_df)}")
        
        if company_names:
            company_name_list = [name.strip() for name in company_names.split(',') if name.strip()]
            st.write(f"输入的企业名称: {company_name_list}")
            st.write(f"匹配到的企业名称: {list(filtered_df['企业名称'].unique())}")
            
            # 检查企业名称在所有年份的数据情况
            filter_condition = pd.Series([False]*len(df), index=df.index)
            for name in company_name_list:
                filter_condition |= df['企业名称'].str.contains(name, na=False)
            all_years_data = df[filter_condition]
            if len(all_years_data) > 0:
                available_years = sorted(all_years_data['年份'].unique())
                st.write(f"企业名称在数据库中的可用年份: {available_years}")
                st.write(f"所选年份范围内的数据行数: {len(filtered_df)}")
        
        # 显示部分数据示例
        if len(filtered_df) > 0:
            st.subheader("数据示例")
            st.dataframe(filtered_df[['股票代码', '企业名称', '年份', '行业名称', '数字化转型指数(0-100分)']].head(10))
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("📈 总记录数", f"{len(filtered_df):,}")
    
    with col2:
        avg_index = round(filtered_df['数字化转型指数(0-100分)'].mean(), 2)
        st.metric("📊 平均指数", avg_index)
    
    with col3:
        max_index = filtered_df['数字化转型指数(0-100分)'].max()
        st.metric("🏆 最高指数", max_index)
    
    with col4:
        unique_companies = filtered_df['企业名称'].nunique()
        st.metric("🏢 企业数量", unique_companies)
    
    # 数据概览
    st.markdown("<h2 class='pink-title'>📋 数据概览</h2>", unsafe_allow_html=True)
    # 显示表格数据
    if len(filtered_df) > 0:
        st.dataframe(filtered_df, use_container_width=True)
    else:
        st.info("没有找到符合条件的数据")
    
    # 2. 行业分布分析
    st.subheader("2. 行业分布分析")
    if len(filtered_df) > 0:
        industry_comparison = filtered_df.groupby('行业名称')['数字化转型指数(0-100分)'].mean().reset_index()
        industry_comparison = industry_comparison.sort_values('数字化转型指数(0-100分)', ascending=False).head(20)
        
        fig, ax = plt.subplots(figsize=(12, 8))
        sns.barplot(x='数字化转型指数(0-100分)', y='行业名称', data=industry_comparison, ax=ax)
        ax.set_title('各行业平均数字化转型指数（前20名）', fontsize=16)
        ax.set_xlabel('平均数字化转型指数', fontsize=12)
        ax.set_ylabel('行业名称', fontsize=12)
        st.pyplot(fig)
        
        # 添加图表导出功能
        buf = io.BytesIO()
        fig.savefig(buf, format="png", dpi=300, bbox_inches='tight')
        buf.seek(0)
        st.download_button(
            label="💾 下载行业对比图",
            data=buf,
            file_name="行业对比图.png",
            mime="image/png"
        )
        
        # 3. 数字技术维度分析
        st.subheader("3. 数字技术维度分析")
        tech_dimensions = ['人工智能', '大数据', '云计算', '物联网', '区块链']
        tech_avg = filtered_df[tech_dimensions].mean().reset_index()
        tech_avg.columns = ['技术维度', '平均得分']
    
        # 条形图展示
        fig, ax = plt.subplots(figsize=(10, 6))
        sns.barplot(x='技术维度', y='平均得分', data=tech_avg, ax=ax, palette='viridis')
        ax.set_title('各数字技术维度平均得分', fontsize=16)
        ax.set_xlabel('技术维度', fontsize=12)
        ax.set_ylabel('平均得分', fontsize=12)
        st.pyplot(fig)
        
        # 添加图表导出功能
        buf = io.BytesIO()
        fig.savefig(buf, format="png", dpi=300, bbox_inches='tight')
        buf.seek(0)
        st.download_button(
            label="💾 下载技术维度条形图",
            data=buf,
            file_name="技术维度条形图.png",
            mime="image/png"
        )
        
        # 添加雷达图展示
        st.markdown("<h3 class='pink-title'>3.1 技术维度雷达图分析</h3>", unsafe_allow_html=True)
        
        # 准备雷达图数据
        tech_dimensions = ['人工智能', '大数据', '云计算', '物联网', '区块链']
        values = filtered_df[tech_dimensions].mean().values
        
        # 计算角度
        angles = np.linspace(0, 2 * np.pi, len(tech_dimensions), endpoint=False).tolist()
        # 闭合雷达图
        values = np.concatenate((values, [values[0]]))
        angles = np.concatenate((angles, [angles[0]]))
        
        # 创建雷达图
        fig, ax = plt.subplots(figsize=(8, 8), subplot_kw=dict(polar=True))
        ax.plot(angles, values, linewidth=2, linestyle='solid', label='平均得分')
        ax.fill(angles, values, alpha=0.25)
        
        # 设置标签
        ax.set_xticks(angles[:-1])
        ax.set_xticklabels(tech_dimensions)
        ax.set_yticklabels([])
        ax.set_title('技术维度雷达图', fontsize=16)
        ax.legend(loc='upper right')
        
        st.pyplot(fig)
        
        # 添加图表导出功能
        buf = io.BytesIO()
        fig.savefig(buf, format="png", dpi=300, bbox_inches='tight')
        buf.seek(0)
        st.download_button(
            label="💾 下载技术维度雷达图",
            data=buf,
            file_name="技术维度雷达图.png",
            mime="image/png"
        )
        
        # 如果选择了多个年份，添加对比雷达图
        if len(selected_years) > 1:
            st.markdown("<h3 class='pink-title'>3.2 不同年份技术维度对比</h3>", unsafe_allow_html=True)
            
            # 准备雷达图数据
            fig, ax = plt.subplots(figsize=(8, 8), subplot_kw=dict(polar=True))
            
            # 为每个年份绘制雷达图
            for year in selected_years:
                year_data = filtered_df[filtered_df['年份'] == year]
                year_values = year_data[tech_dimensions].mean().values
                # 闭合雷达图
                year_values = np.concatenate((year_values, [year_values[0]]))
                ax.plot(angles, year_values, linewidth=2, linestyle='solid', label=str(year))
                ax.fill(angles, year_values, alpha=0.1)
            
            # 设置标签
            ax.set_xticks(angles[:-1])
            ax.set_xticklabels(tech_dimensions)
            ax.set_yticklabels([])
            ax.set_title('不同年份技术维度对比雷达图', fontsize=16)
            ax.legend(loc='upper right')
            
            st.pyplot(fig)
            
            # 添加图表导出功能
            buf = io.BytesIO()
            fig.savefig(buf, format="png", dpi=300, bbox_inches='tight')
            buf.seek(0)
            st.download_button(
                label="💾 下载年份对比雷达图",
                data=buf,
                file_name="年份对比雷达图.png",
                mime="image/png"
            )
        
        # 5. 企业排名
        st.markdown("<h3 class='pink-title'>5. 企业排名</h3>", unsafe_allow_html=True)
        if len(filtered_df) > 0:
            top_10 = filtered_df.nlargest(10, '数字化转型指数(0-100分)')[['企业名称', '年份', '行业名称', '数字化转型指数(0-100分)']]
            st.dataframe(top_10, use_container_width=True)
        
        # 6. 相关性分析
        st.subheader("6. 相关性分析")
        corr_columns = ['数字化转型指数(0-100分)', '人工智能', '大数据', '云计算', '物联网', '区块链', '总词频数']
        corr_matrix = filtered_df[corr_columns].corr()
        
        fig, ax = plt.subplots(figsize=(10, 8))
        sns.heatmap(corr_matrix, annot=True, cmap='coolwarm', linewidths=0.5, ax=ax)
        ax.set_title('各维度相关性热力图', fontsize=16)
        st.pyplot(fig)
        
        # 添加图表导出功能
        buf = io.BytesIO()
        fig.savefig(buf, format="png", dpi=300, bbox_inches='tight')
        buf.seek(0)
        st.download_button(
            label="💾 下载相关性热力图",
            data=buf,
            file_name="相关性热力图.png",
            mime="image/png"
        )
        
        # 7. 地理分布分析
        st.header("🌍 地理分布分析")
        
        # 中国所有省份列表
        all_provinces = ['北京', '上海', '广东', '江苏', '浙江', '山东', '福建', '河南', '湖北', '湖南', 
                         '四川', '河北', '安徽', '江西', '辽宁', '陕西', '山西', '黑龙江', '吉林', '云南', 
                         '贵州', '广西', '天津', '重庆', '内蒙古', '新疆', '甘肃', '宁夏', '青海', '西藏', '海南']
        
        # 计算各省份的平均数字化转型指数
        province_data = filtered_df.groupby('省份')['数字化转型指数(0-100分)'].agg(['mean', 'count']).reset_index()
        province_data.columns = ['省份', '平均数字化转型指数', '企业数量']
        
        # 将'全国'类别的数据排除（如果存在）
        if not province_data.empty and '全国' in province_data['省份'].values:
            province_data = province_data[province_data['省份'] != '全国']
        
        # 创建所有省份的数据框，确保每个省份都有数据
        all_province_data = pd.DataFrame({'省份': all_provinces})
        province_data = pd.merge(all_province_data, province_data, on='省份', how='left')
        
        # 填充缺失值
        province_data['平均数字化转型指数'] = province_data['平均数字化转型指数'].fillna(0)
        province_data['企业数量'] = province_data['企业数量'].fillna(0)
        
        # 转换企业数量为整数类型
        province_data['企业数量'] = province_data['企业数量'].astype(int)
        
        # 添加中国地图可视化
        st.subheader("7. 地理分布地图")
        
        # 创建中国地图
        try:
            import folium
            from streamlit_folium import folium_static
            import ssl
            import urllib.request
            
            # 创建地图对象，中心设为中国
            m = folium.Map(location=[35.8617, 104.1954], zoom_start=4, tiles='CartoDB positron')
            
            # 添加中国省份边界GeoJSON
            # 注意：这里使用了公开的中国省份GeoJSON数据URL
            geojson_url = 'https://geo.datav.aliyun.com/areas_v3/bound/100000_full.json'
            
            # 备选GeoJSON数据源
            backup_geojson_url = 'https://raw.githubusercontent.com/echarts-maps/echarts-china-counties-js/master/echarts-china-provinces-js/china.js'
            
            # 禁用SSL验证（解决自签名证书问题）
            context = ssl.create_default_context()
            context.check_hostname = False
            context.verify_mode = ssl.CERT_NONE
            
            # 将省份数据转换为字典，便于地图着色
            province_index_dict = province_data.set_index('省份')['平均数字化转型指数'].to_dict()
            province_company_dict = province_data.set_index('省份')['企业数量'].to_dict()
            
            try:
                # 使用urllib下载GeoJSON数据并禁用SSL验证
                with urllib.request.urlopen(geojson_url, context=context) as response:
                    geojson_data = response.read().decode('utf-8')
                    
                # 添加GeoJSON层
                folium.Choropleth(
                    geo_data=geojson_data,
                    name='choropleth',
                    data=province_data,
                    columns=['省份', '平均数字化转型指数'],
                    key_on='feature.properties.name',
                    fill_color='YlOrRd',
                    fill_opacity=0.7,
                    line_opacity=0.2,
                    legend_name='平均数字化转型指数(0-100分)',
                    highlight=True,
                    smooth_factor=0
                ).add_to(m)
                
                # 添加省份边界
                folium.GeoJson(
                    geojson_data,
                    name='省份边界',
                    style_function=lambda feature: {
                        'fillColor': '#ffffff',
                        'color': '#000000',
                        'weight': 0.5,
                        'fillOpacity': 0
                    },
                    tooltip=folium.GeoJsonTooltip(
                        fields=['name'],
                        aliases=['省份:'],
                        style=('background-color: white; color: #333333; font-family: arial; font-size: 12px; padding: 10px;')
                    )
                ).add_to(m)
            except Exception as e:
                st.write(f"使用主数据源失败：{e}")
                st.write("尝试使用备用数据源...")
                
                # 尝试使用备用数据源
                try:
                    with urllib.request.urlopen(backup_geojson_url, context=context) as response:
                        geojson_data = response.read().decode('utf-8')
                        
                    # 处理备用数据源的格式差异
                    # 注意：备用数据源可能需要不同的key_on参数
                    folium.Choropleth(
                        geo_data=geojson_data,
                        name='choropleth',
                        data=province_data,
                        columns=['省份', '平均数字化转型指数'],
                        key_on='feature.properties.name',
                        fill_color='YlOrRd',
                        fill_opacity=0.7,
                        line_opacity=0.2,
                        legend_name='平均数字化转型指数(0-100分)',
                        highlight=True,
                        smooth_factor=0
                    ).add_to(m)
                    
                    folium.GeoJson(
                        geojson_data,
                        name='省份边界',
                        style_function=lambda feature: {
                            'fillColor': '#ffffff',
                            'color': '#000000',
                            'weight': 0.5,
                            'fillOpacity': 0
                        },
                        tooltip=folium.GeoJsonTooltip(
                            fields=['name'],
                            aliases=['省份:'],
                            style=('background-color: white; color: #333333; font-family: arial; font-size: 12px; padding: 10px;')
                        )
                    ).add_to(m)
                except Exception as e2:
                    st.write(f"使用备用数据源也失败：{e2}")
                    st.write("将只显示标记点，不显示省份边界")
            
            # 添加交互式标记
            for _, row in province_data.iterrows():
                # 获取省份的中心坐标（简化处理，实际应用中可以使用更准确的坐标数据）
                # 这里使用一个简单的省份中心坐标映射，实际应用中可以替换为更准确的数据
                province_coords = {
                    '北京': [39.9042, 116.4074],
                    '上海': [31.2304, 121.4737],
                    '广东': [23.1291, 113.2644],
                    '江苏': [32.0603, 118.7969],
                    '浙江': [30.2741, 120.1551],
                    '山东': [36.6512, 117.1201],
                    '福建': [26.0745, 119.2965],
                    '河南': [34.7466, 113.6254],
                    '湖北': [30.5928, 114.3055],
                    '湖南': [28.2278, 112.9388],
                    '四川': [30.5728, 104.0668],
                    '河北': [38.0428, 114.5149],
                    '安徽': [31.8206, 117.2272],
                    '江西': [28.6826, 115.8581],
                    '辽宁': [41.8056, 123.4315],
                    '陕西': [34.3416, 108.9398],
                    '山西': [37.8706, 112.5489],
                    '黑龙江': [45.8038, 126.5349],
                    '吉林': [43.8170, 125.3245],
                    '云南': [25.0453, 102.7126],
                    '贵州': [26.5783, 106.7078],
                    '广西': [22.8170, 108.3668],
                    '天津': [39.3434, 117.3616],
                    '重庆': [29.4316, 106.9123],
                    '内蒙古': [40.8183, 111.6708],
                    '新疆': [43.7928, 87.6271],
                    '甘肃': [36.0611, 103.8343],
                    '宁夏': [38.4680, 106.2319],
                    '青海': [36.6172, 101.7782],
                    '西藏': [29.6469, 91.1175],
                    '海南': [20.0440, 110.3496],
                    '香港': [22.3193, 114.1694],
                    '澳门': [22.1987, 113.5493],
                    '台湾': [23.6978, 120.9605],
                    '全国': [35.8617, 104.1954]  # 默认位置
                }
                
                # 获取省份坐标，如果没有则使用默认坐标
                coords = province_coords.get(row['省份'], [35.8617, 104.1954])
                
                # 添加标记
                folium.Marker(
                    location=coords,
                    tooltip=f"{row['省份']}<br>平均指数: {row['平均数字化转型指数']:.1f}<br>企业数量: {row['企业数量']}",
                    popup=folium.Popup(
                        f"<strong>{row['省份']}</strong><br>" +
                        f"平均数字化转型指数: {row['平均数字化转型指数']:.1f}<br>" +
                        f"企业数量: {row['企业数量']}",
                        max_width=300
                    ),
                    icon=folium.Icon(color='blue' if row['平均数字化转型指数'] < 50 else 'red', prefix='fa', icon='building')
                ).add_to(m)
            
            # 添加图层控制器
            folium.LayerControl().add_to(m)
            
            # 在Streamlit中显示地图
            folium_static(m, width=1000, height=600)
            
        except Exception as e:
            st.write(f"地图生成错误：{e}")
            st.write("如果地图无法显示，可能是由于网络连接问题或GeoJSON数据访问限制。")
        
        # 使用matplotlib绘制条形图
        fig, ax = plt.subplots(figsize=(12, 8))
        
        # 按平均数字化转型指数降序排序
        sorted_province_data = province_data.sort_values('平均数字化转型指数', ascending=True)
        
        # 绘制条形图
        bars = ax.barh(sorted_province_data['省份'], sorted_province_data['平均数字化转型指数'], 
                       color=plt.cm.RdBu_r(sorted_province_data['平均数字化转型指数']/100))
        
        # 添加数值标签
        for bar in bars:
            width = bar.get_width()
            ax.text(width + 1, bar.get_y() + bar.get_height()/2, 
                    f'{width:.1f}', ha='left', va='center', fontsize=10)
        
        # 设置图表属性
        ax.set_title('各省份平均数字化转型指数分布', fontsize=16)
        ax.set_xlabel('平均数字化转型指数(0-100分)', fontsize=12)
        ax.set_xlim(0, 100)
        ax.grid(True, alpha=0.3, axis='x')
        
        # 调整布局
        plt.tight_layout()
        
        # 显示图表
        st.pyplot(fig)
        
        # 可选：显示Plotly版本的图表（如果用户需要）
        if st.checkbox("显示Plotly版本图表（可选）"):
            try:
                fig = px.bar(
                    province_data.sort_values('平均数字化转型指数', ascending=False),
                    x="省份",
                    y="平均数字化转型指数",
                    color="平均数字化转型指数",
                    color_continuous_scale="RdBu_r",
                    range_color=(0, 100),
                    labels={"平均数字化转型指数": "平均数字化转型指数(0-100分)", "省份": "省份"},
                    hover_data=["企业数量"],
                    title="各省份平均数字化转型指数分布"
                )
                
                fig.update_layout(
                    height=600,
                    xaxis_tickangle=-45,
                    margin={"r":0,"t":50,"l":0,"b":100}
                )
                
                st.plotly_chart(fig, use_container_width=True)
            except Exception as e:
                st.write(f"Plotly图表生成错误：{e}")
        
        # 显示各省份详细数据
        st.markdown("<h3 class='pink-title'>各省份数字化转型指数详细数据</h3>", unsafe_allow_html=True)
        st.dataframe(province_data.sort_values('平均数字化转型指数', ascending=False), use_container_width=True)

    else:
        st.warning("无法加载数据，请检查文件路径是否正确")

    # 页脚
    st.markdown(
        "<div style='text-align: center; margin-top: 50px; padding: 10px; color: #888;'>© 2024 数字化转型指数分析平台</div>",
        unsafe_allow_html=True
    )