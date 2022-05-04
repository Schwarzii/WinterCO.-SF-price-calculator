from browser import document
import browser.html as ht

# calc = ht.TABLE()
# calc <= ht.TR(ht.TH(ht.DIV("0", id="result"), colspan=3) + ht.TD("C"))
#
# document <= calc

route = {'Jita': {'4-HWWF': 250, 'Otsasai': 50, 'N5Y-4N': 500, 'Oijanen': 200},
         '4-HWWF': {'Jita': 60, 'Otsasai': 100, 'Oijanen': 125},
         'Otsasai': {'Jita': 50, '4-HWWF': 100},
         'N5Y-4N': {'Jita': 500},
         'Oijanen': {'Jita': 300, '4-HWWF': 125}
         }

station = {'Jita': 'IV - Moon 4 - Caldari Navy Assembly Plant',
           '4-HWWF': 'Winter CO. Central Station',
           # 'RF-X7V - Forums.WinTerCo.org',
           'Otsasai': 'Fuxi Prime - Home for Ever',
           'N5Y-4N': 'xingcheng',
           'Oijanen': 'Lowsec jita'}

order = ht.TABLE(id='table')

departure = ht.SELECT(ht.OPTION(station) for station in route.keys())
arrival = ht.SELECT(ht.OPTION(station) for station in route['Jita'].keys())

order <= ht.TR(ht.TH("凛冬联盟顺丰快递费用计算器", colspan=6, style={'text-align': 'center', 'border-style': 'none'}))
order <= ht.TR(ht.TD('出发地') + departure + ht.A(station[departure.value], id='dep_station')
               + ht.TD('互换', id='switch', rowspan=2))
order <= ht.TR(ht.TD('到达地') + arrival + ht.A(station[arrival.value], id='arr_station'))
order <= ht.TR(ht.TD('物品体积') + ht.INPUT(id='volume') + ht.TD('m³'))
order <= ht.TR(ht.TD('保证金') + ht.INPUT(id='collateral') + ht.TD('ISK'))
order <= ht.TR(ht.TD('合同类型') + ht.INPUT(id='contract'))
order <= ht.TR(ht.TD('收费标准', rowspan=2) + ht.A(ht.TD('当前线路价格') + ht.TH('250 ISK/m³', id='route_standard') + ht.TD('下行', id='stream')))
order <= ht.TR(ht.A(ht.TD('额外计费方式') + ht.TH('-', id='other_fee')))
order <= ht.TR(ht.TD('支付运费') + ht.TH('-', id='cost', style={'text-align': 'center', 'border': 'solid'}) + ht.TD('ISK'))
# , 'font-family': 'Palatino Linotype'
# order <= ht.TR(ht.DIV('0', id='change'))

# calc <= (ht.TR(ht.TD(x) for x in line) for line in lines)

document <= order

# change = document['change']
cost = document['cost']
route_standard = document['route_standard']
add_fee = document['other_fee']

lowest_fee = 5000000


# Generate available destinations depending on departure
def arr_option_change():
    document['dep_station'].text = station[departure.value]
    ava_des = list(route[departure.value].keys())  # Available destinations

    diff = abs(len(ava_des) - len(arrival.options))
    now_opt = len(arrival.options)

    # Make the length of option list and new option list the same
    if now_opt < len(ava_des):
        for i in range(diff):
            arrival.options.add(ht.OPTION(''))

    if now_opt > len(ava_des):
        for i in range(diff):
            arrival.options.remove('0')

    # Change every elements in the option list
    for i in range(len(ava_des)):
        arrival.options[i] = ht.OPTION(ava_des[i])

    return ava_des


def dep_select(event):
    arr_option_change()
    document['arr_station'].text = station[arrival.value]

    fee_regulation()


def arr_select(event):
    document['arr_station'].text = station[arrival.value]

    fee_regulation()


def switch_des(event):
    current_dep, current_arr = departure.value, arrival.value
    arr_in_dep = list(route.keys()).index(current_arr)  # Index of current arrival in departure option list
    departure.options[arr_in_dep].selected = True

    new_arr_opt = arr_option_change()  # Check available destinations after switch

    new_arr_idx = list(new_arr_opt).index(current_dep)  # Index of the original departure in new arrival option list
    arrival.options[new_arr_idx].selected = True  # Select original departure

    document['arr_station'].text = station[arrival.value]

    fee_regulation()


def route_fee():
    dep, arr = departure.value, arrival.value
    basic_fee = route[dep][arr]
    upstream = True if arr == 'Jita' else False  # Upstream route or downstream
    return basic_fee, upstream


def fee_regulation():
    volume_input = document['volume'].value
    collateral_input = document['collateral'].value

    # Route fee
    basic_fee, upstream = route_fee()
    route_standard.text = f'{basic_fee} ISK/m³'
    if upstream:
        route_standard.text += ' + 2%保证金'
        document['stream'].text = '上行'
    else:
        document['stream'].text = '下行'

    # Check null input
    if volume_input != '':
        volume_cost = int(volume_input.replace(',', '')) * basic_fee
    else:
        volume_cost = 0
    if collateral_input != '':
        collateral_cost = int(collateral_input.replace(',', '')) * 0.01
    else:
        collateral_cost = 0

    # if
    if collateral_cost == 0 and volume_cost == 0:
        cost.text = '-'
        add_fee.text = '-'
    else:
        if not upstream:  # Downstream route
            if collateral_cost > volume_cost:
                result = collateral_cost
                adopt_standard = '1%保证金'
            else:
                result = volume_cost
                adopt_standard = '-'
        else:  # Upstream route
            result = volume_cost + 2 * collateral_cost
            adopt_standard = '-'

        if result < lowest_fee:  # Check lowest delivery fee
            adopt_standard = f'运费不足5百万ISK按5百万ISK收取 (当前为{format(round(result, 2), ",")} ISK)'
            result = lowest_fee

        cost.text = format(int(result), ',')
        add_fee.text = adopt_standard

    return basic_fee, upstream


def volume_fee(event):
    volume_input = document['volume'].value

    # fee, up_route = route_fee()
    if volume_input != '':
        volume_number = int(document['volume'].value.replace(',', ''))

        vol_limit = 340000
        if volume_number > vol_limit:
            document['volume'].value = format(vol_limit, ',')
            volume_number = vol_limit
        else:
            document['volume'].value = format(volume_number, ',')

    fee_regulation()  # Check if


def collateral_fee(event):
    fee_regulation()

    if document['collateral'] != '':
        collateral_number = int(document['collateral'].value.replace(',', ''))
        document['collateral'].value = format(collateral_number, ',')


departure.bind('change', dep_select)
arrival.bind('change', arr_select)
document['switch'].bind('click', switch_des)
document['collateral'].bind('keyup', collateral_fee)
document['volume'].bind('keyup', volume_fee)
