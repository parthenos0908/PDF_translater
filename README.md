# PDF_translater

**PDF_translater**は英語論文のpdfファイルを入力として，txtに変換・文章の整形・翻訳を行うツールです

## 使い方
1. [PDF_translater.exe](https://github.com/parthenos0908/PDF_translater/raw/main/PDF_translater.exe)をダウンロードします
2. exeファイルと翻訳したい英語論文のpdfファイルを同じディレクトリに配置します
3. exeファイルを実行します

## モード
0. **PDF → txt**  
英語論文のpdfファイル入力し，整形したtxtファイルに変換します
1. **txt → translated_txt**  
英語のtxtファイルを入力し，日本語のtxtファイルに翻訳します
2. **PDF → txt → translated_txt** (非推奨)  
モード0,1を連続して行います．  
モード0での整形はまだ粗が目立つので，モード0で生成したtxtファイルを手動で整形し，モード1を実行することを推奨します

## 生成物
exeファイルと同じディレクトリに以下が生成されます．  
- `filename`.txt：整形済みの英語論文
- `filename`\_unshaped.txt：未整形の英語論文
- `filename`\_translated.txt：`filename`.txtをGoogle翻訳にかけたもの

同名のファイルは上書きされるのでご注意ください．  
特に，モード0を実行したのちに手動で整形した`filename`.txt は別名で保存することを推奨します
