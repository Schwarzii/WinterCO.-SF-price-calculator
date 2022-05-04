# Winter Co. SF-price-calculator

## 2022/5/4 V1.0.1
Update:

- Change fonts and font sizes

New features:

- Different prices associated with different routes (Not completely implemented)
- Route selection
- Automatically update available arrival stations after selected a departure station
- Departure/arrival station switch

改动：

- 调整字体和字体大小

新增内容：

- 不同线路不同计价 （代码中已添加为字典，未完全与线路选择进行关联）
- 线路选择
- 根据已选择的起点自动给出可到达的终点
- 起点与终点的交换



## 2022/5/3 V1.0.0

First version to achieve automatic delivery price calculation depending on volume and collateral.

- Max(1% of collateral, volume fee) is implemented.
- The lowest delivery fee limit 5M ISK is implemented.

Different route prices (upstream/downstream courier and different departure/destinations) and urgent courier contract are not yet taken into account.

联盟论坛发布地址： https://forums.winterco.org/t/topic/13444

目前计算器仅支持Jita到4-HWWF的下行路线的计价，并可实现以下功能：

- 按给出保证金的1%或者体积运费的高价进行计算
- 按保底运费进行计算
- 出发地和目的地的互换（但暂无实用效果）

比照[现行运费计算器](https://platos.gitee.io/s.f-express-calculator/)，仍有以下功能需要实现：
- 上下行不同计价
- 不同路线不同计价
- 加急合同的选择及不同计价
- 游戏内合同样本预览
