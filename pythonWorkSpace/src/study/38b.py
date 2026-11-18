
# a=int(input('数a:'))
# s=int(input('数s:'))

# if a<s:
#  print('a')
#else :
#  print('s')

n = int(input("厂家数:"))

if n < 1:
  print("厂家数不能小于 1")
else :
  m = int(input("输入厂家报价:"))
  if n == 1:
    print(m)
  else :
    for i in range(n-1):
      x = int(input("输入厂家报价:"))
      if m >= x:
        m = x
    print(m)






