import numpy as np

def kurs(s_min, s_max):
    X = np.zeros(8)
    X[0] = s_min
    X[7] = s_max
    for i in range(1, 7): X[i] = X[i - 1] + (X[7] - X[0]) / 7
    return X

def forward_scenario(strike, zp, nominal, is_importer, decimal_s, s_min, s_max):
    X = np.zeros((8, 5))

    X[0, 0] = s_min
    X[0, 1] = strike
    X[0, 2] = nominal * round(X[0, 0], decimal_s)
    X[0, 3] = nominal * round(X[0, 1], decimal_s)
    X[0, 4] = X[0, 2] - X[0, 3]

    if not is_importer:
        X[0, 1] = X[0, 0] + (strike - X[0, 0]) * (zp / 100)
        X[0, 3] = nominal * round(X[0, 1], decimal_s)
        X[0, 4] = X[0, 3] - X[0, 2]

    X[7, 0] = s_max
    X[0, 2] = X[0, 4]

    for i in range(1, 8):
        X[i, 0] = kurs(s_min, s_max)[i]

        if X[i, 0] <= strike:
            # forward structure
            if is_importer:
                X[i, 1] = strike
            else:
                X[i, 1] = X[i, 0] - (X[i, 0] - strike) * (zp / 100)
        else:
            if is_importer:
                X[i, 1] = X[i, 0] + (strike - X[i, 0]) * (zp / 100)
            else:
                X[i, 1] = strike

        X[i, 2] = nominal * round(X[i, 0], decimal_s)
        X[i, 3] = nominal * round(X[i, 1], decimal_s)
        X[i, 4] = X[i, 2] - X[i, 3]

        if not is_importer:
            X[i, 4] = -1 * X[i, 4]

        if 0.01 > X[i, 4] > -0.01:
            X[i, 4] = 0

        X[i, 2] = X[i, 4]

    return X

def kor_zrek_scenario_lever(put_strike, call_strike, zp, lever, bariera, wyp, nominal, is_importer, decimal_s, s_min, s_max):
    X = np.zeros((8, 5))

    X[0, 0] = s_min
    X[0, 1] = wyp
    X[0, 2] = wyp
    X[0, 4] = nominal * round(X[0, 0], decimal_s) - nominal * round(X[0, 2], decimal_s)

    if not is_importer:
        X[0, 1] = put_strike - (put_strike - X[0, 0]) * (1 - zp / 100)
        X[0, 2] = put_strike
        X[0, 4] = nominal * round(X[0, 2], decimal_s) - nominal * round(X[0, 0], decimal_s)

    X[7, 0] = s_max
    X[0, 3] = X[0, 4]
    X[0, 4] = X[0, 1]

    if X[0, 3] > 0:
        X[0, 1] = nominal * lever
        X[0, 3] = X[0, 3] * lever
    else:
        X[0, 1] = nominal

    for i in range(1, 8):
        X[i, 0] = kurs(s_min, s_max)[i]

        if is_importer:
            if X[i, 0] >= call_strike:
                # linia korytarz elastyczny
                X[i, 1] = call_strike + (X[i, 0] - call_strike) * (1 - zp / 100)

            if bariera >= X[i, 0]:
                X[i, 1] = wyp

            if put_strike <= X[i, 0] <= call_strike:
                X[i, 1] = X[i, 0]

            if bariera < X[i, 0] <= put_strike:
                X[i, 1] = put_strike

        if not is_importer:
            if X[i, 0] >= bariera:
                # linia korytarz elastyczny
                X[i, 1] = wyp

            if put_strike <= X[i, 0] <= bariera:
                X[i, 1] = X[i, 0]

            if X[i, 0] <= put_strike:
                X[i, 1] = put_strike - (put_strike - X[i, 0]) * (1 - zp / 100)

            if bariera > X[i, 0] >= call_strike:
                X[i, 1] = call_strike

        # without lever
        if is_importer:
            if X[i, 0] >= call_strike:
                # linia korytarz elastyczny
                X[i, 2] = call_strike

            if bariera >= X[i, 0]:
                X[i, 2] = wyp

            if put_strike <= X[i, 0] <= call_strike:
                X[i, 2] = X[i, 0]

            if bariera < X[i, 0] <= put_strike:
                X[i, 2] = put_strike

        if not is_importer:
            if X[i, 0] >= bariera:
                # linia korytarz elastyczny
                X[i, 2] = wyp

            if put_strike <= X[i, 0] <= bariera:
                X[i, 2] = X[i, 0]

            if X[i, 0] <= put_strike:
                X[i, 2] = put_strike

            if bariera > X[i, 0] >= call_strike:
                X[i, 2] = call_strike

        X[i, 4] = nominal * round(X[i, 0], decimal_s) - nominal * round(X[i, 2], decimal_s)

        if not is_importer:
            X[i, 4] = -1 * X[i, 4]

        if 0.01 > X[i, 4] > -0.01:
            X[i, 4] = 0

        X[i, 3] = X[i, 4]
        X[i, 4] = X[i, 1]

        if X[i, 3] >= 0:
            X[i, 1] = nominal * lever
            X[i, 3] = X[i, 3] * lever
        else:
            X[i, 1] = nominal

        if X[i, 0] == bariera and is_importer:
            X[i, 1] = nominal

        if X[i, 0] == bariera and not is_importer:
            X[i, 1] = nominal

    return X

def forw_zrek_scenario_lever(strike, wyp, zp, lever, putt, nominal, is_importer, decimal_s, s_min, s_max):
    X = np.zeros((8, 5))

    X[0, 0] = s_min
    X[0, 1] = (strike - wyp / 100)
    X[0, 2] = (strike - wyp / 100)
    X[0, 4] = nominal * round(X[0, 0], decimal_s) - nominal * round(X[0, 2], decimal_s)

    if not is_importer:
        X[0, 1] = strike - (strike - X[0, 0]) * (1 - zp / 100)
        X[0, 2] = strike
        X[0, 4] = nominal * round(X[0, 2], decimal_s) - nominal * round(X[0, 0], decimal_s)

    X[7, 0] = s_max
    X[0, 3] = X[0, 4]
    X[0, 4] = X[0, 1]

    if X[0, 3] > 0:
        X[0, 1] = nominal * lever
        X[0, 3] = X[0, 3] * lever
    else:
        X[0, 1] = nominal

    for i in range(1, 8):
        X[i, 0] = kurs(s_min, s_max)[i]

        if putt < strike:
            if is_importer:
                if X[i, 0] <= putt:
                    # forward structure
                    X[i, 1] = (strike - wyp / 100)
                if putt <= X[i, 0] <= strike:
                    # forward structure
                    X[i, 1] = strike
                if X[i, 0] > strike:
                    X[i, 1] = strike - (strike - X[i, 0]) * (1 - zp / 100)
            if not is_importer:
                if putt <= X[i, 0]:
                    # forward structure
                    X[i, 1] = (strike - wyp / 100)
                if strike >= X[i, 0] >= putt:
                    # forward structure
                    X[i, 1] = strike
                if X[i, 0] < strike:
                    X[i, 1] = strike + (X[i, 0] - strike) * (1 - zp / 100)

                if is_importer:
                    if X[i, 0] <= putt:
                        # forward structure
                        X[i, 2] = (strike - wyp / 100)
                    if X[i, 0] > putt:
                        X[i, 2] = strike

                if not is_importer:
                    if putt <= X[i, 0]:
                        # forward structure
                        X[i, 2] = (strike - wyp / 100)
                    if X[i, 0] < putt:
                        X[i, 2] = strike

        # Scenario 2
        if putt >= strike:
            if is_importer:
                if X[i, 0] <= putt:
                    # forward structure
                    X[i, 1] = (strike - wyp / 100)
                if strike >= X[i, 0] >= putt:
                    # forward structure
                    X[i, 1] = strike
                if X[i, 0] < strike:
                    X[i, 1] = strike + (X[i, 0] - strike) * (1 - zp / 100)
            if not is_importer:
                if putt <= X[i, 0]:
                    # forward structure
                    X[i, 1] = (strike - wyp / 100)
                if strike >= X[i, 0] >= putt:
                    # forward structure
                    X[i, 1] = strike
                if X[i, 0] < strike:
                    X[i, 1] = strike + (X[i, 0] - strike) * (1 - zp / 100)

                if is_importer:
                    if X[i, 0] <= putt:
                        # forward structure
                        X[i, 2] = (strike - wyp / 100)
                    if X[i, 0] > putt:
                        X[i, 2] = strike

                if not is_importer:
                    if putt <= X[i, 0]:
                        # forward structure
                        X[i, 2] = (strike - wyp / 100)
                    if X[i, 0] < putt:
                        X[i, 2] = strike

        X[i, 4] = nominal * round(X[i, 0], decimal_s) - nominal * round(X[i, 2], decimal_s)

        if not is_importer:
            X[i, 4] = -1 * X[i, 4]

        if 0.01 > X[i, 4] > -0.01:
            X[i, 4] = 0

        X[i, 3] = X[i, 4]
        X[i, 4] = X[i, 1]

        if X[i, 3] >= 0:
            X[i, 1] = nominal * lever
            X[i, 3] = X[i, 3] * lever
        else:
            X[i, 1] = nominal

    return X

def forw_zrek_scenario(strike, wyp, zp, putt, nominal, is_importer, decimal_s, s_min, s_max):
    X = np.zeros((8, 5))

    X[0, 0] = s_min
    X[0, 1] = (strike - wyp / 100)
    X[0, 2] = nominal * round(X[0, 0], decimal_s)
    X[0, 3] = nominal * round(X[0, 1], decimal_s)
    X[0, 4] = X[0, 2] - X[0, 3]

    if not is_importer:
        X[0, 1] = strike
        X[0, 3] = nominal * round(X[0, 1], decimal_s)
        X[0, 4] = X[0, 3] - X[0, 2]

    X[7, 0] = s_max
    X[0, 2] = X[0, 4]

    for i in range(1, 8):
        X[i, 0] = kurs(s_min, s_max)[i]

        if is_importer:
            if X[i, 0] <= putt:
                # forward structure
                X[i, 1] = (strike - wyp / 100)
            if X[i, 0] > putt:
                X[i, 1] = strike - (strike - X[i, 0]) * (1 - zp / 100)

        if not is_importer:
            if putt <= X[i, 0]:
                # forward structure
                X[i, 1] = (strike - wyp / 100)
            if X[i, 0] < putt:
                X[i, 1] = strike + (X[i, 0] - strike) * (1 - zp / 100)

        X[i, 2] = nominal * round(X[i, 0], decimal_s)
        X[i, 3] = nominal * round(X[i, 1], decimal_s)
        X[i, 4] = X[i, 2] - X[i, 3]

        if not is_importer:
            X[i, 4] = -1 * X[i, 4]

        if 0.01 > X[i, 4] > -0.01:
            X[i, 4] = 0

        X[i, 2] = X[i, 4]

    return X

def forw_zwyl_scenario(strike, bariera, zp, nominal, is_importer, decimal_s, s_min, s_max):
    X = np.zeros((8, 5))

    X[0, 0] = s_min
    X[0, 1] = strike
    X[0, 2] = nominal * round(X[0, 0], decimal_s)
    X[0, 3] = nominal * round(X[0, 1], decimal_s)
    X[0, 4] = X[0, 2] - X[0, 3]

    if not is_importer:
        X[0, 1] = X[0, 0]
        X[0, 3] = nominal * round(X[0, 1], decimal_s)
        X[0, 4] = X[0, 3] - X[0, 2]

    X[7, 0] = s_max
    X[0, 2] = X[0, 4]

    for i in range(1, 8):
        X[i, 0] = kurs(s_min, s_max)[i]

        if is_importer:
            if X[i, 0] <= strike:
                # forward structure
                X[i, 1] = strike
            if bariera <= X[i, 0] <= strike:
                X[i, 1] = strike + (X[i, 0] - strike) * (1 - zp / 100)
            if X[i, 0] >= bariera and X[i, 0] >= strike:
                X[i, 1] = X[i, 0]
        else:
            if X[i, 0] >= strike:
                # forward structure
                X[i, 1] = strike
            if bariera <= X[i, 0] <= strike:
                X[i, 1] = strike - (strike - X[i, 0]) * (1 - zp / 100)
            if X[i, 0] <= bariera and X[i, 0] <= strike:
                X[i, 1] = X[i, 0]

        X[i, 2] = nominal * round(X[i, 0], decimal_s)
        X[i, 3] = nominal * round(X[i, 1], decimal_s)
        X[i, 4] = X[i, 2] - X[i, 3]

        if not is_importer:
            X[i, 4] = -1 * X[i, 4]

        if 0.01 > X[i, 4] > -0.01:
            X[i, 4] = 0

        X[i, 2] = X[i, 4]

    return X

def forw_zwyl_scenario_lever(strike, bariera, zp, lever, nominal, is_importer, decimal_s, s_min, s_max):
    X = np.zeros((8, 5))

    X[0, 0] = s_min
    X[0, 1] = strike
    X[0, 2] = strike
    X[0, 4] = nominal * round(X[0, 0], decimal_s) - nominal * round(X[0, 2], decimal_s)

    if not is_importer:
        X[0, 1] = X[0, 0]
        X[0, 2] = X[0, 0]
        X[0, 4] = nominal * round(X[0, 2], decimal_s) - nominal * round(X[0, 4], decimal_s)

    X[7, 0] = s_max
    X[0, 3] = X[0, 4]
    X[0, 4] = X[0, 1]

    if X[0, 3] >= 0:
        X[0, 1] = nominal * lever
        X[0, 3] = X[0, 3] * lever
    else:
        X[0, 1] = nominal

    for i in range(1, 8):
        X[i, 0] = kurs(s_min, s_max)[i]

        if is_importer:
            if X[i, 0] <= strike:
                # forward structure
                X[i, 1] = strike
            if bariera <= X[i, 0] <= strike:
                X[i, 1] = strike + (X[i, 0] - strike) * (1 - zp / 100)
            if X[i, 0] >= bariera and X[i, 0] >= strike:
                X[i, 1] = X[i, 0]
        else:
            if X[i, 0] >= strike:
                # forward structure
                X[i, 1] = strike
            if bariera <= X[i, 0] <= strike:
                X[i, 1] = strike - (strike - X[i, 0]) * (1 - zp / 100)
            if X[i, 0] <= bariera and X[i, 0] <= strike:
                X[i, 1] = X[i, 0]

        if is_importer:
            if X[i, 0] <= strike:
                # forward structure
                X[i, 2] = strike
            if bariera <= X[i, 0] <= strike:
                X[i, 2] = strike
            if X[i, 0] >= bariera and X[i, 0] >= strike:
                X[i, 2] = X[i, 0]
        else:
            if X[i, 0] >= strike:
                # forward structure
                X[i, 2] = strike
            if bariera <= X[i, 0] <= strike:
                X[i, 2] = strike
            if X[i, 0] <= bariera and X[i, 0] <= strike:
                X[i, 2] = X[i, 0]

        X[i, 4] = nominal * round(X[i, 0], decimal_s) - nominal * round(X[i, 2], decimal_s)

        if not is_importer:
            X[i, 4] = -1 * X[i, 4]

        if 0.01 > X[i, 4] > -0.01:
            X[i, 4] = 0

        X[i, 3] = X[i, 4]
        X[i, 4] = X[i, 1]

        if X[i, 3] >= 0:
            X[i, 1] = nominal * lever
            X[i, 3] = X[i, 3] * lever
        else:
            X[i, 1] = nominal

        if X[i, 0] == strike:
            X[i, 1] = nominal

    return X

def forw_zwyl_iwyp_scenario_lever(strike, bariera, wyp, zp, lever, nominal, is_importer, decimal_s, s_min, s_max):
    X = np.zeros((8, 5))

    X[0, 0] = s_min
    X[0, 1] = strike
    X[0, 2] = strike
    X[0, 4] = nominal * round(X[0, 0], decimal_s) - nominal * round(X[0, 2], decimal_s)

    if not is_importer:
        X[0, 1] = X[0, 0] + (wyp / 100)
        X[0, 2] = X[0, 0] + (wyp / 100) / lever
        X[0, 4] = (wyp / 100) * nominal

    X[7, 0] = s_max
    X[0, 3] = X[0, 4]
    X[0, 4] = X[0, 1]

    if X[0, 3] > 0:
        X[0, 1] = nominal * lever
    else:
        X[0, 1] = nominal

    for i in range(1, 8):
        X[i, 0] = kurs(s_min, s_max)[i]

        if is_importer:
            if X[i, 0] <= strike:
                # forward structure
                X[i, 1] = strike
            if bariera < X[i, 0] < strike:
                X[i, 1] = strike + (X[i, 0] - strike) * (1 - zp / 100)
            if X[i, 0] >= bariera and X[i, 0] >= strike:
                X[i, 1] = X[i, 0] - (wyp / 100)
        else:
            if X[i, 0] > strike:
                # forward structure
                X[i, 1] = strike
            if bariera < X[i, 0] <= strike:
                X[i, 1] = strike - (strike - X[i, 0]) * (1 - zp / 100)
            if X[i, 0] <= bariera:
                X[i, 1] = X[i, 0] + (wyp / 100)

        if is_importer:
            if X[i, 0] <= strike:
                # forward structure
                X[i, 2] = strike
            if bariera < X[i, 0] < strike:
                X[i, 2] = strike
            if X[i, 0] >= bariera and X[i, 0] >= strike:
                X[i, 2] = X[i, 0] - (wyp / 100) / lever
        else:
            if X[i, 0] > strike:
                # forward structure
                X[i, 2] = strike
            if bariera < X[i, 0] <= strike:
                X[i, 2] = strike
            if X[i, 0] <= bariera and X[i, 0] <= strike:
                X[i, 2] = X[i, 0] + (wyp / 100) / lever

        X[i, 4] = nominal * round(X[i, 0], decimal_s) - nominal * round(X[i, 2], decimal_s)

        if X[i, 0] >= bariera and is_importer:
            X[i, 4] = nominal * wyp / 100
        if X[i, 0] <= bariera and not is_importer:
            X[i, 4] = -1 * nominal * wyp / 100

        if not is_importer:
            X[i, 4] = -1 * X[i, 4]

        if 0.01 > X[i, 4] > -0.01:
            X[i, 4] = 0

        X[i, 3] = X[i, 4]
        X[i, 4] = X[i, 1]

        if X[i, 3] > 0:
            X[i, 1] = nominal * lever
        else:
            X[i, 1] = nominal

        if is_importer and X[i, 0] <= bariera and X[i, 3] >= 0:
            X[i, 3] = X[i, 3] * lever
        if not is_importer and X[i, 0] >= bariera and X[i, 3] >= 0:
            X[i, 3] = X[i, 3] * lever

        if X[i, 0] == strike:
            X[i, 1] = nominal

        if X[i, 0] == bariera and is_importer:
            X[i, 3] = (wyp / 100) * nominal
        if X[i, 0] == bariera and not is_importer:
            X[i, 3] = (wyp / 100) * nominal

    return X

def kor_zwyl_iwyp_scenario(put_strike, call_strike, bariera, wyp, zp, nominal, is_importer, decimal_s, s_min, s_max):
    X = np.zeros((8, 5))

    X[0, 0] = s_min
    X[0, 1] = put_strike
    X[0, 2] = nominal * round(X[0, 0], decimal_s)
    X[0, 3] = nominal * round(X[0, 1], decimal_s)
    X[0, 4] = X[0, 2] - X[0, 3]

    if not is_importer:
        X[0, 1] = X[0, 0] + wyp / 100
        X[0, 3] = nominal * round(X[0, 1], decimal_s)
        X[0, 4] = (wyp / 100) * nominal

    X[7, 0] = s_max
    X[0, 2] = X[0, 4]

    for i in range(1, 8):
        X[i, 0] = kurs(s_min, s_max)[i]

        if is_importer:
            if X[i, 0] <= put_strike:
                # forward structure
                X[i, 1] = put_strike
            if put_strike <= X[i, 0] <= call_strike:
                X[i, 1] = X[i, 0]
            if call_strike <= X[i, 0] <= bariera:
                X[i, 1] = call_strike + (X[i, 0] - call_strike) * (1 - zp / 100)
            if X[i, 0] >= bariera and X[i, 0] >= call_strike:
                X[i, 1] = X[i, 0] - wyp / 100

        if not is_importer:
            if X[i, 0] >= call_strike:
                # put line
                X[i, 1] = call_strike
            if put_strike <= X[i, 0] <= call_strike:
                # corridor line
                X[i, 1] = X[i, 0]
            if X[i, 0] <= put_strike and X[i, 0] >= bariera:
                X[i, 1] = put_strike - (X[i, 0] - put_strike) * (1 - zp / 100)
            if X[i, 0] <= put_strike and X[i, 0] <= bariera:
                X[i, 1] = X[i, 0] + wyp / 100

        X[i, 2] = nominal * round(X[i, 0], decimal_s)
        X[i, 3] = nominal * round(X[i, 1], decimal_s)
        X[i, 4] = X[i, 2] - X[i, 3]

        if not is_importer:
            X[i, 4] = -1 * X[i, 4]

        if 0.01 > X[i, 4] > -0.01:
            X[i, 4] = 0

        X[i, 2] = X[i, 4]

    return X

def kor_zwyl_iwyp_scenario_lever(put_strike, call_strike, bariera, wyp, zp, lever, nominal, is_importer, decimal_s, s_min, s_max):
    X = np.zeros((8, 5))

    X[0, 0] = s_min
    X[0, 1] = put_strike
    X[0, 2] = put_strike
    X[0, 4] = nominal * round(X[0, 0], decimal_s) - nominal * round(X[0, 2], decimal_s)

    if not is_importer:
        X[0, 1] = X[0, 0] + (wyp / 100)
        X[0, 2] = X[0, 0] + (wyp / 100) / lever
        X[0, 4] = (wyp / 100) * nominal

    X[7, 0] = s_max
    X[0, 3] = X[0, 4]

    X[0, 4] = X[0, 1]
    if X[0, 3] >= 0:
        X[0, 1] = nominal * lever
    else:
        X[0, 1] = nominal

    for i in range(1, 8):
        X[i, 0] = kurs(s_min, s_max)[i]

        if is_importer:
            if X[i, 0] <= put_strike:
                # forward structure
                X[i, 1] = put_strike
            if put_strike <= X[i, 0] <= call_strike:
                X[i, 1] = X[i, 0]
            if call_strike <= X[i, 0] <= bariera:
                X[i, 1] = call_strike + (X[i, 0] - call_strike) * (1 - zp / 100)
            if X[i, 0] >= bariera and X[i, 0] >= call_strike:
                X[i, 1] = X[i, 0] - wyp / 100

        if not is_importer:
            if X[i, 0] >= call_strike:
                # put line
                X[i, 1] = call_strike
            if put_strike <= X[i, 0] <= call_strike:
                # corridor line
                X[i, 1] = X[i, 0]
            if X[i, 0] <= put_strike and X[i, 0] >= bariera:
                X[i, 1] = put_strike + (X[i, 0] - put_strike) * (1 - zp / 100)
            if X[i, 0] <= put_strike and X[i, 0] <= bariera:
                X[i, 1] = X[i, 0] + wyp / 100

        if is_importer:
            if X[i, 0] <= put_strike:
                # forward structure
                X[i, 2] = put_strike
            if put_strike <= X[i, 0] <= call_strike:
                X[i, 2] = X[i, 0]
            if call_strike <= X[i, 0] >= bariera:
                X[i, 2] = call_strike
            if X[i, 0] >= bariera and X[i, 0] >= call_strike:
                X[i, 2] = X[i, 0] - (wyp / 100) / lever

        if not is_importer:
            if X[i, 0] >= call_strike:
                # put line
                X[i, 2] = call_strike
            if put_strike <= X[i, 0] <= call_strike:
                # corridor line
                X[i, 2] = X[i, 0]
            if X[i, 0] <= put_strike and X[i, 0] >= bariera:
                X[i, 2] = put_strike
            if X[i, 0] <= put_strike and X[i, 0] <= bariera:
                X[i, 2] = X[i, 0] + (wyp / 100) / lever

        X[i, 4] = nominal * round(X[i, 0], decimal_s) - nominal * round(X[i, 2], decimal_s)

        if X[i, 0] >= bariera and is_importer:
            X[i, 4] = nominal * wyp / 100

        if X[i, 0] <= bariera and not is_importer:
            X[i, 4] = nominal * wyp / 100
            X[i, 4] = -1 * X[i, 4]

        if not is_importer:
            X[i, 4] = -1 * X[i, 4]

        if 0.01 > X[i, 4] > -0.01:
            X[i, 4] = 0

        X[i, 3] = X[i, 4]
        X[i, 4] = X[i, 1]

        if X[i, 3] >= 0:
            X[i, 1] = nominal * lever
        else:
            X[i, 1] = nominal

        if is_importer and X[i, 0] <= bariera and X[i, 3] >= 0:
            X[i, 3] = X[i, 3] * lever

        if not is_importer and X[i, 0] >= bariera and X[i, 3] >= 0:
            X[i, 3] = X[i, 3] * lever

        if X[i, 2] == put_strike and is_importer:
            X[i, 1] = nominal

        if X[i, 2] == call_strike and not is_importer:
            X[i, 1] = nominal

        if X[i, 0] == bariera and is_importer:
            X[i, 3] = (wyp / 100) * nominal

        if X[i, 0] == bariera and not is_importer:
            X[i, 3] = (wyp / 100) * nominal

    return X

def kor_mewa_scenario(put_strike, call_strike, bariera, zp, nominal, is_importer, decimal_s, s_min, s_max):
    X = np.zeros((8, 5))

    X[0, 0] = s_min
    X[0, 1] = put_strike
    X[0, 2] = nominal * round(X[0, 0], decimal_s)
    X[0, 3] = nominal * round(X[0, 1], decimal_s)
    X[0, 4] = X[0, 2] - X[0, 3]

    if not is_importer:
        X[0, 1] = X[0, 0] + (bariera - put_strike) * (zp / 100)
        X[0, 3] = nominal * round(X[0, 1], decimal_s)
        X[0, 4] = X[0, 3] - X[0, 2]

    X[7, 0] = s_max
    X[0, 2] = X[0, 4]

    for i in range(1, 8):
        X[i, 0] = kurs(s_min, s_max)[i]

        if is_importer:
            if X[i, 0] <= put_strike:
                # forward structure
                X[i, 1] = put_strike
            if put_strike <= X[i, 0] <= bariera:
                X[i, 1] = X[i, 0]
            if bariera <= X[i, 0] <= call_strike:
                X[i, 1] = bariera + (X[i, 0] - bariera) * (1 - zp / 100)
            if X[i, 0] >= call_strike and X[i, 0] >= bariera:
                X[i, 1] = X[i, 0] - (call_strike - bariera) * (zp / 100)

        if not is_importer:
            if X[i, 0] >= call_strike:
                # put line
                X[i, 1] = call_strike
            if call_strike >= X[i, 0] >= bariera:
                # corridor line
                X[i, 1] = X[i, 0]
            if bariera >= X[i, 0] >= put_strike:
                X[i, 1] = bariera - (bariera - X[i, 0]) * (1 - zp / 100)
            if X[i, 0] <= put_strike and X[i, 0] <= bariera:
                X[i, 1] = X[i, 0] + (bariera - put_strike) * (zp / 100)

        X[i, 2] = nominal * round(X[i, 0], decimal_s)
        X[i, 3] = nominal * round(X[i, 1], decimal_s)
        X[i, 4] = X[i, 2] - X[i, 3]

        if not is_importer:
            X[i, 4] = -1 * X[i, 4]

        if 0.01 > X[i, 4] > -0.01:
            X[i, 4] = 0

        X[i, 2] = X[i, 4]

    return X

def kor_mewa_scenario_lever(put_strike, call_strike, bariera, zp, lever, nominal, is_importer, decimal_s, s_min, s_max):
    X = np.zeros((8, 5))

    X[0, 0] = s_min
    X[0, 1] = put_strike
    X[0, 2] = put_strike
    X[0, 3] = nominal * round(X[0, 1], decimal_s)
    X[0, 4] = nominal * round(X[0, 0], decimal_s) - nominal * round(X[0, 2], decimal_s)

    if not is_importer:
        X[0, 1] = X[0, 0] + (bariera - put_strike) * (zp / 100)
        X[0, 2] = X[0, 0] + (bariera - put_strike)
        X[0, 4] = nominal * round(X[0, 2], decimal_s) - nominal * round(X[0, 0], decimal_s)

    X[7, 0] = s_max
    X[0, 3] = X[0, 4]

    X[0, 4] = X[0, 1]
    if X[0, 3] > 0:
        X[0, 1] = nominal * lever
        X[0, 3] = X[0, 3] * lever
    else:
        X[0, 1] = nominal

    for i in range(1, 8):
        X[i, 0] = kurs(s_min, s_max)[i]

        if is_importer:
            if X[i, 0] <= put_strike:
                # forward structure
                X[i, 1] = put_strike
            if put_strike <= X[i, 0] <= bariera:
                X[i, 1] = X[i, 0]
            if bariera <= X[i, 0] <= call_strike:
                X[i, 1] = bariera + (X[i, 0] - bariera) * (1 - zp / 100)
            if X[i, 0] >= call_strike and X[i, 0] >= bariera:
                X[i, 1] = X[i, 0] - (call_strike - bariera) * (zp / 100)

        if not is_importer:
            if X[i, 0] >= call_strike:
                # put line
                X[i, 1] = call_strike
            if call_strike >= X[i, 0] >= bariera:
                # corridor line
                X[i, 1] = X[i, 0]
            if bariera >= X[i, 0] >= put_strike:
                X[i, 1] = bariera - (bariera - X[i, 0]) * (1 - zp / 100)
            if X[i, 0] <= put_strike and X[i, 0] <= bariera:
                X[i, 1] = X[i, 0] + (bariera - put_strike) * (zp / 100)

        if is_importer:
            if X[i, 0] <= put_strike:
                # forward structure
                X[i, 2] = put_strike
            if put_strike <= X[i, 0] <= bariera:
                X[i, 2] = X[i, 0]
            if bariera <= X[i, 0] <= call_strike:
                X[i, 2] = bariera
            if X[i, 0] >= call_strike and X[i, 0] >= bariera:
                X[i, 2] = X[i, 0] - (call_strike - bariera)

        if not is_importer:
            if X[i, 0] >= call_strike:
                # put line
                X[i, 2] = call_strike
            if call_strike >= X[i, 0] >= bariera:
                # corridor line
                X[i, 2] = X[i, 0]
            if bariera >= X[i, 0] >= put_strike:
                X[i, 2] = bariera
            if X[i, 0] <= put_strike and X[i, 0] <= bariera:
                X[i, 2] = X[i, 0] + (bariera - put_strike)

        X[i, 4] = nominal * round(X[i, 0], decimal_s) - nominal * round(X[i, 2], decimal_s)

        if not is_importer:
            X[i, 4] = -1 * X[i, 4]

        if 0.01 > X[i, 4] > -0.01:
            X[i, 4] = 0

        X[i, 3] = X[i, 4]
        X[i, 4] = X[i, 1]

        if X[i, 3] >= 0:
            X[i, 1] = nominal

def kor_mewa_scenario2(put_strike, call_strike, bariera, zp, nominal, is_importer, decimal_s, s_min, s_max):
    X = np.zeros((8, 5))

    X[0, 0] = s_min
    X[0, 2] = nominal * round(X[0, 0], decimal_s)

    if not is_importer:
        X[0, 1] = put_strike
        X[0, 3] = nominal * round(X[0, 1], decimal_s)
        X[0, 4] = X[0, 3] - X[0, 2]

    if is_importer:
        X[0, 1] = X[0, 0] + (bariera - put_strike) * (zp / 100)
        X[0, 3] = nominal * round(X[0, 1], decimal_s)
        X[0, 4] = X[0, 2] - X[0, 3]

    X[7, 0] = s_max
    X[0, 2] = X[0, 4]

    for i in range(1, 8):
        X[i, 0] = kurs(s_min, s_max)[i]

        if not is_importer:
            if X[i, 0] <= put_strike:
                # forward structure
                X[i, 1] = put_strike
            if put_strike <= X[i, 0] <= bariera:
                X[i, 1] = X[i, 0]
            if bariera <= X[i, 0] <= call_strike:
                X[i, 1] = bariera + (X[i, 0] - bariera) * (1 - zp / 100)
            if X[i, 0] >= call_strike and X[i, 0] >= bariera:
                X[i, 1] = X[i, 0] - (call_strike - bariera) * (zp / 100)

        if is_importer:
            if X[i, 0] >= call_strike:
                # put line
                X[i, 1] = call_strike
            if call_strike >= X[i, 0] >= bariera:
                # corridor line
                X[i, 1] = X[i, 0]
            if bariera >= X[i, 0] >= put_strike:
                X[i, 1] = bariera - (bariera - X[i, 0]) * (1 - zp / 100)
            if X[i, 0] <= put_strike and X[i, 0] <= bariera:
                X[i, 1] = X[i, 0] + (bariera - put_strike) * (zp / 100)

        X[i, 2] = nominal * round(X[i, 0], decimal_s)
        X[i, 3] = nominal * round(X[i, 1], decimal_s)
        X[i, 4] = X[i, 2] - X[i, 3]

        if not is_importer:
            X[i, 4] = -1 * X[i, 4]

        if 0.01 > X[i, 4] > -0.01:
            X[i, 4] = 0

        X[i, 2] = X[i, 4]

    return X

def bestlook_scenario1b(gw, minn, maxx, nominal, adj, is_importer, decimal_s, s_min, s_max):
    X = np.zeros((8, 5))

    if is_importer:
        X[0, 0] = minn * 1.005 + adj
        X[0, 1] = minn * 1.005 + adj
        X[0, 2] = nominal * round(X[0, 0], decimal_s)
        X[0, 3] = nominal * round(X[0, 1], decimal_s)
        X[0, 4] = X[0, 2] - X[0, 3]
        X[7, 0] = maxx - 0.001
    else:
        X[7, 0] = maxx * 0.995 + adj
        X[0, 1] = maxx * 0.995 + adj
        X[0, 0] = minn + 0.001
        X[0, 3] = nominal * round(X[0, 1], decimal_s)
        X[0, 2] = nominal * round(X[0, 0], decimal_s)
        X[0, 4] = X[0, 3] - X[0, 2]

    X[0, 2] = X[0, 4]
    for i in range(1, 8):
        X[i, 0] = X[i - 1, 0] + (X[7, 0] - X[0, 0]) / 7

        if not is_importer:
            X[i, 1] = maxx * 0.995 + adj

        if is_importer:
            X[i, 1] = minn * 1.005 + adj

        X[i, 2] = nominal * round(X[i, 0], decimal_s)
        X[i, 3] = nominal * round(X[i, 1], decimal_s)
        X[i, 4] = X[i, 2] - X[i, 3]

        if not is_importer:
            X[i, 4] = -1 * X[i, 4]

        if 0.01 > X[i, 4] > -0.01:
            X[i, 4] = 0

        X[i, 2] = X[i, 4]

    return X

def bestlook_scenario1(gw, minn, maxx, nominal, adj, is_importer, decimal_s, s_min, s_max):
    X = np.zeros((8, 5))

    if is_importer:
        X[0, 0] = minn * 1.005 + adj
        X[0, 1] = minn * 1.005 + adj
        X[0, 2] = nominal * round(X[0, 0], decimal_s)
        X[0, 3] = nominal * round(X[0, 1], decimal_s)
        X[0, 4] = X[0, 2] - X[0, 3]
        X[7, 0] = maxx - 0.001
    else:
        X[7, 0] = maxx * 0.995 + adj
        X[0, 1] = maxx * 0.995 + adj
        X[0, 0] = minn + 0.001
        X[0, 3] = nominal * round(X[0, 1], decimal_s)
        X[0, 2] = nominal * round(X[0, 0], decimal_s)
        X[0, 4] = X[0, 3] - X[0, 2]

    X[0, 2] = X[0, 4]
    for i in range(1, 8):
        X[i, 0] = X[i - 1, 0] + (X[7, 0] - X[0, 0]) / 7

        if not is_importer:
            X[i, 1] = maxx * 0.995 + adj

        if is_importer:
            X[i, 1] = minn * 1.005 + adj

        X[i, 2] = nominal * round(X[i, 0], decimal_s)
        X[i, 3] = nominal * round(X[i, 1], decimal_s)
        X[i, 4] = X[i, 2] - X[i, 3]

        if not is_importer:
            X[i, 4] = -1 * X[i, 4]

        if 0.01 > X[i, 4] > -0.01:
            X[i, 4] = 0

        X[i, 2] = X[i, 4]

    return X

def bestlook_scenario2(gw, minn, maxx, nominal, is_importer, decimal_s, s_min, s_max):
    X = np.zeros((8, 5))

    X[0, 0] = gw
    X[0, 1] = gw
    X[0, 2] = nominal * round(X[0, 0], decimal_s)
    X[0, 3] = nominal * round(X[0, 1], decimal_s)
    X[0, 4] = X[0, 2] - X[0, 3]

    if not is_importer:
        X[0, 3] = nominal * round(X[0, 1], decimal_s)
        X[0, 4] = X[0, 3] - X[0, 2]

    for i in range(1, 8):
        X[i, 0] = kurs(s_min, s_max)[i]

        X[i, 1] = gw

        X[i, 2] = nominal * round(X[i, 0], decimal_s)
        X[i, 3] = nominal * round(X[i, 1], decimal_s)
        X[i, 4] = X[i, 2] - X[i, 3]

        if not is_importer:
            X[i, 4] = -1 * X[i, 4]

        if 0.01 > X[i, 4] > -0.01:
            X[i, 4] = 0

        X[i, 2] = X[i, 4]

    return X

def forw_elas_scenario(strike, zp, bariera, nominal, is_importer, decimal_s, s_min, s_max):
    X = np.zeros((8, 5))

    X[0, 0] = s_min
    X[0, 1] = strike
    X[0, 2] = nominal * round(X[0, 0], decimal_s)
    X[0, 3] = nominal * round(X[0, 1], decimal_s)
    X[0, 4] = X[0, 2] - X[0, 3]

    if not is_importer:
        X[0, 1] = strike - (strike - X[0, 0]) * (1 - zp / 100)
        X[0, 3] = nominal * round(X[0, 1], decimal_s)
        X[0, 4] = X[0, 3] - X[0, 2]

    X[7, 0] = s_max
    X[0, 2] = X[0, 4]

    for i in range(1, 8):
        X[i, 0] = kurs(s_min, s_max)[i]

        if is_importer:
            if X[i, 0] >= strike:
                X[i, 1] = strike + (X[i, 0] - strike) * (1 - zp / 100)

            if X[i, 0] <= strike and bariera >= X[i, 0]:
                X[i, 1] = strike

            if X[i, 0] <= strike and bariera < X[i, 0]:
                X[i, 1] = X[i, 0]

        if not is_importer:
            if X[i, 0] <= strike:
                X[i, 1] = strike - (strike - X[i, 0]) * (1 - zp / 100)

            if X[i, 0] >= strike and bariera <= X[i, 0]:
                X[i, 1] = strike

            if X[i, 0] >= strike and bariera > X[i, 0]:
                X[i, 1] = X[i, 0]

        X[i, 2] = nominal * round(X[i, 0], decimal_s)
        X[i, 3] = nominal * round(X[i, 1], decimal_s)
        X[i, 4] = X[i, 2] - X[i, 3]

        if not is_importer:
            X[i, 4] = -1 * X[i, 4]

        if 0.01 > X[i, 4] > -0.01:
            X[i, 4] = 0

        X[i, 2] = X[i, 4]

    return X

def Kor_elas_scenario_lever(put_strike, call_strike, zp, lever, bariera, nominal, is_importer, decimal_s, s_min, s_max):
    X = np.zeros((8, 5))

    X[0, 0] = s_min
    X[0, 1] = put_strike
    X[0, 2] = put_strike
    X[0, 4] = nominal * round(X[0, 0], decimal_s) - nominal * round(X[0, 2], decimal_s)

    if not is_importer:
        X[0, 1] = put_strike - (put_strike - X[0, 0]) * (1 - zp / 100)
        X[0, 4] = nominal * round(X[0, 2], decimal_s) - nominal * round(X[0, 0], decimal_s)

    X[7, 0] = s_max
    X[0, 3] = X[0, 4]
    X[0, 4] = X[0, 1]

    if X[0, 3] > 0:
        X[0, 1] = nominal * lever
        X[0, 3] = X[0, 3] * lever
    else:
        X[0, 1] = nominal

    for i in range(1, 8):
        X[i, 0] = kurs(s_min, s_max)[i]

        if is_importer:
            if X[i, 0] >= call_strike:
                X[i, 1] = call_strike + (X[i, 0] - call_strike) * (1 - zp / 100)

            if X[i, 0] <= bariera:
                X[i, 1] = put_strike

            if bariera < X[i, 0] <= call_strike:
                X[i, 1] = X[i, 0]

        if not is_importer:
            if X[i, 0] <= put_strike:
                X[i, 1] = put_strike - (put_strike - X[i, 0]) * (1 - zp / 100)

            if X[i, 0] >= bariera:
                X[i, 1] = call_strike

            if bariera >= X[i, 0] >= put_strike:
                X[i, 1] = X[i, 0]

        if is_importer:
            if X[i, 0] >= call_strike:
                X[i, 2] = call_strike

            if X[i, 0] <= bariera:
                X[i, 2] = put_strike

            if bariera < X[i, 0] <= call_strike:
                X[i, 2] = X[i, 0]

        if not is_importer:
            if X[i, 0] <= put_strike:
                X[i, 2] = put_strike

            if X[i, 0] >= bariera:
                X[i, 2] = call_strike

            if bariera >= X[i, 0] >= put_strike:
                X[i, 2] = X[i, 0]

        X[i, 4] = nominal * round(X[i, 0], decimal_s) - nominal * round(X[i, 2], decimal_s)

        if not is_importer:
            X[i, 4] = -1 * X[i, 4]

        if 0.01 > X[i, 4] > -0.01:
            X[i, 4] = 0

        X[i, 3] = X[i, 4]
        X[i, 4] = X[i, 1]

        if X[i, 3] >= 0:
            X[i, 1] = nominal * lever
            X[i, 3] = X[i, 3] * lever
        else:
            X[i, 1] = nominal

        if X[i, 0] == bariera and is_importer:
            X[i, 1] = nominal

        if X[i, 0] == bariera and not is_importer:
            X[i, 1] = nominal

    return X

def Kor_elas_scenario(put_strike, call_strike, zp, bariera, nominal, is_importer, decimal_s, s_min, s_max):
    X = np.zeros((8, 5))

    X[0, 0] = s_min
    X[0, 1] = put_strike
    X[0, 2] = nominal * round(X[0, 0], decimal_s)
    X[0, 3] = nominal * round(X[0, 1], decimal_s)
    X[0, 4] = X[0, 2] - X[0, 3]

    if not is_importer:
        X[0, 1] = put_strike - (put_strike - X[0, 0]) * (1 - zp / 100)
        X[0, 3] = nominal * round(X[0, 1], decimal_s)
        X[0, 4] = X[0, 3] - X[0, 2]

    X[7, 0] = s_max
    X[0, 2] = X[0, 4]

    for i in range(1, 8):
        X[i, 0] = kurs(s_min, s_max)[i]

        if is_importer:
            if X[i, 0] >= call_strike:
                X[i, 1] = call_strike + (X[i, 0] - call_strike) * (1 - zp / 100)

            if X[i, 0] <= bariera:
                X[i, 1] = put_strike

            if bariera < X[i, 0] <= call_strike:
                X[i, 1] = X[i, 0]

        if not is_importer:
            if X[i, 0] <= put_strike:
                X[i, 1] = put_strike - (put_strike - X[i, 0]) * (1 - zp / 100)

            if X[i, 0] >= bariera:
                X[i, 1] = call_strike

            if bariera >= X[i, 0] >= put_strike:
                X[i, 1] = X[i, 0]

        X[i, 2] = nominal * round(X[i, 0], decimal_s)
        X[i, 3] = nominal * round(X[i, 1], decimal_s)
        X[i, 4] = X[i, 2] - X[i, 3]

        if not is_importer:
            X[i, 4] = -1 * X[i, 4]

        if 0.01 > X[i, 4] > -0.01:
            X[i, 4] = 0

        X[i, 2] = X[i, 4]

    return X

def Partyp_scenario(strike, zp, nominal, is_importer, decimal_s, s_min, s_max):
    X = np.zeros((8, 5))

    X[0, 0] = s_min
    X[0, 1] = zp / 100 * strike + (1 - zp / 100) * X[0, 0]
    X[0, 2] = nominal * round(X[0, 0], decimal_s)
    X[0, 3] = nominal * round(X[0, 1], decimal_s)
    X[0, 4] = X[0, 2] - X[0, 3]

    if not is_importer:
        X[0, 1] = strike
        X[0, 3] = nominal * round(X[0, 1], decimal_s)
        X[0, 4] = X[0, 3] - X[0, 2]

    X[7, 0] = s_max
    X[0, 3] = X[0, 4]
    X[0, 4] = X[0, 1]
    X[0, 2] = strike

    if X[0, 4] != strike:
        X[0, 1] = nominal * zp / 100
    else:
        X[0, 1] = nominal

    for i in range(1, 8):
        X[i, 0] = kurs(s_min, s_max)[i]

        if is_importer:
            if X[i, 0] >= strike:
                X[i, 1] = strike
            else:
                X[i, 1] = zp / 100 * strike + (1 - zp / 100) * X[i, 0]

        if not is_importer:
            if X[i, 0] >= strike:
                X[i, 1] = zp / 100 * strike + (1 - zp / 100) * X[i, 0]
            else:
                X[i, 1] = strike

        X[i, 2] = nominal * round(X[i, 0], decimal_s)
        X[i, 3] = nominal * round(X[i, 1], decimal_s)
        X[i, 4] = X[i, 2] - X[i, 3]

        if not is_importer:
            X[i, 4] = -1 * X[i, 4]

        if 0.01 > X[i, 4] > -0.01:
            X[i, 4] = 0

        X[i, 3] = X[i, 4]
        X[i, 4] = X[i, 1]
        X[i, 2] = strike

        if X[i, 4] != strike:
            X[i, 1] = nominal * (zp / 100)
        else:
            X[i, 1] = nominal

    return X

def Spread_scenario(put_strike, call_strike, koszt, nominal, is_importer, decimal_s, s_min, s_max):
    X = np.zeros((8, 5))

    X[0, 0] = s_min
    X[0, 1] = s_min
    X[0, 2] = nominal * round(X[0, 0], decimal_s)
    X[0, 3] = nominal * round(X[0, 1], decimal_s)
    X[0, 4] = X[0, 2] - X[0, 3]

    if not is_importer:
        X[0, 1] = X[0, 0] + (call_strike - put_strike)
        X[0, 3] = nominal * round(X[0, 1], decimal_s)
        X[0, 4] = X[0, 3] - X[0, 2]

    X[7, 0] = s_max
    X[0, 2] = X[0, 4]

    for i in range(1, 8):
        X[i, 0] = kurs(s_min, s_max)[i]

        if is_importer:
            if X[i, 0] <= put_strike:
                X[i, 1] = X[i, 0]

            if put_strike <= X[i, 0] <= call_strike:
                X[i, 1] = put_strike

            if X[i, 0] >= call_strike:
                X[i, 1] = X[i, 0] - (call_strike - put_strike)

        if not is_importer:
            if X[i, 0] <= put_strike:
                X[i, 1] = X[i, 0] + (call_strike - put_strike)

            if put_strike <= X[i, 0] <= call_strike:
                X[i, 1] = call_strike

            if X[i, 0] >= call_strike:
                X[i, 1] = X[i, 0]

        X[i, 2] = nominal * round(X[i, 0], decimal_s)
        X[i, 3] = nominal * round(X[i, 1], decimal_s)
        X[i, 4] = X[i, 2] - X[i, 3]

        if not is_importer:
            X[i, 4] = -1 * X[i, 4]

        if 0.01 > X[i, 4] > -0.01:
            X[i, 4] = 0

        X[i, 2] = X[i, 4]

    return X
    
def Kor_zrek_scenario(put_strike, call_strike, zp, bariera, wyp, nominal, is_importer, decimal_s, s_min, s_max):
    X = np.zeros((8, 5))

    X[0, 0] = s_min
    X[0, 1] = wyp
    X[0, 2] = nominal * round(X[0, 0], decimal_s)
    X[0, 3] = nominal * round(X[0, 1], decimal_s)
    X[0, 4] = X[0, 2] - X[0, 3]

    if not is_importer:
        X[0, 1] = put_strike - (put_strike - X[0, 0]) * (1 - zp / 100)
        X[0, 3] = nominal * round(X[0, 1], decimal_s)
        X[0, 4] = X[0, 3] - X[0, 2]

    X[7, 0] = s_max
    X[0, 2] = X[0, 4]

    for i in range(1, 8):
        X[i, 0] = kurs(s_min, s_max)[i]

        if is_importer:
            if X[i, 0] >= call_strike:
                # linia korytarz elastyczny
                X[i, 1] = call_strike + (X[i, 0] - call_strike) * (1 - zp / 100)

            if bariera >= X[i, 0]:
                X[i, 1] = wyp

            if put_strike <= X[i, 0] <= call_strike:
                X[i, 1] = X[i, 0]

            if X[i, 0] > bariera and X[i, 0] <= put_strike:
                X[i, 1] = put_strike

        if not is_importer:
            if X[i, 0] >= bariera:
                # linia korytarz elastyczny
                X[i, 1] = wyp

            if put_strike <= X[i, 0] <= bariera:
                X[i, 1] = X[i, 0]

            if X[i, 0] <= put_strike:
                X[i, 1] = put_strike - (put_strike - X[i, 0]) * (1 - zp / 100)

            if X[i, 0] < bariera and X[i, 0] >= call_strike:
                X[i, 1] = call_strike

        X[i, 2] = nominal * round(X[i, 0], decimal_s)
        X[i, 3] = nominal * round(X[i, 1], decimal_s)
        X[i, 4] = X[i, 2] - X[i, 3]

        if not is_importer:
            X[i, 4] = -1 * X[i, 4]

        if 0.01 > X[i, 4] > -0.01:
            X[i, 4] = 0

        X[i, 2] = X[i, 4]

    return X

def Eur_scenario(strike, nominal, is_importer, decimal_s, zp, s_min, s_max):
    X = np.zeros((8, 5))

    X[0, 0] = s_min
    X[0, 1] = s_min
    X[0, 2] = nominal * round(X[0, 0], decimal_s)
    X[0, 3] = nominal * round(X[0, 1], decimal_s)
    X[0, 4] = X[0, 2] - X[0, 3]

    if not is_importer:
        X[0, 1] = strike - (strike - X[0, 0]) * (1 - (zp / 100))
        X[0, 3] = nominal * round(X[0, 1], decimal_s)
        X[0, 4] = X[0, 3] - X[0, 2]

    X[7, 0] = s_max
    X[0, 2] = X[0, 4]

    for i in range(1, 8):
        X[i, 0] = kurs(s_min, s_max)[i]

        if is_importer:
            if X[i, 0] >= strike:
                X[i, 1] = strike + (X[i, 0] - strike) * (1 - (zp / 100))
            else:
                X[i, 1] = X[i, 0]

        if not is_importer:
            if X[i, 0] <= strike:
                X[i, 1] = strike - (strike - X[i, 0]) * (1 - (zp / 100))
            else:
                X[i, 1] = X[i, 0]

        X[i, 2] = nominal * round(X[i, 0], decimal_s)
        X[i, 3] = nominal * round(X[i, 1], decimal_s)
        X[i, 4] = X[i, 2] - X[i, 3]

        if not is_importer:
            X[i, 4] = -1 * X[i, 4]

        if 0.01 > X[i, 4] > -0.01:
            X[i, 4] = 0

        X[i, 2] = X[i, 4]

    return X

def Eur_r_scenario(strike, rebate, proc, nominal, is_importer, decimal_s, zp, s_min, s_max):
    X = np.zeros((8, 5))

    X[0, 0] = s_min
    X[0, 1] = s_min
    X[0, 2] = nominal * round(X[0, 0], decimal_s)
    X[0, 3] = nominal * round(X[0, 1], decimal_s)
    X[0, 4] = X[0, 2] - X[0, 3]

    if not is_importer:
        X[0, 1] = strike - (strike - X[0, 0]) * (1 - (zp / 100))
        X[0, 3] = nominal * round(X[0, 1], decimal_s)
        X[0, 4] = X[0, 3] - X[0, 2]

    X[7, 0] = s_max
    X[0, 2] = X[0, 4]

    for i in range(1, 8):
        X[i, 0] = kurs(s_min, s_max)[i]

        if is_importer:
            if X[i, 0] >= strike:
                X[i, 1] = strike + (X[i, 0] - strike) * (1 - (zp / 100))
            else:
                X[i, 1] = X[i, 0]

        if not is_importer:
            if X[i, 0] <= strike:
                X[i, 1] = strike - (strike - X[i, 0]) * (1 - (zp / 100))
            else:
                X[i, 1] = X[i, 0]

        X[i, 2] = nominal * round(X[i, 0], decimal_s)
        X[i, 3] = nominal * round(X[i, 1], decimal_s)
        X[i, 4] = X[i, 2] - X[i, 3]

        if not is_importer:
            X[i, 4] = -1 * X[i, 4]

        if 0.01 > X[i, 4] > -0.01:
            X[i, 4] = 0

        X[i, 2] = X[i, 4]

    return X

def Kor_scenario_lever(put_strike, call_strike, zp, lever, nominal, is_importer, decimal_s, s_min, s_max):
    X = np.zeros((8, 5))

    X[0, 0] = s_min
    X[0, 1] = put_strike
    X[0, 2] = nominal * round(X[0, 0], decimal_s)
    X[0, 3] = nominal * round(X[0, 1], decimal_s)
    X[0, 4] = X[0, 2] - X[0, 3]

    if not is_importer:
        X[0, 1] = put_strike - (put_strike - X[0, 0]) * (1 - zp / 100)
        X[0, 3] = nominal * round(put_strike, 4)
        X[0, 4] = X[0, 3] - X[0, 2]

    X[7, 0] = s_max
    X[0, 3] = X[0, 4]
    X[0, 4] = X[0, 1]
    X[0, 2] = put_strike

    if X[0, 4] != put_strike:
        X[0, 1] = nominal * lever
        X[0, 3] = X[0, 3] * lever
    else:
        X[0, 1] = nominal

    for i in range(1, 8):
        X[i, 0] = kurs(s_min, s_max)[i]

        if is_importer:
            if X[i, 0] <= put_strike:
                X[i, 1] = put_strike

            if X[i, 0] >= call_strike:
                X[i, 1] = call_strike + (X[i, 0] - call_strike) * (1 - zp / 100)

            if put_strike <= X[i, 0] <= call_strike:
                X[i, 1] = X[i, 0]

        if not is_importer:
            if X[i, 0] <= put_strike:
                X[i, 1] = put_strike - (put_strike - X[i, 0]) * (1 - zp / 100)

            if X[i, 0] >= call_strike:
                X[i, 1] = call_strike

            if put_strike <= X[i, 0] <= call_strike:
                X[i, 1] = X[i, 0]

        if is_importer:
            if X[i, 0] <= put_strike:
                X[i, 2] = put_strike

            if X[i, 0] >= call_strike:
                X[i, 2] = call_strike

            if put_strike <= X[i, 0] <= call_strike:
                X[i, 2] = X[i, 0]

        if not is_importer:
            if X[i, 0] <= put_strike:
                X[i, 2] = put_strike

            if X[i, 0] >= call_strike:
                X[i, 2] = call_strike

            if put_strike <= X[i, 0] <= call_strike:
                X[i, 2] = X[i, 0]

        X[i, 4] = nominal * round(X[i, 0], decimal_s) - nominal * round(X[i, 2], decimal_s)

        if not is_importer:
            X[i, 4] = -1 * X[i, 4]

        if 0.01 > X[i, 4] > -0.01:
            X[i, 4] = 0

        X[i, 3] = X[i, 4]
        X[i, 4] = X[i, 1]

        if X[i, 3] >= 0:
            X[i, 1] = nominal * lever
            X[i, 3] = X[i, 3] * lever
        else:
            X[i, 1] = nominal

        if X[i, 2] == put_strike and is_importer:
            X[i, 1] = nominal

        if X[i, 2] == call_strike and not is_importer:
            X[i, 1] = nominal

    return X

def Kor_scenario(put_strike, call_strike, zp, nominal, is_importer, decimal_s, s_min, s_max):
    X = np.zeros((8, 5))

    X[0, 0] = s_min
    X[0, 1] = put_strike
    X[0, 2] = nominal * round(X[0, 0], decimal_s)
    X[0, 3] = nominal * round(X[0, 1], decimal_s)
    X[0, 4] = X[0, 2] - X[0, 3]

    if not is_importer:
        X[0, 1] = put_strike - (put_strike - X[0, 0]) * (1 - zp / 100)
        X[0, 3] = nominal * round(X[0, 1], decimal_s)
        X[0, 4] = X[0, 3] - X[0, 2]

    X[7, 0] = s_max
    X[0, 2] = X[0, 4]

    for i in range(1, 8):
        X[i, 0] = kurs(s_min, s_max)[i]

        if is_importer:
            if X[i, 0] <= put_strike:
                X[i, 1] = put_strike

            if X[i, 0] >= call_strike:
                X[i, 1] = call_strike + (X[i, 0] - call_strike) * (1 - zp / 100)

            if put_strike <= X[i, 0] <= call_strike:
                X[i, 1] = X[i, 0]

        if not is_importer:
            if X[i, 0] <= put_strike:
                X[i, 1] = put_strike - (put_strike - X[i, 0]) * (1 - zp / 100)

            if X[i, 0] >= call_strike:
                X[i, 1] = call_strike

            if put_strike <= X[i, 0] <= call_strike:
                X[i, 1] = X[i, 0]

        X[i, 2] = nominal * round(X[i, 0], decimal_s)
        X[i, 3] = nominal * round(X[i, 1], decimal_s)
        X[i, 4] = X[i, 2] - X[i, 3]

        if not is_importer:
            X[i, 4] = -1 * X[i, 4]

        if 0.01 > X[i, 4] > -0.01:
            X[i, 4] = 0

        X[i, 2] = X[i, 4]

    return X
