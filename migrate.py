import mysql.connector
import os
from dotenv import load_dotenv

# 環境変数の読み込み
load_dotenv()

# データベース接続情報
db_config = {
    'host': os.getenv('DB_HOST', '10.194.2.38'),
    'port': int(os.getenv('DB_PORT', '3307')),
    'user': os.getenv('DB_USER', 'knowledge_user'),
    'password': os.getenv('DB_PASSWORD', 'knowledge_password'),
    'database': os.getenv('DB_NAME', 'knowledge_db')
}

def execute_migration():
    """マイグレーションSQLを実行する関数"""
    conn = None
    cursor = None
    
    try:
        # データベースに接続
        print("データベースに接続しています...")
        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor()
        
        # データベースのバックアップを推奨
        print("注意: 続行する前にデータベースのバックアップを取得することを強く推奨します")
        confirmation = input("マイグレーションを実行しますか？ (yes/no): ")
        
        if confirmation.lower() != 'yes':
            print("マイグレーションがキャンセルされました")
            return
        
        # マイグレーションSQLファイルを読み込む
        print("マイグレーションSQLを読み込んでいます...")
        with open('migration.sql', 'r', encoding='utf-8') as file:
            sql_commands = file.read().split(';')
            
            # 各SQLコマンドを実行
            for command in sql_commands:
                if command.strip():
                    print(f"実行中: {command[:50]}...")  # 最初の50文字のみ表示
                    cursor.execute(command)
            
            # コミット
            conn.commit()
            print("マイグレーションが正常に完了しました")
    
    except Exception as e:
        if conn:
            conn.rollback()
        print(f"エラーが発生しました: {str(e)}")
    
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()

if __name__ == "__main__":
    execute_migration() 