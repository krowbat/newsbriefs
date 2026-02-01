# 新闻简报系统

自动生成和发布新闻简报到 GitHub Pages。

## 使用方法

### 方式1：通过 JSON 文件

创建一个 JSON 文件（例如 `news.json`），格式如下：

```json
{
  "date": "2026-02-01",
  "sources": ["BBC", "CNN", "The Guardian", "Al Jazeera", "CBC"],
  "items": [
    {
      "title": "爱泼斯坦文件持续发酵",
      "sources": ["BBC", "CNN"],
      "points": [
        "第二位受害者称2010年被送往英国与安德鲁王子会面",
        "文件显示爱泼斯坦向曼德尔森相关账户转账75,000美元",
        "律师称政府处理文件方式'令人愤慨'"
      ]
    },
    {
      "title": "俄乌冲突升级",
      "sources": ["Guardian"],
      "points": [
        "俄罗斯无人机袭击乌克兰矿工巴士，至少12人死亡",
        "俄军打击造成更多平民伤亡"
      ]
    }
  ]
}
```

然后运行：

```bash
python3 publish-brief.py news.json
```

### 方式2：通过管道（推荐自动化）

```bash
echo '{"date":"2026-02-01","items":[]}' | python3 publish-brief.py
```

## 输出

脚本会：
1. ✅ 生成 HTML 文件
2. ✅ 保存到 newsbriefs 目录
3. ✅ Git commit
4. ✅ Push 到 GitHub
5. 📖 返回可访问的 URL

## 生成的 URL

`https://krowbat.github.io/newsbriefs/news-brief-2026-02-01.html`

## 添加到 Instapaper

访问上面的 URL 后，用 Instapaper 扩展保存即可。

---

*Created by Krowbat 🦇*