import os
from flask import Flask, render_template, request, redirect, url_for, flash, session
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash


app = Flask(__name__, template_folder='templates')
app.secret_key = 'your_secret_key'  # セッションやフラッシュメッセージ用の秘密鍵

# データベースのURI設定（instanceフォルダ内のデータベースファイルを指定）
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True  # SQLログの出力を有効にする（デバッグ用）
db = SQLAlchemy(app)

# ユーザーモデルの定義
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), nullable=False, unique=True)
    password = db.Column(db.String(150), nullable=False)

# データベースの初期化
with app.app_context():
    db.create_all()

@app.route('/', methods=['GET', 'POST'])
def main():
    if request.method == 'POST':
        # フォームや特定の操作に対応（ここでは特に何もしない）
        return redirect(url_for('register'))  # POST時に/registerにリダイレクト

    # GETリクエスト時のHTMLレスポンス
    return '''
        <h1>ようこそ！</h1>
        <form action="/register" method="get">
            <button type="submit">登録ページへ</button>
        </form>
    '''

# 登録ページ
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        hashed_password = generate_password_hash(password)  # デフォルトで pbkdf2:sha256

        new_user = User(username=username, password=hashed_password)

        try:
            db.session.add(new_user)
            db.session.commit()
            flash('登録が成功しました！ログインしてください。')
            return redirect(url_for('login'))
        except:
            flash('ユーザー名が既に存在しています。')
            return redirect(url_for('register'))
    return render_template('register.html')

# ログインページ
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        user = User.query.filter_by(username=username).first()
        if user and check_password_hash(user.password, password):
            session['user_id'] = user.id
            flash('ログイン成功！')
            return redirect(url_for('home'))
        else:
            flash('ユーザー名またはパスワードが違います。')
    return render_template('login.html')

# ホームページ（ログイン後）
@app.route('/home')
def home():
    if 'user_id' in session:
        return render_template('home.html')
    else:
        flash('ログインしてください。')
        return redirect(url_for('login'))

# ログアウト
@app.route('/logout')
def logout():
    session.pop('user_id', None)
    flash('ログアウトしました。')
    return redirect(url_for('login'))

@app.route('/health', methods=['GET', 'POST'])
def health():
    if 'user_id' in session:
        return render_template('health.html')
    else:
        flash('ログインしてください。')
        return redirect(url_for('login'))


if __name__ == "__main__":
    # Flaskのインスタンスフォルダがない場合は作成
    if not os.path.exists(app.instance_path):
        os.makedirs(app.instance_path)
    app.run(debug=True)
