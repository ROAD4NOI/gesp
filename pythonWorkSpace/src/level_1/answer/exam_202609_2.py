n = int(input())
# f:当前的格子有多少麦子，ans: 总共有多少麦子
f, ans = 1, 0
# 遍历棋盘的每一个格子
for i in range(n):
# 把当前格子的麦子加入到总结果
  ans += f
# 下一个格子的麦子数目乘以2
  f *= 2

print(ans)