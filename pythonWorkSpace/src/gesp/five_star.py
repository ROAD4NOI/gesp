import turtle

t = turtle.Turtle()

print(t.position())

t.fillcolor("red")
t.begin_fill()
for i in range(5):
    t.forward(200)
    t.right(144)
t.end_fill()

t.penup()
t.goto(100,-100)
t.pendown()

t.fillcolor("red")
t.begin_fill()
# t.circle(100,extent=360,steps=10)
t.end_fill()

print(t.position())

turtle.done()