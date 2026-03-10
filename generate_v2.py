import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import plotly.offline as pyo
from datetime import datetime, timedelta

# 读取数据
df = pd.read_excel('/tmp/openclaw/bot-resource-1773120994950-a6bf4fd6-deed-4105-98a6-5039d5a98e13.xlsx')
df['SO Date'] = pd.to_datetime(df['SO Date'])

# 1月目标数据（千台）
targets = {
    '总目标': 47.5,
    '官网': 7.0,
    '天猫': 23.5,
    '京东官旗': 5.0,
    '抖快': 12.0
}

# 计算实际销售（千台）
actual_total = df['TTL SO'].sum() / 1000
channel_sales = df.groupby('客户细分2')['TTL SO'].sum() / 1000

# 计算达成率
achievement_rate = (actual_total / targets['总目标']) * 100

# 计算倒计时（假设1月31日截止）
end_date = datetime(2026, 1, 31)
now = datetime.now()
days_left = (end_date - now).days
if days_left < 0:
    days_left = 0

# 创建HTML报告
html_content = """
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>2026年1月Pad销售数据看板</title>
    <script src="https://cdn.plot.ly/plotly-latest.min.js"></script>
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body { 
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif; 
            background: #f0f2f5; 
            padding: 20px;
        }
        .container { max-width: 1400px; margin: 0 auto; }
        
        /* 顶部横幅 */
        .header-banner {
            background: linear-gradient(135deg, #ff9500 0%, #ff7700 100%);
            color: white;
            padding: 30px;
            border-radius: 12px;
            text-align: center;
            margin-bottom: 20px;
            box-shadow: 0 4px 12px rgba(255, 119, 0, 0.3);
        }
        .header-banner h1 { 
            font-size: 32px; 
            font-weight: 600;
            margin: 0;
        }
        .header-banner p {
            font-size: 16px;
            margin-top: 8px;
            opacity: 0.9;
        }
        
        /* 第一行：倒计时 + 总达成 + 店铺Mix */
        .top-row {
            display: grid;
            grid-template-columns: 1fr 1.5fr 1fr;
            gap: 20px;
            margin-bottom: 20px;
        }
        
        .card {
            background: white;
            border-radius: 12px;
            padding: 24px;
            box-shadow: 0 2px 8px rgba(0,0,0,0.08);
        }
        
        .card-title {
            font-size: 14px;
            color: #666;
            margin-bottom: 16px;
            font-weight: 500;
        }
        
        /* 倒计时样式 */
        .countdown-container {
            display: flex;
            justify-content: center;
            gap: 12px;
        }
        .countdown-box {
            background: #1890ff;
            color: white;
            padding: 16px 20px;
            border-radius: 8px;
            text-align: center;
            min-width: 60px;
        }
        .countdown-number {
            font-size: 32px;
            font-weight: bold;
            line-height: 1;
        }
        .countdown-label {
            font-size: 12px;
            margin-top: 4px;
            opacity: 0.9;
        }
        .countdown-separator {
            font-size: 32px;
            color: #1890ff;
            font-weight: bold;
            align-self: center;
        }
        
        /* 达成进度样式 */
        .achievement-big {
            text-align: center;
        }
        .achievement-percent {
            font-size: 56px;
            font-weight: bold;
            color: #333;
            line-height: 1;
        }
        .achievement-bar {
            width: 100%;
            height: 12px;
            background: #e8e8e8;
            border-radius: 6px;
            margin: 16px 0;
            overflow: hidden;
        }
        .achievement-bar-fill {
            height: 100%;
            background: linear-gradient(90deg, #52c41a 0%, #73d13d 100%);
            border-radius: 6px;
            transition: width 0.5s ease;
        }
        .achievement-numbers {
            display: flex;
            justify-content: center;
            gap: 8px;
            font-size: 16px;
            color: #666;
        }
        .achievement-current {
            color: #1890ff;
            font-weight: 600;
        }
        .achievement-target {
            color: #999;
        }
        
        /* 渠道达成卡片 */
        .channel-row {
            display: grid;
            grid-template-columns: repeat(4, 1fr);
            gap: 16px;
            margin-bottom: 20px;
        }
        .channel-card {
            background: white;
            border-radius: 12px;
            padding: 20px;
            box-shadow: 0 2px 8px rgba(0,0,0,0.08);
            text-align: center;
        }
        .channel-name {
            font-size: 13px;
            color: #666;
            margin-bottom: 8px;
        }
        .channel-percent {
            font-size: 36px;
            font-weight: bold;
            color: #333;
            line-height: 1;
        }
        .channel-bar {
            width: 100%;
            height: 8px;
            background: #e8e8e8;
            border-radius: 4px;
            margin-top: 12px;
            overflow: hidden;
        }
        .channel-bar-fill {
            height: 100%;
            background: #1890ff;
            border-radius: 4px;
        }
        .channel-numbers {
            display: flex;
            justify-content: center;
            gap: 4px;
            font-size: 12px;
            color: #666;
            margin-top: 8px;
        }
        .channel-current {
            color: #1890ff;
            font-weight: 500;
        }
        .channel-target {
            color: #999;
        }
        
        /* 图表区域 */
        .chart-row {
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 20px;
            margin-bottom: 20px;
        }
        .chart-card {
            background: white;
            border-radius: 12px;
            padding: 20px;
            box-shadow: 0 2px 8px rgba(0,0,0,0.08);
        }
        .chart-title {
            font-size: 16px;
            font-weight: 600;
            margin-bottom: 16px;
            color: #333;
        }
        .full-width {
            grid-column: 1 / -1;
        }
        
        /* 数据表格 */
        .data-table {
            background: white;
            border-radius: 12px;
            padding: 20px;
            box-shadow: 0 2px 8px rgba(0,0,0,0.08);
            overflow-x: auto;
        }
        table {
            width: 100%;
            border-collapse: collapse;
        }
        th, td {
            padding: 12px;
            text-align: left;
            border-bottom: 1px solid #f0f0f0;
        }
        th {
            background: #fafafa;
            font-weight: 600;
            color: #333;
        }
        tr:hover { background: #fafafa; }
    </style>
</head>
<body>
    <div class="container">
        <!-- 顶部横幅 -->
        <div class="header-banner">
            <h1>1月直营平板销售</h1>
            <p>数据时间：2026年1月 | 生成时间：""" + datetime.now().strftime('%Y-%m-%d %H:%M') + """</p>
        </div>
        
        <!-- 第一行：倒计时 + 总达成 + 店铺Mix -->
        <div class="top-row">
            <!-- 倒计时 -->
            <div class="card">
                <div class="card-title" style="text-align: center;">FY26 1月倒计时</div>
                <div class="countdown-container">
                    <div class="countdown-box">
                        <div class="countdown-number">0</div>
                        <div class="countdown-label">月</div>
                    </div>
                    <div class="countdown-separator">:</div>
                    <div class="countdown-box">
                        <div class="countdown-number">""" + str(days_left) + """</div>
                        <div class="countdown-label">天</div>
                    </div>
                    <div class="countdown-separator">:</div>
                    <div class="countdown-box">
                        <div class="countdown-number">00</div>
                        <div class="countdown-label">时</div>
                    </div>
                </div>
            </div>
            
            <!-- 总达成进度 -->
            <div class="card">
                <div class="card-title" style="text-align: center;">FY26 1月直营PO达成进度</div>
                <div class="achievement-big">
                    <div class="achievement-percent">""" + f"{achievement_rate:.0f}" + """%</div>
                    <div class="achievement-bar">
                        <div class="achievement-bar-fill" style="width: """ + f"{min(achievement_rate, 100)}" + """%;"></div>
                    </div>
                    <div class="achievement-numbers">
                        <span class="achievement-current">当前 """ + f"{actual_total:.1f}" + """K</span>
                        <span>|</span>
                        <span class="achievement-target">目标 """ + f"{targets['总目标']:.1f}" + """K</span>
                    </div>
                </div>
            </div>
            
            <!-- 店铺Mix -->
            <div class="card">
                <div class="card-title">直营分店铺Mix</div>
                <div id="store-mix-chart"></div>
            </div>
        </div>
        
        <!-- 渠道达成卡片 -->
        <div class="channel-row">
"""

# 计算各渠道达成率
channel_data = []
for channel, target in targets.items():
    if channel != '总目标':
        actual = channel_sales.get(channel, 0)
        rate = (actual / target) * 100 if target > 0 else 0
        channel_data.append((channel, rate, actual, target))
        html_content += f"""
            <div class="channel-card">
                <div class="channel-name">FY26 1月{channel}PO</div>
                <div class="channel-percent">{rate:.0f}%</div>
                <div class="channel-bar">
                    <div class="channel-bar-fill" style="width: {min(rate, 100)}%;"></div>
                </div>
                <div class="channel-numbers">
                    <span class="channel-current">{actual*1000:,.0f}</span>
                    <span>|</span>
                    <span class="channel-target">{target*1000:,.0f}</span>
                </div>
            </div>
"""

html_content += """
        </div>
        
        <!-- 图表区域 -->
        <div class="chart-row">
            <div class="chart-card">
                <div class="chart-title">各渠道销售分布</div>
                <div id="channel-chart"></div>
            </div>
            <div class="chart-card">
                <div class="chart-title">产品销量排行</div>
                <div id="product-chart"></div>
            </div>
        </div>
        
        <div class="chart-row">
            <div class="chart-card full-width">
                <div class="chart-title">每日销量走势</div>
                <div id="daily-chart"></div>
            </div>
        </div>
        
        <div class="chart-row">
            <div class="chart-card">
                <div class="chart-title">各大区销售分布</div>
                <div id="region-chart"></div>
            </div>
            <div class="chart-card">
                <div class="chart-title">重点产品分天销售走势</div>
                <div id="product-daily-chart"></div>
            </div>
        </div>
"""

# 店铺Mix饼图 - 使用客户细分2（渠道）
store_data = df.groupby('客户细分2')['TTL SO'].sum().reset_index().sort_values('TTL SO', ascending=False)
# 计算百分比
store_data['占比'] = store_data['TTL SO'] / store_data['TTL SO'].sum() * 100
fig1 = go.Figure(data=[go.Pie(
    labels=store_data['客户细分2'],
    values=store_data['TTL SO'],
    textinfo='label+percent',
    textposition='inside',
    textfont_size=11,
    marker_colors=['#1890ff', '#52c41a', '#faad14', '#f5222d', '#722ed1']
)])
fig1.update_layout(showlegend=False, margin=dict(l=0, r=0, t=0, b=0), height=200)
html_content += f"<script>var fig1 = {fig1.to_json()}; Plotly.newPlot('store-mix-chart', fig1.data, fig1.layout);</script>"

# 渠道分布饼图
channel_dist = df.groupby('客户细分2')['TTL SO'].sum().reset_index().sort_values('TTL SO', ascending=False)
fig2 = px.pie(channel_dist, values='TTL SO', names='客户细分2', hole=0.4,
              color_discrete_sequence=px.colors.qualitative.Set3)
fig2.update_traces(textposition='inside', textinfo='percent+label')
fig2.update_layout(showlegend=False, height=350)
html_content += f"<script>var fig2 = {fig2.to_json()}; Plotly.newPlot('channel-chart', fig2.data, fig2.layout);</script>"

# 产品销量柱状图
product_data = df.groupby('重点机型')['TTL SO'].sum().reset_index().sort_values('TTL SO', ascending=True).tail(8)
fig3 = px.bar(product_data, x='TTL SO', y='重点机型', orientation='h', color='TTL SO',
              color_continuous_scale=['#e6f7ff', '#1890ff'])
fig3.update_layout(yaxis_title='', xaxis_title='销量（台）', height=350, coloraxis_showscale=False)
html_content += f"<script>var fig3 = {fig3.to_json()}; Plotly.newPlot('product-chart', fig3.data, fig3.layout);</script>"

# 每日销量走势
daily_data = df.groupby(df['SO Date'].dt.date)['TTL SO'].sum().reset_index()
daily_data.columns = ['日期', '销量']
fig4 = px.line(daily_data, x='日期', y='销量', markers=True, line_shape='spline',
               color_discrete_sequence=['#1890ff'])
fig4.update_layout(xaxis_title='日期', yaxis_title='销量（台）', height=300, 
                   plot_bgcolor='white', paper_bgcolor='white')
html_content += f"<script>var fig4 = {fig4.to_json()}; Plotly.newPlot('daily-chart', fig4.data, fig4.layout);</script>"

# 大区分布
region_data = df.groupby('大区')['TTL SO'].sum().reset_index().sort_values('TTL SO', ascending=False)
fig5 = px.bar(region_data, x='大区', y='TTL SO', color='TTL SO', 
              color_continuous_scale=['#e6f7ff', '#1890ff'])
fig5.update_layout(xaxis_title='', yaxis_title='销量（台）', height=350, coloraxis_showscale=False)
html_content += f"<script>var fig5 = {fig5.to_json()}; Plotly.newPlot('region-chart', fig5.data, fig5.layout);</script>"

# 产品分天走势
top_products = df.groupby('重点机型')['TTL SO'].sum().nlargest(4).index
product_daily = df[df['重点机型'].isin(top_products)].groupby([
    df['SO Date'].dt.date, '重点机型'
])['TTL SO'].sum().reset_index()
product_daily.columns = ['日期', '产品', '销量']
fig6 = px.line(product_daily, x='日期', y='销量', color='产品', markers=True, line_shape='spline')
fig6.update_layout(xaxis_title='日期', yaxis_title='销量（台）', height=350,
                   legend=dict(orientation='h', yanchor='bottom', y=1.02, xanchor='right', x=1))
html_content += f"<script>var fig6 = {fig6.to_json()}; Plotly.newPlot('product-daily-chart', fig6.data, fig6.layout);</script>"

# 数据表格
html_content += """
        <!-- 数据表格 -->
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

summary_df = df.groupby(['大区', '客户细分2', '重点机型']).agg({'TTL SO': 'sum'}).reset_index()
summary_df.columns = ['大区', '渠道', '产品', '销量']
summary_df = summary_df.sort_values('销量', ascending=False).head(20)

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
output_path = '/Users/richardj/.openclaw/workspace-judy/dashboard/index.html'
with open(output_path, 'w', encoding='utf-8') as f:
    f.write(html_content)

print(f"✅ 看板已更新: {output_path}")
print(f"📊 更新内容:")
print(f"  - 达成率: {achievement_rate:.0f}% (27.1K / 47.5K)")
print(f"  - 倒计时: {days_left} 天")
print(f"  - 各渠道达成卡片")
print(f"  - 黄色标题横幅")
print(f"  - 优化布局风格")
