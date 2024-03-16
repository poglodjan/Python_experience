import numpy as np
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import numpy as np

# types of charts:
def do_chart(s, base, term, min_c, max_c, decimal_c, array_forward):
    plt.figure(figsize=(6, 4))
    plt.plot(array_forward[:, 1], array_forward[:, 1], color='black', linestyle='dotted', label="No Hedge")
    plt.plot(array_forward[:, 1], array_forward[:, 0], linewidth=3, color='#73c2fc', label=s)
    plt.fill_between(array_forward[:, 1], array_forward[:, 2], array_forward[:, 2] + array_forward[:, 4], color='#0f1632', alpha=0.3, label='Profit')
    plt.fill_between(array_forward[:, 1], array_forward[:, 2], array_forward[:, 2] + array_forward[:, 3], color='#245be2', alpha=0.3, label='Loss')
    plt.yticks(fontsize=9)
    plt.xticks(fontsize=9)
    plt.legend(fontsize=7, loc="upper left")
    plt.grid(True, linestyle='-', which='both', alpha=0.3)
    plt.ylim(min_c, max_c)
    plt.xlim(min_c, max_c)
    plt.xlabel('Spot at Expiry')
    plt.ylabel(base + " / " + term + " Rate")
    plt.gca().xaxis.set_major_formatter(ticker.StrMethodFormatter(f'{{x:.{decimal_c}f}}'))
    plt.gca().yaxis.set_major_formatter(ticker.StrMethodFormatter(f'{{x:.{decimal_c}f}}'))
    plt.gca().yaxis.set_major_locator(plt.MultipleLocator((max_c - min_c) / 5))
    plt.gca().xaxis.set_major_locator(plt.MultipleLocator((max_c - min_c) / 5))
    plt.gca().tick_params(axis='y', labelrotation=0)
    plt.gca().tick_params(axis='both', which='both', labelbottom=True)
    plt.xlim(min_c, max_c)
    return plt

def do_option_chart(s, base, term, min_c, max_c, decimal_c, array_option):
    plt.figure(figsize=(6, 4))
    plt.plot(array_option[:, 0], array_option[:, 0], color='black', linestyle='dotted', label="No Hedge")
    plt.plot(array_option[:, 0], array_option[:, 1], linewidth=3, color='#73c2fc', label=s + " without premium cost")
    plt.plot(array_option[:, 0], array_option[:, 3], linewidth=3, color='navy', label=s+" with premium cost")
    plt.fill_between(array_option[:, 0], array_option[:, 3], array_option[:, 3] - array_option[:, 4], color='#0f1632', alpha=0.3, label='Profit')
    plt.fill_between(array_option[:, 0], array_option[:, 3], array_option[:, 3] - array_option[:, 5], color='#245be2', alpha=0.3, label='Loss')
    plt.yticks(fontsize=9)
    plt.xticks(fontsize=9)
    plt.legend(fontsize=7, loc="upper left")
    plt.grid(True, linestyle='-', which='both', alpha=0.3)
    plt.ylim(min_c, max_c)
    plt.xlim(min_c, max_c)
    plt.xlabel('Spot at Expiry')
    plt.ylabel(base + " / " + term + " Rate")
    plt.gca().xaxis.set_major_formatter(ticker.StrMethodFormatter(f'{{x:.{decimal_c}f}}'))
    plt.gca().yaxis.set_major_formatter(ticker.StrMethodFormatter(f'{{x:.{decimal_c}f}}'))
    plt.gca().yaxis.set_major_locator(plt.MultipleLocator((max_c - min_c) / 5))
    plt.gca().xaxis.set_major_locator(plt.MultipleLocator((max_c - min_c) / 5))
    plt.gca().tick_params(axis='y', labelrotation=0)
    plt.gca().tick_params(axis='both', which='both', labelbottom=True)
    plt.xlim(min_c, max_c)
    return plt

# 1) Forward
def forward_fun(strike, zp, is_importer, min_c, max_c, decimal_s):
    X = np.zeros((501, 5)) 
    index = min_c

    for i in range(501):
        # no hedge
        X[i, 1] = round(index, 4)

        if index < strike:
            # structure
            if is_importer: X[i, 0] = round(strike, decimal_s)
            else: X[i, 0] = round(index - (index - strike) * (zp / 100), 4)
        else:
            if is_importer: X[i, 0] = round(index - (index - strike) * (zp / 100), 4)
            else: X[i, 0] = round(strike, decimal_s)

        # pros / cons
        X[i, 2] = X[i, 0]
        if is_importer:
            X[i, 3] = min(index - X[i, 0], 0)
            X[i, 4] = max(index - X[i, 0], 0)
        else:
            X[i, 3] = max(index - X[i, 0], 0)
            X[i, 4] = min(index - X[i, 0], 0)

        index += (max_c - min_c) / 500
    return X

# 2) Collar
def kor_fun(put_strike, call_strike, zp, is_importer, min_c, max_c):
    X = np.zeros((501, 5))
    i = 0
    index = min_c

    for i in range(501):
        # no hedge
        X[i, 1] = index

        if is_importer:
            if index <= put_strike:
                # linia put
                X[i, 0] = put_strike
            elif index >= call_strike:
                # linia call
                X[i, 0] = call_strike + (index - call_strike) * (1 - zp / 100)
            elif put_strike <= index < call_strike:
                # linia korytarz
                X[i, 0] = index
        else:
            if index <= put_strike:
                # linia put
                X[i, 0] = put_strike + (index - put_strike) * (1 - zp / 100)
            elif index >= call_strike:
                # linia call
                X[i, 0] = call_strike
            elif put_strike <= index < call_strike:
                # linia korytarz
                X[i, 0] = index

        # pros / cons
        X[i, 2] = X[i, 0]
        if is_importer:
            X[i, 3] = min(index - X[i, 0], 0)
            X[i, 4] = max(index - X[i, 0], 0)
        else:
            X[i, 3] = max(index - X[i, 0], 0)
            X[i, 4] = min(index - X[i, 0], 0)

        index += (max_c - min_c) / 500
    return X

# 3) Forward with subsidy
def forw_zwyl_iwyp_fun(strike, bariera, wyp, zp, is_importer, min_c, max_c):
    X = np.zeros((501, 5))
    index = min_c

    for i in range(501):
        # no hedge
        X[i, 1] = index

        if is_importer:
            if index < strike:
                # linia put
                X[i, 0] = strike
            elif strike < index < bariera:
                # linia call
                X[i, 0] = strike + (index - strike) * (1 - zp / 100)
            elif index > bariera:
                # linia korytarz
                X[i, 0] = index - wyp / 100
        else:
            if index > strike:
                # linia put
                X[i, 0] = strike
            elif bariera < index < strike:
                # linia call
                X[i, 0] = strike - (strike - index) * (1 - zp / 100)
            elif index < bariera:
                # linia korytarz
                X[i, 0] = index + wyp / 100

        # pros / cons
        X[i, 2] = X[i, 0]
        if is_importer:
            X[i, 3] = min(index - X[i, 0], 0)
            X[i, 4] = max(index - X[i, 0], 0)
        else:
            X[i, 3] = max(index - X[i, 0], 0)
            X[i, 4] = min(index - X[i, 0], 0)

        index += (max_c - min_c) / 500
    return X

# 4) Collar with subsidy
def kor_zwyl_iwyp_fun(put_strike, call_strike, bariera, wyp, zp, is_importer, min_c, max_c):
    X = np.zeros((501, 5))
    i = 0
    index = min_c

    for i in range(501):
        # no hedge
        X[i, 1] = index

        if is_importer:
            if index < put_strike:
                X[i, 0] = put_strike
            elif put_strike < index < call_strike:
                # collar line
                X[i, 0] = index
            elif call_strike < index < bariera:
                X[i, 0] = call_strike - (call_strike - index) * (1 - zp / 100)
            elif call_strike < index > bariera:
                X[i, 0] = index - wyp / 100
        else:
            if index > call_strike:
                X[i, 0] = call_strike
            elif put_strike < index < call_strike:
                # collar line
                X[i, 0] = index
            elif put_strike > index > bariera:
                X[i, 0] = put_strike + (index - put_strike) * (1 - zp / 100)
            elif put_strike > index < bariera:
                X[i, 0] = index + wyp / 100

        # pros / cons
        X[i, 2] = X[i, 0]
        if is_importer:
            X[i, 3] = min(index - X[i, 0], 0)
            X[i, 4] = max(index - X[i, 0], 0)
        else:
            X[i, 3] = max(index - X[i, 0], 0)
            X[i, 4] = min(index - X[i, 0], 0)

        index += (max_c - min_c) / 500
    return X

# 5) Capped Forward
def kor_mewa_fun(put_strike, call_strike, bariera, zp, is_importer, min_c, max_c):
    X = np.zeros((501, 5))
    i = 0
    index = min_c

    for i in range(501):
        X[i, 1] = index

        if is_importer:
            if index < put_strike:
                X[i, 0] = put_strike
            elif put_strike <= index < bariera:
                X[i, 0] = index
            elif bariera < index <= call_strike:
                X[i, 0] = bariera + (index - bariera) * (1 - zp / 100)
            elif index > call_strike and index >= bariera:
                X[i, 0] = index - (call_strike - bariera) * (zp / 100)
        else:
            if index > call_strike:
                X[i, 0] = call_strike
            elif call_strike >= index >= bariera:
                X[i, 0] = index
            elif bariera >= index >= put_strike:
                X[i, 0] = bariera - (bariera - index) * (1 - zp / 100)
            elif put_strike >= index <= bariera:
                X[i, 0] = index + (bariera - put_strike) * (zp / 100)

        # pros / cons
        X[i, 2] = X[i, 0]
        if is_importer:
            X[i, 3] = min(index - X[i, 0], 0)
            X[i, 4] = max(index - X[i, 0], 0)
        else:
            X[i, 3] = max(index - X[i, 0], 0)
            X[i, 4] = min(index - X[i, 0], 0)

        index += (max_c - min_c) / 500
    return X

# 6) Loss Capped Forward
def Kor_mewa_fun2(put_strike, call_strike, bariera, zp, is_importer, min_c, max_c):
    X = np.zeros((501, 5))

    index = min_c
    for i in range(501):
        X[i, 1] = index

        if not is_importer:
            if index < put_strike:
                X[i, 0] = put_strike - (put_strike - index) * (1 - zp / 100)
            elif put_strike <= index < bariera:
                X[i, 0] = index
            elif bariera < index <= call_strike:
                X[i, 0] = bariera
            elif call_strike < index:
                X[i, 0] = index - (call_strike - bariera)

        if is_importer:
            if index >= call_strike:
                X[i, 0] = call_strike + (index - call_strike) * (1 - zp / 100)
            elif call_strike >= index >= bariera:
                X[i, 0] = index
            elif bariera >= index >= put_strike:
                X[i, 0] = bariera
            elif put_strike >= index:
                X[i, 0] = index + (bariera - put_strike)

        # pros / cons
        X[i, 2] = X[i, 0]
        if is_importer:
            X[i, 3] = min(index - X[i, 0], 0)
            X[i, 4] = max(index - X[i, 0], 0)
        else:
            X[i, 3] = max(index - X[i, 0], 0)
            X[i, 4] = min(index - X[i, 0], 0)

        index = index + (max_c - min_c) / 500
    return X

# 6) Capped Forward
def forw_elas_fun(strike, bariera, zp, is_importer, min_c, max_c):
    X = np.zeros((501, 5))
    index = min_c

    for i in range(501):
        # no hedge
        X[i, 1] = index

        if is_importer:
            if index >= strike:
                X[i, 0] = strike + (index - strike) * (1 - zp / 100)
            if index <= strike and bariera >= index:
                X[i, 0] = strike
            if index <= strike and bariera <= index:
                X[i, 0] = index
        else:
            if index <= strike:
                X[i, 0] = strike + (index - strike) * (1 - zp / 100)
            if index >= strike and bariera >= index:
                X[i, 0] = index
            if index >= strike and bariera <= index:
                X[i, 0] = strike

        # pros / cons
        X[i, 2] = X[i, 0]
        if is_importer:
            X[i, 3] = min(index - X[i, 0], 0)
            X[i, 4] = max(index - X[i, 0], 0)
        else:
            X[i, 3] = max(index - X[i, 0], 0)
            X[i, 4] = min(index - X[i, 0], 0)

        index += (max_c - min_c) / 500

    return X

# 7) Conv Forward
def kor_elas_fun(put_strike, call_strike, bariera, zp, is_importer, min_c, max_c):
    X = np.zeros((501, 5))
    index = min_c

    for i in range(501):
        X[i, 1] = index

        if is_importer:
            if index >= call_strike:
                X[i, 0] = call_strike - (call_strike - index) * (1 - zp / 100)
            if index <= call_strike and index >= bariera:
                X[i, 0] = index
            if index <= bariera:
                X[i, 0] = put_strike
            X[i, 2] = X[i, 0]
        else:
            if index <= put_strike:
                X[i, 0] = put_strike + (index - put_strike) * (1 - zp / 100)
            if index >= bariera:
                X[i, 0] = call_strike
            if index <= bariera and index >= put_strike:
                X[i, 0] = index
            if index >= bariera and index >= call_strike:
                X[i, 0] = call_strike
            # pros / cons
            X[i, 2] = X[i, 0]

        if is_importer:
            X[i, 3] = min(index - X[i, 0], 0)
            X[i, 4] = max(index - X[i, 0], 0)
        else:
            X[i, 3] = max(index - X[i, 0], 0)
            X[i, 4] = min(index - X[i, 0], 0)

        index += (max_c - min_c) / 500

    return X

# 8) step Forward
def forw_zrek_fun(strike, wyp, zp, putt, is_importer, min_c, max_c):
    X = np.zeros((501, 5))
    index = min_c

    for i in range(501):
        # putt = trigger
        X[i, 1] = index

        if is_importer:
            if index <= putt and index <= strike and putt <= strike:
                X[i, 0] = strike - wyp / 100
            if index >= putt and index <= strike and putt <= strike:
                X[i, 0] = strike
            if index <= putt and index >= strike and putt <= strike:
                X[i, 0] = strike - wyp / 100
            if index >= putt and index >= strike and putt <= strike:
                X[i, 0] = strike + (index - strike) * (1 - zp / 100)
            if index >= putt and index >= strike and putt > strike:
                X[i, 0] = strike + (index - strike) * (1 - zp / 100)
            if index <= putt and index >= strike and putt > strike:
                X[i, 0] = (strike - wyp / 100) + (index - (strike - wyp / 100)) * (1 - zp / 100)
            if index <= putt and index <= strike and putt > strike:
                X[i, 0] = strike - wyp / 100
            if index <= (strike - wyp / 100) and putt > strike:
                X[i, 0] = strike - wyp / 100
        else:
            if index <= putt and index <= strike and putt >= strike:
                X[i, 0] = strike - (strike - index) * (1 - zp / 100)
            if putt >= index and index >= strike and putt >= strike:
                X[i, 0] = strike
            if putt <= index and index >= strike and putt >= strike:
                X[i, 0] = strike
            if index >= putt and putt >= strike:
                X[i, 0] = strike - wyp / 100
            if putt <= index and index <= (strike - wyp / 100) and putt < strike:
                X[i, 0] = (strike - wyp / 100) - ((strike - wyp / 100) - index) * (1 - zp / 100)
            if putt >= index and index <= (strike - wyp / 100) and putt < strike:
                X[i, 0] = strike - (strike - index) * (1 - zp / 100)
            if index >= (strike - wyp / 100) and putt < strike:
                X[i, 0] = (strike - wyp / 100)

        # pros / cons
        X[i, 2] = X[i, 0]
        if is_importer:
            X[i, 3] = min(index - X[i, 0], 0)
            X[i, 4] = max(index - X[i, 0], 0)
        else:
            X[i, 3] = max(index - X[i, 0], 0)
            X[i, 4] = min(index - X[i, 0], 0)

        index += (max_c - min_c) / 500

    return X

# 9) step Collar
def kor_zrek_fun(put_strike, call_strike, bariera, wyp, zp, is_importer, min_c, max_c):
    X = np.zeros((501, 5))
    index = min_c

    for i in range(501):
        # no hedge
        X[i, 1] = index

        if is_importer:
            if index <= bariera:
                # linia put
                X[i, 0] = wyp
            if index >= call_strike:
                # linia call
                X[i, 0] = call_strike + (index - call_strike) * (1 - zp / 100)
            # linia korytarz
            if index <= put_strike and bariera <= index:
                X[i, 0] = put_strike
            if index >= put_strike and index <= call_strike:
                X[i, 0] = index
        else:
            if index >= bariera:
                X[i, 0] = wyp
            if index >= call_strike and bariera >= index:
                X[i, 0] = call_strike
            if index >= put_strike and call_strike >= index:
                X[i, 0] = index
            if index <= put_strike:
                X[i, 0] = put_strike - (put_strike - index) * (1 - zp / 100)

        # pros / cons
        X[i, 2] = X[i, 0]
        if is_importer:
            X[i, 3] = min(index - X[i, 0], 0)
            X[i, 4] = max(index - X[i, 0], 0)
        else:
            X[i, 3] = max(index - X[i, 0], 0)
            X[i, 4] = min(index - X[i, 0], 0)

        index += (max_c - min_c) / 500
    return X

# 10) option
def Eur_fun(strike, zp, koszt, spot, is_importer, min_c, max_c):
    X = np.zeros((501, 6))

    index = min_c
    for i in range(501):
        # no hedge
        X[i, 0] = index
        
        if is_importer:
            if index >= strike:
                # linia opcja
                X[i, 1] = strike + (index - strike) * (1 - (zp / 100))
            else:
                X[i, 1] = index
            
            X[i, 2] = max(X[i, 1], index)
            X[i, 3] = X[i, 1] + (koszt / 100 * spot)
        else:
            if index <= strike:
                # linia opcja
                X[i, 1] = strike - (strike - index) * (1 - (zp / 100))
            else:
                X[i, 1] = index
            
            X[i, 2] = min(X[i, 1], index)
            X[i, 3] = X[i, 1] - (koszt / 100 * spot)
        
        # pros / cons
        if is_importer:
            X[i, 4] = max(X[i, 3] - index, 0)
            X[i, 5] = min(X[i, 3] - index, 0)
        else:
            X[i, 4] = min(X[i, 3] - index, 0)
            X[i, 5] = max(X[i, 3] - index, 0)
        
        index = index + (max_c - min_c) / 500
    
    return X

# 11) spread
def Spread_fun(put_strike, call_strike, koszt, spot, is_importer, min_c, max_c):
    X = np.zeros((501, 6))

    index = min_c
    for i in range(501):
        # no hedge
        X[i, 0] = index
        
        if is_importer:
            if index <= put_strike:
                # linia opcja
                X[i, 1] = index
            if call_strike >= index >= put_strike:
                X[i, 1] = put_strike
            if index >= call_strike:
                X[i, 1] = index - (call_strike - put_strike)
            
            X[i, 2] = max(X[i, 1], index)
            X[i, 3] = X[i, 1] + (koszt / 100 * spot)
        else:
            if index >= call_strike:
                # linia opcja
                X[i, 1] = index
            if call_strike >= index >= put_strike:
                X[i, 1] = call_strike
            if index <= put_strike:
                X[i, 1] = index + (call_strike - put_strike)
            
            X[i, 2] = min(X[i, 1], index)
            X[i, 3] = X[i, 1] - (koszt / 100 * spot)
        
        # pros / cons
        if is_importer:
            X[i, 4] = max(X[i, 3] - index, 0)
            X[i, 5] = min(X[i, 3] - index, 0)
        else:
            X[i, 4] = min(X[i, 3] - index, 0)
            X[i, 5] = max(X[i, 3] - index, 0)
        
        index = index + (max_c - min_c) / 500
    
    return X

# (12) option with rebate
def Eur_r_fun(strike, rebate, proc, zp, koszt, spot, is_importer, min_c, max_c):
    X = np.zeros((501, 6))

    index = min_c
    for i in range(501):
        # no hedge
        X[i, 0] = index
        
        if is_importer:
            if index >= strike:
                # linia opcja
                X[i, 1] = strike + (index - strike) * (1 - (zp / 100))
            else:
                X[i, 1] = index
            
            X[i, 2] = max(X[i, 1], index)
            
            if index >= rebate:
                X[i, 3] = X[i, 1] + (koszt / 100 * spot)
            elif index <= rebate:
                X[i, 3] = X[i, 1] + ((koszt / 100) * ((100 - proc) / 100) * spot)
        else:
            if index <= strike:
                # linia opcja
                X[i, 1] = strike - (strike - index) * (1 - (zp / 100))
            else:
                X[i, 1] = index
            
            X[i, 2] = min(X[i, 1], index)
            
            if index <= rebate:
                X[i, 3] = X[i, 1] - (koszt / 100 * spot)
            elif index >= rebate:
                X[i, 3] = X[i, 1] - ((koszt / 100) * ((100 - proc) / 100) * spot)
        
        # pros / cons
        if is_importer:
            X[i, 4] = max(X[i, 3] - index, 0)
            X[i, 5] = min(X[i, 3] - index, 0)
        else:
            X[i, 4] = min(X[i, 3] - index, 0)
            X[i, 5] = max(X[i, 3] - index, 0)
        
        index = index + (max_c - min_c) / 500
    
    return X

# 13) participator
def Partyp_fun(strike, zp, is_importer, min_c, max_c):
    X = np.zeros((501, 5))

    index = min_c
    for i in range(501):
        # no hedge
        X[i, 1] = index
        
        if is_importer:
            if index >= strike:
                # forward structure
                X[i, 0] = strike
            else:
                X[i, 0] = (zp / 100) * strike + (1 - zp / 100) * index
        else:
            if index >= strike:
                # forward structure
                X[i, 0] = (zp / 100) * strike + (1 - zp / 100) * index
            else:
                X[i, 0] = strike
        
        # pros / cons
        X[i, 2] = X[i, 0]
        if is_importer:
            X[i, 3] = min(index - X[i, 0], 0)
            X[i, 4] = max(index - X[i, 0], 0)
        else:
            X[i, 3] = max(index - X[i, 0], 0)
            X[i, 4] = min(index - X[i, 0], 0)

        index = index + (max_c - min_c) / 500
    
    return X



