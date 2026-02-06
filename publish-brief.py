#!/usr/bin/env python3
"""
发布新闻简报到 GitHub Pages

用法:
    python3 publish-brief.py [内容JSON文件]
    或直接提供新闻内容

示例:
    python3 publish-brief.py news_content.json
"""

import json
import subprocess
import sys
from datetime import datetime
from pathlib import Path

# 配置
NEWSBRIEFS_DIR = Path.home() / "Desktop" / "newsbriefs"
REPO_URL = "git@github.com:krowbat/newsbriefs.git"
GITHUB_PAGES_BASE = "https://krowbat.github.io/newsbriefs/"


def read_content_from_stdin():
    """从标准输入读取新闻内容（JSON格式）"""
    try:
        content = sys.stdin.read()
        return json.loads(content)
    except json.JSONDecodeError:
        print("❌ 无效的JSON格式")
        sys.exit(1)


def generate_html(content):
    """根据新闻内容生成HTML"""
    date_str = content.get("date", datetime.now().strftime("%Y-%m-%d"))
    items = content.get("items", [])
    sources = content.get("sources", [])

    html = f"""<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>新闻简报 - {date_str}</title>
    <style>
        body {{
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
            max-width: 800px;
            margin: 40px auto;
            padding: 0 20px;
            line-height: 1.6;
            color: #333;
        }}
        h1 {{
            color: #e63946;
            border-bottom: 3px solid #e63946;
            padding-bottom: 10px;
        }}
        .date {{
            color: #666;
            font-size: 0.9em;
            margin-bottom: 40px;
        }}
        h2 {{
            color: #1d3557;
            margin-top: 40px;
            border-left: 4px solid #e63946;
            padding-left: 15px;
        }}
        .news-item {{
            background: #f8f9fa;
            padding: 20px;
            border-radius: 8px;
            margin: 20px 0;
        }}
        .news-item h3 {{
            color: #457b9d;
            margin-top: 0;
        }}
        .news-item ul {{
            margin-top: 15px;
            padding-left: 20px;
        }}
        .source {{
            color: #a8dadc;
            font-weight: bold;
        }}
        .summary {{
            color: #555;
            font-style: italic;
            border-left: 3px solid #457b9d;
            padding-left: 12px;
            margin: 10px 0;
            background: #e9f5ff;
            padding: 10px;
            border-radius: 4px;
        }}
        .news-link {{
            color: #457b9d;
            text-decoration: none;
            border-bottom: 1px dashed #457b9d;
        }}
        .news-link:hover {{
            color: #e63946;
            border-bottom-style: solid;
        }}
        hr {{
            border: none;
            border-top: 2px solid #eee;
            margin: 40px 0;
        }}
        .footer {{
            color: #666;
            font-style: italic;
            margin-top: 40px;
        }}
    </style>
</head>
<body>
    <h1>📰 新闻简报</h1>
    <p class="date"><strong>{date_str}</strong></p>

    <hr>

    <h2>🔴 头条新闻</h2>

"""

    for idx, item in enumerate(items, 1):
        title = item.get("title", "")
        points = item.get("points", [])
        sources_list = item.get("sources", [])

        # 添加概括（如果有）
        summary = item.get("summary", "")

        # 添加标题链接（如果有）
        url = item.get("url", "")
        if url:
            title_html = f'<a href="{url}" target="_blank" class="news-link">{idx}. {title}</a>'
        else:
            title_html = f"{idx}. {title}"

        # 添加概括（如果有）
        summary = item.get("summary", "")

        html += f"""
    <div class="news-item">
        <h3>{title_html}</h3>
        {f'<p class="summary">{summary}</p>' if summary else ''}
        {f'<p><span class="source">来源: {", ".join(sources_list)}</span></p>' if sources_list else ''}
"""
        if points:
            html += "        <ul>\n"
            for point in points:
                html += f"            <li>{point}</li>\n"
            html += "        </ul>\n"

        html += "    </div>\n"

    if sources:
        html += f"""
    <hr>

    <p><strong>数据来源:</strong> {', '.join(sources)}</p>
"""

    html += """
    <p class="footer">由 Krowbat 🦇 为你整理</p>
</body>
</html>
"""
    return html


def save_and_publish(html, date=None):
    """保存HTML文件并推送到GitHub"""
    if date is None:
        date = datetime.now().strftime("%Y-%m-%d")

    filename = f"news-brief-{date}.html"
    filepath = NEWSBRIEFS_DIR / filename

    # 保存文件
    filepath.write_text(html, encoding="utf-8")
    print(f"✅ 文件已保存: {filepath}")

    # Git 操作
    try:
        # 添加文件
        subprocess.run(
            ["git", "add", filename],
            cwd=NEWSBRIEFS_DIR,
            check=True,
            capture_output=True,
        )

        # 提交
        commit_msg = f"Add news brief for {date}"
        subprocess.run(
            ["git", "commit", "-m", commit_msg],
            cwd=NEWSBRIEFS_DIR,
            check=True,
            capture_output=True,
        )

        # 推送
        subprocess.run(
            ["git", "push"],
            cwd=NEWSBRIEFS_DIR,
            check=True,
            capture_output=True,
        )

        print("✅ 已推送到GitHub")

        # 返回 GitHub Pages URL
        url = f"{GITHUB_PAGES_BASE}{filename}"
        print(f"\n📖 简报链接: {url}")
        print(f"\n💾 Instapaper URL: https://www.instapaper.com/text?url={url}")

        return url

    except subprocess.CalledProcessError as e:
        print(f"❌ Git操作失败: {e.stderr.decode()}")
        sys.exit(1)


def main():
    content = None

    # 优先从文件读取
    if len(sys.argv) > 1:
        content_file = Path(sys.argv[1])
        if content_file.exists():
            content = json.loads(content_file.read_text(encoding="utf-8"))
        else:
            print(f"❌ 文件不存在: {content_file}")
            sys.exit(1)

    # 其次从标准输入读取（支持管道）
    elif not sys.stdin.isatty():
        content = read_content_from_stdin()

    else:
        print("❌ 请提供JSON文件内容")
        print("\n用法:")
        print("  python3 publish-brief.py < content.json")
        print('  或: echo \'{"date":"2026-02-01","items":[]}\' | python3 publish-brief.py')
        sys.exit(1)

    # 生成HTML并发布
    html = generate_html(content)
    save_and_publish(html, content.get("date"))


if __name__ == "__main__":
    main()