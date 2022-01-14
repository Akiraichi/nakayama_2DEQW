# Quantum Walk Simulation
 
様々なタイプの量子ウォークをシミュレーションできます。
 
# features


# Requirement
 
* Python 3.7以降
* numba
* matplotlib
* seaborn
* pandas

Environments under [Anaconda](https://www.anaconda.com/) is tested.
 
```bash
# なんかコードを入れる
conda create -n pyxel pip python=3.6 Anaconda
activate pyxel
```
 
# Installation
 
```bash
conda install numpy,matplotlib,seaborn,numba,pandas
```
 
# Usage

使い方を説明する
 
```bash
python main.py
```
 
# Note
 
シミュレーション結果の正当性については保証していません。多分正しいとは思うけど。

# Future features
 - 旧形式データ互換性のためのクラスを削除
 - joblibで保存する際は、クラスのインスタンスで保存しないようにする（クラス名やディレクトリパスにデータが依存してしまうから
 - READMEの作成
 - Exampleを書いたjupyterファイルの作成とcolabでの実行リンクの作成
 - ドキュメントの作成

# Author
 
 
# License
 
"Quantum Walk Simulation" is under [MIT license](https://en.wikipedia.org/wiki/MIT_License).