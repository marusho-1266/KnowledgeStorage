from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime, date, time

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your-secret-key-here'
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://knowledge_user:knowledge_password@10.194.2.150:3307/knowledge_db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

class KnowledgeBase(db.Model):
    __tablename__ = 'knowledge_base'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255), nullable=False)
    response_date = db.Column(db.Date, nullable=False, default=date.today)  # 対応日
    area = db.Column(db.String(100), nullable=False, default='')  # エリア
    department = db.Column(db.String(100), nullable=False)  # 部署
    requester = db.Column(db.String(100), nullable=False)   # 問い合わせ者名
    inquiry_type = db.Column(db.String(50), nullable=False, default='その他')  # 問い合わせ区分
    content = db.Column(db.Text, nullable=False)  # 内容
    respondent = db.Column(db.String(100), nullable=False, default='')  # 対応者
    response_time = db.Column(db.Time, nullable=False, default=time(0, 0))  # 対応時間
    response_content = db.Column(db.Text, nullable=False, default='')  # 回答内容
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

# 問い合わせ区分の選択肢
INQUIRY_TYPES = ['メール', '電話', 'その他']

# エリアと部署の選択肢の定義
AREAS = [
    '高知本社', '営業本部', '本社企画', '東京支店', '四国中央', 
    'その他', '配送拠点', '東日本', '九州', 'アクトヒューマンケア'
]

DEPARTMENTS_BY_AREA = {
    '高知本社': ['経理', '営業事務', 'WEB', 'ｹｱｻﾌﾟﾗｲ', '営業支援', '仕入'],
    '営業本部': ['営業', '営業企画'],
    '本社企画': ['企画'],
    '東京支店': ['営業'],
    '四国中央': ['物流管理'],
    'その他': ['東海営業', '岡山営業', '広島営業', '徳島営業', '福岡営業'],
    '配送拠点': ['西日本', '福島倉庫', '横浜倉庫', '八尾', '福岡倉庫', '松山倉庫'],
    '東日本': ['営業事務'],
    '九州': ['WEB', 'FAX'],
    'アクトヒューマンケア': ['愛媛', '福岡']
}

# 対応時間の選択肢（15分刻み）
def generate_time_options():
    options = []
    for hour in range(25):  # 0時から24時まで
        for minute in [0, 15, 30, 45]:
            if hour == 24 and minute > 0:
                continue  # 24時以降は24:00のみ
            options.append(f"{hour:02d}:{minute:02d}")
    return options

TIME_OPTIONS = generate_time_options()

def parse_date(date_str):
    """日付文字列をdate型に変換する"""
    if not date_str:
        return date.today()
    try:
        return datetime.strptime(date_str, '%Y-%m-%d').date()
    except ValueError:
        return date.today()

def parse_time(time_str):
    """時間文字列をtime型に変換する"""
    if not time_str:
        return time(0, 0)
    try:
        return datetime.strptime(time_str, '%H:%M').time()
    except ValueError:
        return time(0, 0)

@app.route('/')
def index():
    knowledge_entries = KnowledgeBase.query.all()
    return render_template('index.html', knowledge_entries=knowledge_entries)

@app.route('/add', methods=['GET', 'POST'])
def add_knowledge():
    if request.method == 'POST':
        # 基本情報の取得
        title = request.form.get('title')
        department = request.form.get('department')
        requester = request.form.get('requester')
        content = request.form.get('content')
        
        # 新規フィールドの取得
        response_date_str = request.form.get('response_date')
        area = request.form.get('area')
        inquiry_type = request.form.get('inquiry_type')
        respondent = request.form.get('respondent')
        response_time_str = request.form.get('response_time')
        response_content = request.form.get('response_content')

        # 必須項目のバリデーション
        if not title or not department or not requester or not content:
            flash('タイトル、部署、問い合わせ者名、内容は必須です。', 'error')
            return redirect(url_for('add_knowledge'))
        
        # 日付と時間の変換
        response_date = parse_date(response_date_str)
        response_time = parse_time(response_time_str)
        
        # 問い合わせ区分のバリデーション
        if inquiry_type not in INQUIRY_TYPES:
            inquiry_type = 'その他'

        # 新規エントリの作成
        new_entry = KnowledgeBase(
            title=title,
            response_date=response_date,
            area=area or '',
            department=department,
            requester=requester,
            inquiry_type=inquiry_type,
            content=content,
            respondent=respondent or '',
            response_time=response_time,
            response_content=response_content or ''
        )

        try:
            db.session.add(new_entry)
            db.session.commit()
            flash('ナレッジが正常に追加されました。', 'success')
            return redirect(url_for('index'))
        except Exception as e:
            db.session.rollback()
            flash(f'エラーが発生しました: {str(e)}', 'error')
            return redirect(url_for('add_knowledge'))

    # GETリクエスト時のデフォルト値
    today = date.today().strftime('%Y-%m-%d')
    return render_template('add.html', today=today, inquiry_types=INQUIRY_TYPES, 
                          areas=AREAS, departments_by_area=DEPARTMENTS_BY_AREA, 
                          time_options=TIME_OPTIONS)

@app.route('/edit/<int:id>', methods=['GET', 'POST'])
def edit_knowledge(id):
    entry = KnowledgeBase.query.get_or_404(id)
    
    if request.method == 'POST':
        # 基本情報の取得
        title = request.form.get('title')
        department = request.form.get('department')
        requester = request.form.get('requester')
        content = request.form.get('content')
        
        # 新規フィールドの取得
        response_date_str = request.form.get('response_date')
        area = request.form.get('area')
        inquiry_type = request.form.get('inquiry_type')
        respondent = request.form.get('respondent')
        response_time_str = request.form.get('response_time')
        response_content = request.form.get('response_content')

        # 必須項目のバリデーション
        if not title or not department or not requester or not content:
            flash('タイトル、部署、問い合わせ者名、内容は必須です。', 'error')
            return redirect(url_for('edit_knowledge', id=id))
        
        # 日付と時間の変換
        response_date = parse_date(response_date_str)
        response_time = parse_time(response_time_str)
        
        # 問い合わせ区分のバリデーション
        if inquiry_type not in INQUIRY_TYPES:
            inquiry_type = 'その他'

        try:
            # フィールドの更新
            entry.title = title
            entry.response_date = response_date
            entry.area = area or ''
            entry.department = department
            entry.requester = requester
            entry.inquiry_type = inquiry_type
            entry.content = content
            entry.respondent = respondent or ''
            entry.response_time = response_time
            entry.response_content = response_content or ''
            
            db.session.commit()
            flash('ナレッジが正常に更新されました。', 'success')
            return redirect(url_for('index'))
        except Exception as e:
            db.session.rollback()
            flash(f'エラーが発生しました: {str(e)}', 'error')
            return redirect(url_for('edit_knowledge', id=id))

    # 日付と時間をフォーム用に文字列に変換
    response_date_str = entry.response_date.strftime('%Y-%m-%d')
    response_time_str = entry.response_time.strftime('%H:%M')
    
    return render_template('edit.html', entry=entry, 
                          response_date=response_date_str, 
                          response_time=response_time_str,
                          inquiry_types=INQUIRY_TYPES,
                          areas=AREAS, departments_by_area=DEPARTMENTS_BY_AREA,
                          time_options=TIME_OPTIONS)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True) 