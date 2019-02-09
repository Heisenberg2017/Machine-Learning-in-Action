# 机器学习实践 - Python
介绍一些机器学习算法的简单实现及应用
 

## 分类算法
 
### k-近邻算法
#### 预测约会网站对象的喜欢程度

![alt text][knn-dating-image-1]
![alt text][knn-dating-image-2]


Matplotlib创建散点图帮助理解数据之间的关系，通过散点图可以发现玩游戏所耗时间百分比和每年的飞行里程数可以更好的区分对约会对象的喜欢程度。

#### 识别手写数字
![alt text][knn-number-image-1]
![alt text][knn-number-image-2]

使用k-近邻算法识别手写数字

###### 案例来源: [Machine-Learning-in-Action][k-nearest-neighbors-demo-source]
###### k近邻算法: [Wikipedia][k-nearest-neighbors-algorithm]
 
### 决策树

#### 使用ID3决策树预测隐形眼镜类型
![alt text][decision-tree-image-1]

图形化展示了隐形眼镜数据集在ID3算法上生成的决策树

###### 案例来源: [Machine-Learning-in-Action][decision-tree-algorithm]
###### 决策树: [Wikipedia][decision-ID3-tree-demo-source]





[knn-dating-image-1]: https://github.com/Heisenberg2017/Machine-Learning-in-Action/blob/master/images/kNNDating1.gif "kNN Dating Plot"
[knn-dating-image-2]: https://github.com/Heisenberg2017/Machine-Learning-in-Action/blob/master/images/kNNDating2.gif "kNN Dating Plot"
[knn-number-image-1]: https://github.com/Heisenberg2017/Machine-Learning-in-Action/blob/master/images/kNNNumber1.gif "kNN Number Data"
[knn-number-image-2]: https://github.com/Heisenberg2017/Machine-Learning-in-Action/blob/master/images/kNNNumber8.gif "kNN Number Data"
[decision-tree-image-1]: https://github.com/Heisenberg2017/Machine-Learning-in-Action/blob/master/images/DecisionTree1.gif "Decision Tree ID3"


[k-nearest-neighbors-algorithm]: https://en.wikipedia.org/wiki/K-nearest_neighbors_algorithm
[decision-tree-algorithm]: https://en.wikipedia.org/wiki/Decision_tree


[k-nearest-neighbors-demo-source]: https://livebook.manning.com/#!/book/machine-learning-in-action/chapter-2/
[decision-ID3-tree-demo-source]: https://livebook.manning.com/#!/book/machine-learning-in-action/chapter-3/
