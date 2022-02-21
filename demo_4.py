# import csv
# import matplotlib.pyplot as plt
import numpy as np
import matplotlib.pyplot as plt

commissionbit = 0.98#佣金 比特币
commissiongold = 0.99 #佣金 ，黄金

start = 15
end   = 50

class Wallet:
    def __init__(self):       #基本信息设置
        self.dollor = 1000      #美元
        self.gold   = 0         #黄金
        self.bitcoin= 0         #比特币

        self.base = 980.0      #基准
        self.lilv = commissionbit*commissionbit

        self.record = []  # 记录交易时间
        self.recordnum = 0  # 记录交易次数
        self.dollorin = []  # 记录购买视觉
        self.dollorout = []  # 记录卖出时间

        self.bitcoinm = 0

    def now(self):           #方便随时显示基本信息
        print("现有本金" + str(self.dollor) + "美元 \n黄金" + str(self.gold) + "美元 \n比特币" + str(self.bitcoin) + "美元")
        return self.dollor,self.gold,self.bitcoin


class Price:
    def __init__(self):
        self.file1 = open('BCHAIN-MKPRU.csv', 'r')
        self.file2 = open('LBMA-GOLD.csv', 'r')

        self.bitcoindata = []       #比特币日期
        self.golddata    = []       #黄金日期
        self.bitcoinnow  = []       #比特币对应日期的价格
        self.goldnow     = []       #黄金同上
        self.goldstate   = []       #黄金是否可以交易

        for i in self.file1:
            info = i.split(",")
            if info[0] == "Date":
                continue
            self.bitcoinnow.append(float(info[1]))
            #data = info[0].split('/')
            self.bitcoindata.append(info[0])
            #print(info[0])

        j = 0#辅助变量，帮助遍历黄金
        for i in self.file2:    #补齐没有的周六周天，将黄金和比特币统一大小
            info = i.split(",")
            if info[0] == "Date":
                continue
            while info[0] != self.bitcoindata[j]:
                self.golddata.append(self.bitcoindata[j])
                self.goldnow.append(self.goldnow[-1])
                self.goldstate.append(False)
                j+=1
            if len(info[1]) < 2:
                self.goldnow.append(self.goldnow[-1])
            else:
                self.goldnow.append(float(info[1]))
            self.golddata.append(info[0])
            self.goldstate.append(True)
            j+=1
        #print(len(self.goldnow))
        #print(len(self.bitcoinnow))


#计算线性回归  切记，返回值乘五万了
def regression(*args):

    sum = 0
    args = args[0]
    #print(args)
    for i in args:
        sum += i
    average = sum/len(args)
    sumxy = 0
    sumxx = 0
    count = 0
    for i in range(1,len(args) + 1):
        sumxy += i*args[count]
        sumxx += i*i
        count += 1

    #print((sumxy - len(args)*average*(len(args)+1)/2)/(sumxx - len(args)*((len(args)+1)/2)*((len(args)+1)/2)))
    return (sumxy - len(args)*average*(len(args)+1)/2)/(sumxx - len(args)*((len(args)+1)/2)*((len(args)+1)/2))

da = []
xiao = []

def judge(wallet,i,slope,*args):
    goldlistj = args[0]         #黄金价格  j结尾
    bitcoinlistj = args[1]      #比特币价格 j结尾

    # a.append(goldlinem)
    # b.append(bitcoinlinem)
    # c.append(goldlinen)
    # d.append(bitcoinlinen)
    # print(goldlinem)
    # print(bitcoinlinem)
    # print(goldlinen)
    # print(bitcoinlinen)
    bitcoinn = []           #比特币now的 也就是最近二十天的数据
    bitcoins = 0            #比特币sum 总和 s结尾
    for j in range(20,0,-1):
        bitcoinn.append(price.bitcoinnow[i - j])
        bitcoins += price.bitcoinnow[i - j]
    bitcoina = bitcoins/50  #比特币最近二十天的平均值
    bitcoinn.sort(key=None,reverse=False)
    #print(bitcoinn)
    #goldlinem = regression(goldlistj)  # 黄金回归曲线
    bitcoinlinem = regression(bitcoinlistj)*50000  # 比特币回归曲线
    #goldlinen = regression(goldlistj[-int(round / 5):-1])  # 黄金近期曲线
    #bitcoinlinen = regression(bitcoinlistj[-int(round / 5):-1])  # 比特币近期曲线
    bitcoinlinen = regression(bitcoinlistj[-3:-1])*50000  # 比特币近期曲线
    da.append(bitcoinlinem)
    xiao.append(bitcoinlinen)

    ##################################################################################################################
    #策略  返回0买（得有钱），返回1卖（得有比特币） 返回其他任意数字均为不动
    # print("da" , end="")
    # print(bitcoinlinem)
    # print("xiao" , end="")
    # print(bitcoinlinen)
    if wallet.dollor == 0:
        if wallet.bitcoin >= wallet.base * wallet.lilv and bitcoinlinem > -0.7:  # 如果比特币升值，总体也升值，就放置
            wallet.lilv = (wallet.dollor + wallet.bitcoin) / wallet.base
            if bitcoinlinen > 0:  # 最近几天也上升
                #print(wallet.lilv)
                return 2
            else:  # 最近几天下降
                if (wallet.bitcoin) / wallet.base < wallet.lilv * 0.982:  # 0.882
                    #print(wallet.lilv)
                    return 1
                else:
                    #print(wallet.lilv)
                    return 2
        elif wallet.bitcoin < wallet.base * wallet.lilv and bitcoinlinem > -0.7:  # 如果比特币贬值，但整体升值，和手续费比较，能抵消就不卖
            if (wallet.bitcoin) / wallet.base < wallet.lilv * 0.882:  # 0.882
                if bitcoinlinen < 0:
                    #print(wallet.lilv)
                    return 1
                else:
                    #print(wallet.lilv)
                    return 2
            else:
                #print(wallet.lilv)
                return 2
        elif wallet.bitcoin >= wallet.base * wallet.lilv and bitcoinlinem < 0:  # 如果比特币升值，但总体下降，立马卖
            wallet.lilv = (wallet.dollor + wallet.bitcoin) / wallet.base
            #print(wallet.lilv)
            return 1
        else:  # 如果比特币贬值，整体也下降，就卖
            if (wallet.bitcoin) / wallet.base < wallet.lilv*0.892:  # 0.882
                #print(wallet.lilv)
                return 2
            else:
                #print(wallet.lilv)
                return 1
    else:
        if bitcoinlinem > 8.2:

            wallet.lilv = commissionbit * commissionbit * 1.11
            #print(wallet.lilv)
            return 0

        else:
            return 2
    #策略
    ##########################################################################################################################



a = []
b = []
c = []
d = []

round = 25 #基于多少数据

goldmiss = 0         #对黄金没有出售的天数的补偿
y = 600     #没用
hhh = 0  #计算最大值的
kkk = 0  #计算最大值的序号

goldlist = []   #过去一段时间黄金利率列表
bitcoinlist = []#过去一段时间比特币利率列表
buy = []
sell = []
price = Price()
wallet = Wallet()
if __name__ == "__main__":

    print(len(price.goldstate))

    aaa = []
    bbb = []
    ccc = []

    e = []
    f = []
    g = []
    for n in range(start,end,1):
    # 走完五年的时间，通过循环模拟
        wallet.bitcoin = 0
        wallet.dollor = 1000
        goldmiss = 0
        round = n
        wallet.record.clear()
        wallet.recordnum = 0
        wallet.dollorin.clear()
        wallet.dollorout.clear()
        wallet.base = 980
        wallet.lilv = commissionbit*commissionbit
        for i in range(0,1826):

            #print("############" + str(i))
            if price.goldstate[i] == False:
                #print("############" + str(i))
                goldmiss += 1
                if len(goldlist) == 0 or len(bitcoinlist) == 0:
                    bitcoinlist.append(1)
                    wallet.record.append(wallet.dollor + wallet.bitcoin)
                    continue
                elif len(bitcoinlist) < round:
                    bitcoinlist.append(price.bitcoinnow[i] / price.bitcoinnow[i - 1])
                    wallet.record.append(wallet.dollor + wallet.bitcoin)
                    continue
                else:
                    bitcoinlist.append(price.bitcoinnow[i] / price.bitcoinnow[i - 1])
                date = price.golddata[i].split('/')
                #print('今天是20' + date[2] + '年' + date[0] + "月" + date[1], end=" ")
                #print('今天不可交易黄金' + '\t比特币的价格是' + str(price.bitcoinnow[i]))

                if judge(wallet, i, commissionbit, goldlist, bitcoinlist) == 0:
                    # print("今天相比昨天涨了" + str(bitcoinlist[-1]))
                    wallet.base = (wallet.dollor + wallet.bitcoin) * 0.98
                    wallet.bitcoin = wallet.dollor * commissionbit
                    wallet.dollor = 0
                    wallet.recordnum += 1
                    wallet.dollorin.append(wallet.bitcoin)
                    buy.append(i)
                if judge(wallet, i, commissionbit, goldlist, bitcoinlist) == 1:
                    # print("今天相比昨天降了" + str(bitcoinlist[-1]))
                    wallet.base = (wallet.dollor + wallet.bitcoin) * 0.98
                    wallet.dollor = wallet.bitcoin * commissionbit

                    wallet.bitcoin = 0
                    wallet.recordnum += 1
                    wallet.dollorout.append(wallet.bitcoin)
                    sell.append(i)


            else:
                #print("############" + str(i))
                if len(goldlist) == 0 or len(bitcoinlist) == 0:
                    bitcoinlist.append(price.goldnow[i] / price.goldnow[i - 1])
                    goldlist.append(1)
                    wallet.record.append(wallet.dollor + wallet.bitcoin)
                    continue
                elif len(bitcoinlist) < round:
                    goldlist.append(price.goldnow[i - goldmiss] / price.goldnow[i - goldmiss - 1])
                    bitcoinlist.append(price.bitcoinnow[i] / price.bitcoinnow[i - 1])
                    wallet.record.append(wallet.dollor + wallet.bitcoin)
                    continue
                else:
                    goldlist.append(price.goldnow[i - goldmiss] / price.goldnow[i - goldmiss - 1])
                    bitcoinlist.append(price.bitcoinnow[i] / price.bitcoinnow[i - 1])
                date = price.golddata[i].split('/')
                #print('今天是20' + date[2] + '年' + date[0] + "月" + date[1], end=" ")
                #print('今天不可交易黄金' + '\t比特币的价格是' + str(price.bitcoinnow[i]))
                #print('今天可以交易黄金\t黄金的价格是' + str(price.goldnow[i]) + '\t比特币的价格是' + str(price.bitcoinnow[i]))

                if judge(wallet, i, commissionbit, goldlist, bitcoinlist) == 0:
                    # print("今天相比昨天涨了" + str(bitcoinlist[-1]))
                    wallet.base = (wallet.dollor + wallet.bitcoin) * 0.98
                    wallet.bitcoin = wallet.dollor * commissionbit
                    wallet.dollor = 0
                    wallet.recordnum += 1
                    wallet.dollorin.append(wallet.bitcoin)
                    buy.append(i)
                if judge(wallet, i, commissionbit, goldlist, bitcoinlist) == 1:
                    # print("今天相比昨天降了" + str(bitcoinlist[-1]))
                    wallet.base = (wallet.dollor + wallet.bitcoin)*0.98
                    wallet.dollor = wallet.bitcoin * commissionbit

                    wallet.bitcoin = 0
                    wallet.recordnum += 1
                    wallet.dollorout.append(wallet.bitcoin)
                    sell.append(i)

            wallet.record.append(wallet.dollor+wallet.bitcoin)
            wallet.bitcoin *= (bitcoinlist[-1])
            #wallet.gold    *= (goldlist[-1])
            y *= bitcoinlist[-1]
            del bitcoinlist[0]
            if price.goldstate[i]:
                del goldlist[0]
        print(n ,end=" ")
        print(wallet.recordnum,end="  ")
        aaa.append(round)
        bbb.append(wallet.recordnum)
        ccc.append(wallet.dollor+wallet.bitcoin)
        e.append(n)
        f.append(wallet.recordnum)
        g.append(wallet.dollor+wallet.bitcoin)
        #wallet.record.sort(key=None,reverse=False)
        print(wallet.record[-1])
        if wallet.record[-1] > hhh:
            hhh = wallet.record[-1]
            kkk = n
        #plt.plot(range(len(wallet.record)), wallet.record)
        #plt.show()

    plt.rcParams['font.sans-serif'] = ['SimHei']
    plt.rcParams['axes.unicode_minus'] = False
    iii = []
    for i in range(len(wallet.record)):
        iii.append(wallet.record[i])
        price.bitcoinnow[i] *= 10
    #plt.plot(range(0,len(wallet.record)),iii)

    #plt.plot(e, f,g)
    #print(wallet.record)

    r = 0
    t = []
    for i in wallet.record:
        t.append(i*10-r*10)
        r = i
    buyy = []



    for i in range(len(buy)):
        buyy.append(price.bitcoinnow[buy[i]])
    selly = []
    for i in range(len(sell)):
        selly.append(price.bitcoinnow[sell[i]])

    # plt.plot(range(len(price.bitcoinnow)),price.bitcoinnow)
    # plt.plot(buy,buyy,'bo',ms=3,color='red')
    # plt.plot(sell,selly,'bo',ms=3,color='blue')
    #plt.show()
    # print(wallet.recordnum)
    # print(wallet.dollorin)
    # print(wallet.dollorout)
    #
    # print(len(price.goldnow))
    # print(len(goldlist))
    # print(hhh)
    # print(kkk)
    # for i in range(1809):
    #     del da[i],xiao[i]
    # v = 0
    # for j in range(len(da)):
    #     if (da[i] > 0 and xiao[i] < 0) or(da[i] < 0 and xiao[i] > 0):
    #         print(da[i]*xiao[i])
    # print(v)
    # print(da)
    # print(xiao)
    # plt.plot(range(len(da)),da)

    # ax1 = plt.subplot(221)
    # ax1.plot(range(0, len(a)), a,c)
    # ax2 = plt.subplot(222)
    # ax2.plot(range(0, len(b)), b,d)
    # ax3 = plt.subplot(223)
    # ax3.plot(range(0, len(c)), a,b)
    # ax4 = plt.subplot(224)
    # ax4.plot(range(0, len(d)), c,d)


    newrecord = []
    newrecordnum = 0
    nrecordnum = []
    sumrecord = 0
    # for i in range(18):
    #     print(regression(wallet.record[i*100:(i+1)*100]))
    #     newrecord.append(regression(wallet.record[i*100:(i+1)*100]))
    #     if regression(wallet.record[i*100:(i+1)*100]) < 0:
    #         newrecordnum += 1
    #         nrecordnum.append(regression(wallet.record[i*100:(i+1)*100]))
    #     else:
    #         sumrecord+=regression(wallet.record[i*100:(i+1)*100])



    #plt.plot(range(18),newrecord)
    # print(newrecordnum)
    # print(nrecordnum)
    # print(sumrecord/18)
    #plt.show()

    f1,a1 = plt.subplots()
    a1.plot(aaa,bbb)
    a1.set_title("使用数据天数与交易次数的关系")
    a1.set_xlabel("使用数据天数")
    a1.set_ylabel("交易次数")
    plt.grid()

    plt.show()
    f1, a1 = plt.subplots()
    a1.plot(aaa, ccc)
    a1.set_title("使用数据天数与最终利润的关系")
    a1.set_xlabel("使用数据天数")
    a1.set_ylabel("最终利润")
    plt.grid()

    plt.show()
    # f = open('data.csv','a+')
    # for i in range(1826):
    #     data = price.bitcoindata[i].split('/')
    #     f.write(data[2]+'.'+data[0]+'.'+data[1]+','+str(wallet.record[i])+','+str(price.bitcoinnow[i]*0.1)+','+str(price.goldnow[i])+'\n')