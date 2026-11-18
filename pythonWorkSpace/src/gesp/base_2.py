# name = "乐乐"
# father = "爸爸"
# print(f"你好，{name}，我是你{father}")

a = input("你叫什么？")
print("我叫",a)

# a = 3
# b = int(a)

# if b > 3:
#	print("test")
# else:
#	print("ddddd")

# input = "1"
# print(input)

# for_ = "fd "
# print(for_)

name = input("你叫什么？")
mother = name == "刘硕"
print(mother)
if name == "刘倩":
	print(f"WOW，{name}真是大美女")
elif name == "刘博":
	print("你可真厉害")
elif name == "乐乐":
	print("你可真帅")
else:
	print(f"{name},你是大好人")

# name2 = int(name)+1

name2 = float(name)+1.1
print(name2)

mother = "mm"
father = mother * 3
print(father)

num = 123
print(num%10)
num //= 10
print(num)