import csv
import matplotlib.pyplot as plt
import numpy as np

import matplotlib.pyplot as plt

file1 = open('BCHAIN-MKPRU.csv','r')
file2 = open('LBMA-GOLD.csv','r')
def drawpicture(file):
    nums = []
    num2 = []
    strs = []
    init = 1000
    j = 0
    for i in file:
        str = i.split(',')
        nn = str[0].split('/')
        print(nn[0])
        print(nn[1])
        print(nn[2])
        # print(str[1],end='')
        if len(str[1]) == 1:
            nums.append(1)
            num2.append(init)
            strs.append(str[0])
            j+=1
            print('######################################')
            continue
        num = float(str[1])
        strs.append(str[0])
        nums.append(num/init)
        num2.append(num)
        # if(num/init == 1):
        #     print('########################')
        #print(num)
        print(num/init)

        #print(type(i))
        init = num
        print(j)
        j+=1

    del nums[0],num2[0]
    print(nums)
    range1 = range(0,len(nums))
    # print(len(range1))
    print(len(''))
    # nums.sort(key= None,reverse=False)
    #num2.sort(key= None,reverse=False)

    plt.plot(range1,num2)
    plt.show()
    return nums,strs
num1,strs1 = drawpicture(file1)
num2,strs2 = drawpicture(file2)

#
# range2 = [0,0,0,0,0,0,0,0,0,0,0,]
# # #画柱状图
# # for i in num1:
# #     if i > 1.1:
# #         range2[0]+=1
# #         continue
# #     elif i > 1.08:
# #         range2[1] += 1
# #         continue
# #     elif i > 1.06:
# #         range2[2]+=1
# #         continue
# #     elif i > 1.04:
# #         range2[3]+=1
# #         continue
# #     elif i > 1.02:
# #         range2[4]+=1
# #         continue
# #     elif i > 0.98:
# #         range2[5]+=1
# #         continue
# #     elif i > 0.96:
# #         range2[6]+=1
# #         continue
# #     elif i > 0.94:
# #         range2[7]+=1
# #         continue
# #     elif i > 0.92:
# #         range2[8]+=1
# #         continue
# #     elif i > 0.9:
# #         range2[9]+=1
# #         continue
# #     else:
# #         range2[10]+=1
# #         continue
#
#
# # plt.bar(x =['0.9','0.92','0.94','0.96','0.98','1.0','1.02','1.04','1.06','1.08','1.1'],height=range2)
# # print(range2)
# # plt.show()
#
# #更细致的柱状图
# for i in num2:
#     if i > 1.04:
#         range2[10]+=1
#         continue
#     elif i > 1.032:
#
#         range2[9]+=1
#         continue
#     elif i > 1.024:
#         range2[8]+=1
#         continue
#     elif i > 1.016:
#         range2[7]+=1
#         continue
#     elif i > 1.008:
#         range2[6]+=1
#         continue
#     elif i > 1:
#         range2[5]+=1
#         continue
#     elif i > 0.992:
#         range2[4]+=1
#         continue
#     elif i > 0.984:
#         range2[3]+=1
#         continue
#     elif i > 0.976:
#         range2[2]+=1
#         continue
#     elif i > 0.968:
#         range2[1]+=1
#         continue
#     else:
#         range2[0]+=1
#         continue
#
# plt.bar(x =['1.04','1.032','1.024','1.016','1.008','1.0','0.992','0.984','0.976','0.968','0.960'],height=range2)
# print(range2)
# print(len(num2))
# plt.show()
#
#
#统计连续涨跌的幅度及次数
j = 0

num3 = []#比特币的涨跌记录
num4 = []#黄金的涨跌记录

num5 = []
num6 = []

strs3 = []#记录对应日期
strs4 = []#记录对应日期

y = 0#跌的次数
x = 0#长的次数

while j != 1824:#比特币的
    l = j
    k = 1
    while num1[j]>1:
        k *= num1[j]
        j += 1
    if k != 1:
        print(strs1[l],end='至')
        print(strs1[j],end='涨幅为')
        num3.append(k)
        print(k,end='  ')
        print('第'+str(j)+'个交易日')
        x += 1
        num5.append(j-l)
        continue
    while num1[j] < 1:
        k *= num1[j]
        j += 1
    if k != 1:
        print(strs1[l], end='至')
        print(strs1[j], end='跌幅为')
        print(k, end='  ')
        num3.append(k)
        print('第'+str(j)+'个交易日')
        y += 1
        num5.append(j - l)
        continue
    if k == 1:
        j+=1
        print(j)
        num5.append(j - l)
        num3.append(k)
        continue



print(x)
print(y)

j = 0
y = 0
x = 0
while j != 1264:#黄金的
    l = j
    k = 1
    while num1[j]>1:
        k *= num1[j]
        j += 1
    if k != 1:
        print(strs1[l],end='至')
        print(strs1[j],end='涨幅为')
        print(k,end='  ')
        num4.append(k)
        print('第'+str(j)+'个交易日')
        x+=1
        num6.append(j - l)
        continue
    while num1[j] < 1:
        k *= num1[j]
        j += 1
    if k != 1:
        print(strs1[l], end='至')
        print(strs1[j], end='跌幅为')
        print(k, end='  ')
        num4.append(k)
        print('第'+str(j)+'个交易日')
        y+=1
        num6.append(j - l)
        continue
    if k == 1:
        j+=1
        print(j)
        num6.append(j - l)
        num4.append(k)
        continue
#
# print(x)
# print(y)

# # rangeb = range(0,len(num3))
# # plt.plot(rangeb,num3)
# # plt.show()
# #
# # rangeg = range(0,len(num4))
# # plt.plot(rangeg,num4)
# # plt.show()
#
#
# # o = 1000 #本金
# # u = 1324.6 #用于验证的黄金初始价格
# # p = 0 #计算涨的次数
# # print(num3)
# # for i in num3:
# #     if i > 1.04123:
# #         print(i)
# #         p+=1
# #         o *= 0.98*i*0.98
# # print(len(num3))
# #
# # print(o)#总收益
# # print(p)#涨的次数
# # print(u)#黄金最终价格（已删除
# # j = 0
#
# num7 = []
# num8 = []
#
# for i in num3:
#     if i > 1:
#         print('涨' + str(num5[j]) + "天")
#         num7.append(num5[j])
#         j+=1
#
#     elif i < 1:
#         print('跌' + str(num5[j]) + '天')
#         num7.append(-1*num5[j])
#         j +=1
#
#     else:
#         num7.append(0)
#         print('平')
#         j+=1
# print(j)
#
# rank = [0,0,0,0,0]
#
# rank1 = range(0,len(num7))
#
# for i in num8:
#     if i > 5:
#         rank[0]+=1
#     elif i > 3:
#         rank[1]+=1
#     elif i > 2:
#         rank[2]+=1
#     elif i > 1:
#         rank[3]+=1
#     else:
#         rank[4]+=1
# plt.rcParams['font.sans-serif'] = ['SimHei']
# plt.rcParams['axes.unicode_minus'] = False
# # plt.bar(x =['5以上','3-5','3','2','1'],height=rank)
# plt.plot(rank1,num7)
# print(num7)
# plt.show()