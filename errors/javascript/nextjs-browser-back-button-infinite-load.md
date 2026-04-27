---
title: "Next.js: Browser back button causes infinite loading state"
tags: [nextjs, react, state-management, browser-navigation, async]
severity: high
source: personal
project: decision-log-system
env: "Node.js 18, Next.js 14, React 18, TypeScript"
os: Ubuntu
date: "2026-04-19"
---

# Next.js: ブラウザ戻るボタンで無限ローディング状態

| 項目 | 内容 |
|------|------|
| プロジェクト | decision-log-system |
| 環境 | Node.js 18, Next.js 14, React 18, TypeScript |
| OS | Ubuntu |
| 発生時期 | 実行時（ブラウザ操作時） |
| 日時 | 2026-04-19 |

## 症状

詳細ページからダッシュボードに戻るときにブラウザの戻るボタンを使用すると、ページが無限ローディング状態のままハングする。F5（完全リロード）を押すまで応答しない。

```
ブラウザ戻るボタン → 詳細ページから脱出
→ ページが loading 状態のまま動かない
→ F5 リロードで初めて解放される
```

## 原因

- ✅ **マウント/アンマウント時のレースコンディション**
  - ブラウザ戻るボタン使用時に、コンポーネント破棄と非同期処理の完了タイミングがズレる
- ✅ **アンマウント後の状態更新試行**
  - 破棄されたコンポーネントに対して state を設定しようとする
- ✅ **メモリリーク：クローズされない Promise**
  - fetch 完了後の state 更新が pending のまま残る
- ✅ **cleanup 欠落**
  - useEffect で適切に cleanup 関数を定義していない

## 解決策

### 1. DecisionLogList Component に `mountedRef` を追加

```typescript
// components/DecisionLogList.tsx
import { useEffect, useRef, useState } from 'react';

export function DecisionLogList() {
  const [isLoading, setIsLoading] = useState(true);
  const mountedRef = useRef(true);  // ← マウント状態を追跡

  useEffect(() => {
    mountedRef.current = true;
    return () => {
      mountedRef.current = false;  // ← アンマウント時に false に
    };
  }, []);

  const fetchLogs = async () => {
    try {
      const data = await fetch('/api/logs');
      // アンマウント後は state 更新しない
      if (mountedRef.current) {
        setIsLoading(false);
      }
    } catch (error) {
      if (mountedRef.current) {
        setIsLoading(false);
      }
    }
  };

  return <div>{isLoading ? 'Loading...' : '...'}</div>;
}
```

### 2. Timeout 機構で強制的にローディングを終了

```typescript
// hooks/useDecisionLogs.ts
const [loadingTimeout, setLoadingTimeout] = useState<NodeJS.Timeout | null>(null);

useEffect(() => {
  // 5 秒でタイムアウト
  const timeout = setTimeout(() => {
    if (mountedRef.current && isLoading) {
      setIsLoading(false);
      setError('Loading took too long. Please refresh.');
    }
  }, 5000);

  setLoadingTimeout(timeout);

  return () => {
    clearTimeout(timeout);
  };
}, []);
```

### 3. useAuth Hook で isMounted フラグを使用

```typescript
// hooks/useAuth.ts
const [isMounted, setIsMounted] = useState(false);

useEffect(() => {
  setIsMounted(true);
  return () => setIsMounted(false);
}, []);

const login = async (email: string, password: string) => {
  try {
    const result = await supabaseClient.auth.signInWithPassword({
      email,
      password,
    });
    if (isMounted) {
      setUser(result.data.user);
    }
  } catch (error) {
    if (isMounted) {
      setError(error.message);
    }
  }
};
```

### 4. AbortController で fetch をキャンセル（推奨）

```typescript
// より堅牢な実装
useEffect(() => {
  const controller = new AbortController();

  const fetchData = async () => {
    try {
      const res = await fetch('/api/logs', {
        signal: controller.signal,  // ← キャンセル可能に
      });
      const data = await res.json();
      setIsLoading(false);
    } catch (error) {
      if (error.name !== 'AbortError') {
        setError(error);
      }
    }
  };

  fetchData();

  return () => {
    controller.abort();  // ← アンマウント時に自動キャンセル
  };
}, []);
```

## 予防

- [ ] **常に mountedRef または isMounted フラグを使用**
  - useEffect 内の非同期処理では必須
  - アンマウント後の state 更新を防止

- [ ] **Timeout 機構を実装**
  - fetch が遅い場合の安全弁として
  - ユーザーへのエラーメッセージ表示

- [ ] **AbortController でキャンセル処理を統合**
  - 最も安全で標準的な実装方法
  - 不要な network リクエストも自動キャンセル

- [ ] **cleanup 関数を必ず定義**
  ```typescript
  useEffect(() => {
    // ... 処理
    return () => {
      // cleanup: タイマー、fetch キャンセル等
    };
  }, []);
  ```

- [ ] **ナビゲーションテスト**
  - ブラウザ戻るボタン時の状態確認
  - router.back() + 非同期処理の組み合わせテスト

## 参考リンク

- [React Docs - useEffect cleanup](https://react.dev/reference/react/useEffect#cleaning-up-an-effect)
- [MDN - AbortController](https://developer.mozilla.org/en-US/docs/Web/API/AbortController)
- [Next.js - Data Fetching Patterns](https://nextjs.org/docs/app/building-your-application/data-fetching)

## メモ

このエラーは「コンポーネント設計の問題」ではなく「非同期処理のライフサイクル管理」の問題。ブラウザ戻るボタンは特にマウント/アンマウントのタイミングが予測しづらいため、常に mountedRef または AbortController での対策が必須。

**記録者**: dev-nodee  
**更新日**: 2026-04-27
