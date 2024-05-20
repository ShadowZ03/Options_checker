import pandas as pd
import yfinance as yf

# Add user input for selecting multiple tickers
# Add user input for deciding call/put display
# Add user input for days out

ticker = yf.Ticker("ARM")
current_price = ticker.info['currentPrice']


def option_brief(option):
    filtered_indices = option.index[option['strike'] == int(current_price)].tolist()

    surrounding_indices = []
    for idx in filtered_indices:
        for i in range(-3, 4):  # Range from -3 to 3
            if 0 <= idx + i < len(option):
                surrounding_indices.append(idx + i)

    surrounding_indices = sorted(set(surrounding_indices))
    filtered_df = option.iloc[surrounding_indices]
    return filtered_df


def option_seeker(days: int, option: str):
    master_df = None
    op = None

    option_filter = ['strike', 'bid', 'lastPrice', 'ask', 'contractSymbol']

    for date in range(days):
        select_date = ticker.options[date]
        counter = date + 1  # Start counter from 1

        if option == "call":
            op = ticker.option_chain(select_date).calls
        if option == "put":
            op = ticker.option_chain(select_date).puts

        filter_call = op[option_filter]

        x = option_brief(filter_call).copy()

        value_list = []
        value_per_days = []

        for i in x['bid']:
            value = (i * 100) / (counter * 5)
            value_per_days.append(round(value))

            value2 = (i * 100)
            value_list.append(round(value2))

        x.loc[:, 'Value'] = value_list
        x.loc[:, 'ValuePerDays'] = value_per_days

        # Concatenate the filtered and computed DataFrame to the master DataFrame
        if not x.empty:
            master_df = pd.concat([master_df, x], ignore_index=True)

    return master_df


print(option_seeker(3, "call"))
