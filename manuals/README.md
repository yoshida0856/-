# 僕の資産戦略を、この一冊に。

## 現行版 v5.0

[PDFをダウンロード（横型５ページ・約2.54MB）](https://github.com/yoshida0856/-/raw/refs/heads/main/manuals/basis-manual-v5.0.pdf)

2026年10月15日作成。白・ミント・水色の装飾、資産を連想できるアイコン、２行に収めた「持っているBTCを、運用（ステーキング）にも活かす。」の見出しを反映しました。５ページはそれぞれ独立しており、一覧画像ではありません。

1. 表紙：資産配分表・注目銘柄・実際に使う運用方法
2. 本人申告の資産配分：現金45%、金20%、PSLV5%、BTC15%、XRP10%、ETH5%
3. PAXG・LINKの比較・研究用候補（外部リンクなし）
4. BASISの開始の流れ・期間・出金条件・費用
5. 始め方・公式ロゴ・登録ボタン・まとめた注意事項

年率・利回り・複利の数値は未確認のため掲載していません。利益１万円の分配例も掲載していません。具体的な本人の運用実績は創作していません。

PDF最終ページの登録ボタン：

- Coincheck：https://campaign.coincheck.com/invitation?code=RzLuJLQ
- MEXC：https://promote.mexc.com/a/VlM5ZfOs
- BASIS：https://basis.pro/register/IUMS4759

修正用スクリプトは `source/build_v5.py`、ページ画像は `source/v5-images/`、公式ロゴは `source/brand-assets/` に保存しています。Python・PyMuPDF・Pillowで再生成できます。

```sh
python manuals/source/build_v5.py
```

本文は画像として配置し、登録リンクと目次はPDFに設定しています。BASISの条件は以前取得した資料に基づくもので、今回新たに最新の利回りを確認したものではありません。

## 旧版 v4.5 の記録（以下は旧版の内容）

[PDFをダウンロード（横型５ページ・約1.6MB）](https://github.com/yoshida0856/-/raw/refs/heads/main/manuals/basis-manual-v4.5.pdf)

配布時の案内に合わせて、本人の実際の資産配分・注目銘柄候補・実際に利用するBASISを中心に再構成しました。

1. 表紙
2. 本人申告の現在の資産配分（2026年10月12日確認）
3. 公開情報から選んだPAXG・LINKの研究候補
4. 本人が利用するBASISの訴求・特徴と条件
5. 登録・認証 → 入金 → stTokenへの変換 → ステークの始め方

銘柄は依頼に応じて編集上選定した候補で、本人の保有・推奨を示しません。独自情報・非公開情報ではありません。運用期間・元本・損益・出金実績の具体値は未提供で、創作していません。収益の安定性を保証する内容ではありません。候補銘柄は配布前に本人による最終確認を想定したレビュー案です。

![表紙](previews/v4-5-cover.png)

![資産配分](previews/v4-5-allocation.png)

![注目銘柄候補](previews/v4-5-watchlist.png)

## 確認資料

- PAXG発行体：https://www.paxos.com/paxgold
- Chainlink公式：https://docs.chain.link/getting-started/conceptual-overview
- BASIS：https://docs.basis.pro/
- 成功報酬：https://docs.basis.pro/economics-and-rewards/performance-fee-mechanics
- 解除：https://docs.basis.pro/economics-and-rewards/unstaking-and-7-day-rule
- リスク：https://docs.basis.pro/risk-safety-and-asset-protection/risk-disclosure

BASISの条件は2026年10月11日取得の資料を参照。PAXG・Chainlinkの公式説明は2026年10月12日に取得。実際の安全性・収益性・日本での必要な登録の独立検証ではありません。

![BASISの訴求](previews/v4-5-fees.png)

![始め方](previews/v4-5-routes.png)

４ページ目は「持っているBTCを運用にも活かす」を主題に変更。手数料の説明を「運用利益に対する手数料20％」とし、実行コスト控除後の利益１万円なら手数料2,000円・分配8,000円という仮の例を追加しています。

## 登録案内

５ページ目にCoincheck・MEXC・BASISの役割別の紹介導線を掲載し、BASISの開始手順も保持しました。

![登録案内](previews/v4-5-routes.png)

- Coincheck：https://campaign.coincheck.com/invitation?code=RzLuJLQ
- MEXC：https://promote.mexc.com/a/VlM5ZfOs
- BASIS：https://basis.pro/register/IUMS4759

Coincheckの公式キャンペーンページを2026年10月12日に表示・確認。1,500円相当BTCの付与には新規登録・本人確認・税務上の届出等による口座開設完了が必要で、既存アカウント等は対象外です。紹介ページから別ページへ移動すると対象外になる旨も記載されています。キャンペーンは変更・終了され得るためリンク先の最新条件を優先してください。

MEXCは日本居住者向けのため無条件の推奨として扱わず、規約確認と紹介ページの案内としています。金融庁の2024年11月28日付警告を短く注記しています。確認資料：https://www.fsa.go.jp/policy/virtual_currency02/mexc_global_keikokushiryo.pdf

紹介リンクには利益相反の簡潔な開示を付けています。別のアフィリエイト案件への切替は比較情報がなく推奨していません。

v4.4では配分ページ下部のグレーの説明文を削除し、緑の注記を12ptで「※全員に同じ割合を勧めるモデルではありません。」に変更しました。

v4.5では上部の小さな英語ラベルと注目銘柄の外部リンクを削除しました。一般的な注意書きは最終ページへ集約し、Coincheck条件・紹介関係のフッター２行は削除。BASISの費用・解除条件を３項目の平易な説明に変更しました。５ページ目は白背景・淡色カードにし、公式ロゴを各サービス名の右隣に配置しています。

## 過去版

- [v4.4：配分ページの注記修正](basis-manual-v4.4.pdf)

- [v4.3：３サービスの紹介案内](basis-manual-v4.3.pdf)

- [v4.2：BASIS訴求と手数料説明](basis-manual-v4.2.pdf)

- [v4.1：特徴と始め方](basis-manual-v4.1.pdf)

- [v4.0：個人戦略５ページ版](basis-manual-v4.0.pdf)

- [v2.0：横型13ページ](basis-manual-v2.0.pdf)
- [v1.2：縦型12ページ](basis-manual-v1.2.pdf)

## 修正用ソース

`source/design_v4_5.py` に生成用スクリプトを保持しています。再生成にはPython・PyMuPDF・Noto Sans CJKの通常体と太字が必要です。レビュー用PDFはページ画像版で、リンクを保持しています。
