# 🏴 国旗クイズゲーム

[![Python](https://img.shields.io/badge/Python-3.7+-blue.svg)](https://www.python.org/)
[![Flask](https://img.shields.io/badge/Flask-2.3.3-green.svg)](https://flask.palletsprojects.com/)
[![Gemini](https://img.shields.io/badge/Gemini-2.0%20Flash-purple.svg)](https://ai.google.dev/)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Deploy](https://img.shields.io/badge/Deploy-Render-00f2c3.svg)](https://render.com)

AI搭載の国旗クイズゲーム。Gemini 2.0 Flash APIを活用し、国旗を見て国名を当てるインタラクティブなWebアプリケーションです。

**🚀 ライブデモ**: [https://flag-quiz-python.onrender.com](https://flag-quiz-python.onrender.com)

## ✨ 特徴

- 🌍 **国連加盟193カ国** の国旗に対応
- 🤖 **Gemini AI** による質問回答システム
- 💡 **3種類のヒント** （主食・面積・言語）
- 🎨 **モダンデザイン** （グラスモーフィズム）
- 📱 **レスポンシブ対応** （PC・タブレット・スマホ）
- 🇯🇵 **完全日本語対応**
- ☁️ **クラウドデプロイ済み** （Render）

## 🎯 プロジェクト概要

このプロジェクトは、以下の技術スキルを実践的に学ぶために開発されたポートフォリオ作品です：

- **バックエンド開発**: Flaskフレームワークを使用したWebアプリケーション構築
- **AI統合**: Google Gemini APIとの連携による対話型機能の実装
- **フロントエンド**: モダンなCSS（グラスモーフィズム）とレスポンシブデザイン
- **クラウドデプロイ**: Renderを使用した本格的なWebサービス公開
- **API設計**: 外部サービス（国旗画像、AI）との統合
- **セキュリティ**: 環境変数による機密情報管理

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

## 🛠️ 技術スタック

### バックエンド
- **Flask 2.3.3** - 軽量で高速なWebフレームワーク
- **Google Gemini 2.0 Flash** - 最新のAI質問回答API
- **flagcdn.com** - 高品質な国旗画像データソース
- **Gunicorn** - 本番環境用WSGIサーバー

### フロントエンド
- **HTML5** - セマンティックなマークアップ
- **CSS3** - モダンなスタイリング（グラスモーフィズム、CSS Grid、Flexbox）
- **Google Fonts** - Poppins、Playfair Display
- **レスポンシブデザイン** - モバイルファーストアプローチ

### インフラ・デプロイ
- **Render** - クラウドプラットフォーム
- **環境変数管理** - セキュアな設定管理
- **自動デプロイ** - GitHub連携によるCI/CD

### 主要機能・アーキテクチャ
- **セッションベースの状態管理** - Flask-Sessionによる安全なゲーム状態管理
- **リアルタイムAI応答** - 非同期処理による高速なAI応答
- **エラーハンドリング** - 包括的なエラー処理とユーザーフレンドリーなメッセージ
- **セキュリティ** - CSRF保護、入力検証、XSS対策

## 📁 プロジェクト構造

```
flag-quiz-python/
├── app.py                 # メインアプリケーション（Flask）
├── requirements.txt       # Python依存関係
├── requirements.md        # 詳細な要件定義書
├── README.md             # このファイル
├── render.yaml           # Renderデプロイ設定
├── .gitignore            # Git除外設定
├── LICENSE               # MITライセンス
├── static/
│   └── style.css         # モダンなスタイルシート
└── templates/
    ├── index.html        # ホームページ（ゲーム開始画面）
    └── game.html         # ゲームプレイ画面
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

## 🔧 開発者向け情報

### ローカル環境での実行
開発やカスタマイズを行いたい場合は、以下の手順でローカル環境を構築できます：

1. **リポジトリをクローン**
```bash
git clone https://github.com/yourusername/flag-quiz-python.git
cd flag-quiz-python
```

2. **仮想環境を作成・有効化**
```bash
# Windows
python -m venv venv
venv\Scripts\activate

# macOS/Linux
python3 -m venv venv
source venv/bin/activate
```

3. **依存関係をインストール**
```bash
pip install -r requirements.txt
```

4. **環境変数を設定**
```bash
# Windows
set GEMINI_API_KEY=your_gemini_api_key_here

# macOS/Linux
export GEMINI_API_KEY=your_gemini_api_key_here
```

5. **アプリケーションを起動**
```bash
python app.py
```

6. **ブラウザでアクセス**
```
http://localhost:5000
```

### カスタマイズ・拡張
- **デザイン変更**: `static/style.css` を編集
- **機能拡張**: 難易度システム、スコア機能、カテゴリ別クイズ等
- **技術的拡張**: データベース統合、API拡張、テスト自動化等

## 🚀 パフォーマンス・スケーラビリティ

### 現在の実装
- **軽量なFlaskアプリケーション**: 高速なレスポンス
- **静的アセット最適化**: CSS・HTMLの効率的な配信
- **セッション管理**: メモリ効率の良い状態管理

### 将来の改善点
- **CDN統合**: 画像・CSSの高速配信
- **キャッシュ戦略**: Redis等による高速化
- **ロードバランシング**: 複数インスタンスでの負荷分散

## 🤝 貢献

プルリクエストやイシューの報告を歓迎します！

1. フォーク
2. フィーチャーブランチ作成 (`git checkout -b feature/amazing-feature`)
3. コミット (`git commit -m 'Add amazing feature'`)
4. プッシュ (`git push origin feature/amazing-feature`)
5. プルリクエスト作成

### 貢献のガイドライン
- コードスタイルの統一（PEP 8準拠）
- 適切なコメントとドキュメント
- テストの追加・更新
- セキュリティの考慮

## 📝 ライセンス

このプロジェクトはMITライセンスの下で公開されています。詳細は [LICENSE](LICENSE) ファイルをご覧ください。

## 🙏 謝辞

- [Google Gemini AI](https://ai.google.dev/) - 最先端のAI機能
- [flagcdn.com](https://flagcdn.com/) - 高品質な国旗画像データ
- [Google Fonts](https://fonts.google.com/) - 美しいフォント
- [Render](https://render.com/) - 優れたクラウドプラットフォーム

## 📞 お問い合わせ・フィードバック

質問やフィードバックがある場合は、以下までお気軽にご連絡ください：

- **GitHub Issues**: [Issues Page](https://github.com/yourusername/flag-quiz-python/issues)
- **プロジェクトページ**: [https://flag-quiz-python.onrender.com](https://flag-quiz-python.onrender.com)

## 🌟 今後の展望

このプロジェクトは継続的に改善・拡張される予定です：

- **多言語対応**: 英語・中国語等の追加
- **モバイルアプリ**: React Native版の開発
- **AI機能強化**: より高度な質問応答システム
- **コミュニティ機能**: ユーザー間の交流機能

---

⭐ このプロジェクトが気に入ったら、ぜひスターを付けてください！

**🔗 ライブデモ**: [https://flag-quiz-python.onrender.com](https://flag-quiz-python.onrender.com)
