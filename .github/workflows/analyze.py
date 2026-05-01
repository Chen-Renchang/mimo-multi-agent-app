"""
代码库健康度扫描 Agent（MiMo 适配原型）
纯 Python 标准库，模拟多步推理与长链分析逻辑，生成结构化报告。
"""
import os, json, time, subprocess
from datetime import datetime
from collections import Counter

def run_git_log():
    """获取最近 30 天的提交信息（模拟 Agent 信息采集步骤）"""
    try:
        result = subprocess.run(
            ["git", "log", "--since=30.days", "--pretty=format:%an|%s|%ad", "--date=short"],
            capture_output=True, text=True
        )
        return result.stdout.strip().split("\n") if result.stdout else []
    except:
        return []

def analyze_commits(logs):
    """模拟长链推理：提交类型分析、活跃度评估"""
    authors = Counter()
    types = Counter()
    for line in logs:
        if "|" not in line:
            continue
        author, msg, date = line.split("|", 2)
        authors[author] += 1
        # 简单推断提交类型
        if msg.lower().startswith("fix") or "bug" in msg.lower():
            types["修复"] += 1
        elif msg.lower().startswith("feat") or "add" in msg.lower():
            types["新增功能"] += 1
        elif msg.lower().startswith("refactor"):
            types["重构"] += 1
        elif msg.lower().startswith("docs"):
            types["文档"] += 1
        else:
            types["其他"] += 1

    return {
        "提交总数": len(logs),
        "贡献者": dict(authors.most_common()),
        "提交类型分布": dict(types),
        "活跃度评价": "优秀 👏" if len(logs) > 20 else ("一般 👍" if len(logs) > 5 else "不足 ⚠️")
    }

def scan_project_structure():
    """扫描项目文件结构，评估可维护性（模拟 Agent 感知环境）"""
    structure = {}
    for root, dirs, files in os.walk("."):
        if ".git" in root or "public" in root:
            continue
        for f in files:
            ext = os.path.splitext(f)[1]
            structure[ext] = structure.get(ext, 0) + 1
    return structure

def generate_recommendations(stats, structure):
    """根据分析结果生成优化建议（Agent 的最终决策输出）"""
    recs = []
    if stats["提交总数"] < 5:
        recs.append("🔔 提交频率偏低，建议保持日常小步提交。")
    if "README.md" not in os.listdir("."):
        recs.append("📄 缺少 README.md，请添加项目说明文档。")
    if ".py" in structure and "requirements.txt" not in os.listdir("."):
        recs.append("🐍 Python 项目建议包含 requirements.txt 声明依赖。")
    if not recs:
        recs.append("✅ 当前仓库结构健康，继续保持！")
    return recs

def generate_html(report):
    """生成最终静态报告页面"""
    html = f"""<!DOCTYPE html>
<html lang="zh">
<head>
    <meta charset="UTF-8">
    <title>代码库健康度报告 - {datetime.now().strftime('%Y-%m-%d')}</title>
    <style>
        body {{ font-family: system-ui; max-width: 800px; margin: auto; padding: 2rem; background: #f8f9fa; }}
        h1 {{ color: #2c3e50; }}
        .card {{ background: white; border-radius: 12px; padding: 1.5rem; margin: 1rem 0; box-shadow: 0 2px 5px rgba(0,0,0,0.1); }}
        .metric {{ font-size: 2rem; font-weight: bold; color: #3498db; }}
        .badge {{ background: #eaf2f8; padding: 0.3rem 0.6rem; border-radius: 20px; font-size: 0.85rem; }}
        .warning {{ color: #e67e22; }}
    </style>
</head>
<body>
    <h1>🩺 代码库健康度扫描报告</h1>
    <p>扫描时间：{report['timestamp']}</p>
    
    <div class="card">
        <h2>📊 提交活跃度</h2>
        <p class="metric">{report['commit_stats']['提交总数']}</p>
        <p>近30天提交次数</p>
        <p>活跃度评价：{report['commit_stats']['活跃度评价']}</p>
        <h3>贡献者排行榜</h3>
        <ul>
"""
    for author, count in report['commit_stats']['贡献者'].items():
        html += f"<li>{author}: {count} commits</li>"
    html += f"""</ul>
        <h3>提交类型</h3>
        <ul>
"""
    for t, c in report['commit_stats']['提交类型分布'].items():
        html += f"<li>{t}: {c} 次</li>"
    html += f"""</ul>
    </div>

    <div class="card">
        <h2>📁 项目结构</h2>
        <ul>
"""
    for ext, count in report['file_distribution'].items():
        html += f"<li>.{ext}: {count} 个文件</li>"
    html += """</ul>
    </div>

    <div class="card">
        <h2>💡 智能优化建议</h2>
        <ul>
"""
    for rec in report['recommendations']:
        html += f"<li class=\"warning\">{rec}</li>"
    html += """</ul>
    </div>
    
    <p style="text-align:center; margin-top:2rem; color:#7f8c8d;">
        由 MiMo Multi-Agent 健康度扫描 Agent 自动生成 | 适配 MiMo 大模型长链推理
    </p>
</body>
</html>"""
    return html

def main():
    print("🚀 Agent 启动：开始多步推理分析...")
    time.sleep(0.3)
    # 步骤1：信息采集
    logs = run_git_log()
    # 步骤2：提交分析
    commit_stats = analyze_commits(logs)
    # 步骤3：结构扫描
    file_dist = scan_project_structure()
    # 步骤4：生成建议
    recommendations = generate_recommendations(commit_stats, file_dist)
    
    report = {
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "commit_stats": commit_stats,
        "file_distribution": file_dist,
        "recommendations": recommendations
    }
    
    # 输出报告到 public 目录（供 Pages 发布）
    os.makedirs("public/report", exist_ok=True)
    html = generate_html(report)
    with open("public/report/index.html", "w", encoding="utf-8") as f:
        f.write(html)
    
    # 同时保存 JSON 备用
    with open("public/report/report.json", "w") as f:
        json.dump(report, f, indent=2, ensure_ascii=False)
    
    print("✅ 报告已生成，准备发布至 GitHub Pages。")

if __name__ == "__main__":
    main()
