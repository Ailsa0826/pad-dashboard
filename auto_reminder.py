#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
3C行业资讯看板 - 自动更新提醒脚本
每周一早上9点执行，发送提醒通知

注意：由于AI工具调用的限制，实际搜索和更新需要在对话中完成
此脚本用于：
1. 发送更新提醒
2. 生成搜索关键词清单
3. 检查是否需要创建月份存档
4. 推送已有的更新到GitHub
"""

import os
import sys
import json
import subprocess
from datetime import datetime, timedelta
from pathlib import Path

# 品牌清单
LAPTOP_BRANDS = [
    ("Apple", "苹果", "MacBook"),
    ("Lenovo", "联想", "ThinkBook/小新/Legion"),
    ("Huawei", "华为", "MateBook"),
    ("ASUS", "华硕", "灵耀/无畏/天选"),
    ("HP", "惠普", "战系列/星Book"),
    ("MECHREVO", "机械革命", "耀世/苍龙/蛟龙"),
    ("Xiaomi", "小米", "Xiaomi Book")
]

TABLET_BRANDS = [
    ("Apple", "苹果", "iPad"),
    ("Huawei", "华为", "MatePad"),
    ("Xiaomi", "小米", "小米平板/REDMI"),
    ("Lenovo", "联想", "小新Pad/Y700"),
    ("HONOR", "荣耀", "MagicPad"),
    ("OPPO", "OPPO", "OPPO Pad"),
    ("vivo", "vivo", "vivo Pad"),
    ("REDMAGIC", "红魔", "红魔平板")
]

def get_current_week_info():
    """获取当前周次信息"""
    today = datetime.now()
    year = today.year
    month = today.month
    
    # 计算是本月的第几周
    week_num = (today.day - 1) // 7 + 1
    
    # 计算周的起止日期
    week_start = today - timedelta(days=today.weekday())
    week_end = week_start + timedelta(days=6)
    
    return {
        "year": year,
        "month": month,
        "week_num": week_num,
        "week_start": week_start.strftime("%m月%d日"),
        "week_end": week_end.strftime("%m月%d日"),
        "date_str": today.strftime("%Y-%m-%d"),
        "weekday": today.weekday()  # 0=周一
    }

def generate_search_tasks():
    """生成搜索任务清单"""
    week_info = get_current_week_info()
    year = week_info["year"]
    month = week_info["month"]
    
    tasks = []
    
    # 笔记本品牌搜索
    for brand_en, brand_cn, series in LAPTOP_BRANDS:
        tasks.append({
            "brand": brand_cn,
            "category": "笔记本",
            "query": f"{brand_cn} 笔记本 {year}年{month}月 新品 发布",
            "series": series
        })
    
    # 平板品牌搜索
    for brand_en, brand_cn, series in TABLET_BRANDS:
        tasks.append({
            "brand": brand_cn,
            "category": "平板",
            "query": f"{brand_cn} 平板 {year}年{month}月 新品 发布",
            "series": series
        })
    
    return tasks

def create_update_reminder():
    """创建更新提醒"""
    week_info = get_current_week_info()
    tasks = generate_search_tasks()
    
    reminder = f"""
{'='*60}
📊 3C行业资讯看板 - 每周更新提醒
{'='*60}

⏰ 更新时间：{week_info['date_str']} 周一早上
📅 更新周期：{week_info['year']}年{week_info['month']}月第{week_info['week_num']}周
🗓️ 时间范围：{week_info['week_start']} - {week_info['week_end']}

{'='*60}
🔍 搜索任务清单（共{len(tasks)}个品牌）
{'='*60}

【笔记本电脑 - 7个品牌】
"""
    
    for i, task in enumerate(tasks[:7], 1):
        reminder += f"{i}. {task['brand']} ({task['series']})\n"
        reminder += f"   搜索词: {task['query']}\n"
    
    reminder += f"""
【平板电脑 - 8个品牌】
"""
    
    for i, task in enumerate(tasks[7:], 1):
        reminder += f"{i}. {task['brand']} ({task['series']})\n"
        reminder += f"   搜索词: {task['query']}\n"
    
    reminder += f"""
{'='*60}
✅ 更新检查清单
{'='*60}

□ 1. 搜索各品牌{week_info['month']}月新品资讯
□ 2. 核实产品发布日期（精确到年月日）
□ 3. 更新看板HTML内容
□ 4. 检查月份导航是否需要更新
□ 5. 推送到GitHub
□ 6. 发送群通知

{'='*60}
📁 相关文件
{'='*60}

- 主看板：/Users/richardj/.openclaw/workspace-judy/pad-dashboard/3c-dashboard.html
- 在线地址：https://ailsa0826.github.io/pad-dashboard/3c-dashboard.html
- 品牌清单：memory/3c-dashboard-brands.md
- 更新规范：memory/3c-dashboard-rules.md

{'='*60}
"""
    
    return reminder

def save_reminder_to_file():
    """保存提醒到文件"""
    week_info = get_current_week_info()
    reminder = create_update_reminder()
    
    # 保存到文件
    work_dir = Path("/Users/richardj/.openclaw/workspace-judy/pad-dashboard")
    reminder_file = work_dir / f"reminder_{week_info['date_str']}.txt"
    reminder_file.write_text(reminder, encoding='utf-8')
    
    # 同时保存为最新的提醒
    latest_reminder = work_dir / "UPDATE_REMINDER.txt"
    latest_reminder.write_text(reminder, encoding='utf-8')
    
    return reminder_file

def create_month_archive():
    """创建月份存档"""
    week_info = get_current_week_info()
    year = week_info["year"]
    month = week_info["month"]
    
    work_dir = Path("/Users/richardj/.openclaw/workspace-judy/pad-dashboard")
    archive_file = work_dir / f"{year}-{month:02d}.html"
    
    if archive_file.exists():
        print(f"✓ 月份存档已存在: {archive_file.name}")
        return False
    
    # 复制当前看板作为存档
    current_dashboard = work_dir / "3c-dashboard.html"
    if current_dashboard.exists():
        content = current_dashboard.read_text(encoding='utf-8')
        # 修改标题为存档月份
        content = content.replace(
            f"<title>3C行业周度资讯看板 - {year}年{month}月",
            f"<title>3C行业周度资讯看板 - {year}年{month}月存档"
        )
        # 修改月份导航中的active状态
        content = content.replace(
            f'href="{year}-{month:02d}.html" class="month-link active"',
            f'href="{year}-{month:02d}.html" class="month-link"'
        )
        archive_file.write_text(content, encoding='utf-8')
        print(f"✓ 创建月份存档: {archive_file.name}")
        return True
    
    return False

def git_push_update():
    """推送更新到GitHub"""
    work_dir = "/Users/richardj/.openclaw/workspace-judy/pad-dashboard"
    week_info = get_current_week_info()
    
    try:
        # 拉取最新代码
        subprocess.run(["git", "pull", "origin", "main"], 
                      cwd=work_dir, check=True, capture_output=True)
        
        # 添加所有更改
        subprocess.run(["git", "add", "-A"], 
                      cwd=work_dir, check=True, capture_output=True)
        
        # 提交
        commit_msg = f"Auto: {week_info['date_str']} 更新提醒和月份存档"
        result = subprocess.run(["git", "commit", "-m", commit_msg], 
                               cwd=work_dir, capture_output=True, text=True)
        
        if "nothing to commit" in result.stdout or "nothing to commit" in result.stderr:
            print("✓ 没有需要提交的更改")
            return True
        
        # 推送
        subprocess.run(["git", "push", "origin", "main"], 
                      cwd=work_dir, check=True, capture_output=True)
        print(f"✓ 已推送更新")
        return True
        
    except subprocess.CalledProcessError as e:
        print(f"✗ Git操作失败: {e}")
        return False

def main():
    """主函数"""
    week_info = get_current_week_info()
    
    print("="*60)
    print("📊 3C行业资讯看板 - 自动更新系统")
    print("="*60)
    print()
    
    # 检查是否是周一
    if week_info["weekday"] != 0:
        print(f"⏰ 今天是周{['一','二','三','四','五','六','日'][week_info['weekday']]}，非更新时间")
        print("   系统将在每周一早上9点执行")
        return
    
    print(f"📅 今天: {week_info['date_str']} 周一")
    print(f"📊 周期: {week_info['year']}年{week_info['month']}月第{week_info['week_num']}周")
    print()
    
    # 1. 创建月份存档（如果是新月第一周）
    if week_info["week_num"] == 1:
        print("【月份存档】新月第一周，检查存档...")
        created = create_month_archive()
        if created:
            print("   已创建新的月份存档")
        print()
    
    # 2. 生成更新提醒
    print("【生成提醒】创建搜索任务清单...")
    reminder_file = save_reminder_to_file()
    print(f"   提醒已保存: {reminder_file.name}")
    print()
    
    # 3. 显示提醒内容
    reminder = create_update_reminder()
    print(reminder)
    
    # 4. 推送到GitHub
    print("【Git推送】推送提醒文件到GitHub...")
    git_push_update()
    print()
    
    print("="*60)
    print("✅ 自动提醒完成")
    print("="*60)
    print()
    print("⚠️  注意：实际搜索和内容更新需要Judy在对话中完成")
    print("   请查看UPDATE_REMINDER.txt获取搜索任务清单")

if __name__ == "__main__":
    main()
