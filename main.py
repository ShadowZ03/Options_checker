import pandas as pd
import yfinance as yf

# Add user input for selecting multiple tickers
# Add user input for deciding call/put display
# Add user input for weeks out

ticker = yf.Ticker("ARM")
current_price = ticker.info['currentPrice']


def option_brief(option):
    """
    Grabs relevant information for options
    :param option: "call" or "put"
    :return: filtered dataframe copy from main dataframe
    """
    filtered_indices = option.index[option['strike'] == int(current_price)].tolist()

    surrounding_indices = []
    for idx in filtered_indices:
        for i in range(-3, 4):  # Range from -3 to 3
            if 0 <= idx + i < len(option):
                surrounding_indices.append(idx + i)

    surrounding_indices = sorted(set(surrounding_indices))
    filtered_df = option.iloc[surrounding_indices]
    return filtered_df.copy()


def option_seeker(weeks: int, option: str):
    f"""
    Looks at current price of strike price options +/- 3 from current price, for {weeks}, on desired {option}
    :param weeks: number of weeks seeking data
    :param option: "call" or "put"
    :return: appended dataframe of option, by weeks, in range of +/- 3 of current price
    """
    master_df = None
    op = None

    option_filter = ['strike', 'bid', 'lastPrice', 'ask', 'contractSymbol']

    for date in range(weeks):
        select_date = ticker.options[date]
        counter = date + 1  # Start counter from 1

        if option == "call":
            op = ticker.option_chain(select_date).calls
        if option == "put":
            op = ticker.option_chain(select_date).puts

        filter_call = op[option_filter]

        x = option_brief(filter_call)

        value_list = []
        value_per_weeks = []

        for i in x['bid']:
            value = (i * 100) / (counter * 5)
            value_per_weeks.append(round(value))

            value2 = (i * 100)
            value_list.append(round(value2))

        x.loc[:, 'Value'] = value_list
        x.loc[:, 'ValuePerweeks'] = value_per_weeks

        # Concatenate the filtered and computed DataFrame to the master DataFrame
        if not x.empty:
            master_df = pd.concat([master_df, x], ignore_index=True)

    return master_df

print(option_seeker(3, "call"))
