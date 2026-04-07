#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
3C行业资讯看板自动更新脚本
每周一早上自动搜索各品牌新品资讯并更新看板
"""

import os
import sys
import json
import subprocess
from datetime import datetime, timedelta
from pathlib import Path

# 品牌清单
LAPTOP_BRANDS = [
    ("Apple", "苹果"),
    ("Lenovo", "联想"),
    ("Huawei", "华为"),
    ("ASUS", "华硕"),
    ("HP", "惠普"),
    ("MECHREVO", "机械革命"),
    ("Xiaomi", "小米")
]

TABLET_BRANDS = [
    ("Apple", "苹果"),
    ("Huawei", "华为"),
    ("Xiaomi", "小米"),
    ("Lenovo", "联想"),
    ("HONOR", "荣耀"),
    ("OPPO", "OPPO"),
    ("vivo", "vivo"),
    ("REDMAGIC", "红魔")
]

def get_current_week_info():
    """获取当前周次信息"""
    today = datetime.now()
    year = today.year
    month = today.month
    
    # 计算是本月的第几周
    first_day = today.replace(day=1)
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
        "date_str": today.strftime("%Y-%m-%d")
    }

def generate_search_queries():
    """生成搜索关键词"""
    week_info = get_current_week_info()
    year = week_info["year"]
    month = week_info["month"]
    
    queries = []
    
    # 笔记本品牌搜索词
    for brand_en, brand_cn in LAPTOP_BRANDS:
        queries.append(f"{brand_cn} 笔记本 {year}年{month}月 新品 发布")
    
    # 平板品牌搜索词
    for brand_en, brand_cn in TABLET_BRANDS:
        queries.append(f"{brand_cn} 平板 {year}年{month}月 新品 发布")
    
    return queries

def update_dashboard():
    """更新看板主逻辑"""
    week_info = get_current_week_info()
    
    print(f"=== 3C行业资讯看板自动更新 ===")
    print(f"时间: {week_info['date_str']}")
    print(f"周期: {week_info['year']}年{week_info['month']}月第{week_info['week_num']}周")
    print(f"({week_info['week_start']} - {week_info['week_end']})")
    print()
    
    # 生成搜索关键词
    queries = generate_search_queries()
    print(f"生成 {len(queries)} 个搜索关键词")
    for i, q in enumerate(queries[:5], 1):
        print(f"  {i}. {q}")
    print(f"  ... 共 {len(queries)} 个")
    print()
    
    # TODO: 调用搜索API获取资讯
    # TODO: 解析并整理新品信息
    # TODO: 更新HTML文件
    
    print("注意: 当前为自动化框架，搜索和内容更新需要手动完成或接入搜索API")
    print()
    
    return True

def create_month_archive():
    """创建月份存档"""
    week_info = get_current_week_info()
    year = week_info["year"]
    month = week_info["month"]
    
    work_dir = Path("/Users/richardj/.openclaw/workspace-judy/pad-dashboard")
    archive_file = work_dir / f"{year}-{month:02d}.html"
    
    if archive_file.exists():
        print(f"月份存档已存在: {archive_file}")
        return
    
    # 复制当前看板作为存档
    current_dashboard = work_dir / "3c-dashboard.html"
    if current_dashboard.exists():
        # 读取当前内容并修改标题
        content = current_dashboard.read_text(encoding='utf-8')
        # 修改标题为存档月份
        content = content.replace(
            f"{year}年{month}月第",
            f"{year}年{month}月存档 - 第"
        )
        archive_file.write_text(content, encoding='utf-8')
        print(f"创建月份存档: {archive_file}")

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
        commit_msg = f"Auto update: {week_info['year']}年{week_info['month']}月第{week_info['week_num']}周"
        result = subprocess.run(["git", "commit", "-m", commit_msg], 
                               cwd=work_dir, capture_output=True, text=True)
        
        if "nothing to commit" in result.stdout or "nothing to commit" in result.stderr:
            print("没有需要提交的更改")
            return True
        
        # 推送
        subprocess.run(["git", "push", "origin", "main"], 
                      cwd=work_dir, check=True, capture_output=True)
        print(f"已推送更新: {commit_msg}")
        return True
        
    except subprocess.CalledProcessError as e:
        print(f"Git操作失败: {e}")
        return False

def send_notification():
    """发送更新通知到飞书群"""
    week_info = get_current_week_info()
    
    message = f"""📊 3C行业资讯看板已更新

周期：{week_info['year']}年{week_info['month']}月第{week_info['week_num']}周
时间：{week_info['week_start']} - {week_info['week_end']}

🔗 在线看板：https://ailsa0826.github.io/pad-dashboard/3c-dashboard.html

请查看最新新品动态和行业资讯。"""
    
    print("通知消息:")
    print(message)
    print()
    
    # TODO: 调用飞书API发送消息
    # chat_id = "oc_a8a566ef39b0ee49aede12872bbc2f90"

def main():
    """主函数"""
    print("=" * 50)
    print("3C行业资讯看板自动更新脚本")
    print("=" * 50)
    print()
    
    # 1. 获取周次信息
    week_info = get_current_week_info()
    
    # 2. 检查是否需要创建月份存档（每月第一周）
    if week_info["week_num"] == 1:
        print("【月份存档】新月第一周，创建上月存档...")
        create_month_archive()
        print()
    
    # 3. 更新看板内容
    print("【内容更新】搜索新品资讯...")
    update_dashboard()
    print()
    
    # 4. 推送更新
    print("【Git推送】推送更新到GitHub...")
    git_push_update()
    print()
    
    # 5. 发送通知
    print("【发送通知】发送更新通知...")
    send_notification()
    print()
    
    print("=" * 50)
    print("自动更新完成")
    print("=" * 50)

if __name__ == "__main__":
    main()
