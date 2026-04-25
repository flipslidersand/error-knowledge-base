# [エラーメッセージ / 現象をここに記載]

## 基本情報

| 項目 | 内容 |
|------|------|
| **プロジェクト** | [プロジェクト名] |
| **環境** | Python 3.11 / Node.js 18 / など |
| **OS** | macOS 13 / Ubuntu 22.04 / Windows 11 |
| **発生時期** | [セットアップ時 / 実行時 / テスト時 / デプロイ時] |
| **日時** | YYYY-MM-DD HH:MM |

---

## 症状

何が起きたのか、具体的に描写してください。

```
[エラーメッセージ / スタックトレース をコピペ]
```

---

## 原因

根本的な原因は何だったのか。

- [ ] 環境問題（Python バージョン、PATH など）
- [ ] 依存関係の問題（パッケージ未インストール、バージョン競合）
- [ ] 設定ファイルの問題（.env、config 等）
- [ ] コードロジック
- [ ] ネットワーク / API
- [ ] その他

---

## 解決策

**やったこと** と **結果** を書いてください。

### 試したこと（失敗したもの）
1. [試した方法 1]
   - 結果: 失敗 / 変わらず

2. [試した方法 2]
   - 結果: 失敗

### 最終的に解決した方法
[うまくいった方法]

```bash
# 実際のコマンド例
pip install --upgrade package-name
# または
export PYTHONPATH=/path/to/module:$PYTHONPATH
```

---

## 予防

**次から踏まないための対策チェックリスト**

- [ ] ドキュメントに記載する
- [ ] セットアップスクリプトに追加する
- [ ] CI/CD で自動検出する
- [ ] チームに周知する
- [ ] テストケースを追加する

### 具体例

```python
# requirements.txt
package-name==X.Y.Z  # バージョン固定しないと競合する

# .env.example
DATABASE_URL=postgresql://user:pass@localhost/dbname
```

---

## 参考リンク

- [公式ドキュメント](https://example.com)
- [StackOverflow の同じ質問](https://stackoverflow.com)
- [GitHub Issue](https://github.com/org/repo/issues/123)
- [関連するエラー記録](./other-error.md)

---

## メモ

追加情報・補足事項があれば。

---

**記録者**: [名前 or ユーザー名]  
**更新日**: YYYY-MM-DD
