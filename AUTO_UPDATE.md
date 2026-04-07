# 3C行业资讯看板 - 自动化更新配置

## 自动更新脚本

已创建两个脚本：

### 1. 主更新脚本
- 路径：`/Users/richardj/.openclaw/workspace-judy/pad-dashboard/update_dashboard.py`
- 功能：
  - 自动计算当前周次
  - 生成15个品牌搜索关键词
  - 检查并创建月份存档
  - 推送更新到GitHub
  - 生成通知消息

### 2. Shell包装脚本
- 路径：`/Users/richardj/.openclaw/workspace-judy/pad-dashboard/auto_update.sh`
- 功能：调用Python脚本并记录日志

## 定时任务配置

### 手动设置Cron（推荐）

在终端执行以下命令：

```bash
# 编辑crontab
crontab -e

# 添加以下行（每周一早上9点执行）
0 9 * * 1 cd /Users/richardj/.openclaw/workspace-judy/pad-dashboard && /usr/bin/python3 update_dashboard.py >> /tmp/3c_dashboard_update.log 2>&1
```

### 验证Cron设置

```bash
# 查看当前crontab
crontab -l

# 查看日志
tail -f /tmp/3c_dashboard_update.log
```

## 手动执行更新

如果需要手动更新，执行：

```bash
cd /Users/richardj/.openclaw/workspace-judy/pad-dashboard
python3 update_dashboard.py
```

## 更新流程说明

1. **每周一早上9点**自动执行
2. 脚本会：
   - 检查是否需要创建新的月份存档
   - 生成15个品牌的搜索关键词
   - 推送更新到GitHub
   - 生成飞书群通知消息（需手动发送或接入API）

3. **注意**：当前脚本框架已搭建完成，但搜索和内容更新部分需要：
   - 方案A：手动搜索后更新（当前方式）
   - 方案B：接入搜索API实现全自动（需配置API密钥）

## 品牌清单

### 笔记本（7个）
Apple、Lenovo、Huawei、ASUS、HP、MECHREVO、Xiaomi

### 平板（8个）
Apple、Huawei、Xiaomi、Lenovo、HONOR、OPPO、vivo、REDMAGIC

## 文件说明

- `3c-dashboard.html` - 当前月份看板（主文件）
- `2026-03.html` - 3月历史存档
- `2026-04.html` - 4月历史存档
- `update_dashboard.py` - 自动更新脚本
- `auto_update.sh` - Shell包装脚本
- `README.md` - 项目说明

## 在线看板

https://ailsa0826.github.io/pad-dashboard/3c-dashboard.html
