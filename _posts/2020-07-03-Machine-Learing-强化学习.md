---
categories: [Machine Learing]
tags: [强化学习,似然函数]
---
# 强化学习

- 似然函数

  - ​     
    $$
    \theta=argmax_\theta \{Reward\_function\}
    $$

# PPO算法

- **Proximal Policy Optimization近端策略优化**

- 目标函数表示

  - <img src="C:\Users\lxz\AppData\Roaming\Typora\typora-user-images\1665215716544.png" alt="1665215716544" style="zoom:50%;" />

  - 这个目标函数就是要找到使得整场奖励最大的\theta，但是由于对相同的\theta有可能出现不同的action（是基于概率的选择），所有理论上要将所有可能的action对应的reward计算起来，求得使得所有action对应的reward的期望最大的\theta。但是这个计算不太可能，所有使用大数定理去逼近这个期望，即采取足够多的抽样预测期望。
  - <img src="C:\Users\lxz\AppData\Roaming\Typora\typora-user-images\1665216106901.png" alt="1665216106901" style="zoom:50%;" />
  - 也可写成 ，其中π(T)表示当前序列可能性，r(T)为奖励：
  - <img src="C:\Users\lxz\AppData\Roaming\Typora\typora-user-images\1665216488030.png" alt="1665216488030" style="zoom:50%;" />
  - 对\theta求梯度
  - <img src="C:\Users\lxz\AppData\Roaming\Typora\typora-user-images\1665216701036.png" alt="1665216701036" style="zoom:50%;" />
  - <img src="C:\Users\lxz\AppData\Roaming\Typora\typora-user-images\1665216760822.png" alt="1665216760822" style="zoom:50%;" />
  - <img src="C:\Users\lxz\AppData\Roaming\Typora\typora-user-images\1665216645582.png" alt="1665216645582" style="zoom:50%;" />
  - 求得梯度之后，出现了一个问题：我们每次对整场游戏进行多次采样以逼近那个期望，但是这样的多次采样得到的数据只可以更新一次\theta参数，这样训练的代价还是比较大
  - ppo将On policy转变成Off policy一定程度上解决了这个问题
  - <img src="C:\Users\lxz\AppData\Roaming\Typora\typora-user-images\1665217109989.png" alt="1665217109989" style="zoom:50%;" />
  - 这个的意思就是我们通过对q(x)进行采样，再通过乘上p(x)/q(x)的权重，来模拟这些数据是从当前p(x)分布采取的数据，这样我们通过对q(x)的一次采样,就可以多次对p(x)的\theta进行更新
  - 但是这样每次p(x)/q(x)会在p(x)更新之后会发生改变，所以我们应该尽可能使得p(x)/q(x)=1，就是\theta'=\theta，这样的后果就是对于一次q(x)的采样，p(x)更新是有限制次数的
  - 也可以看成下图，当p(x)与q(x)分布相差太大，我们**有限次的抽样**就不可以保证上面的积分相等（如果不是抽样，就满足）
  - <img src="C:\Users\lxz\AppData\Roaming\Typora\typora-user-images\1665218116921.png" alt="1665218116921" style="zoom:50%;" />
  - 所以使用一个替代的\theta训练\theta的梯度可以表示成
  - <img src="C:\Users\lxz\AppData\Roaming\Typora\typora-user-images\1665217680495.png" alt="1665217680495" style="zoom:50%;" />
  - 其中的π(T)可以写成p(a|s)*p(s)
  - 然后p(s)/q(s)可以看成1，得到下式
  - <img src="C:\Users\lxz\AppData\Roaming\Typora\typora-user-images\1665217954600.png" alt="1665217954600" style="zoom:50%;" />
  - 当\theta'与\theta的kl散度超过阈值停止此次更新
  - 最后ppo与ppo2的loss

  - <img src="C:\Users\lxz\AppData\Roaming\Typora\typora-user-images\1665218940361.png" alt="1665218940361" style="zoom:50%;" />

  - <img src="C:\Users\lxz\AppData\Roaming\Typora\typora-user-images\1665218892906.png" alt="1665218892906" style="zoom:50%;" />

- tips
  - reward
    - 对于每场游戏的总reward应该减去一个值，因为很有可能reward没有负值，这对没有sample到但是事实reward是很好的不公平
    - 对于单独一场游戏的reward，当前action的reward应该只与其后面的reward相关，并且有折扣
    - <img src="C:\Users\lxz\AppData\Roaming\Typora\typora-user-images\1665219145644.png" alt="1665219145644" style="zoom:67%;" />

# DQN

- Q-Leanring
  
  - 总的思想是根据以前的经验判断当前的行为使得后面所得奖励最大
  - 学习目标是以前的经验
  
- **DQN**

  - 将Q-Leanring扩展到连续空间可得到DQN

    - 在DQN中训练目标为一个神经网络，这个神经网络会输入**当前状态计算最大的Q值对于的action**（模型的目标输出Q值），得到一个新状态，以及一个奖励，以前的记忆网络根据新状态计算出记忆中最好的Q值对应的action，在新的网络这个当前状态对应action的Q值会根据以前的记忆网络计算出来了的Q值加上此时奖励的值进行回归训练。

    - 这个就类似将当其的行为选择与奖励和以后的行为联系起来

    - ```python
      q_eval = self.eval_net(batch_state).gather(1, batch_action)#得到当前Q(s,a)
      q_next = self.target_net(batch_next_state).detach()#得到Q(s',a')，下面选max
      q_target = batch_reward + GAMMA*q_next.max(1)[0].view(BATCH_SIZE, 1)#公式
      loss = self.loss(q_eval, q_target)#差异越小越好
      ```

# A3C

- 