# ROUTE_OPTIMIZATION

## 紹介と使い方

  - excelファイルのaddress一覧を読み取り、最適なルートを検索する。

  - 一番上の行にスタート地点、一番下の行にゴール地点を記載する。また、その間に途中に立ち寄りたい地点を記載する。(記載は、住所でも「東京タワー」等の有名な施設名でも認識します。)

  - 途中の立ち寄り地点を全て経由して、スタートからゴールまで距離が短くなるルートを探索します。結果は、htmlファイルで出力されます。

  - 歩きのみ対応していますが、パラメータを変更すれば歩き以外にも対応します。

  - env.exampleを.envへ変更して、APIキーを入力すれば使用できるはずです。

## 工夫した点

  - geocodingで住所データを座標データに変換　→　openrouteserviceから距離データのマトリックスを取得　→　pulpで最適ルート計測　→　openrouteserviceでルート検索　→　foliumで描画しています。

## 苦戦した点

  - pythonを初めて触ったので、ライブラリ等の検索に時間を使いました。pulpは色々応用が効きそうなので、次回も触ってみたいと思います。

## 参考にした web サイトなど

  - https://qiita.com/tubarin/items/774b61ffbde17c7df89a

## Memo

  - pipreqs --encoding UTF8 .
  - pip install -r requirements.txt