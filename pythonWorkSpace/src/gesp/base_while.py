
i = 1
while i <= 500:
	if i % 11 == 0:
		i += 10
		continue
	if i % 101 == 0:
		break
	print(i)
	i += 10

print("while循环结束")
a = 5748748
s = ""
while a > 0:
	q = a % 10
	print(q)
	s = s + str(q)
	a = a // 10
print(s)

c = 1
for i in range(5):
	print(i)
	
	if i == 2:
		break
	c += 1
print(c)	
