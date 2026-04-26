---
title: "Vite: Complex multi-file export chaos (TypeScript not recognized)"
tags: [vite, react, typescript, esm, multi-file, cache, bundling]
severity: high
source: personal
project: work-log-ui
env: "Node.js 18, Vite 5, React 18, TypeScript 5"
os: Ubuntu
date: "2026-04-25"
---

# Vite: 複合エラー（複数ファイル分散による export 認識失敗）

| 項目 | 内容 |
|------|------|
| プロジェクト | work-log-ui |
| 環境 | Node.js 18, Vite 5, React 18, TypeScript 5 |
| OS | Ubuntu |
| 発生時期 | コンポーネント・型・ロジックを複数ファイルに分散させた段階 |
| 日時 | 2026-04-25 |

## 症状

複数の症状が同時に発生：

1. **Named Export エラー**
```
The requested module '/src/types/index.ts' does not provide an export named 'WorkLog'
The requested module '/src/components/WorkLogCard.tsx' does not provide an export named 'WorkStatus'
```

2. **TypeScript ファイルがブラウザで認識されない**
```
GET http://localhost:5173/src/components/Header.tsx 404 (Not Found)
GET http://localhost:5173/src/utils/helpers.ts 404 (Not Found)
```

3. **ホットモジュールリロード（HMR）が動作しない**
- ファイル保存時にブラウザが更新されない
- サーバーを再起動してもエラー消えない

## 原因

Vite の ESM（ECMAScript Modules）モジュール解決が、複雑な依存関係を持つ複数ファイル構成に対応できなくなった：

```
App.tsx
  ├── imports → src/components/Header.tsx
  │             ├── imports → src/types/index.ts
  │             └── imports → src/utils/helpers.ts
  ├── imports → src/components/WorkLogCard.tsx
  │             ├── imports → src/types/index.ts
  │             └── imports → src/utils/helpers.ts
  └── imports → src/types/index.ts
```

このような **循環参照** または **相互参照** が生じると：
- Vite のキャッシュ（`node_modules/.vite/`）に矛盾した情報が残る
- モジュール解決が失敗する
- TypeScript の型情報がブラウザに伝わらない
- HMR が機能停止

## 解決策

### 試した失敗パターン（すべて無効）
```bash
# ❌ キャッシュクリア単独
rm -rf node_modules/.vite

# ❌ node_modules 再インストール
rm -rf node_modules && npm install

# ❌ ブラウザキャッシュクリア（Ctrl+Shift+R）

# ❌ dev サーバー再起動
npm run dev

# ❌ TypeScript リコンパイル
tsc --noEmit
```

**これらはすべて一時的な効果しかなく、ファイル保存時に再発する**

### 最終的な解決方法（成功）

**コンポーネント・型・ユーティリティを全て単一ファイルに統合する**

ファイル構成を以下のように変更：

```
src/
├── App.tsx         ← すべてここに集約
└── index.css
```

App.tsx に以下を統合：

```typescript
// types 定義
type Priority = 'high' | 'medium' | 'low';
type WorkStatus = 'completed' | 'in-progress' | 'pending';

interface WorkLog {
  id: string;
  title: string;
  priority: Priority;
  status: WorkStatus;
  date: string;
}

// utility 関数
const getPriorityColor = (priority: Priority): string => {
  const colors: Record<Priority, string> = {
    high: '#cc3300',
    medium: '#cc7700',
    low: '#007700',
  };
  return colors[priority];
};

// コンポーネント
const Header: React.FC = () => {
  return <header style={{ ... }}>Header</header>;
};

const SummaryCards: React.FC<{ logs: WorkLog[] }> = ({ logs }) => {
  return <div>{/* ... */}</div>;
};

const WorkLogCard: React.FC<{ log: WorkLog }> = ({ log }) => {
  return <div>{/* ... */}</div>;
};

// メインアプリケーション
export default function App() {
  const [logs, setLogs] = React.useState<WorkLog[]>([
    // サンプルデータ
  ]);

  return (
    <div>
      <Header />
      <SummaryCards logs={logs} />
      {/* ... */}
    </div>
  );
}
```

### 重要なポイント

1. **初期段階では絶対に複数ファイルに分散しない**
   - `src/App.tsx` にすべてを実装
   - ブラウザで動作確認してから段階的に分割

2. **動作確認後に分割する場合の進め方**
   ```
   Phase 1: 単一ファイル（App.tsx）で動作確認 ✅
   Phase 2: コンポーネント層を src/components/ に分割
   Phase 3: 型定義を src/types/ に集約
   Phase 4: ユーティリティを src/utils/ に分離
   ```
   各フェーズ後に ブラウザで動作確認とキャッシュクリアを実施

3. **複数ファイルが必須な場合の対策**
   - 循環参照を避ける（import の方向を一方向に統一）
   - `index.ts` re-export を使わない（直接 import）
   - 型と実装を同じファイルに保つ

## 予防

- [ ] **初期実装は必ず単一ファイルから始める**（App.tsx）
- [ ] **複数ファイル分散は必要になってから検討**（YAGNIの原則）
- [ ] **Vite キャッシュ定期クリア**（`rm -rf node_modules/.vite`）
- [ ] **複数ファイル間の依存関係を可視化**（import グラフを明示）
- [ ] **型チェック**: `tsc --noEmit` で事前チェック
- [ ] **HMR が動作しなくなったら構成を疑う**（ファイル分散が原因の可能性）

## 参考リンク

- [Vite - Troubleshooting](https://vitejs.dev/guide/troubleshooting.html#full-reload-and-change-not-reflected)
- [ES Modules - Circular Dependencies](https://nodejs.org/en/docs/guides/ecmascript-modules/#circular-module-dependency)
- [TypeScript - ESM Module Resolution](https://www.typescriptlang.org/docs/handbook/esm-node.html)
- [React - Code Splitting Best Practices](https://react.dev/reference/react/lazy#determining-when-to-split)

## メモ

このエラーの本質は「Vite が複雑すぎる構成を解決できない」ことにある。Vite は単純な構成を得意とするツールであり、無理に複雑化させると破綻する。

**解決のポイント**：最初はシンプルに。複雑さは段階的に増やす。

**記録者**: dev-nodee  
**更新日**: 2026-04-25
