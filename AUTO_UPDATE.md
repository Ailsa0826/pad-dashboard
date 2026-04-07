# 3C行业资讯看板 - 自动化更新配置

## 实际自动化方案

由于AI工具调用的限制（cron任务无法直接调用Brave Search等API），采用以下方案：

### 方案：自动提醒 + 人工执行

**每周一早上9点自动执行**：
1. 生成搜索任务清单
2. 创建月份存档（如需要）
3. 推送提醒到GitHub
4. **Judy在对话中完成搜索和更新**

---

## 自动提醒脚本

### auto_reminder.py
- 路径：`/Users/richardj/.openclaw/workspace-judy/pad-dashboard/auto_reminder.py`
- 功能：
  - 每周一早上自动生成搜索任务清单
  - 创建月份存档
  - 生成UPDATE_REMINDER.txt提醒文件
  - 推送提醒到GitHub

### 生成的提醒文件
- `UPDATE_REMINDER.txt` - 最新的更新任务清单
- `reminder_YYYY-MM-DD.txt` - 历史提醒存档

---

## 定时任务配置

### 设置Cron

在终端执行：

```bash
crontab -e
```

添加以下行：
```
# 3C行业资讯看板每周一自动提醒
0 9 * * 1 cd /Users/richardj/.openclaw/workspace-judy/pad-dashboard && /usr/bin/python3 auto_reminder.py >> /tmp/3c_dashboard_reminder.log 2>&1
```

### 验证设置

```bash
# 查看crontab
crontab -l

# 查看日志
tail -f /tmp/3c_dashboard_reminder.log
```

---

## 更新执行流程

### 每周一自动执行（Cron）
1. 生成搜索任务清单
2. 创建月份存档
3. 推送提醒文件到GitHub

### Judy收到提醒后执行
1. 读取UPDATE_REMINDER.txt或等待用户提醒
2. 按清单搜索15个品牌的新品资讯
3. 核实发布日期（精确到年月日）
4. 更新3c-dashboard.html
5. 推送到GitHub
6. 发送群通知

---

## 品牌清单

### 笔记本（7个）
| 品牌 | 系列 |
|------|------|
| Apple | MacBook |
| Lenovo | ThinkBook/小新/Legion |
| Huawei | MateBook |
| ASUS | 灵耀/无畏/天选 |
| HP | 战系列/星Book |
| MECHREVO | 耀世/苍龙/蛟龙 |
| Xiaomi | Xiaomi Book |

### 平板（8个）
| 品牌 | 系列 |
|------|------|
| Apple | iPad |
| Huawei | MatePad |
| Xiaomi | 小米平板/REDMI |
| Lenovo | 小新Pad/Y700 |
| HONOR | MagicPad |
| OPPO | OPPO Pad |
| vivo | vivo Pad |
| REDMAGIC | 红魔平板 |

---

## 文件说明

| 文件 | 说明 |
|------|------|
| `3c-dashboard.html` | 当前月份看板（主文件） |
| `2026-03.html` | 3月历史存档 |
| `2026-04.html` | 4月历史存档 |
| `auto_reminder.py` | 自动提醒脚本 |
| `UPDATE_REMINDER.txt` | 最新更新任务清单 |
| `AUTO_UPDATE.md` | 本文档 |

---

## 在线看板

🔗 https://ailsa0826.github.io/pad-dashboard/3c-dashboard.html

---

## 注意事项

1. **信息准确性**：每个产品必须有具体发布日期（年月日）
2. **排除旧产品**：搜索时需确认是当月新品，不是2025年或更早的产品
3. **展会产品**：MWC/CES展会上展示的不一定是当月新品
4. **更新时间**：每周一早上9点前完成更新
