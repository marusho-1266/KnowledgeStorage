# AIヘルプデスク ナレッジ蓄積システム仕様書

## 1. プロジェクト概要
AIヘルプデスク用のナレッジ蓄積システム。

## 2. 必要条件
- Python 3.8以上
- Docker
- Docker Compose

## 3. セットアップ方法
```bash
git clone [repository-url]
cd [repository-name]
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
docker-compose up -d
python app.py
```

## 4. アクセス方法
- ローカルアクセス: http://localhost:5000
- 外部アクセス: http://[サーバーのIPアドレス]:5000

## 5. 技術スタック
- Flask==3.0.2
- Flask-SQLAlchemy==3.1.1
- PyMySQL==1.1.0
- python-dotenv==1.0.1
- MySQL 8.0
- Bootstrap 5.3

## 6. データベース接続情報
- ホスト: localhost
- ポート: 3307
- データベース名: knowledge_db
- ユーザー名: knowledge_user
- パスワード: knowledge_password

## 7. データベース構造
### テーブル一覧
1. categories
   - id: INT (PRIMARY KEY)
   - name: VARCHAR(100)
   - description: TEXT
   - created_at: TIMESTAMP

2. knowledge_base
   - id: INT (PRIMARY KEY)
   - title: VARCHAR(255)
   - content: TEXT
   - department: VARCHAR(100)
   - requester: VARCHAR(100)
   - category_id: INT (FOREIGN KEY)
   - created_at: TIMESTAMP
   - updated_at: TIMESTAMP

### サンプルカテゴリ
- 一般: 一般的な質問や回答
- 技術: 技術的な質問や回答
- 運用: 運用に関する質問や回答
- トラブルシューティング: トラブルシューティングに関する質問や回答

## 8. アプリケーション概要
### 8.1. 主要機能
- ナレッジの登録、編集、削除
- カテゴリ管理
- ナレッジ一覧表示

### 8.2. ルーティング
- `/`: ナレッジ一覧表示
- `/add`: ナレッジ追加画面
- `/edit/<int:id>`: ナレッジ編集画面

### 8.3. テンプレート
- `templates/index.html`: ナレッジ一覧画面
- `templates/add.html`: ナレッジ追加画面
- `templates/edit.html`: ナレッジ編集画面
- `templates/base.html`: ベーステンプレート

## 9. 自動起動の設定方法
### Windowsでの設定手順
1. タスクスケジューラーを開く
2. 基本タスクの作成
   - 名前: `KnowledgeStorage`
   - 説明: `AIヘルプデスク ナレッジ蓄積システムの自動起動`
3. トリガーの設定
   - 「コンピューターの起動時」を選択
4. アクションの設定
   - プログラム/スクリプト: `[プロジェクトのパス]\start_app.bat` を指定
5. 完了
6. タスクの詳細設定
   - 「全般」タブで「最上位の特権で実行する」にチェック
   - 「設定」タブで「タスクが失敗した場合は再起動する」にチェック

## 10. 注意事項
- 本番環境では、必ずパスワードを変更してください
- 定期的なバックアップを推奨します
- セキュリティ設定は必要に応じて調整してください
- 外部アクセスを許可する場合は、ファイアウォールでポート5000と3307を開放してください
- 本番環境では、`debug=True`を無効にすることを推奨します
