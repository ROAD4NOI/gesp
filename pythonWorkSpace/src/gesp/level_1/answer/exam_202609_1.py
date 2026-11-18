# 202609 真题 1 参考程序

# 接收乌龟到终点的时间，兔子速度，兔子的睡眠时间
t1 = float(input())
v  = float(input())
t2 = float(input())

# 兔子到达的时间，1000/v是跑步的时间，t2是睡觉的时间
tt = 1000.0 / v + t2

# 乌龟到达时间大于兔子到达时间
if tt < t1:
	print('rabbit')
# 乌龟到达时间小于兔子到达时间
elif tt > t1:
	print('turtle')
# 平局
else:
	print('tie')

print(f'{tt:.2f}')

td = int(tt)
print(f'{td:d}')