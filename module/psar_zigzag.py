# Reference:
# https://www.bonjin-biz.xyz/parabolic-sar-calculation/#6_SAR2
# https://qiita.com/siruku6/items/76f4072c06a988dfe2cb
import pandas as pd

# parabolicSAR生成
# # # # # # # # # # # # # # # # # # # # # # # # # # # #
#                   Parabolic SAR                     #
# # # # # # # # # # # # # # # # # # # # # # # # # # # #
INITIAL_AF = 0.02
MAX_AF = 0.2


def calc_next_parabolic(last_sar, ep, acceleration_f=INITIAL_AF):
    return last_sar + acceleration_f * (ep - last_sar)


def parabolic_is_touched(bull, current_parabo, current_h, current_l):
    if bull and (current_parabo > current_l):
        return True
    elif not bull and (current_parabo < current_h):
        return True
    return False


def calc_parabolic(candles):
    # 初期値
    acceleration_factor = INITIAL_AF
    # INFO: 初期状態は上昇トレンドと仮定して計算
    bull = True
    extreme_price = candles.high[0]
    temp_sar_array = [candles.low[0]]

    # HACK: dataframeのまま処理するより、to_dictで辞書配列化した方が処理が早い
    candles_array = candles.to_dict('records')
    for i, row in enumerate(candles_array):
        current_high = row['high']
        current_low = row['low']
        last_sar = temp_sar_array[-1]

        # レートがparabolicに触れたときの処理
        if parabolic_is_touched(
                bull=bull,
                current_parabo=last_sar,
                current_h=current_high, current_l=current_low
        ):
            temp_sar = extreme_price
            acceleration_factor = INITIAL_AF
            if bull:
                bull = False
                extreme_price = current_low
            else:
                bull = True
                extreme_price = current_high
        else:
            # SARの仮決め
            temp_sar = calc_next_parabolic(
                last_sar=last_sar, ep=extreme_price, acceleration_f=acceleration_factor
            )

            # AFの更新
            if (bull and extreme_price < current_high) \
                    or not bull and extreme_price > current_low:
                acceleration_factor = min(
                    acceleration_factor + INITIAL_AF,
                    MAX_AF
                )

            # SARの調整
            if bull:
                temp_sar = min(
                    temp_sar, candles_array[i - 1]['low'], candles_array[i - 2]['low']
                )
                extreme_price = max(extreme_price, current_high)
            else:
                temp_sar = max(
                    temp_sar, candles_array[i - 1]['high'], candles_array[i - 2]['high']
                )
                extreme_price = min(extreme_price, current_low)

        if i == 0:
            temp_sar_array[-1] = temp_sar
        else:
            temp_sar_array.append(temp_sar)

    return pd.DataFrame(data=temp_sar_array, columns=['SAR'])
