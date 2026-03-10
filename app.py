import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import os

# 页面配置
st.set_page_config(
    page_title="Pad销售数据看板",
    page_icon="📊",
    layout="wide"
)

# 标题
st.title("📊 2026年Pad销售数据看板")
st.markdown("---")

# 数据加载
@st.cache_data
def load_data():
    """加载数据"""
    # 尝试多个路径
    possible_paths = [
        "/tmp/openclaw/bot-resource-1773120994950-a6bf4fd6-deed-4105-98a6-5039d5a98e13.xlsx",
        "../bot-resource-1773120994950-a6bf4fd6-deed-4105-98a6-5039d5a98e13.xlsx",
        "data.xlsx"
    ]
    
    for path in possible_paths:
        if os.path.exists(path):
            df = pd.read_excel(path)
            df['SO Date'] = pd.to_datetime(df['SO Date'])
            return df
    
    return None

df = load_data()

if df is None:
    st.error("❌ 未找到数据文件，请上传Excel文件")
    uploaded_file = st.file_uploader("上传Excel文件", type=['xlsx', 'xls'])
    if uploaded_file:
        df = pd.read_excel(uploaded_file)
        df['SO Date'] = pd.to_datetime(df['SO Date'])
        st.success("✅ 数据加载成功！")
    else:
        st.stop()

# 侧边栏筛选器
st.sidebar.header("🔍 筛选条件")

# 时间范围
date_range = st.sidebar.date_input(
    "时间范围",
    value=(df['SO Date'].min(), df['SO Date'].max()),
    min_value=df['SO Date'].min(),
    max_value=df['SO Date'].max()
)

# 渠道筛选
channels = st.sidebar.multiselect(
    "销售渠道",
    options=df['客户细分2'].unique(),
    default=df['客户细分2'].unique()
)

# 产品筛选
products = st.sidebar.multiselect(
    "产品机型",
    options=df['重点机型'].unique(),
    default=df['重点机型'].unique()
)

# 大区筛选
regions = st.sidebar.multiselect(
    "销售大区",
    options=df['大区'].unique(),
    default=df['大区'].unique()
)

# 应用筛选
filtered_df = df[
    (df['SO Date'] >= pd.Timestamp(date_range[0])) &
    (df['SO Date'] <= pd.Timestamp(date_range[1])) &
    (df['客户细分2'].isin(channels)) &
    (df['重点机型'].isin(products)) &
    (df['大区'].isin(regions))
]

# 核心指标
st.header("📈 核心指标")
col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric("总销量", f"{filtered_df['TTL SO'].sum():,} 台")

with col2:
    st.metric("总订单数", f"{len(filtered_df):,} 笔")

with col3:
    st.metric("平均单笔", f"{filtered_df['TTL SO'].mean():.2f} 台")

with col4:
    st.metric("日均销量", f"{filtered_df['TTL SO'].sum() / filtered_df['SO Date'].nunique():.0f} 台")

st.markdown("---")

# 图表区域
st.header("📊 数据可视化")

# 第一行：渠道分布 + 产品构成
row1_col1, row1_col2 = st.columns(2)

with row1_col1:
    st.subheader("各渠道销售分布")
    channel_data = filtered_df.groupby('客户细分2')['TTL SO'].sum().reset_index()
    channel_data = channel_data.sort_values('TTL SO', ascending=False)
    
    fig1 = px.pie(
        channel_data, 
        values='TTL SO', 
        names='客户细分2',
        hole=0.4,
        color_discrete_sequence=px.colors.qualitative.Set3
    )
    fig1.update_traces(textposition='inside', textinfo='percent+label')
    st.plotly_chart(fig1, use_container_width=True)

with row1_col2:
    st.subheader("产品销量构成")
    product_data = filtered_df.groupby('重点机型')['TTL SO'].sum().reset_index()
    product_data = product_data.sort_values('TTL SO', ascending=True).tail(10)
    
    fig2 = px.bar(
        product_data,
        x='TTL SO',
        y='重点机型',
        orientation='h',
        color='TTL SO',
        color_continuous_scale='Viridis'
    )
    fig2.update_layout(yaxis_title="", xaxis_title="销量（台）")
    st.plotly_chart(fig2, use_container_width=True)

# 第二行：每日销量走势
st.subheader("📅 每日销量走势")
daily_data = filtered_df.groupby(filtered_df['SO Date'].dt.date)['TTL SO'].sum().reset_index()
daily_data.columns = ['日期', '销量']

fig3 = px.line(
    daily_data,
    x='日期',
    y='销量',
    markers=True,
    line_shape='spline'
)
fig3.update_layout(
    xaxis_title="日期",
    yaxis_title="销量（台）",
    hovermode='x unified'
)
st.plotly_chart(fig3, use_container_width=True)

# 第三行：大区分布 + 店铺Mix
row3_col1, row3_col2 = st.columns(2)

with row3_col1:
    st.subheader("各大区销售分布")
    region_data = filtered_df.groupby('大区')['TTL SO'].sum().reset_index()
    region_data = region_data.sort_values('TTL SO', ascending=False)
    
    fig4 = px.bar(
        region_data,
        x='大区',
        y='TTL SO',
        color='TTL SO',
        color_continuous_scale='Blues'
    )
    fig4.update_layout(xaxis_title="", yaxis_title="销量（台）")
    st.plotly_chart(fig4, use_container_width=True)

with row3_col2:
    st.subheader("店铺类型Mix")
    store_data = filtered_df.groupby('客户细分4')['TTL SO'].sum().reset_index()
    store_data = store_data.sort_values('TTL SO', ascending=False).head(8)
    
    fig5 = px.pie(
        store_data,
        values='TTL SO',
        names='客户细分4',
        color_discrete_sequence=px.colors.qualitative.Pastel
    )
    fig5.update_traces(textposition='inside', textinfo='percent+label')
    st.plotly_chart(fig5, use_container_width=True)

# 第四行：产品分天销售走势
st.subheader("🔥 重点产品分天销售走势")
top_products = filtered_df.groupby('重点机型')['TTL SO'].sum().nlargest(5).index
product_daily = filtered_df[filtered_df['重点机型'].isin(top_products)].groupby([
    filtered_df['SO Date'].dt.date, '重点机型'
])['TTL SO'].sum().reset_index()
product_daily.columns = ['日期', '产品', '销量']

fig6 = px.line(
    product_daily,
    x='日期',
    y='销量',
    color='产品',
    markers=True,
    line_shape='spline'
)
fig6.update_layout(
    xaxis_title="日期",
    yaxis_title="销量（台）",
    hovermode='x unified'
)
st.plotly_chart(fig6, use_container_width=True)

# 数据表格
st.markdown("---")
st.header("📋 详细数据")

# 汇总表格
summary_df = filtered_df.groupby(['大区', '客户细分2', '重点机型']).agg({
    'TTL SO': 'sum'
}).reset_index()
summary_df.columns = ['大区', '渠道', '产品', '销量']
summary_df = summary_df.sort_values('销量', ascending=False)

st.dataframe(summary_df, use_container_width=True)

# 下载按钮
csv = summary_df.to_csv(index=False).encode('utf-8')
st.download_button(
    label="📥 下载数据",
    data=csv,
    file_name='pad_sales_summary.csv',
    mime='text/csv'
)

# 页脚
st.markdown("---")
st.caption("Pad销售数据看板 | 数据更新时间: " + pd.Timestamp.now().strftime("%Y-%m-%d %H:%M"))
