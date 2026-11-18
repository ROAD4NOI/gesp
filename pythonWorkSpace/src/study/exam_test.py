tt = '帅小伙'

H1 = int(input()) # Alice 的身高
H2 = int(input())
H3 = int(input())
H4 = int(input())
# 我们只关心 H2, H3, H4（其他三个小朋友）
# 先算出每个人和 Alice 的身高差（用绝对值，这样不会负数）
# 与H2小朋友的身高差
# 如果身高差为负数，转换为正数。
diff2 = H2 - H1

if diff2 < 0:
	diff2 = -diff2

# 与H3小朋友的身高差
diff3 = H3 - H1
if diff3 < 0:
	diff3 = -diff3
# 与H4小朋友的身高差
diff4 = H4 - H1
if diff4 < 0:
	diff4 = -diff4
# 刚开始假设最好的朋友是 H2
best = H2 # 最好的小朋友身高，
best_diff = diff2 # 与最好小朋友的身高差
# 比较 H3 小朋友
if diff3 < best_diff: # 如果 H3 更接近，即身高差更小
	best = H3 # 最好小朋友的身高进行更新
	best_diff = diff3 # 与最好小朋友的身高差更新
elif diff3 == best_diff and H3 < best: # 如果一样近，但 H3 小朋友更矮
	best = H3
# 比较 H4
if diff4 < best_diff: # 如果 H4 更接近
	best = H4 # 最好小朋友的身高进行更新
	best_diff = diff4 # 与最好小朋友的身高差更新
elif diff4 == best_diff and H4 < best: # 如果一样近，但 H4 更矮
	best = H4

# 输出结果，即输出最好小朋友的身高
print(best)