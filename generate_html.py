import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import plotly.offline as pyo

# 读取数据
df = pd.read_excel('/tmp/openclaw/bot-resource-1773120994950-a6bf4fd6-deed-4105-98a6-5039d5a98e13.xlsx')
df['SO Date'] = pd.to_datetime(df['SO Date'])

# 创建HTML报告
html_content = """
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>2026年Pad销售数据看板</title>
    <script src="https://cdn.plot.ly/plotly-latest.min.js"></script>
    <style>
        body { font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif; margin: 0; padding: 20px; background: #f5f5f5; }
        .container { max-width: 1400px; margin: 0 auto; }
        .header { background: white; padding: 30px; border-radius: 10px; margin-bottom: 20px; box-shadow: 0 2px 4px rgba(0,0,0,0.1); }
        .header h1 { margin: 0; color: #333; }
        .metrics { display: grid; grid-template-columns: repeat(4, 1fr); gap: 20px; margin-bottom: 20px; }
        .metric-card { background: white; padding: 25px; border-radius: 10px; text-align: center; box-shadow: 0 2px 4px rgba(0,0,0,0.1); }
        .metric-value { font-size: 36px; font-weight: bold; color: #1f77b4; }
        .metric-label { font-size: 14px; color: #666; margin-top: 5px; }
        .chart-row { display: grid; grid-template-columns: 1fr 1fr; gap: 20px; margin-bottom: 20px; }
        .chart-card { background: white; padding: 20px; border-radius: 10px; box-shadow: 0 2px 4px rgba(0,0,0,0.1); }
        .chart-title { font-size: 18px; font-weight: 600; margin-bottom: 15px; color: #333; }
        .full-width { grid-column: 1 / -1; }
        .data-table { background: white; padding: 20px; border-radius: 10px; box-shadow: 0 2px 4px rgba(0,0,0,0.1); overflow-x: auto; }
        table { width: 100%; border-collapse: collapse; }
        th, td { padding: 12px; text-align: left; border-bottom: 1px solid #ddd; }
        th { background: #f8f9fa; font-weight: 600; }
        tr:hover { background: #f8f9fa; }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>📊 2026年Pad销售数据看板</h1>
            <p style="color: #666; margin-top: 10px;">数据时间：2026年1月 | 生成时间：""" + pd.Timestamp.now().strftime('%Y-%m-%d %H:%M') + """</p>
        </div>
        
        <div class="metrics">
            <div class="metric-card">
                <div class="metric-value">{:,}</div>
                <div class="metric-label">总销量（台）</div>
            </div>
            <div class="metric-card">
                <div class="metric-value">{:,}</div>
                <div class="metric-label">总订单数（笔）</div>
            </div>
            <div class="metric-card">
                <div class="metric-value">{:.2f}</div>
                <div class="metric-label">平均单笔（台）</div>
            </div>
            <div class="metric-card">
                <div class="metric-value">{:,.0f}</div>
                <div class="metric-label">日均销量（台）</div>
            </div>
        </div>
""".format(
    df['TTL SO'].sum(),
    len(df),
    df['TTL SO'].mean(),
    df['TTL SO'].sum() / df['SO Date'].nunique()
)

# 1. 渠道分布饼图
channel_data = df.groupby('客户细分2')['TTL SO'].sum().reset_index().sort_values('TTL SO', ascending=False)
fig1 = px.pie(channel_data, values='TTL SO', names='客户细分2', hole=0.4,
              color_discrete_sequence=px.colors.qualitative.Set3)
fig1.update_traces(textposition='inside', textinfo='percent+label')
fig1.update_layout(title='各渠道销售分布', showlegend=False, height=400)
html_content += f"""
        <div class="chart-row">
            <div class="chart-card">
                <div class="chart-title">各渠道销售分布</div>
                <div id="chart1"></div>
            </div>
"""
html_content += f"<script>var chart1 = {fig1.to_json()}; Plotly.newPlot('chart1', chart1.data, chart1.layout);</script>"

# 2. 产品销量柱状图
product_data = df.groupby('重点机型')['TTL SO'].sum().reset_index().sort_values('TTL SO', ascending=True).tail(10)
fig2 = px.bar(product_data, x='TTL SO', y='重点机型', orientation='h', color='TTL SO',
              color_continuous_scale='Viridis')
fig2.update_layout(title='产品销量排行（Top 10）', yaxis_title='', xaxis_title='销量（台）', height=400)
html_content += f"""
            <div class="chart-card">
                <div class="chart-title">产品销量排行</div>
                <div id="chart2"></div>
            </div>
        </div>
"""
html_content += f"<script>var chart2 = {fig2.to_json()}; Plotly.newPlot('chart2', chart2.data, chart2.layout);</script>"

# 3. 每日销量走势
daily_data = df.groupby(df['SO Date'].dt.date)['TTL SO'].sum().reset_index()
daily_data.columns = ['日期', '销量']
fig3 = px.line(daily_data, x='日期', y='销量', markers=True, line_shape='spline')
fig3.update_layout(title='每日销量走势', xaxis_title='日期', yaxis_title='销量（台）', height=400)
html_content += f"""
        <div class="chart-row">
            <div class="chart-card full-width">
                <div class="chart-title">每日销量走势</div>
                <div id="chart3"></div>
            </div>
        </div>
"""
html_content += f"<script>var chart3 = {fig3.to_json()}; Plotly.newPlot('chart3', chart3.data, chart3.layout);</script>"

# 4. 大区分布
region_data = df.groupby('大区')['TTL SO'].sum().reset_index().sort_values('TTL SO', ascending=False)
fig4 = px.bar(region_data, x='大区', y='TTL SO', color='TTL SO', color_continuous_scale='Blues')
fig4.update_layout(title='各大区销售分布', xaxis_title='', yaxis_title='销量（台）', height=400)
html_content += f"""
        <div class="chart-row">
            <div class="chart-card">
                <div class="chart-title">各大区销售分布</div>
                <div id="chart4"></div>
            </div>
"""
html_content += f"<script>var chart4 = {fig4.to_json()}; Plotly.newPlot('chart4', chart4.data, chart4.layout);</script>"

# 5. 店铺类型分布
store_data = df.groupby('客户细分4')['TTL SO'].sum().reset_index().sort_values('TTL SO', ascending=False).head(8)
fig5 = px.pie(store_data, values='TTL SO', names='客户细分4', color_discrete_sequence=px.colors.qualitative.Pastel)
fig5.update_traces(textposition='inside', textinfo='percent+label')
fig5.update_layout(title='店铺类型Mix', showlegend=False, height=400)
html_content += f"""
            <div class="chart-card">
                <div class="chart-title">店铺类型Mix</div>
                <div id="chart5"></div>
            </div>
        </div>
"""
html_content += f"<script>var chart5 = {fig5.to_json()}; Plotly.newPlot('chart5', chart5.data, chart5.layout);</script>"

# 6. 产品分天走势
top_products = df.groupby('重点机型')['TTL SO'].sum().nlargest(5).index
product_daily = df[df['重点机型'].isin(top_products)].groupby([df['SO Date'].dt.date, '重点机型'])['TTL SO'].sum().reset_index()
product_daily.columns = ['日期', '产品', '销量']
fig6 = px.line(product_daily, x='日期', y='销量', color='产品', markers=True, line_shape='spline')
fig6.update_layout(title='重点产品分天销售走势', xaxis_title='日期', yaxis_title='销量（台）', height=400)
html_content += f"""
        <div class="chart-row">
            <div class="chart-card full-width">
                <div class="chart-title">重点产品分天销售走势</div>
                <div id="chart6"></div>
            </div>
        </div>
"""
html_content += f"<script>var chart6 = {fig6.to_json()}; Plotly.newPlot('chart6', chart6.data, chart6.layout);</script>"

# 数据表格
summary_df = df.groupby(['大区', '客户细分2', '重点机型']).agg({'TTL SO': 'sum'}).reset_index()
summary_df.columns = ['大区', '渠道', '产品', '销量']
summary_df = summary_df.sort_values('销量', ascending=False).head(20)

html_content += """
        <div class="data-table">
            <div class="chart-title">详细数据（Top 20）</div>
            <table>
                <thead>
                    <tr>
                        <th>大区</th>
                        <th>渠道</th>
                        <th>产品</th>
                        <th>销量</th>
                    </tr>
                </thead>
                <tbody>
"""

for _, row in summary_df.iterrows():
    html_content += f"""
                    <tr>
                        <td>{row['大区']}</td>
                        <td>{row['渠道']}</td>
                        <td>{row['产品']}</td>
                        <td>{row['销量']:,}</td>
                    </tr>
"""

html_content += """
                </tbody>
            </table>
        </div>
    </div>
</body>
</html>
"""

# 保存文件
output_path = '/Users/richardj/.openclaw/workspace-judy/dashboard/pad_dashboard.html'
with open(output_path, 'w', encoding='utf-8') as f:
    f.write(html_content)

print(f"✅ 看板已生成: {output_path}")
print(f"📊 包含图表:")
print("  1. 各渠道销售分布（饼图）")
print("  2. 产品销量排行（柱状图）")
print("  3. 每日销量走势（折线图）")
print("  4. 各大区销售分布（柱状图）")
print("  5. 店铺类型Mix（饼图）")
print("  6. 重点产品分天销售走势（折线图）")
print("  7. 详细数据表格")
