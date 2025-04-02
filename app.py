from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your-secret-key-here'
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://knowledge_user:knowledge_password@127.0.0.1:3307/knowledge_db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

class Category(db.Model):
    __tablename__ = 'categories'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class KnowledgeBase(db.Model):
    __tablename__ = 'knowledge_base'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255), nullable=False)
    content = db.Column(db.Text, nullable=False)
    department = db.Column(db.String(100), nullable=False)  # 部署
    requester = db.Column(db.String(100), nullable=False)   # 問い合わせ者名
    category_id = db.Column(db.Integer, db.ForeignKey('categories.id'))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # カテゴリとの関連付けを追加
    category = db.relationship('Category', backref=db.backref('knowledge_entries', lazy=True))

@app.route('/')
def index():
    categories = Category.query.all()
    knowledge_entries = KnowledgeBase.query.all()
    # カテゴリのマッピングを作成
    category_map = {category.id: category.name for category in categories}
    return render_template('index.html', 
                         categories=categories, 
                         knowledge_entries=knowledge_entries,
                         category_map=category_map)

@app.route('/add', methods=['GET', 'POST'])
def add_knowledge():
    if request.method == 'POST':
        title = request.form.get('title')
        content = request.form.get('content')
        department = request.form.get('department')
        requester = request.form.get('requester')
        category_id = request.form.get('category_id')

        if not title or not content or not department or not requester:
            flash('タイトル、内容、部署、問い合わせ者名は必須です。', 'error')
            return redirect(url_for('add_knowledge'))

        # カテゴリの存在確認
        category = Category.query.get(category_id)
        if not category:
            flash('有効なカテゴリを選択してください。', 'error')
            return redirect(url_for('add_knowledge'))

        new_entry = KnowledgeBase(
            title=title,
            content=content,
            department=department,
            requester=requester,
            category_id=category_id
        )

        try:
            db.session.add(new_entry)
            db.session.commit()
            flash('ナレッジが正常に追加されました。', 'success')
            return redirect(url_for('index'))
        except Exception as e:
            db.session.rollback()
            flash('エラーが発生しました。', 'error')
            return redirect(url_for('add_knowledge'))

    categories = Category.query.all()
    return render_template('add.html', categories=categories)

@app.route('/edit/<int:id>', methods=['GET', 'POST'])
def edit_knowledge(id):
    entry = KnowledgeBase.query.get_or_404(id)
    
    if request.method == 'POST':
        title = request.form.get('title')
        content = request.form.get('content')
        department = request.form.get('department')
        requester = request.form.get('requester')
        category_id = request.form.get('category_id')

        if not title or not content or not department or not requester:
            flash('タイトル、内容、部署、問い合わせ者名は必須です。', 'error')
            return redirect(url_for('edit_knowledge', id=id))

        # カテゴリの存在確認
        category = Category.query.get(category_id)
        if not category:
            flash('有効なカテゴリを選択してください。', 'error')
            return redirect(url_for('edit_knowledge', id=id))

        try:
            entry.title = title
            entry.content = content
            entry.department = department
            entry.requester = requester
            entry.category_id = category_id
            db.session.commit()
            flash('ナレッジが正常に更新されました。', 'success')
            return redirect(url_for('index'))
        except Exception as e:
            db.session.rollback()
            flash('エラーが発生しました。', 'error')
            return redirect(url_for('edit_knowledge', id=id))

    categories = Category.query.all()
    return render_template('edit.html', entry=entry, categories=categories)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True) 