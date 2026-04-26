---
title: "Vite: GET /src/index.css net::ERR_ABORTED 500 (Tailwind CSS v4 PostCSS)"
tags: [vite, react, tailwind, postcss, css, v4, configuration]
severity: high
project: work-log-ui
env: "Node.js 18, Vite 5, Tailwind CSS v4"
os: Ubuntu
date: "2026-04-25"
---

# Vite: CSS 500 エラー（Tailwind v4 PostCSS 設定不正）

| 項目 | 内容 |
|------|------|
| プロジェクト | work-log-ui |
| 環境 | Node.js 18, Vite 5, Tailwind CSS v4 |
| OS | Ubuntu |
| 発生時期 | CSS フレームワーク導入時 |
| 日時 | 2026-04-25 |

## 症状

ブラウザコンソールに以下のエラー：

```
GET http://localhost:5173/src/index.css net::ERR_ABORTED 500 (Internal Server Error)
```

ターミナルには `postcss` エラーが出力：

```
Error [ERR_MODULE_NOT_FOUND]: Cannot find module 'tailwindcss'
```

あるいは：

```
PostCSS plugin error: Unknown word in @tailwind directive
```

CSS が読み込まれず、ページが完全にスタイルなし状態で表示される。

## 原因

Tailwind CSS v4 では PostCSS の設定方式が変更された：

- ✅ **v3 (旧方式)**: `tailwind.config.js` + `postcss.config.js` を手動で設定
- ✅ **v4 (新方式)**: PostCSS が不要。CSS ファイルで `@import 'tailwindcss'` を使用

このプロジェクトでは旧方式の設定（`postcss.config.js`、`tailwind.config.js`）がある状態で Tailwind v4 を導入しようとしたため、プラグイン認識エラーが発生した。

さらに `index.css` に `@tailwind` directives が残っていると、PostCSS が処理方法を見失う。

## 解決策

### 試した失敗パターン
```bash
# ❌ postcss-cli をインストール（v4 では不要）
npm install postcss postcss-cli
npm run dev  # 相変わらずエラー

# ❌ Tailwind を再インストール
npm uninstall tailwindcss && npm install tailwindcss
npm run dev  # 相変わらずエラー
```

### 最終的な解決方法（成功）

**Tailwind と PostCSS 関連の設定ファイルを完全削除する**

```bash
# 設定ファイルを削除
rm -f postcss.config.js
rm -f tailwind.config.js

# node_modules を再インストール（クリーンな状態で）
rm -rf node_modules && npm install

# Vite キャッシュをクリア
rm -rf node_modules/.vite

# 開発サーバー再起動
npm run dev
```

**CSS ファイルから `@tailwind` directives を削除**

```css
/* src/index.css - 変更前（失敗） */
@import 'tailwindcss/base';
@import 'tailwindcss/components';
@import 'tailwindcss/utilities';

body {
  margin: 0;
  padding: 0;
}
```

```css
/* src/index.css - 変更後（成功） */
body {
  margin: 0;
  padding: 0;
  font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
}

button {
  cursor: pointer;
  border: none;
  padding: 8px 12px;
  border-radius: 4px;
}

/* など、シンプルな CSS のみ */
```

### 代替手段

Tailwind が不要な場合（このプロジェクトでは不要）：

```typescript
// React コンポーネント内で inline styles を使用
const buttonStyle = {
  padding: '8px 12px',
  backgroundColor: '#0066cc',
  color: 'white',
  border: 'none',
  borderRadius: '4px',
  cursor: 'pointer',
};

<button style={buttonStyle}>Click me</button>
```

## 予防

- [ ] **Tailwind CSS の導入は慎重に**
  - v4 ではバージョン仕様を確認してから導入する
  - 公式ドキュメント: https://tailwindcss.com/docs/installation
- [ ] **PostCSS 設定は最小限に**
  - 単純な CSS で十分なら無理に導入しない
- [ ] **Vite の CSS 処理フロー確認**
  - `vite.config.js` で CSS 関連の設定を明示的に行わない（デフォルトで十分）
- [ ] **CSS エラーが出たら設定ファイルを疑う**
  - `postcss.config.js` が存在するか確認
  - 不要な PostCSS プラグインが入っていないか確認

## 参考リンク

- [Tailwind CSS v4 Installation Guide](https://tailwindcss.com/docs/installation)
- [Vite - CSS](https://vitejs.dev/guide/features.html#css)
- [PostCSS Documentation](https://postcss.org/)
- [Tailwind CSS v3 → v4 Migration](https://tailwindcss.com/docs/v4-migration)

## メモ

Tailwind CSS v4 では PostCSS が**デフォルトで不要**になった。この点が大きな変更である。設定ファイルが存在すると逆に問題になるため、完全削除が必須。このプロジェクトでは Inline Styles または Vanilla CSS で十分な UI レベルであるため、Tailwind 導入は保留。

**記録者**: dev-nodee  
**更新日**: 2026-04-25
