---
title: "Vite: The requested module does not provide an export named 'Priority'"
tags: [vite, react, typescript, esm, named-export, cache, module-resolution]
severity: medium
project: work-log-ui
env: "Node.js 18, Vite 5, React 18, TypeScript 5"
os: Ubuntu
date: "2026-04-25"
---

# Vite: モジュール named export エラー（Priority 認識されない）

| 項目 | 内容 |
|------|------|
| プロジェクト | work-log-ui |
| 環境 | Node.js 18, Vite 5, React 18, TypeScript 5 |
| OS | Ubuntu |
| 発生時期 | 初期セットアップ時（型定義分散）|
| 日時 | 2026-04-25 |

## 症状

ブラウザコンソールで以下のエラーが表示：

```
The requested module '/src/types/workLog.ts' does not provide an export named 'Priority'
```

App.tsx で `Priority` 型を import しようとすると、モジュール解決が失敗する。

```typescript
// 失敗した例
import { Priority } from './types/workLog';  // ❌ エラー
```

## 原因

- ✅ 型定義を複数ファイルに分散（`src/types/workLog.ts` + 他ファイル）
- Vite のモジュール解決機構がファイル間の import/export 関係を正しく追跡できない
- Vite キャッシュ（`.vite` フォルダ）に古い状態が残っている
- ESM モジュール解決で複雑な依存関係が競合

## 解決策

### 試した失敗パターン
```bash
# ❌ キャッシュクリアのみでは不十分
rm -rf node_modules/.vite
npm run dev  # 再度エラー

# ❌ node_modules 再インストールも効かない場合がある
rm -rf node_modules && npm install
npm run dev
```

### 最終的な解決方法（成功）

**型定義を単一ファイルに統合する**

```typescript
// src/utils/workLogUtils.ts に統一
export type Priority = 'high' | 'medium' | 'low';
export type WorkStatus = 'completed' | 'in-progress' | 'pending';
export interface WorkLog {
  id: string;
  title: string;
  priority: Priority;
  status: WorkStatus;
  date: string;
}

// その他のユーティリティ関数もここに定義
export const getPriorityColor = (priority: Priority): string => {
  // ...
};
```

App.tsx で import:
```typescript
import { Priority, WorkStatus, WorkLog, getPriorityColor } from './utils/workLogUtils';
```

### 重要なポイント

1. **複数の型定義ファイルを避ける**
   - `src/types/workLog.ts`、`src/types/index.ts` など複数ファイルの分散は避ける
   - すべて 1 ファイルに統合

2. **初期セットアップは単一ファイル実装**
   - `src/App.tsx` にコンポーネント・型・ロジックをまとめる
   - 動作確認後に段階的に分割

## 予防

- [ ] **初期段階では単一ファイル実装を原則とする**
- [ ] **型定義は絶対に複数ファイル分散しない**
- [ ] **Vite キャッシュを定期的にクリア**（`rm -rf node_modules/.vite`）
- [ ] **ブラウザのハードリロード**（Ctrl+Shift+R）を習慣化
- [ ] **型チェック**: TypeScript コンパイラで `tsc --noEmit` を実行し、エラーを事前に検出

## 参考リンク

- [Vite - Troubleshooting](https://vitejs.dev/guide/troubleshooting.html)
- [ES Modules - Module resolution](https://nodejs.org/en/docs/guides/ecmascript-modules/)
- [TypeScript - Module Resolution](https://www.typescriptlang.org/docs/handbook/module-resolution.html)

## メモ

このエラーは「モジュール自体が壊れている」のではなく、Vite のキャッシュ・モジュール解決の問題である。ファイル構成をシンプルにすることで根本的に解決できる。

**記録者**: dev-nodee  
**更新日**: 2026-04-25
