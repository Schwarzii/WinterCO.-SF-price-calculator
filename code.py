from browser import document, alert
import browser.html as ht

route = {'Jita': {'4-HWWF': [350, False, 10], 'Otsasai': [250, False, 25], 'K3JR-J': [650, False, 25], 'Oijanen': [500, False, 25]},
         '4-HWWF': {'Jita': [350, True, 10], 'Otsasai': [250, False, 25], 'Oijanen': [125, False, 25]},
         'Otsasai': {'Jita': [250, True, 25], '4-HWWF': [250, True, 25]},
         'K3JR-J': {'Jita': [650, True, 25]},
         'Oijanen': {'Jita': [700, True, 25], '4-HWWF': [125, True, 25]}
         }  # [Route fee, upstream, minimum fee]

station = {'Jita': 'IV - Moon 4 - Caldari Navy Assembly Plant',
           '4-HWWF': 'WinterCo. Central Station',
           'RF-X7V': 'Forums.WinTerCo.org',
           'Otsasai': 'Fuxi Prime - Home for Ever',
           'N5Y-4N': 'xingcheng',
           'K3JR-J': "Teski's home",
           'Oijanen': 'Lowsec jita'}

# Global colors
honghui = '#82878c'  # 红灰
maolv = '#155461'  # 毛绿
cuilv = '#006e5f'  # 翠绿
tanxiang = '#dc943b'  # 檀香色
zhubiao = '#e35c3e'  # 朱磦
zaohong = '#89303f'  # 枣红
qianghong = '#902A1B'  # 墙红，从故宫照片提取
default_color = '#282e55'

order = ht.TABLE(id='table')
input_width = 690 + 60 + 4

departure = ht.SELECT(ht.OPTION(station) for station in route.keys())
arrival = ht.SELECT(ht.OPTION(station) for station in route['Jita'].keys())

order <= ht.TR(ht.TH("凛冬联盟顺丰快递费用计算器", colspan=6, style={'text-align': 'center', 'border-style': 'none'}))
order <= ht.TR(ht.TD('出发地') + departure + ht.A(station[departure.value], id='dep_station')
               + ht.TD('互换', id='switch', rowspan=2, style={'background-color': tanxiang}))
order <= ht.TR(ht.TD('到达地') + arrival + ht.A(station[arrival.value], id='arr_station'))
order <= ht.TR(ht.TD('物品体积') +
               ht.INPUT(id='volume') +
               ht.TD('m' + ht.SUP('3', Class='sup_white'), style={'padding': '10px 30px 10px 30px'}))
order <= ht.TR(ht.TD('保证金') + ht.INPUT(id='collateral', maxlength=18) + ht.TD('ISK'))
order <= ht.TR(ht.TD('合同类型') +
               ht.TD(ht.TD('标准合同', id='s_contract',
                           style={'width': f'{input_width / 2- 60 - 1}px', 'background-color': maolv}) +
                     ht.TD('加急合同 (接单24小时内运达)', id='a_contract',
                           style={'width': f'{input_width / 2 + 120 - 60 - 1}px',
                                  'position': 'relative',
                                  'right': '-2px',
                                  'padding': '10px 30px 10px 30px',
                                  'background-color': honghui}),
                     colspan=2, style={'padding': '0px 0px 0px 0px', 'background-color': 'unset'})
               # + ht.TD('')
               )
order <= ht.TR(ht.TD('收费标准', rowspan=3) +
               ht.A(ht.TD('当前线路价格', style={'padding': '15px 5px 15px 5px', 'width': '177px'}) +
                    ht.TH('250 ISK/m' + ht.SUP('3'), id='route_standard',
                          style={'width': f'{input_width - 187 - 60 - 4}px'}),
                    Class='charging_rule_A') +
               ht.TD('下行线路', id='stream', rowspan=3, style={'width': '60px', 'background-color': maolv}))
order <= ht.TR(ht.A(ht.TD('线路起步价', style={'padding': '15px 5px 15px 5px', 'width': '177px'}) +
                    ht.TH('10M ISK (10,000,000 ISK)', id='min_fee',
                          style={'width': f'{input_width - 187 - 60 - 4}px'}),
                    Class='charging_rule_A'))
order <= ht.TR(ht.A(ht.TD('计费标准', style={'padding': '15px 5px 15px 5px', 'width': '177px', 'height': '68px'}) +
                    ht.TH('-', id='other_fee',
                          style={'width': f'{input_width - 187 - 60 - 4}px',
                                 'line-height': '1.3',
                                 'white-space': 'pre-line'}),
                    Class='charging_rule_A'))
order <= ht.TR(ht.TD('送达时间') + ht.TH('2天', id='express_time', Class='time') +
               ht.TD('主线路', id='route_tag', Class='route'))
order <= ht.TR(ht.TD('支付运费', Class='important') +
               ht.TH('-', id='cost', style={'text-align': 'center', 'border': 'solid', 'color': qianghong}) +
               ht.TD('ISK', Class='important'))
# , 'font-family': 'Palatino Linotype'
pop = ht.DIV('yy', role='alert')

document <= order

# Global elements
cost = document['cost']
route_standard = document['route_standard']
add_fee = document['other_fee']
route_tag = document['route_tag']
express_time = document['express_time']

# Global variables
selected_color = maolv
unselected_color = honghui
highlight_color = qianghong

accelerated = False
upstream = False

alert_position = 0
collateral_full = ''
m = 1e6  # 1 million


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


# Choose a departure station
def dep_select(event):
    arr_option_change()
    document['arr_station'].text = station[arrival.value]

    fee_regulation()
    accelerated_availability()


# Choose a destination station
def arr_select(event):
    document['arr_station'].text = station[arrival.value]

    fee_regulation()
    accelerated_availability()


# Switch between the chosen departure station and destination station
def switch_des(event):

    current_dep, current_arr = departure.value, arrival.value
    arr_in_dep = list(route.keys()).index(current_arr)  # Index of current arrival in departure option list
    departure.options[arr_in_dep].selected = True

    new_arr_opt = arr_option_change()  # Check available destinations after switch

    new_arr_idx = list(new_arr_opt).index(current_dep)  # Index of the original departure in new arrival option list
    arrival.options[new_arr_idx].selected = True  # Select original departure

    document['arr_station'].text = station[arrival.value]

    fee_regulation()
    accelerated_availability()


# Calculate required unit fee defined by routes
def route_fee():
    global upstream  # Change global upstream status and category of route
    dep, arr = departure.value, arrival.value
    basic_fee, upstream, minimum_fee_coe = route[dep][arr]

    if dep == 'Jita' and arr == '4-HWWF':
        route_tag.text = '主线路'
        express_time.text = '2天内'
    else:
        route_tag.text = '常规线'
        express_time.text = '7天内'
    if accelerated:
        express_time.text = '1天内 (加急合同)'
        express_time.style.color = highlight_color
        express_time.style.borderColor = highlight_color
    else:
        express_time.style.color = default_color
        express_time.style.borderColor = maolv
    return basic_fee, minimum_fee_coe


# Calculation total fee needed to charge
def fee_regulation():
    volume_input = document['volume'].value
    collateral_input = document['collateral'].value

    # Route fee
    basic_fee, minimum_fee_coe = route_fee()
    route_standard.text = f'{basic_fee} ISK/m'
    route_standard.appendChild(ht.SUP('3'))

    if upstream:
        route_standard.insertAdjacentText('beforeend', ' + 1%保证金 (仅保证金 > 5B时)')
        document['stream'].text = '上行线路'
    else:
        document['stream'].text = '下行线路'

    document['min_fee'].text = f'{minimum_fee_coe}M ISK ({format(int(minimum_fee_coe * m), ",")} ISK)'

    # Check null input
    if volume_input != '':
        volume_input = float(volume_input.replace(',', ''))  # Change type of volume input to float
        # Redefine volume input for accelerated contract
        if accelerated:
            if volume_input <= 150000:
                volume_input = 150000
            elif 150000 < volume_input <= 250000:
                volume_input = 250000
            else:
                volume_input = 340000
        volume_cost = volume_input * basic_fee
    else:
        volume_cost = 0
    if collateral_input != '':
        collateral_cost = float(collateral_input.replace(',', '')) * 0.01
    else:
        collateral_cost = 0

    # Calculate total fee
    if collateral_cost == 0 and volume_cost == 0:
        cost.text = '-'
        add_fee.text = '-'
    else:
        if not upstream:  # Downstream route
            if collateral_cost > volume_cost:  # If high collateral applicable
                result = collateral_cost
                adopt_standard = '1%保证金'
            else:
                result = volume_cost
                adopt_standard = '线路计费'
        else:  # Upstream route
            if collateral_cost > 5e7:  # Check if collateral is taken into account
                result = volume_cost + collateral_cost
                adopt_standard = '线路计费 (加收保证金)'
            else:
                result = volume_cost
                adopt_standard = '线路计费 (不加收保证金)'

        # Check lowest delivery fee
        if result < minimum_fee_coe * m:
            adopt_standard = f'未达到线路起步价按起步价收取 \n(当前为{format(int(result), ",")} ISK)'
            result = minimum_fee_coe * m

        # Display result and charging rule
        cost.text = format(int(result), ',')
        if not accelerated:
            add_fee.text = adopt_standard
        else:
            if adopt_standard == '1%保证金':
                priority = '优先计费：1%保证金 \n'
            else:
                priority = ''
            add_fee.text = priority + f'加急合同 ({format(volume_input, ",")} m'
            add_fee.appendChild(ht.SUP('3'))
            add_fee.insertAdjacentText('beforeend', ' 标准体积运费)')


# Split input number to integer part and decimals part
def split_decimal(str_input):
    number_str = str_input.split('.')
    if len(number_str) == 2:
        integer, decimals = number_str[0], '.' + number_str[1]
    else:
        integer = str_input
        decimals = ''
    return integer, decimals


# Enter a volume
def volume_fee(event):
    volume_input = document['volume'].value
    cursor = document['volume'].selectionStart  # Get cursor position
    input_len = len(volume_input)

    if volume_input != '':
        integer, decimals = split_decimal(volume_input)
        volume_number = int(integer.replace(',', ''))

        # Check package volume upper limit
        vol_limit = 340000
        if volume_number >= vol_limit:
            document['volume'].value = format(vol_limit, ',')
        else:
            document['volume'].value = format(volume_number, ',') + decimals
            # Compensation for adding or deleting comma
            if len(document['volume'].value) > input_len:
                cursor += 1
            elif len(document['volume'].value) < input_len and cursor > 0:
                cursor -= 1
            # Move cursor to the last typing position
            document['volume'].selectionStart = cursor
            document['volume'].selectionEnd = cursor

    fee_regulation()


# Enter a collateral
def collateral_fee(event):
    global collateral_full
    collateral_input = document['collateral'].value
    if len(collateral_input.replace(',', '').replace('.', '')) <= 14:  # Limit maximum amount of input digits to 14
        cursor = document['collateral'].selectionStart  # Get cursor position
        input_len = len(collateral_input)

        fee_regulation()

        if collateral_input != '':
            integer, decimals = split_decimal(collateral_input)
            collateral_number = int(integer.replace(',', ''))
            document['collateral'].value = format(collateral_number, ',') + decimals
            collateral_full = document['collateral'].value
            # Compensation for adding or deleting comma
            if len(document['collateral'].value) > input_len:
                cursor += 1
            elif len(document['collateral'].value) < input_len and cursor > 0:
                cursor -= 1
            # Move cursor to the last typing position
            document['collateral'].selectionStart = cursor
            document['collateral'].selectionEnd = cursor
    else:  # Rollback to last input
        document['collateral'].value = collateral_full


# Select standard contract as contract type
def select_standard():
    global accelerated
    document['s_contract'].style.backgroundColor = selected_color
    document['a_contract'].style.backgroundColor = unselected_color
    accelerated = False

    fee_regulation()


# Select accelerated contract as contract type
def select_accelerated():
    global accelerated
    document['s_contract'].style.backgroundColor = unselected_color
    document['a_contract'].style.backgroundColor = highlight_color
    accelerated = True

    fee_regulation()


# Check upstream
def accelerated_availability():
    if upstream:  # Deactivate accelerated contract option
        select_standard()
        document['a_contract'].text = '上行线路不可选加急合同'
    else:
        document['a_contract'].text = '加急合同 (接单24小时内运达)'


# Choose standard contract type
def standard_courier(event):
    select_standard()


# Choose accelerated contract type
def accelerated_courier(event):
    if not upstream:
        select_accelerated()


departure.bind('change', dep_select)
arrival.bind('change', arr_select)
document['switch'].bind('click', switch_des)
document['collateral'].bind('keyup', collateral_fee)
document['volume'].bind('keyup', volume_fee)
document['s_contract'].bind('click', standard_courier)
document['a_contract'].bind('click', accelerated_courier)
