# AIヘルプデスク ナレッジ蓄積システム

このプロジェクトは、AIヘルプデスク用のナレッジ蓄積システムです。

## 必要条件

- Docker
- Docker Compose

## セットアップ方法

1. リポジトリをクローン
```bash
git clone [repository-url]
cd [repository-name]
```

2. Dockerコンテナの起動
```bash
docker-compose up -d
```

3. データベース接続情報
- ホスト: localhost
- ポート: 3306
- データベース名: knowledge_db
- ユーザー名: knowledge_user
- パスワード: knowledge_password

## データベース構造

### テーブル一覧

1. knowledge_base
   - id: INT (PRIMARY KEY)
   - title: VARCHAR(255)
   - content: TEXT
   - category: VARCHAR(100)
   - created_at: TIMESTAMP
   - updated_at: TIMESTAMP

2. categories
   - id: INT (PRIMARY KEY)
   - name: VARCHAR(100)
   - description: TEXT
   - created_at: TIMESTAMP

## 注意事項

- 本番環境では、必ずパスワードを変更してください
- 定期的なバックアップを推奨します
- セキュリティ設定は必要に応じて調整してください 