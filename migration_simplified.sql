-- 簡略化したマイグレーションスクリプト
-- 現在の状態では、ほとんどのカラムはすでに追加されていますが、
-- category_idカラムがまだ残っている可能性があります。

-- category_id カラムを削除（もし存在すれば）
ALTER TABLE knowledge_base DROP COLUMN category_id; 