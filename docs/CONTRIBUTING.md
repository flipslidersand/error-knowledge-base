# 貢献ガイド（CONTRIBUTING）

このリポジトリへのエラー記録に際し、以下のガイドをお読みください。

---

## エラー記録の基本

### 目的

このリポジトリは、実装中に踏んだエラーを**ナレッジ化**し、  
チーム全体が同じ問題を回避できるようにするためのものです。

### 記録者

- 個人環境で開発中にエラーを経験した人
- チーム内の誰もが記録者になれます

---

## ステップバイステップ

### 1. テンプレートを使う

```bash
cp ERROR_TEMPLATE.md errors/[category]/[error-name].md
```

**カテゴリ選択**:
- `python/` - Python, pip, venv など
- `javascript/` - Node.js, npm, JavaScript など
- `database/` - SQL, MongoDB, PostgreSQL など
- `deployment/` - GitHub Actions, CI/CD, デプロイなど
- `system/` - OS, 環境変数、PATH, 権限など
- `other/` - その他

### 2. 情報を記入

テンプレートの各セクションを埋めてください：

#### 基本情報
```markdown
| 項目 | 内容 |
|------|------|
| **プロジェクト** | work-log-ui など、関連するプロジェクト名 |
| **環境** | Python 3.11, Node.js 18 など |
| **OS** | macOS 13, Ubuntu 22.04 など |
| **発生時期** | セットアップ時、実行時、テスト時、デプロイ時など |
| **日時** | 2024-04-25 14:30 |
```

#### 症状
実際のエラーメッセージをコピペしてください。  
個人情報は必ずマスキングすること（後述）。

```markdown
## 症状

ModuleNotFoundError: No module named 'numpy'

Traceback (most recent call last):
  File "main.py", line 1, in <module>
    import numpy
ModuleNotFoundError: No module named 'numpy'
```

#### 原因
根本的な原因を分析してください。  
複数当てはまる場合は複数選択 OK。

- [ ] 環境問題（Python バージョン、PATH など）
- [ ] 依存関係の問題（パッケージ未インストール、バージョン競合）
- [ ] 設定ファイルの問題（.env、config 等）
- [ ] その他

#### 解決策
**重要**: 試したすべての方法（失敗含む）と、最終的に成功した方法の両方を書いてください。

```markdown
### 試したこと（失敗したもの）
1. `pip install numpy` 直後の import
   - 結果: 失敗。インストールがスキップされていた模様

### 最終的に解決した方法
venv を再作成してから numpy をインストール
```

#### 予防
次から踏まないための対策を書いてください。

```markdown
- [ ] 開発ガイドに venv 再作成手順を追加
- [ ] requirements.txt に numpy を明示的に記載
- [ ] CI で venv キャッシュをクリアするオプション追加
```

### 3. 個人情報をマスキング

**公開リポジトリなので、以下は絶対に含めないでください：**

#### パスワード・トークン

❌ **WRONG**:
```
Authentication failed: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIxMjM0NTY3ODkwIn0.dozjgNryP4J3jVmNHl0w5N_XgL0n3I9PlFUP0THsR8U
```

✅ **CORRECT**:
```
Authentication failed: Invalid [JWT_TOKEN]
```

#### ホスト名・IP アドレス

❌ **WRONG**:
```
Failed to connect to prod-db-01.internal.company.com:5432
```

✅ **CORRECT**:
```
Failed to connect to [INTERNAL_DB_HOST]:5432
```

#### ユーザー ID

❌ **WRONG**:
```
Permission denied for user id_12345@company.com
```

✅ **CORRECT**:
```
Permission denied for user [USER_EMAIL]
```

#### 会社固有の情報

❌ **WRONG**:
```
Error in finance/salary-calc.py
Configuration loaded from /home/jiro/work/company-projects/
```

✅ **CORRECT**:
```
Error in [INTERNAL_MODULE]
Configuration loaded from [PROJECT_PATH]
```

#### チェックリスト

記録する前に必ず確認：

- [ ] パスワード、API キー、トークンは含まない
- [ ] 内部サーバーのホスト名や IP は含まない
- [ ] 実名や従業員 ID は含まない
- [ ] 会社のシステム名や機密情報は含まない

---

## ファイル命名規則

```
errors/[category]/[error-type]-[brief-description].md

例:
- errors/python/import-error-module-not-found.md
- errors/database/connection-timeout-postgresql.md
- errors/deployment/github-actions-build-failure.md
- errors/javascript/node-gyp-compilation-failed.md
- errors/system/permission-denied-venv-activation.md
```

**ルール**:
- 小文字のみ
- スペースはハイフン (`-`) で表現
- アンダースコア (`_`) は避ける
- 簡潔に（30 文字程度）

---

## Git コミット時のメッセージ

記録追加時：
```bash
git commit -m "docs: add error record for [brief-description]"
```

既存記録の更新：
```bash
git commit -m "docs: update error record - [filename] - [what changed]"
```

重複記録の削除：
```bash
git commit -m "docs: remove duplicate error record - [filename]"
```

---

## 記録後のチェック

### GitHub への Push 前

```bash
# 差分確認
git diff

# ファイル内容確認
cat errors/[category]/[filename].md

# 個人情報のダブルチェック
grep -i "password\|token\|api.key\|@company.com\|internal\|prod-db" errors/[category]/[filename].md
```

個人情報が含まれていなければ OK。

### Push 後

- [ ] GitHub のリポジトリで見えるか確認
- [ ] Web UI に反映されているか確認（30 秒待機）

---

## よくある間違いと対策

| 間違い | 問題 | 対策 |
|-------|------|------|
| パスワードをコピペ | 公開 → セキュリティリスク | push 前に grep で検索 |
| エラーメッセージ全文コピー | 個人情報が含まれる可能性 | 重要な部分だけ抽出、マスキング |
| 関係ない情報まで書く | 検索性が低下 | テンプレート項目に絞る |
| 記録を更新しない | 古い情報が残る | 解決後は「予防」項目を追加更新 |

---

## 記録後にさらに情報が増えた場合

既存記録に追記する場合：

```bash
# ファイルを編集
nano errors/[category]/[filename].md

# 記述例：参考リンクを追加
## 参考リンク
- [既存リンク 1]
- [新しく見つけたリンク 2]  ← 追記

# コミット
git add errors/[category]/[filename].md
git commit -m "docs: add reference link to [filename]"
git push
```

---

## デリケートな情報

**会社の営業秘密やビジネス上のデータについて**:

記録を避けるべき例：
- ❌ 会社の売上データ、契約条件
- ❌ 顧客名や顧客データ
- ❌ プロダクトロードマップや未公開機能
- ❌ セキュリティ脆弱性の詳細

代わりにできること：
- ✅ 技術的なエラー内容に絞る
- ✅ 会社固有の情報はマスキング
- ✅ 必要なら Slack の秘密チャネルで別途共有

---

## 質問・相談

記録に迷った場合：

1. **個人情報が不確かな場合** → マスキングする（疑わしきは記載しない）
2. **エラーの原因が不明な場合** → 「原因: 不明」と記載し、試した方法と結果のみ書く
3. **記録すべきかわからない場合** → Slack で相談 or ドラフトとして残す

---

## 記録例（テンプレート記入済み）

```markdown
# Python venv activation でエラーが出る

## 基本情報

| 項目 | 内容 |
|------|------|
| **プロジェクト** | work-log-ui |
| **環境** | Python 3.11, Ubuntu 22.04 |
| **OS** | Ubuntu 22.04 LTS |
| **発生時期** | セットアップ時 |
| **日時** | 2024-04-20 09:30 |

---

## 症状

```bash
$ source venv/bin/activate
bash: venv/bin/activate: No such file or directory
```

venv が存在しているのに activate スクリプトが見つからないエラー。

---

## 原因

- [x] 環境問題（Python バージョン、PATH など）

venv ディレクトリは存在していたが、前回のテスト実行時に不完全なまま残されていた。

---

## 解決策

### 試したこと（失敗したもの）

1. 存在するディレクトリを確認
   ```bash
   ls -la venv/
   ```
   - 結果: `bin/` ディレクトリがない。venv が不完全な状態

2. venv を `python -m venv` で再作成しようとした
   ```bash
   python -m venv venv
   ```
   - 結果: 失敗。既に venv ディレクトリが存在するというエラー

### 最終的に解決した方法

不完全な venv を削除し、新規作成

```bash
# 古い venv を削除
rm -rf venv/

# 新しく venv を作成
python -m venv venv

# activate スクリプトが正しく生成されたか確認
ls -la venv/bin/activate

# 有効化
source venv/bin/activate
```

---

## 予防

- [ ] セットアップドキュメントに「venv 再作成手順」を追加
- [ ] CI/CD で venv キャッシュをクリアするオプションを検討
- [ ] team の人全員に周知する

---

## 参考リンク

- [Python venv 公式ドキュメント](https://docs.python.org/3/library/venv.html)
- [StackOverflow - venv activate not found](https://stackoverflow.com/questions/XXXXX)

---

**記録者**: Flying_Jester  
**更新日**: 2024-04-20
```

---

## 感謝

このリポジトリに貢献いただきありがとうございます！  
ナレッジの共有で、チーム全体の開発効率が向上します。
