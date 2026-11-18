import turtle


# turtle.circle(100)

turtle.pencolor("red")
turtle.pensize(10)

for i in range(4):
	turtle.forward(100)
	turtle.right(90)

turtle.penup()

turtle.forward(200)
turtle.pendown()

turtle.circle(100)

turtle.penup()
turtle.backward(300)

turtle.pendown()

turtle.circle(100)

turtle.done()
