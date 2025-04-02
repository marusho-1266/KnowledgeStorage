-- カテゴリーテーブルの作成
CREATE TABLE IF NOT EXISTS categories (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    description TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- ナレッジベーステーブルの作成
CREATE TABLE IF NOT EXISTS knowledge_base (
    id INT AUTO_INCREMENT PRIMARY KEY,
    title VARCHAR(255) NOT NULL,
    content TEXT NOT NULL,
    category_id INT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (category_id) REFERENCES categories(id)
);

-- インデックスの作成
CREATE INDEX idx_category_id ON knowledge_base(category_id);
CREATE INDEX idx_created_at ON knowledge_base(created_at);

-- サンプルカテゴリの挿入
INSERT INTO categories (name, description) VALUES
('一般', '一般的な質問や回答'),
('技術', '技術的な質問や回答'),
('運用', '運用に関する質問や回答'),
('トラブルシューティング', 'トラブルシューティングに関する質問や回答'); 