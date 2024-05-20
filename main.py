import pandas
import yfinance as yf

# add user input for selecting multiple tickers
# add user input for deciding call/put display
# add user input for days out

ticker = yf.Ticker("ARM")
current_price = ticker.info['currentPrice']

def option_brief(option: pandas.DataFrame):
    filtered_indices = option.index[option['strike'] == int(current_price)].tolist()

    surrounding_indices = []
    for idx in filtered_indices:
        for i in range(-4, 5):  # Range from -3 to 3
            if 0 <= idx + i < len(option):
                surrounding_indices.append(idx + i)

    surrounding_indices = sorted(set(surrounding_indices))
    filtered_df = option.iloc[surrounding_indices]
    return filtered_df

for date in range(3):

    select_date = ticker.options[date]
    counter = 0
    counter +=1

    call = ticker.option_chain(select_date)[0]
    put = ticker.option_chain(select_date)[1]

    option_filter = ['strike', 'bid', 'lastPrice', 'ask', 'contractSymbol']
    # column names
    # print(put.columns)

    filter_put = put[option_filter]
    filter_call = call[option_filter]

    x = option_brief(filter_call).copy()

    value_list = []
    value_by_days = []

    for i in x['bid']:
        value = (i*100)/(counter*5)
        value_by_days.append(round(value))

        value2 = (i * 100)
        value_list.append(round(value2))

    x.loc[:, 'Value'] = value_list
    x.loc[:, 'ValueByDays'] = value_by_days

    print(x)
