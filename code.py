from browser import document
import browser.html as ht

# calc = ht.TABLE()
# calc <= ht.TR(ht.TH(ht.DIV("0", id="result"), colspan=3) + ht.TD("C"))
#
# document <= calc

order = ht.TABLE(id='table')
# fill = ht.TD(style={'width': '100%'})
# fill = ht.TD()
order <= ht.TR(ht.TH("凛冬联盟顺丰快递费用计算器", colspan=5, style={'text-align': 'center', 'border-style': 'none'}))
order <= ht.TR(ht.TD('出发地') + ht.INPUT(value='Jita', id='dep') + ht.TD('互换', id='switch', rowspan=2))
order <= ht.TR(ht.TD('到达地') + ht.INPUT(value='4-HWWF', id='des'))
order <= ht.TR(ht.TD('物品体积') + ht.INPUT(id='volume'))
order <= ht.TR(ht.TD('保证金') + ht.INPUT(id='collateral'))
order <= ht.TR(ht.TD('合同类型') + ht.INPUT(id='contract'))
order <= ht.TR(ht.TD('支付运费') + ht.TH('-', id='cost'))
order <= ht.TR(ht.TD('收费标准') + ht.TH('-', id='standard'))
# order <= ht.TR(ht.DIV('0', id='change'))

# calc <= (ht.TR(ht.TD(x) for x in line) for line in lines)

document <= order


# change = document['change']
cost = document['cost']
standard = document['standard']


fee = 250
lowest_fee = 5000000


def volume_fee(event):
    volume_input = document['volume'].value
    if volume_input != '':
        volume_number = int(document['volume'].value.replace(',', ''))

        vol_limit = 340000
        if volume_number > vol_limit:
            document['volume'].value = format(vol_limit, ',')
            volume_number = vol_limit
        else:
            document['volume'].value = format(volume_number, ',')

        cost.text = format(volume_number * fee, ',') + " isk"
    check_cost()


def switch_des(event):
    document['dep'].value, document['des'].value = document['des'].value, document['dep'].value


def check_cost():
    volume_input = document['volume'].value
    collateral_input = document['collateral'].value

    if volume_input != '':
        volume_cost = int(volume_input.replace(',', '')) * 250
    else:
        volume_cost = 0
    if collateral_input != '':
        collateral_cost = int(collateral_input.replace(',', '')) * 0.01
    else:
        collateral_cost = 0

    if collateral_cost == 0 and volume_cost == 0:
        cost.text = '-'
        standard.text = '-'
    else:
        if collateral_cost > volume_cost:
            result = collateral_cost
            adopt_standard = '保证金1%'
        else:
            result = volume_cost
            adopt_standard = f'{fee} ISK/m³'

        if result < lowest_fee:  # Check lowest delivery fee
            adopt_standard = f'运费不足5百万ISK按5百万ISK收取 (当前为{format(round(result, 2), ",")} ISK)'
            result = lowest_fee

        cost.text = format(round(result, 2), ',') + " ISK"
        standard.text = adopt_standard


def collateral_fee(event):
    check_cost()

    if document['collateral'] != '':
        collateral_number = int(document['collateral'].value.replace(',', ''))
        document['collateral'].value = format(collateral_number, ',')


document['switch'].bind('click', switch_des)
document['collateral'].bind('keyup', collateral_fee)
document['volume'].bind('keyup', volume_fee)



