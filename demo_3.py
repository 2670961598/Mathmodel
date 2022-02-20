import pandas

bit = pandas.read_csv('BCHAIN-MKPRUM.csv')['Value'].tolist()

money = [0, 1000]

for n in range(len(bit) - 1):
    a = bit[n + 1] / bit[n]
    if a > 1/0.98 and money[1] != 0:
        money[0] += money[1] * 0.98
        money[1] = 0
        bit_buy = bit[n]
    elif a < 1 and money[0] != 0:
        money[1] += money[0] * 0.98 * bit[n] / bit_buy
        money[0] = 0
    print(money)
    print(money[0] + money[1], '\n')



