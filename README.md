# ExpensesApp-
kivyで家計デスクトップアプリを作っています。

**実装した機能：**  
・メイン画面基本レイアウト（左側は選択した月のカテゴリパイチャート、右側は各カテゴリ内訳のパイチャート）  
・パイチャートウィジェット  
・登録データのカテゴリによって、動的にカテゴリ内訳のパイチャートを生成する（例えば：２つカテゴリが登録されたら、２つのサブパイチャートが画面に表示）  
・年と月のドロップダウンと選択による画面更新  
・入力画面、出費入力と登録  
・データの保存とロード（現時点はpklファイルとしてパソコンのローカルに保存する）  

**これから実装する予定：**  
・既存カテゴリを見る方法（入力画面の右側）  
・時系列グラフを表示する画面  
・カテゴリ内訳パイチャートのリストビュー  
・すでに登録されているデータを見ると編集する機能  
・パイチャートのラベル  
・言語サポート  
・ＵＩの調整（もっときれいにする）  
・定期出費の自動追加  
・支払いリマインダー（光熱費など）  
・RDBMSとの連携  
・領収書をスキャンするだけで出費を登録できる機能  
・（できれば）クレジットカード参照のAPIとの連携  

**現時点（ローカル保存式）のデータ構成：**  
メイン辞書：  
　　　キー：年と月のstring i.e. 202101 →2021年01月  
　　　バリュー：月のクラスインスタンスオブジェクト  
月のクラスインスタンスオブジェクト：  
　　　その中にデータを保存する辞書のクラスプロパティー：  
　　　　　　キー：カテゴリ （食費、交通費など）  
　　　　　　バリュー：そのカテゴリに当てはまるpandas dataframe オブジェクト  
　　　　　　　　　pandas df：出費項目と金額の列　（昼ごはん、700円など）  

EN:  
Making a desktop app for tracking and visualizing expenditure using kivy.

**Implemented features:**  
・Main screen layout (left side for pie chart broken down by categories, right side for sub pie charts of each category further broken down by item)  
・Pie Chart widget  
・Dynamically changes the number of sub pie charts based on registered data(if there are only 2 categories, then only 2 sub pie charts will be shown)  
・Year and month dropdown menu, screen updating based on selection  
・Input screen layout and input functions  
・Data saving and data loading function (data is currently saved in pkl file in local)  

**To be implemented in the future:**  
・Existing category listview (added to the right side of the input screen)  
・Time series graph screen  
・listview of items in sub pie chart  
・View and edit registered data  
・Pie chart labels  
・Language support  
・Improve UI aesthetics  
・Auto add feature for recurring expenses  
・Reminders for bill payments  
・RDBMS implementation  
・Receipt scanning function  
・(if possible) linking to credit card api to get data on items purchased with cards  

**Currently used data structure (for pkl file saved in local):**  
Main dictionary:  
　　　key: string containing year and month i.e. Jan 2021 is 202101  
　　　value: month class instance object  
Month class instance object:  
　　　dictionary containing data: (class property)  
　　　　　　key: expenditure category (i.e. food transport etc)  
　　　　　　value: pandas dataframe object  
　　　　　　　　　pandas dataframe object: columns for item name, and item price (i.e. lunch, $7)  
