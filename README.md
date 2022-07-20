# Dig! python

清华附中 C16 / G19 著名多人即时对战游戏“掘”的python版本

## 游戏规则
### 0 回合制
游戏参与者称为角色，所有角色同时出招，称为一回合，游戏总回合数无限制，当且仅当符合胜利条件时，游戏结束。
### 1 资源
游戏中使用一种称为“掘”的资源，需要消耗一回合来获得一个“掘”。消耗“掘”，可以用来攻击或建造建筑，甚至防御。
### 2 建筑
#### 2.1 塔
消耗一个“掘”。积攒“塔”，可以用来解锁攻击“射”和“高射”。
#### 2.2 兵营
消耗两个“掘”，可以用来生产“兵”。每个“兵”的产生需要在有“兵营”存在的条件下，消耗一回合来获取。“兵”可以用来解锁攻击“砍”。同时，在受到致命伤害时，消耗两个“兵”可以抵消该次攻击。
### 3 攻击
#### 3.1 猛进
消耗两个“掘”，可指定单一目标。可被“防猛”或“抱头”防御。
#### 3.2 射
消耗一个“塔”，可指定单一目标。可被“防射”或“抱头”防御。
#### 3.3 高射
消耗两个“塔”，可指定单一目标。可被“防高射”或“抱头”防御。
#### 3.4 下地
消耗两个“抱头次数”，指定除自己外全体目标，可被“防射”防御。
#### 3.5 砍
消耗一个“兵”，可指定单一目标。可被“防砍”或“抱头”防御。
###  4 防御
#### 4.1 防猛
可防御“猛进”。当使用“防猛”成功防御“猛进”后，可积攒“防猛次数”。当“防猛次数”大于等于二时，可消耗两个“防猛次数”来使用任意攻击。
#### 4.2 防射
可防御“射”和“下地”。
#### 4.3 防高射
可防御“高射”。
#### 4.4 抱头
消耗一个“掘”，可防御除“下地”外所有攻击。当使用“抱头”后，可积攒“抱头次数”。当“抱头次数”大于等于二时，可消耗两个“抱头次数”来使用下地。
### 5 角色死亡
当受到攻击后，角色需要进行死亡结算。
#### 5.1 情况一：成功防御
当角色只受到单一类型攻击时，且角色使用了恰当防御，角色存活。
#### 5.2 情况二：防守反击
当角色只受到单一来源攻击时，若角色使用了攻击力大于对方的攻击，角色存活，对方角色死亡；若角色使用了与对方相同的攻击，双方均存活；若角色使用了攻击力小于对方的攻击，角色死亡。

攻击力顺序：高射 > 砍 > 猛进 > 射 > 下地。
#### 5.3 情况三：其他
除上文特别说明外，角色死亡。
### 胜利条件
场上仅一人存活时，该角色胜利。

## Author

此项目由 [ZHC](https://github.com/zhc7) 开发和维护，游戏规则来自清华附中 G19。