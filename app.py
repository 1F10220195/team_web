import os
from flask import Flask, render_template, request, redirect, url_for, flash, session, jsonify
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from langchain_community.chat_models import ChatOpenAI
from langchain.schema import HumanMessage


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

chat = ChatOpenAI(
    openai_api_key='84Wr7FR0h14mT3k90dHAtUu7fIHdz8EgkKfnixMCg0QvOK6QcRvAlCk16mSNZtznQTTgta7AXKeCyKMzQNGZ4_g',
    openai_api_base='https://api.openai.iniad.org/api/v1',
    model_name='gpt-4o-mini',
    temperature=0
)

# APIルート
@app.route('/analyze', methods=['POST'])
def analyze():
    # ユーザー入力を取得
    food_input = request.json.get("food_input", "")
    
    # ChatGPTにクエリを送信
    messages = [HumanMessage(content=f"{food_input}を食べました。不足する栄養素と補う食品、料理の例を教えてください。")]
    result = chat(messages)
    
    # 結果を返す
    return jsonify({"result": result.content})




@app.route('/', methods=['GET', 'POST'])
def main():
    if request.method == 'POST':
        return redirect(url_for('register'))  # POST時に/registerにリダイレクト
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
        hashed_password = generate_password_hash(password)

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
  

# ホーム画面ルート
@app.route('/advice')
def advice():
    return render_template('index.html')


# 新しいルート: health.htmlを表示するルート
@app.route('/health')
def health():
    if 'user_id' in session:
        return render_template('health.html')
    else:
        flash('ログインしてください。')
        return redirect(url_for('login'))

# ログアウト
@app.route('/logout')
def logout():
    session.pop('user_id', None)
    flash('ログアウトしました。')
    return redirect(url_for('login'))

if __name__ == "__main__":
    if not os.path.exists(app.instance_path):
        os.makedirs(app.instance_path)
    app.run(debug=True)

