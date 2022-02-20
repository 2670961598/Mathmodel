if wallet.dollor == 0:
    if wallet.bitcoin >= wallet.base * wallet.lilv and bitcoinlinem > 0:  # 如果比特币升值，总体也升值，就放置
        wallet.lilv = (wallet.dollor + wallet.bitcoin) / wallet.base
        if bitcoinlinen > 0:  # 最近几天也上升
            return 2
        else:  # 最近几天下降
            if (wallet.bitcoin) / wallet.base < wallet.lilv * 0.882:  # 0.882
                return 1
            else:
                return 2
    elif wallet.bitcoin < wallet.base * wallet.lilv and bitcoinlinem > 0:  # 如果比特币贬值，但整体升值，和手续费比较，能抵消就不卖
        if (wallet.bitcoin) / wallet.base < wallet.lilv * 0.882:  # 0.882
            if bitcoinlinen > 0:


        else:
            return 2
    elif wallet.bitcoin >= wallet.base * wallet.lilv and bitcoinlinem < 0:  # 如果比特币升值，但总体下降，立马卖
        return 1
    else:  # 如果比特币贬值，整体也下降，就卖
        return 1
else:
    if bitcoinlinem > 8.2:
        wallet.lilv = commissionbit * commissionbit
        return 0
    else:
        return 2