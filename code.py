from browser import document, alert, window, ajax
import browser.html as ht

route = {'Jita': {'4-HWWF': [350, False, 5],
                  'Otsasai': [250, False, 5],
                  '5ZXX-K': [600, False, 5],
                  'N5Y': [800, False, 25],
                  'BKG': [950, False, 50]},
         '4-HWWF': {'Jita': [300, True, 10]},
         'Otsasai': {'Jita': [300, True, 10]},
         '5ZXX-K': {'Jita': [300, True, 10]},
         'N5Y': {'Jita': [500, True, 25]},
         'BKG': {'Jita': [700, True, 50]}
         }  # [Route fee, upstream, minimum fee]

station = {'Jita': 'IV - Moon 4 - Caldari Navy Assembly Plant',
           '4-HWWF': 'WinterCo. Central Station',
           'RF-X7V': 'Forums.WinTerCo.org',
           'Otsasai': 'Fuxi Prime - Home for Ever',
           'N5Y-4N': 'xingcheng',
           'K3JR-J': "Teski's home",
           'Oijanen': 'Lowsec jita',
           '5ZXX-K': 'Northern Protectorate Palace',
           'N5Y': '',
           'BKG': ''}

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
order <= ht.TR(ht.TH("凛冬联盟顺丰快递费用计算器", colspan=6, Class='title'))
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
                     colspan=2, style={'padding': '0px 0px 0px 0px', 'background-color': 'transparent'})
               # + ht.TD('')
               )
order <= ht.TR(ht.TD('收费标准', rowspan=3) +
               ht.A(ht.TD('当前线路价格', style={'padding': '15px 5px 15px 5px', 'width': '177px'}) +
                    ht.TH(f'{route[departure.value][arrival.value][0]} ISK/m' + ht.SUP('3'), id='route_standard',
                          style={'width': f'{input_width - 187 - 60 - 4}px'}),
                    Class='charging_rule_A') +
               ht.TD('下行线路', id='stream', rowspan=3, style={'width': '60px', 'background-color': maolv}))
order <= ht.TR(ht.A(ht.TD('线路最低费用', style={'padding': '15px 5px 15px 5px', 'width': '177px'}) +
                    ht.TH('10M ISK (10,000,000 ISK)', id='min_fee',
                          style={'width': f'{input_width - 187 - 60 - 4}px'}),
                    Class='charging_rule_A'))
order <= ht.TR(ht.A(ht.TD('计费标准', style={'padding': '15px 5px 15px 5px', 'width': '177px', 'height': '65px'}) +
                    ht.TH('-', id='other_fee',
                          style={'width': f'{input_width - 187 - 60 - 4}px',
                                 'line-height': '1.3',
                                 'white-space': 'pre-line'}),
                    Class='charging_rule_A'))
order <= ht.TR(ht.TD('送达时间') + ht.TH('2天内', id='express_time', Class='time') +
               ht.TD('主线路', id='route_tag', Class='route_tag'))
order <= ht.TR(ht.TD('支付运费', Class='important') +
               ht.TH('-', id='cost', style={'text-align': 'center', 'border': 'solid', 'color': qianghong}) +
               ht.TD('ISK', Class='important'))
# order <= ht.TR(ht.TD('', Class='placeholder_cell') + ht.TD('查看合同样本', id='contract_preview'))
order <= ht.TR(ht.TD('test', id='test') + ht.TD('send', id='send'))
pop = ht.DIV('yy', role='alert')

# document <= order
# table_margin_top = int(window.getComputedStyle(document["table"]).marginTop.replace('px', ''))
# background = ht.DIV('', Class='shadow',
#                     style={'margin-top': f'-{document["table"].offsetHeight + table_margin_top}px'})
# document <= background

background = ht.DIV('', id='order_form', Class='shadow')
background <= order

background <= ht.TD('查看合同样本 (暂不可用)', id='contract_preview',
                    style={'display': 'table',
                           'position': 'relative',
                           'top': '80px',
                           'margin': '0 auto',
                           'background-color': tanxiang})
# background <= ht.DIV('xx1xxxxxxxxxxxx1', style={'position': 'relative', 'top': '40px'})

document <= background

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
movement = False

alert_position = 0
collateral_full = ''
m = 1e6  # 1 million
animation_time = 2


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


def layout_change(event):
    global movement
    table_margin_left = float(window.getComputedStyle(document['order_form']).marginLeft.replace('px', ''))
    print(table_margin_left)
    if movement:  # Move back to center position
        # document['order_form'].style.transform = 'translateX(0)'
        document['order_form'].style.marginLeft = 'calc(50% - 540px)'
        movement = False
    else:
        # document['order_form'].style.transform = f'translateX(-{table_margin_left - 30}px)'
        document['order_form'].style.marginLeft = '25px'
        movement = True


def test_connection(ev):
    ajax.get("http://127.0.0.1:5000/?read=true", oncomplete=print_out)


def print_out(req):
    preference = req.text
    print('ajax:', preference)
    # print(preference["Me"])
    print('helloWorld')


def send_file(ev):
    # json_str = f'{{"{departure.value}": "{document["volume"].value}"}}'
    # json_str_2 = f'{{"Me": "22:00", "Peter": "23:00"}}'
    # print(json_str)

    # file = ajax.Ajax()
    # file.bind('complete', print_out)
    # file.open('POST', 'http://127.0.0.1:5000/update', True)
    # # file.set_header('content-type', 'application/x-www-form-urlencoded')
    # # file.set_header('Access-Control-Allow-Origin', '*')
    # file.send({'your_name': 'Piyush', 'company_name': 'Geeks'})

    send_data = {'name': f'{departure.value}'}
    # send_data = json.dumps(send_data)
    ajax.post('http://127.0.0.1:5000/update', data=send_data)

    # ajax.get("http://127.0.0.1:5000/?read=true", mode='json', oncomplete=print_out)


departure.bind('change', dep_select)
arrival.bind('change', arr_select)
document['switch'].bind('click', switch_des)
document['collateral'].bind('keyup', collateral_fee)
document['volume'].bind('keyup', volume_fee)
# document['s_contract'].bind('click', standard_courier)
# document['a_contract'].bind('click', accelerated_courier)
# document['contract_preview'].bind('click', layout_change)
document['test'].bind('click', test_connection)
document['send'].bind('click', send_file)
