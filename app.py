# 必要なライブラリのインポート
import os  # 環境変数取得用
import random  # ランダム選択用
import google.generativeai as genai  # Gemini AI API用
from flask import Flask, render_template, request, session, redirect, url_for, flash

# Flaskアプリケーションの初期化
app = Flask(__name__)
# セッション管理用の秘密鍵を設定
# 本番環境では環境変数、開発環境では固定値を使用
app.secret_key = os.getenv('SECRET_KEY', os.urandom(24))

# Gemini AI APIの設定
# 環境変数からAPIキーを取得して設定
try:
    api_key = os.getenv('GEMINI_API_KEY')
    if not api_key:
        raise ValueError("GEMINI_API_KEY環境変数が設定されていません")
    genai.configure(api_key=api_key)
    model = genai.GenerativeModel('gemini-2.0-flash-exp')
except Exception as e:
    print(f"⚠️ Gemini API初期化エラー: {e}")
    print("環境変数GEMINI_API_KEYを設定してください")
    exit(1)

# フォールバック用の国リスト
# Gemini APIが失敗した場合に使用する、確実に動作する10カ国のデータ
FALLBACK_COUNTRIES = [
    {"jp": "日本", "en": "Japan", "code": "jp"},
    {"jp": "アメリカ", "en": "United States", "code": "us"},
    {"jp": "イギリス", "en": "United Kingdom", "code": "gb"},
    {"jp": "フランス", "en": "France", "code": "fr"},
    {"jp": "ドイツ", "en": "Germany", "code": "de"},
    {"jp": "イタリア", "en": "Italy", "code": "it"},
    {"jp": "スペイン", "en": "Spain", "code": "es"},
    {"jp": "カナダ", "en": "Canada", "code": "ca"},
    {"jp": "オーストラリア", "en": "Australia", "code": "au"},
    {"jp": "ブラジル", "en": "Brazil", "code": "br"}
]

# ホームページのルート
@app.route('/')
def index():
    """ホームページを表示する関数
    
    Returns:
        str: index.htmlテンプレートをレンダリングした結果
    """
    return render_template('index.html')

def get_country_from_ai():
    """Gemini AIから国情報を取得する関数
    
    国連加盟193カ国からランダムに1カ国を選択し、
    日本語国名、英語国名、国コードを取得します。
    
    Returns:
        tuple: (日本語国名, 英語国名, 国コード) または None（失敗時）
        
    エラーハンドリング:
        - API通信エラー: Noneを返す
        - レスポンス解析エラー: Noneを返す
        - 不完全なデータ: Noneを返す
    """
    try:
        # Gemini AIに送信するプロンプト
        prompt = """国連加盟国から1カ国をランダムに選択:
日本語国名: [国名]
英語国名: [国名]
国コード: [2文字小文字]"""
        
        # Gemini APIにリクエストを送信
        response = model.generate_content(prompt)
        
        # レスポンスが空の場合はエラー
        if not response or not response.text:
            print("⚠️ Gemini APIからのレスポンスが空です")
            return None
            
        # レスポンステキストを行ごとに分割
        lines = response.text.strip().split('\n')
        
        # 各行から必要な情報を抽出
        country_jp = country_en = country_code = ""
        for line in lines:
            if '日本語国名:' in line:
                country_jp = line.split(':', 1)[1].strip()
            elif '英語国名:' in line:
                country_en = line.split(':', 1)[1].strip()
            elif '国コード:' in line:
                country_code = line.split(':', 1)[1].strip()
        
        # すべての情報が取得できた場合のみ成功
        if country_jp and country_en and country_code:
            print(f"✅ AI国生成成功: {country_jp} ({country_code})")
            return country_jp, country_en, country_code
        else:
            print(f"⚠️ 不完全なAIレスポンス: jp={country_jp}, en={country_en}, code={country_code}")
            
    except Exception as e:
        # すべての例外をキャッチしてログ出力
        print(f"❌ AI国生成エラー: {type(e).__name__}: {e}")
        
    return None

@app.route('/new_game', methods=['POST'])
def new_game():
    """新しいゲームを開始する関数
    
    処理の流れ:
    1. Gemini AIから国を取得を試行
    2. 失敗時はフォールバック国リストから選択
    3. セッションデータを初期化
    4. ゲーム画面にリダイレクト
    
    エラーハンドリング:
    - AI取得失敗時: フォールバック国リストを使用
    - セッション初期化失敗: システムエラーメッセージを表示
    """
    try:
        # AIから国を取得、失敗時はフォールバック
        result = get_country_from_ai()
        if result:
            country_jp, country_en, country_code = result
            print(f"🎲 ゲーム開始: AI選択国 - {country_jp}")
        else:
            # フォールバック: 事前定義された国リストからランダム選択
            fallback = random.choice(FALLBACK_COUNTRIES)
            country_jp, country_en, country_code = fallback["jp"], fallback["en"], fallback["code"]
            print(f"🎲 ゲーム開始: フォールバック国 - {country_jp}")
        
        # セッションデータの初期化
        # ゲームの状態をすべてリセットして新しい問題を設定
        session.update({
            'current_country': country_en,        # AI判定用の英語国名
            'current_country_jp': country_jp,     # 表示用の日本語国名
            'country_flag': f"https://flagcdn.com/w320/{country_code}.png",  # 国旗画像URL
            'answers_left': 2,                    # 残り回答回数
            'questions_left': 10,                 # 残り質問回数
            'hints_used': [],                     # 使用済みヒント種類
            'question_log': [],                   # 質問履歴
            'game_started': True                  # ゲーム開始フラグ
        })
        
        flash('新しいゲームが開始されました！', 'success')
        return redirect(url_for('game'))
        
    except Exception as e:
        # セッション初期化や画面遷移でのエラー
        print(f"❌ ゲーム開始エラー: {type(e).__name__}: {e}")
        flash('ゲーム開始に失敗しました。もう一度お試しください。', 'error')
        return redirect(url_for('index'))

@app.route('/game')
def game():
    """ゲーム画面を表示する関数
    
    セッション状態をチェックし、ゲームが開始されている場合のみ
    ゲーム画面を表示します。
    
    Returns:
        str: game.htmlテンプレートまたはリダイレクト
        
    エラーハンドリング:
    - ゲーム未開始: ホーム画面にリダイレクト
    """
    # ゲーム開始状態をチェック
    if not session.get('game_started'):
        flash('まずゲームを開始してください', 'info')
        return redirect(url_for('index'))
    
    # ゲーム画面を表示
    return render_template('game.html')

@app.route('/ask_question', methods=['POST'])
def ask_question():
    """プレイヤーの質問にAIが回答する機能
    
    処理の流れ:
    1. ゲーム状態と質問回数制限をチェック
    2. 質問内容の入力検証
    3. Gemini AIに質問を送信して回答を取得
    4. セッションデータを更新
    
    エラーハンドリング:
    - ゲーム未開始: エラーメッセージでゲーム画面に戻る
    - 質問回数上限: エラーメッセージでゲーム画面に戻る
    - 空の質問: 入力を促すメッセージ
    - AI通信エラー: エラーメッセージを表示
    """
    # ゲーム状態と質問回数制限をチェック
    if not session.get('game_started'):
        flash('ゲームが開始されていません', 'error')
        return redirect(url_for('game'))
        
    if session.get('questions_left', 0) <= 0:
        flash('質問回数の上限に達しました', 'error')
        return redirect(url_for('game'))
    
    # 質問内容の取得と検証
    question = request.form.get('question', '').strip()
    if not question:
        flash('質問を入力してください', 'error')
        return redirect(url_for('game'))
    
    try:
        # Gemini AIへの質問プロンプトを作成
        prompt = f"""質問: "{question}"
対象国: {session['current_country']}

「はい」または「いいえ」のみで回答してください。
国名・地域名は言及禁止。"""
        
        # AIに質問を送信
        response = model.generate_content(prompt)
        
        # レスポンスの検証
        if not response or not response.text:
            raise ValueError("AIからの回答が空です")
            
        answer = response.text.strip()
        
        # 質問ログに記録（最大10件まで保持）
        if 'question_log' not in session:
            session['question_log'] = []
        session['question_log'].append(f"Q: {question} → A: {answer}")
        
        # 残り質問回数を減らす
        session['questions_left'] -= 1
        
        # 成功メッセージを表示
        flash(f'回答: {answer}', 'info')
        print(f"💬 質問処理成功: {question} → {answer}")
        
    except Exception as e:
        # AI通信エラーや処理エラーをキャッチ
        print(f"❌ 質問処理エラー: {type(e).__name__}: {e}")
        flash('質問の処理に失敗しました。もう一度お試しください。', 'error')
    
    return redirect(url_for('game'))

@app.route('/get_hint', methods=['POST'])
def get_hint():
    """ヒントを取得する機能
    
    3種類のヒント（主食・面積・言語）をAIから取得します。
    各ヒントは1回ずつしか使用できません。
    
    処理の流れ:
    1. ゲーム状態とヒント使用状況をチェック
    2. 指定されたヒント種類の検証
    3. Gemini AIにヒント生成を依頼
    4. セッションデータを更新
    
    エラーハンドリング:
    - ゲーム未開始: エラーメッセージ
    - 無効なヒント種類: エラーメッセージ
    - 既に使用済み: エラーメッセージ
    - ヒント上限達成: エラーメッセージ
    - AI通信エラー: エラーメッセージ
    """
    # ヒント種類を取得
    hint_type = request.form.get('hint_type')
    
    # 複合的な条件チェック
    if not session.get('game_started'):
        flash('ゲームが開始されていません', 'error')
        return redirect(url_for('game'))
        
    if not hint_type:
        flash('ヒント種類が指定されていません', 'error')
        return redirect(url_for('game'))
        
    if hint_type not in ['主食', '面積', '言語']:
        flash('無効なヒント種類です', 'error')
        return redirect(url_for('game'))
        
    # 使用済みヒントリストの初期化
    if 'hints_used' not in session:
        session['hints_used'] = []
        
    if hint_type in session['hints_used']:
        flash(f'ヒント「{hint_type}」は既に使用済みです', 'error')
        return redirect(url_for('game'))
        
    if len(session['hints_used']) >= 3:
        flash('すべてのヒントを使用済みです', 'error')
        return redirect(url_for('game'))
    
    try:
        # ヒント種類別のプロンプト定義
        hints = {
            '主食': f"{session['current_country']}の主食を50文字以内で。国名・地域名禁止。",
            '面積': f"{session['current_country']}の面積を日本と比較。50文字以内。国名・地域名禁止。",
            '言語': f"{session['current_country']}の公用語を50文字以内で。国名・地域名禁止。"
        }
        
        # AIにヒント生成を依頼
        response = model.generate_content(hints[hint_type])
        
        # レスポンスの検証
        if not response or not response.text:
            raise ValueError("AIからのヒントが空です")
            
        hint = response.text.strip()
        
        # ヒント使用状況を更新
        session['hints_used'].append(hint_type)
        session['current_hint'] = f"{hint_type}: {hint}"
        
        # 成功メッセージを表示
        flash(f'ヒント「{hint_type}」: {hint}', 'info')
        print(f"💡 ヒント取得成功: {hint_type} - {hint[:20]}...")
        
    except Exception as e:
        # AI通信エラーや処理エラーをキャッチ
        print(f"❌ ヒント取得エラー: {type(e).__name__}: {e}")
        flash('ヒントの取得に失敗しました。もう一度お試しください。', 'error')
    
    return redirect(url_for('game'))

@app.route('/submit_answer', methods=['POST'])
def submit_answer():
    """プレイヤーの回答を判定する機能
    
    2段階の判定システム:
    1. 厳密な文字列マッチング（優先）
    2. AIによる柔軟な判定（フォールバック）
    
    処理の流れ:
    1. ゲーム状態と回答回数制限をチェック
    2. 回答内容の入力検証
    3. 厳密マッチング判定を実行
    4. 不一致の場合はAI判定を実行
    5. 結果に応じてゲーム状態を更新
    
    エラーハンドリング:
    - ゲーム未開始: エラーメッセージ
    - 回答回数上限: エラーメッセージ
    - 空の回答: 入力を促すメッセージ
    - AI判定エラー: 不正解として処理
    """
    # ゲーム状態と回答回数制限をチェック
    if not session.get('game_started'):
        flash('ゲームが開始されていません', 'error')
        return redirect(url_for('game'))
        
    if session.get('answers_left', 0) <= 0:
        flash('回答回数の上限に達しました', 'error')
        return redirect(url_for('game'))
    
    # 回答内容の取得と検証
    answer = request.form.get('answer', '').strip()
    if not answer:
        flash('回答を入力してください', 'error')
        return redirect(url_for('game'))
    
    # 正解の国名を取得
    country_jp = session['current_country_jp']
    
    # 第1段階: 厳密な文字列マッチング（最も確実）
    is_correct = answer == country_jp
    judgment_method = "厳密マッチング"
    
    # 第2段階: AIによる柔軟な判定（フォールバック）
    if not is_correct:
        try:
            # AI判定用のプロンプト
            prompt = f"""正解: {country_jp}
回答: {answer}

略称・表記ゆれのみ正解。全く違う国名・地域名・都市名は不正解。
「正解」または「不正解」のみ回答。"""
            
            response = model.generate_content(prompt)
            
            # レスポンスの検証
            if not response or not response.text:
                raise ValueError("AIからの判定結果が空です")
                
            ai_result = response.text.strip()
            is_correct = ai_result == "正解"
            judgment_method = f"AI判定({ai_result})"
            
            print(f"🤖 AI判定: {answer} → {ai_result} (正解: {country_jp})")
            
        except Exception as e:
            # AI判定に失敗した場合は不正解として処理
            print(f"❌ AI判定エラー: {type(e).__name__}: {e}")
            is_correct = False
            judgment_method = "AI判定失敗(不正解扱い)"
    
    # 残り回答回数を減らす
    session['answers_left'] -= 1
    
    print(f"📝 回答判定: {answer} → {'正解' if is_correct else '不正解'} ({judgment_method})")
    
    # 判定結果に応じた処理
    if is_correct:
        # 正解時: ゲーム終了
        flash(f'🎉 正解！答えは「{country_jp}」でした！', 'success')
        session['game_started'] = False
        print(f"🎊 ゲーム成功終了: {country_jp}")
    else:
        # 不正解時: 回答回数をチェック
        if session['answers_left'] > 0:
            # まだ回答チャンスが残っている
            flash(f'❌ 不正解です。残り{session["answers_left"]}回回答できます。', 'error')
            print(f"⏳ 回答継続: 残り{session['answers_left']}回")
        else:
            # 回答チャンス終了
            flash(f'😢 ゲーム終了！正解は「{country_jp}」でした。', 'error')
            session['game_started'] = False
            print(f"💔 ゲーム失敗終了: 正解は{country_jp}")
    
    return redirect(url_for('game'))

@app.route('/reset_game', methods=['POST'])
def reset_game():
    """ゲームをリセットしてホーム画面に戻る機能
    
    セッションからゲーム関連のデータをすべて削除し、
    初期状態に戻します。
    
    削除されるセッションデータ:
    - game_started: ゲーム開始フラグ
    - current_country: 英語国名
    - current_country_jp: 日本語国名
    - country_flag: 国旗画像URL
    - answers_left: 残り回答回数
    - questions_left: 残り質問回数
    - hints_used: 使用済みヒント
    - question_log: 質問履歴
    - current_hint: 現在のヒント
    
    エラーハンドリング:
    - セッションクリアエラーは無視（ゲームリセットを優先）
    """
    try:
        # クリアするセッションキーのリスト
        keys_to_clear = [
            'game_started',        # ゲーム開始フラグ
            'current_country',     # 英語国名（AI処理用）
            'current_country_jp',  # 日本語国名（表示用）
            'country_flag',        # 国旗画像URL
            'answers_left',        # 残り回答回数
            'questions_left',      # 残り質問回数
            'hints_used',          # 使用済みヒントリスト
            'question_log',        # 質問履歴
            'current_hint'         # 現在表示中のヒント
        ]
        
        # 各キーをセッションから削除（存在しなくてもエラーにならない）
        for key in keys_to_clear:
            session.pop(key, None)
        
        print("🔄 ゲームリセット完了")
        flash('ゲームをリセットしました', 'info')
        
    except Exception as e:
        # セッションクリアでエラーが発生してもゲームリセットは続行
        print(f"⚠️ セッションクリア中にエラー: {type(e).__name__}: {e}")
        flash('ゲームをリセットしました', 'info')
    
    return redirect(url_for('index'))

# メイン実行部分
if __name__ == '__main__':
    """アプリケーションのメインエントリーポイント
    
    開発モードでFlaskアプリケーションを起動します。
    デバッグモードが有効なため、コード変更時に自動リロードされます。
    
    起動情報:
    - ホスト: localhost (127.0.0.1)
    - ポート: 5000
    - デバッグモード: 有効
    """
    try:
        # 本番環境かどうかを判定（Renderでは PORT 環境変数が設定される）
        port = int(os.getenv('PORT', 5000))
        debug = os.getenv('FLASK_ENV') != 'production'
        
        if debug:
            print("🚀 国旗クイズゲーム起動中...")
            print(f"📍 アクセスURL: http://localhost:{port}")
            print("🔧 デバッグモード: 有効")
            print("⚠️  本番環境では debug=False に設定してください")
        
        app.run(host='0.0.0.0', port=port, debug=debug)
    except Exception as e:
        print(f"❌ アプリケーション起動エラー: {type(e).__name__}: {e}")
        print("🔍 GEMINI_API_KEY環境変数が設定されているか確認してください")