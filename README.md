# 🏴 国旗クイズゲーム

[![Python](https://img.shields.io/badge/Python-3.7+-blue.svg)](https://www.python.org/)
[![Flask](https://img.shields.io/badge/Flask-2.3.3-green.svg)](https://flask.palletsprojects.com/)
[![Gemini](https://img.shields.io/badge/Gemini-2.0%20Flash-purple.svg)](https://ai.google.dev/)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

AI搭載の国旗クイズゲーム。Gemini 2.0 Flash APIを活用し、国旗を見て国名を当てるインタラクティブなWebアプリケーションです。

![Game Screenshot](screenshot.png)

## ✨ 特徴

- 🌍 **国連加盟193カ国** の国旗に対応
- 🤖 **Gemini AI** による質問回答システム
- 💡 **3種類のヒント** （主食・面積・言語）
- 🎨 **モダンデザイン** （グラスモーフィズム）
- 📱 **レスポンシブ対応** （PC・タブレット・スマホ）
- 🇯🇵 **完全日本語対応**

## 🎮 ゲームルール

### 基本ルール
- 表示された国旗を見て、その国名を日本語で回答
- **2回まで** 回答チャンス
- **10回まで** AI質問可能
- **3種類** のヒント利用可能

### ヒントシステム
- **🍚 主食**: その国の代表的な食べ物
- **📏 面積**: 日本との面積比較
- **🗣️ 言語**: 公用語情報

### 質問システム
- AIに「はい/いいえ」形式で質問可能
- 地理・文化・政治に関する一般的な質問のみ
- 国名を直接聞く質問は無効

## 🚀 クイックスタート

### 必要環境
- Python 3.7以上
- Gemini API キー

### インストール

1. **リポジトリをクローン**
```bash
git clone https://github.com/yourusername/flag-quiz-python.git
cd flag-quiz-python
```

2. **依存関係をインストール**
```bash
pip install -r requirements.txt
```

3. **環境変数を設定**
```bash
# Windows
set GEMINI_API_KEY=your_gemini_api_key_here

# macOS/Linux
export GEMINI_API_KEY=your_gemini_api_key_here
```

4. **アプリケーションを起動**
```bash
python app.py
```

5. **ブラウザでアクセス**
```
http://localhost:5000
```

## 🛠️ 技術スタック

### バックエンド
- **Flask** - Webフレームワーク
- **Google Gemini 2.0 Flash** - AI質問回答
- **flagcdn.com** - 国旗画像データ

### フロントエンド
- **HTML5** - マークアップ
- **CSS3** - スタイリング（グラスモーフィズム）
- **Google Fonts** - Poppins、Playfair Display

### 主要機能
- セッションベースの状態管理
- リアルタイムAI応答
- レスポンシブデザイン
- エラーハンドリング

## 📁 プロジェクト構造

```
flag-quiz-game/
├── app.py                 # メインアプリケーション
├── requirements.txt       # Python依存関係
├── requirements.md        # 要件定義書
├── README.md             # このファイル
├── static/
│   └── style.css         # スタイルシート
└── templates/
    ├── index.html        # ホームページ
    └── game.html         # ゲームページ
```

## 🎯 使用方法

### 1. ゲーム開始
- ホームページで「新しいゲームを開始」をクリック
- ランダムに選択された国の国旗が表示される

### 2. 情報収集
- **質問**: AIに「はい/いいえ」で答えられる質問を投げかけ
- **ヒント**: 3種類のヒントボタンから情報を取得

### 3. 回答
- 国名を日本語で入力（例：「日本」「アメリカ」）
- 2回まで回答可能

### 4. 結果
- 正解時：おめでとうメッセージ
- 不正解時：正解の表示とゲーム終了

## 🔧 カスタマイズ

### デザイン変更
`static/style.css` を編集してデザインをカスタマイズできます。

### 機能拡張
- 新しいヒント種類の追加
- 難易度システムの実装
- スコア機能の追加

## 🤝 貢献

プルリクエストやイシューの報告を歓迎します！

1. フォーク
2. フィーチャーブランチ作成 (`git checkout -b feature/amazing-feature`)
3. コミット (`git commit -m 'Add amazing feature'`)
4. プッシュ (`git push origin feature/amazing-feature`)
5. プルリクエスト作成

## 📝 ライセンス

このプロジェクトはMITライセンスの下で公開されています。詳細は [LICENSE](LICENSE) ファイルをご覧ください。

## 🙏 謝辞

- [Google Gemini AI](https://ai.google.dev/) - AI機能
- [flagcdn.com](https://flagcdn.com/) - 国旗画像データ
- [Google Fonts](https://fonts.google.com/) - フォント

## 📞 お問い合わせ

質問やフィードバックがある場合は、以下までお気軽にご連絡ください：

- GitHub Issues: [Issues Page](https://github.com/yourusername/flag-quiz-python/issues)

---

⭐ このプロジェクトが気に入ったら、ぜひスターを付けてください！