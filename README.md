# Winter Co. SF-price-calculator

从Gitee平台访问：https://schwarzi.gitee.io/winterco.-sf-price-calculator/interface.html

## 2022/5/10 V1.2.1

Amendments:

- Update routes
- Update charging rules
- Update minimum charging fee
- Change reddish color

New feature:

- Add minimum charging fee display
- Add maximum delivery time display

改动：

- 更新线路
- 更新计费规则
- 更新起步价
- 更换红色颜色

新增内容：

- 新增线路起步价显示
- 新增最大送达时间（时效）显示

## 2022/5/7 V1.2.0

Issue fix and amendment:

- Support decimals input for number inputs
- Limit the maximum amount of digit input for collateral to 14

New features:

- Implement accelerated contract type option
- Add new text for fee standard
- Support freely adding or deleting digits at any positions within a number input

修复与改动：

- 数字输入支持小数点输入与代入计算
- 保证金条目限制最大输入14位数字

新增内容：
- 实现加急合同功能
- 新增计费规则文本
- 数字输入支持在数字的任意位置键入或删除数字

## 2022/5/6 V1.1.1

- Add buttons to switch contract type (not link with the fee)
- Adjust cell background colors


- 新增切换合同类型的按钮（还未与计费进行关联）
- 微调字块背景颜色

Gitee pages完成部署

## 2022/5/5 V1.1.0

New features:

- New layout and colors
- Use SUP tag to show superscipt "3"
- Support different route prices
- Support upstream/downstream route prices and indication
- Indicate route fee and charge standard separately

Contract type will be implemented in the next version

新增内容：

- 新布局及颜色
- 使用SUP标签来表示上标“3”
- 支持不同线路计费
- 支持上行/下行线路不同计费及上下行标示
- 分开标示线路价格及计费标准

加急合同功能将在下版本中实装

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
- 起点与终点的互换



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
