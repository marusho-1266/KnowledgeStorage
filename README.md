# AIヘルプデスク ナレッジ蓄積システム

このプロジェクトは、AIヘルプデスク用のナレッジ蓄積システムです。

## 必要条件

- Python 3.8以上
- Docker
- Docker Compose

## セットアップ方法

1. リポジトリをクローン
```bash
git clone [repository-url]
cd [repository-name]
```

2. Python仮想環境の作成と有効化
```bash
# 仮想環境の作成
python -m venv venv

# 仮想環境の有効化（Windows）
venv\Scripts\activate

# 必要なパッケージのインストール
pip install -r requirements.txt
```

3. Dockerコンテナの起動
```bash
docker-compose up -d
```

4. アプリケーションの起動
```bash
python app.py
```

## アクセス方法

### ローカルアクセス
- URL: http://localhost:5000

### 外部アクセス
- URL: http://[サーバーのIPアドレス]:5000
- ポート: 5000（Flaskアプリケーション）
- ポート: 3307（MySQL）

## データベース接続情報
- ホスト: localhost
- ポート: 3307
- データベース名: knowledge_db
- ユーザー名: knowledge_user
- パスワード: knowledge_password

## データベース構造

### テーブル一覧

1. knowledge_base
   - id: INT (PRIMARY KEY)
   - title: VARCHAR(255)
   - content: TEXT
   - category_id: INT (FOREIGN KEY)
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
- 外部アクセスを許可する場合は、ファイアウォールでポート5000と3307を開放してください
- 本番環境では、`debug=True`を無効にすることを推奨します 