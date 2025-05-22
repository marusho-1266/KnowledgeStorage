-- 各ステップを条件付きで実行するように修正

-- カラムの存在確認と追加を動的SQLで実行
-- response_date カラムの追加
SET @column_exists = 0;
SELECT COUNT(*) INTO @column_exists FROM INFORMATION_SCHEMA.COLUMNS 
WHERE TABLE_SCHEMA = DATABASE() AND TABLE_NAME = 'knowledge_base' AND COLUMN_NAME = 'response_date';
SET @query = IF(@column_exists = 0, 'ALTER TABLE knowledge_base ADD COLUMN response_date DATE NOT NULL DEFAULT (CURRENT_DATE)', 'SELECT 1');
PREPARE stmt FROM @query;
EXECUTE stmt;
DEALLOCATE PREPARE stmt;

-- area カラムの追加
SET @column_exists = 0;
SELECT COUNT(*) INTO @column_exists FROM INFORMATION_SCHEMA.COLUMNS 
WHERE TABLE_SCHEMA = DATABASE() AND TABLE_NAME = 'knowledge_base' AND COLUMN_NAME = 'area';
SET @query = IF(@column_exists = 0, 'ALTER TABLE knowledge_base ADD COLUMN area VARCHAR(100) NOT NULL DEFAULT \'\'', 'SELECT 1');
PREPARE stmt FROM @query;
EXECUTE stmt;
DEALLOCATE PREPARE stmt;

-- inquiry_type カラムの追加
SET @column_exists = 0;
SELECT COUNT(*) INTO @column_exists FROM INFORMATION_SCHEMA.COLUMNS 
WHERE TABLE_SCHEMA = DATABASE() AND TABLE_NAME = 'knowledge_base' AND COLUMN_NAME = 'inquiry_type';
SET @query = IF(@column_exists = 0, 'ALTER TABLE knowledge_base ADD COLUMN inquiry_type VARCHAR(50) NOT NULL DEFAULT \'その他\'', 'SELECT 1');
PREPARE stmt FROM @query;
EXECUTE stmt;
DEALLOCATE PREPARE stmt;

-- respondent カラムの追加
SET @column_exists = 0;
SELECT COUNT(*) INTO @column_exists FROM INFORMATION_SCHEMA.COLUMNS 
WHERE TABLE_SCHEMA = DATABASE() AND TABLE_NAME = 'knowledge_base' AND COLUMN_NAME = 'respondent';
SET @query = IF(@column_exists = 0, 'ALTER TABLE knowledge_base ADD COLUMN respondent VARCHAR(100) NOT NULL DEFAULT \'\'', 'SELECT 1');
PREPARE stmt FROM @query;
EXECUTE stmt;
DEALLOCATE PREPARE stmt;

-- response_time カラムの追加
SET @column_exists = 0;
SELECT COUNT(*) INTO @column_exists FROM INFORMATION_SCHEMA.COLUMNS 
WHERE TABLE_SCHEMA = DATABASE() AND TABLE_NAME = 'knowledge_base' AND COLUMN_NAME = 'response_time';
SET @query = IF(@column_exists = 0, 'ALTER TABLE knowledge_base ADD COLUMN response_time TIME NOT NULL DEFAULT \'00:00:00\'', 'SELECT 1');
PREPARE stmt FROM @query;
EXECUTE stmt;
DEALLOCATE PREPARE stmt;

-- response_content カラムの追加
SET @column_exists = 0;
SELECT COUNT(*) INTO @column_exists FROM INFORMATION_SCHEMA.COLUMNS 
WHERE TABLE_SCHEMA = DATABASE() AND TABLE_NAME = 'knowledge_base' AND COLUMN_NAME = 'response_content';
SET @query = IF(@column_exists = 0, 'ALTER TABLE knowledge_base ADD COLUMN response_content TEXT NOT NULL DEFAULT \'\'', 'SELECT 1');
PREPARE stmt FROM @query;
EXECUTE stmt;
DEALLOCATE PREPARE stmt;

-- 既存データの対応日を作成日に設定（response_dateが存在する場合のみ）
SET @column_exists = 0;
SELECT COUNT(*) INTO @column_exists FROM INFORMATION_SCHEMA.COLUMNS 
WHERE TABLE_SCHEMA = DATABASE() AND TABLE_NAME = 'knowledge_base' AND COLUMN_NAME = 'response_date';
SET @query = IF(@column_exists > 0, 'UPDATE knowledge_base SET response_date = DATE(created_at) WHERE response_date IS NULL OR response_date = \'0000-00-00\'', 'SELECT 1');
PREPARE stmt FROM @query;
EXECUTE stmt;
DEALLOCATE PREPARE stmt;

-- category_backup テーブルが存在するか確認
SET @table_exists = 0;
SELECT COUNT(*) INTO @table_exists FROM INFORMATION_SCHEMA.TABLES 
WHERE TABLE_SCHEMA = DATABASE() AND TABLE_NAME = 'category_backup';

-- category_backup テーブルがない場合のみ作成
SET @query = IF(@table_exists = 0, 'CREATE TABLE category_backup (id INT, category_name VARCHAR(100))', 'SELECT 1');
PREPARE stmt FROM @query;
EXECUTE stmt;
DEALLOCATE PREPARE stmt;

-- category_backup テーブルにデータがあるか確認
SET @has_data = 0;
SET @query = IF(@table_exists > 0, 'SELECT COUNT(*) INTO @has_data FROM category_backup', 'SET @has_data = 0');
PREPARE stmt FROM @query;
EXECUTE stmt;
DEALLOCATE PREPARE stmt;

-- category_id カラムの有無を確認
SET @column_exists = 0;
SELECT COUNT(*) INTO @column_exists FROM INFORMATION_SCHEMA.COLUMNS 
WHERE TABLE_SCHEMA = DATABASE() AND TABLE_NAME = 'knowledge_base' AND COLUMN_NAME = 'category_id';

-- カテゴリのバックアップ（category_idが存在し、バックアップテーブルが空の場合のみ）
SET @query = IF(@column_exists > 0 AND @has_data = 0, 
                'INSERT INTO category_backup SELECT kb.id, c.name FROM knowledge_base kb LEFT JOIN categories c ON kb.category_id = c.id', 
                'SELECT 1');
PREPARE stmt FROM @query;
EXECUTE stmt;
DEALLOCATE PREPARE stmt;

-- 外部キー制約の存在確認
SET @fk_exists = 0;
SELECT COUNT(*) INTO @fk_exists FROM INFORMATION_SCHEMA.KEY_COLUMN_USAGE
WHERE TABLE_SCHEMA = DATABASE() AND TABLE_NAME = 'knowledge_base' 
  AND REFERENCED_TABLE_NAME = 'categories' AND CONSTRAINT_NAME = 'knowledge_base_ibfk_1';

-- 外部キー制約を削除（存在する場合のみ）
SET @query = IF(@fk_exists > 0, 
                'ALTER TABLE knowledge_base DROP FOREIGN KEY knowledge_base_ibfk_1', 
                'SELECT 1');
PREPARE stmt FROM @query;
EXECUTE stmt;
DEALLOCATE PREPARE stmt;

-- category_id カラムを削除（存在する場合のみ）
SET @query = IF(@column_exists > 0, 
                'ALTER TABLE knowledge_base DROP COLUMN category_id', 
                'SELECT 1');
PREPARE stmt FROM @query;
EXECUTE stmt;
DEALLOCATE PREPARE stmt; 