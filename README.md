# 数字化转型指数分析平台

一个基于Streamlit的数字化转型指数分析平台，用于分析和可视化企业数字化转型数据。

## 项目结构

```
/数字化转型指数分析平台
├── digital_transformation_app.py          # 主应用程序文件
├── classify_tech_keywords.py               # 技术关键词分类模块
├── requirements.txt                        # 项目依赖
├── README.md                               # 项目说明文档
└── 1999-2023年数字化转型指数与行业合并表.xlsx  # 主要数据文件
```

## 需要上传到GitHub的文件

以下是需要上传到GitHub的所有文件：

1. **应用程序文件**
   - `digital_transformation_app.py` - 主Streamlit应用程序，包含所有UI和功能逻辑
   - `classify_tech_keywords.py` - 技术关键词分类模块，用于分析数字化转型数据

2. **配置文件**
   - `requirements.txt` - 项目依赖库列表，包含所有需要安装的Python包
   - `README.md` - 项目说明文档，包含部署说明和功能介绍

3. **数据文件**
   - `1999-2023年数字化转型指数与行业合并表.xlsx` - 主要数据文件，包含1999-2023年上市公司的数字化转型指数数据

## 部署方法

### 在Streamlit Cloud上部署

1. **创建GitHub仓库**
   - 将上述文件上传到GitHub仓库中
   - 确保仓库结构清晰，所有文件都在根目录下

2. **部署到Streamlit Cloud**
   - 访问 [Streamlit Cloud](https://share.streamlit.io/)
   - 点击 "New app" 按钮
   - 选择你的GitHub仓库
   - 选择分支（通常是main）
   - 选择主应用程序文件（`digital_transformation_app.py`）
   - 点击 "Deploy!" 按钮

3. **等待部署完成**
   - Streamlit Cloud会自动安装依赖并启动应用程序
   - 部署完成后，你可以通过提供的URL访问应用程序

### 本地运行

```bash
# 安装依赖
pip install -r requirements.txt

# 运行应用程序
streamlit run digital_transformation_app.py
```

## 功能特点

- 📊 数字化转型指数可视化分析
- 🔍 多维度数据筛选（年份、行业、企业等）
- 🗺️ 地理分布分析
- 📈 趋势分析和对比
- 🌙 暗色模式和粉色模式切换
- 💾 数据导出功能

## 技术栈

- Python 3.8+
- Streamlit
- Pandas
- Matplotlib
- Seaborn
- Plotly
- Folium
- XlsxWriter

## 数据说明

数据文件包含1999-2023年上市公司的数字化转型指数数据，包括：
- 企业基本信息（股票代码、企业名称、年份等）
- 行业分类信息
- 数字化转型指数（总体指数、技术维度指数等）

## 注意事项

1. 确保所有文件都在GitHub仓库的根目录下
2. 数据文件较大（约2.6 MB），上传可能需要一些时间
3. 部署时Streamlit Cloud会自动安装requirements.txt中的依赖
4. 如果遇到部署问题，请检查依赖版本是否兼容

## 更新日志

- 2025-12-19: 初始版本发布，包含基本的数字化转型指数分析功能
- 支持年份、行业、企业等多维度筛选
- 提供地理分布分析和趋势图表
- 支持暗色模式和粉色模式切换