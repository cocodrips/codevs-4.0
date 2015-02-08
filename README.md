# codevs-4.0

Python3.4からサポートされたenumを使ってるので、enum34をインストールしないと動きません。
> pip install enum34




## model 
- character.py ユニットオブジェクト
- units.py 敵/自分のユニット全体のオブジェクト。あるマスがダメージをどれくらい受けるかなど。
- resource.py 資源オブジェクト
- point.py 座標



## そのほか
- controller.py 実行したりするプログラム
- brain.py メインのAIプログラム。AI判別とかをする。
- stage.py ステージ情報持ってる
- codevs.py ゲーム設定いろいろする
- default-.* デフォルトのユニットの挙動
- その他 - キャラクタごとのAI
