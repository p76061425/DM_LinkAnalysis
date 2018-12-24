# <center>Data Mining Project 3</center>
## <center>P76061425 林聖軒</center>


## Usage
### link_analysis.py
```sh
$ python3 link_analysis.py [-h] 
```
| optional Options | Description |
| ---              | --- |
| -h --help       | show this help message and exit |
|  -f GRAPH_FILE | graph file,(default="./hw3dataset/graph_1.txt") |
| -mode MODE |ha=HubsAuthorities, pr=PageRank, sr=SimRank, all=all above, (default=all) |
| -d D | PageRank d, (default=0.1) |
| -c C | SimRank c, (default=0.8) |



## Implementation detail
三種演算法都寫在link_analysis.py檔案中。
* HITS
依照投影片所寫的演算法，如下</br>
![](https://i.imgur.com/P18YETR.png)</br>
利用兩層for迴圈進行計算，第一層回圈對每一個node迭代，第二層迴圈則計算單個node的authorites值和hub值，authorites用該node每個parent的hub值相加，hub則用該node每個chid的authorites值相加，再對所有的authorites值和hub值除以2norm來做normalization，一直迭代到authorites值和hub值前一次結果差值的2norm加總小於epsilon(這邊設為1e-10)則結束迭代。

* PageRank 
同樣依照投影片所寫的公式計算，如下</br>
![](https://i.imgur.com/4wDjkSV.png)</br>
對每個node做迭代，用上面的公式計算pageRank值，D值設定為0.1，並做2norm normalization，一直迭代到和前一次結果差值的2norm加總小於epsilon(這邊設為1e-10)則結束迭代。


* SimRank</br>
![](https://i.imgur.com/BSrrlfl.png)</br>
  依照上面的公式定義，對每個點與其它所有的計算相似度，給定初始值後，用一個二維矩陣來做計算，對每個點迭代計算與其它所有不同點的結果，迭代到與上次誤差不大則結束迭代。

## Result analysis and discussion
### 以下呈現 graph 1~6及IBM的data的directed、bidirected結果
### graph_1.txt 
* HITS</br>
![](https://i.imgur.com/nt78xdu.png)

* PageRank </br>
![](https://i.imgur.com/UwpzSI2.png)

* SimRank</br>
![](https://i.imgur.com/TktqS8p.png)

### graph_2.txt 
* HITS</br>
![](https://i.imgur.com/sMXSexR.png)

* PageRank </br>
![](https://i.imgur.com/YlaAhJy.png)

* SimRank</br>
![](https://i.imgur.com/efK4M6d.png)


### graph_3.txt 
* HITS</br>
  ![](https://i.imgur.com/BFVPfMd.png)

* PageRank </br>
  ![](https://i.imgur.com/KT65kHf.png)

* SimRank</br>
  ![](https://i.imgur.com/xpTsXPf.png)

### graph_4.txt
* HITS</br>
  ![](https://i.imgur.com/FBMBD7h.png)

* PageRank </br>
  ![](https://i.imgur.com/NqiLUh7.png)

* SimRank</br>
  部分結果</br>
  ![](https://i.imgur.com/vQCW3h3.png)

### graph_5.txt
* HITS</br>
  ![](https://i.imgur.com/oxq3o3G.png)</br>

  ![](https://i.imgur.com/5K4lLW6.png)
  
* PageRank </br>
  ![](https://i.imgur.com/mZP1Jel.png)

* SimRank</br>
  部分結果</br>
  ![](https://i.imgur.com/XGY7HEO.png)

### graph_6.txt
* HITS</br>
  部分結果</br>
  ![](https://i.imgur.com/Ml0wUi3.png)</br>
  ![](https://i.imgur.com/xptpiEJ.png)

  
* PageRank </br>
  部分結果</br>
  ![](https://i.imgur.com/C1oIzEH.png) 

* SimRank</br>
  部分結果</br>
  ![](https://i.imgur.com/iMD1adf.png)
  
  
### ibmData_directed.txt
* HITS</br>
  部分結果</br>
  ![](https://i.imgur.com/cmJtZTH.png)</br>
  ![](https://i.imgur.com/4nPfCo2.png)</br>

* PageRank </br>
  部分結果</br>
  ![](https://i.imgur.com/pSE8jhu.png)

### ibmData_bidirected.txt
* HITS</br>
  部分結果</br>
  ![](https://i.imgur.com/Okc1Baf.png)</br>
  ![](https://i.imgur.com/f8I7A7Y.png)</br>

* PageRank </br>
  部分結果</br>
  ![](https://i.imgur.com/aKPaSKb.png)


  
### discussion
* 透過上面呈現的結果可以觀察到，像圖1這種直接從1連續連連到5也沒有cycle的圖，authorities會在起始node(0)的位置值為0，因為沒有父節點可以計算出值，hub則是會在結束點(6)位置為0，因為沒有子節點能夠計算出值，而PageRank則會在起始點比較低。
* 在實作SimRank的過程中，發現若依照遞迴式直接coding，在遇到有cycle的圖片時會無法結束，所以會用給予每個node對應其他node的相似度初始值，再依照公式計算，直到誤差夠小就結束迭代的這種計算方式來實作此演算法。


## Computation performance analysis
### HITS
* time

  | graph   | time     |
  | ---     |  ---     |
  | graph_1 | 0m0.091s |
  | graph_2 | 0m0.092s |
  | graph_3 | 0m0.091s |
  | graph_4 | 0m0.093s |
  | graph_5 | 0m0.129s |
  | graph_6 | 0m0.813s |
  | ibmData_directed | 0m5.744s |
  | ibmData_bidirected | 0m5.446s |

### PageRank 
* time

  | graph   | time     |
  | ---     |  ---     |
  | graph_1 | 0m0.090s |
  | graph_2 | 0m0.091s |
  | graph_3 | 0m0.090s |
  | graph_4 | 0m0.091s |
  | graph_5 | 0m0.157s |
  | graph_6 | 0m0.322s |
  | ibmData_directed | 0m1.942s |
  | ibmData_bidirected | 2m19.967s |

### SimRank
* time

  | graph   | time     | 
  | ---     |  ---     |
  | graph_1 | 0m0.092s |
  | graph_2 | 0m0.092s |
  | graph_3 | 0m0.092s |
  | graph_4 | 0m0.096s |
  | graph_5 | 0m9.897s |
  | graph_6 | 0m39.897s|


### analysis
* 上面的執行時間結果可以觀察到，在圖1~4這種很小的圖時間差距不大觀察不出什麼，而5、6和ibmData_directed及ibmData_bidirected開始，就會因為點數的不同和link的特性而有不同的執行時間，而SimRank時間複雜度較高，在點數多圖複雜時，時間差距就會很明顯。


## Discussion 
* 在這個project中要我們實作HITS、PageRank及SimRank三種不同的演算法，此三種方法概念上略有一些差異，但都對搜尋引擎有很大的幫助，可以應用於含有元素之間相互參照的情況，而且不只是要考慮經度問題，還要將計算的時間複雜度考量進去，因此在寫程式時上網搜尋作法也會發現一些演算法變體。



## Find a way (e.g., add/delete some links) to increase hub, authority,and PageRank of Node 1 in first 3 graphs respectively
* hub的計算方式是child node的authority值相加出來的，所以若要增加hub，以圖1為例，要增加結束點6(無child或少child)之node的child link數，或是增加影響權重，圖2及圖3也是同理。

* authority的方法也類似，authority的計算方法是parent node的hub值相加出來的，因此要增加authority擇要增加起始點(無或少parent)之node的parent link數，，或是增加影響權重，圖2及圖3也是依此類推。



## Questions & Discussion


### More limitations about link analysis algorithms
* 大部分的演算法，都沒有辦法在圖中很好的找到每個node之間最佳的相關性，評分的標準只用連結束來判定可能有些不足，連結數多寡的可能有太多變因，網頁質量和連結數其實相關性是不太足夠的。


### Can link analysis algorithms really find the “important” pages from Web?
* 如上題所述，沒有辦法找到很好的important pages，在實際情況中的連結可能也有很多相干度不高的網頁，甚至是廣告蓋版的問題等等，更舊的網頁分數也會因為演算反可能分數高，但實際重要程度可能不及新網頁的質量。


### What are practical issues when implement these algorithms in a real Web?
* 最常見的就是用在搜尋引擎，做網頁排名，像PageRank是google早期用來對搜尋引擎的搜尋結果中做網頁排名的演算法，而像google這種資料量如此龐大的公司，不僅僅是要考量到演算法的精準度，還要顧及時間複雜度不能夠太高，以免造成效能不佳導致使用者體驗不好的問題，因此也有了許多的演算法變體。


### Any new idea about the link analysis algorithm?
* 可能可以多考慮幾層的關係而不只是一層，但時間複雜度也要有所取捨，或為不同的網頁判斷不同的權重，不然就是加入一些使用者偏好的因素在裡面，如瀏覽紀錄或書籤網站等等，藉此來設計新的演算法。


### What is the effect of “C” parameter in SimRank? 
* C在SimRank的演算法中代表著阻尼常數，有衰退的效用，較近的共同父節點有比較強的影響力，而比較遠的會因為此係數的關係影響遞減。




