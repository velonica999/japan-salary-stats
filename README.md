# japan-salary-stats：職種別・都道府県別の平均年収データ（CSV）

厚生労働省「賃金構造基本統計調査」をもとに [給料相場.com](https://kyuryo-souba.com/) が集計した、**144職種×47都道府県×性別**の平均年収・月給・賞与・平均年齢・勤続年数・労働時間・労働者数の CSV です。2020年以降の推移も入っています。

- データの説明とダウンロード：https://kyuryo-souba.com/data/
- サイトで見る（職種別・都道府県別のページ）：https://kyuryo-souba.com/
- 更新：このリポジトリの CSV は、毎日サイトの `/data/` から自動で取り込んでいます。サイトは毎月7日に公表元（e-Stat）を確認して自動更新します。賃金構造基本統計調査そのものは年1回（例年3月ごろ）の公表です。

## ファイル

| ファイル | 内容 |
|-|-|
| `data/occupation_prefecture_latest.csv` | 職種×都道府県×性別（最新の調査年） |
| `data/occupation_prefecture_yearly.csv` | 職種×都道府県×性別の推移（2020年〜・現行の職種分類）。職種の正式名と大分類名は latest と職種コードで突き合わせてください |
| `data/major_prefecture_yearly.csv` | 職種大分類×都道府県×性別の推移 |
| `data/prefecture_yearly.csv` | 都道府県×性別（全職種）の推移 |
| `data/occupation_age_latest.csv` | 職種×年齢階級（全国・男女計・最新の調査年） |

文字コードは UTF-8（BOM 付き）で、Excel でそのまま開けます。都道府県コードは 01〜47、全国は 00。性別は「男女計／男／女」。

## 列

| 列名 | 意味 | Description |
|-|-|-|
| 平均年収_万円 | 月給×12＋年間賞与（推計・額面） | annual income (10,000 yen) = monthly × 12 + bonus |
| 月給_万円 | きまって支給する現金給与額（残業代・手当込み） | monthly cash earnings incl. overtime (10,000 yen) |
| 所定内給与_万円 | 所定内給与額 | scheduled cash earnings (10,000 yen) |
| 年間賞与_万円 | 年間賞与その他特別給与額 | annual bonus (10,000 yen) |
| 平均年齢_歳 | 平均年齢 | average age |
| 勤続年数_年 | 平均勤続年数 | average years of service |
| 所定内労働時間_時間 | 月の所定内実労働時間数 | scheduled hours worked per month |
| 超過労働時間_時間 | 月の超過実労働時間数（残業） | overtime hours per month |
| 労働者数_人 | 労働者数（推計・10人単位で丸め） | number of workers (estimate) |
| 参考値 | 1＝労働者数300人未満で変動が大きい | 1 = reference value (fewer than 300 workers) |

対象は一般労働者（短時間労働者以外の常用労働者）。都道府県の全体値は職種大分類別の平均を労働者数で加重平均した値です。集計方法の詳細は https://kyuryo-souba.com/about/ を見てください。

## 利用条件（ライセンス）

[CC BY 4.0](https://creativecommons.org/licenses/by/4.0/deed.ja)。商用・非商用を問わず、報道・ブログ・研究・授業・アプリ・AI の学習や回答などに自由に使えます。条件は出典を明記することだけです。

**「出典を明記する」とは？** 使った数字がどこのデータかを、読む人に分かるように書き添えることです。次の1行をコピーして、数字や表・グラフのすぐ下か、記事・資料の最後に貼り付けてください。

```
出典：給料相場.com（厚生労働省「賃金構造基本統計調査」をもとに集計） https://kyuryo-souba.com/data/
```

- ブログ・ホームページ：表やグラフのすぐ下に貼る
- 資料・スライド・レポート：そのページの下の端か、最後の「参考資料」に書く
- SNS・動画：投稿文や概要欄の最後に書く
- 表を加工・グラフ化したとき：「出典：給料相場.comのデータをもとに作成 https://kyuryo-souba.com/data/」と書く
- URL は行の最後に置き、前に空白を入れる（URL のすぐ後ろに文字やカッコを続けると、リンクが切れることがあります）

許可の連絡やお金は要りません。出典さえ書けば、仕事（商用）でも自由に使えます。

元の統計は厚生労働省「賃金構造基本統計調査」（[e-Stat](https://www.e-stat.go.jp/)）で、[政府統計の総合窓口 利用規約](https://www.e-stat.go.jp/terms-of-use)に基づいて加工しています。当サイトの集計は公表値の四則演算のみで、厚生労働省が作成したものではありません。

---

## English

Average annual salary in Japan by **occupation (144) × prefecture (47) × sex**, aggregated by [kyuryo-souba.com](https://kyuryo-souba.com/) from the *Basic Survey on Wage Structure* (Ministry of Health, Labour and Welfare, via e-Stat). Includes yearly series from 2020. Amounts are in units of 10,000 yen. Files are UTF-8 with BOM. License: CC BY 4.0 — please credit "kyuryo-souba.com, based on the MHLW Basic Survey on Wage Structure: https://kyuryo-souba.com/data/". The data in this repository is synced daily from https://kyuryo-souba.com/data/.
