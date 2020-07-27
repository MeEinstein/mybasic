#输出结果
print('hello_world')

#注释, 不是代码不执行

#引入包
import math
from math import exp

#使用包
print(math.e)  #e是math的一个变量
print(math.exp(10))  #exp是math的一个函数
print(exp(10))

#自定义变量
a = 10  #整型数 int
b = 1.0  #浮点数, 也就是小数 float
c = 'hello' #字符串 str
d = True #布尔数 bool
e = [1, 2, 3, 4, 5, 6] #数组 list
f = {'Tom': 99,
     'Alice': 100,
     'Jone': 60}  #字典dictory

#自定义一个函数
def add(param1, param2):  #param1, param2是函数的参数
    result = param1 + param2
    return result   #return返回结果

#使用自定义的函数
print(add(10, 20))
print(add(a, b))

#程序控制
if a > b:  #选择
    print('对')
else:
    print('错')

for i in range(10):  #循环
    print(i)

while b < a:  #循环
    print('还没')
    print(b)
    b = b + 1

#while True:
#    print('死循环')

#格式 tab对齐
from PIL import Image
image = Image.open('./尺子.jpg')
image.show()

if __name__ == '__main__':  #主程序入口
    print(add(11, 22))



