# PDF_translater

**PDF_translater**は英語論文のpdfファイルを入力として，txtに変換・文章の整形・翻訳を行うツールです

## 使い方
1. [PDF_translater.exe](https://github.com/parthenos0908/PDF_translater/raw/main/PDF_translater.exe)をダウンロードします
2. exeファイルと翻訳したい英語論文のpdfファイルを同じディレクトリに配置します
3. exeファイルを実行します

## モード
1. **PDF → txt**  
英語論文のpdfファイル入力し，整形したtxtファイルに変換します
2. **txt → translated_txt**  
英語のtxtファイルを入力し，日本語のtxtファイルに翻訳します
3. **PDF → txt → translated_txt** (非推奨)  
1,2を連続して行います．1での整形はまだ粗が目立つので，1で生成したtxtファイルを手動で整形して2を実行することを推奨します

## 生成物
exeファイルと同じディレクトリに以下が生成されます．  
同名のファイルは上書きされるのでご注意ください．  
特に，モード1を実行したのちに手動で整形した`filename`.txt は別名で保存することを推奨します
- `filename`.txt：整形済みの英語論文のtxtファイル
- `filename`\_unshaped.txt：未整形の英語論文のtxtファイル
- `filename`\_translated.txt：`filename`.txtをGoogle翻訳にかけたもの
