import turtle
N = int(input("请输入射线数量："))
Angle = 360 / N #计算出每条射线之间间隔的角度

for i in range(N):
	if i % 5 == 0:
		turtle.pencolor("red")
	else:
		turtle.pencolor("black")
	turtle.right(Angle)
	turtle.forward(100)
	turtle.goto(0,0)

turtle.done()