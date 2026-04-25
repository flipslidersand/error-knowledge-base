#!/usr/bin/env python3
"""
Markdown エラー記録を HTML に変換して GitHub Pages 用に出力
"""
import os
import markdown
from pathlib import Path
from datetime import datetime

def build():
    build_dir = Path("build")
    build_dir.mkdir(exist_ok=True)
    
    errors_dir = Path("errors")
    
    # インデックス HTML を作成
    index_html = """<!DOCTYPE html>
<html lang="ja">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Error Knowledge Base</title>
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body { font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif; 
               background: #f5f5f5; color: #333; line-height: 1.6; }
        .container { max-width: 900px; margin: 0 auto; padding: 20px; }
        h1 { margin: 20px 0; color: #222; }
        .category { background: white; border-radius: 8px; padding: 20px; margin: 20px 0; 
                   box-shadow: 0 2px 4px rgba(0,0,0,0.1); }
        .category h2 { color: #0066cc; margin-bottom: 15px; font-size: 1.3em; }
        .error-list { list-style: none; }
        .error-list li { padding: 10px 0; border-bottom: 1px solid #eee; }
        .error-list li:last-child { border-bottom: none; }
        .error-list a { color: #0066cc; text-decoration: none; }
        .error-list a:hover { text-decoration: underline; }
        footer { text-align: center; margin-top: 40px; color: #666; font-size: 0.9em; }
    </style>
</head>
<body>
    <div class="container">
        <h1>🔍 Error Knowledge Base</h1>
        <p>実装中に踏んだエラーをナレッジ化したリポジトリです。</p>
        <hr style="margin: 20px 0; border: none; border-top: 1px solid #ddd;">
"""
    
    # カテゴリごとに HTML を生成
    for category_dir in sorted(errors_dir.iterdir()):
        if not category_dir.is_dir():
            continue
        
        category_name = category_dir.name
        md_files = sorted(category_dir.glob("*.md"))
        
        if not md_files:
            continue
        
        index_html += f'        <div class="category">\n'
        index_html += f'            <h2>📁 {category_name.upper()}</h2>\n'
        index_html += '            <ul class="error-list">\n'
        
        for md_file in md_files:
            html_name = md_file.stem + ".html"
            index_html += f'                <li><a href="{category_name}/{html_name}">{md_file.stem}</a></li>\n'
        
        index_html += '            </ul>\n'
        index_html += '        </div>\n'
    
    index_html += f"""        <footer>
            <p>Last updated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</p>
            <p><a href="https://github.com">GitHub Repository</a></p>
        </footer>
    </div>
</body>
</html>
"""
    
    (build_dir / "index.html").write_text(index_html)
    
    # 各 Markdown ファイルを HTML に変換
    for category_dir in errors_dir.iterdir():
        if not category_dir.is_dir():
            continue
        
        category_name = category_dir.name
        output_dir = build_dir / category_name
        output_dir.mkdir(exist_ok=True)
        
        for md_file in category_dir.glob("*.md"):
            html_content = markdown.markdown(
                md_file.read_text(encoding="utf-8"),
                extensions=['tables', 'fenced_code', 'codehilite']
            )
            
            full_html = f"""<!DOCTYPE html>
<html lang="ja">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{md_file.stem}</title>
    <style>
        * {{ margin: 0; padding: 0; box-sizing: border-box; }}
        body {{ font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif; 
               background: #f5f5f5; color: #333; line-height: 1.6; }}
        .container {{ max-width: 900px; margin: 0 auto; padding: 20px; background: white; 
                    border-radius: 8px; box-shadow: 0 2px 8px rgba(0,0,0,0.1); }}
        h1 {{ color: #222; margin: 20px 0 10px; }}
        h2 {{ color: #0066cc; margin: 20px 0 10px; font-size: 1.2em; }}
        code {{ background: #f4f4f4; padding: 2px 6px; border-radius: 3px; 
               font-family: 'Monaco', 'Courier New', monospace; }}
        pre {{ background: #f4f4f4; padding: 15px; border-radius: 5px; overflow-x: auto; margin: 10px 0; }}
        pre code {{ background: none; padding: 0; }}
        a {{ color: #0066cc; text-decoration: none; }}
        a:hover {{ text-decoration: underline; }}
        .meta {{ color: #666; font-size: 0.9em; margin-bottom: 20px; }}
        .back {{ margin-bottom: 20px; }}
        .back a {{ color: #0066cc; }}
        table {{ border-collapse: collapse; width: 100%; margin: 15px 0; }}
        th, td {{ border: 1px solid #ddd; padding: 10px; text-align: left; }}
        th {{ background: #f4f4f4; font-weight: bold; }}
    </style>
</head>
<body>
    <div class="container">
        <div class="back"><a href="../">← インデックスに戻る</a></div>
        <div class="meta">カテゴリ: <strong>{category_name}</strong></div>
        {html_content}
    </div>
</body>
</html>
"""
            (output_dir / (md_file.stem + ".html")).write_text(full_html, encoding="utf-8")
    
    print(f"✅ Build complete: {build_dir}/index.html")

if __name__ == "__main__":
    build()
