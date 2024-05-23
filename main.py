import pandas as pd
import yfinance as yf

# Add user input for selecting multiple tickers
# Add user input for deciding call/put display
# Add user input for weeks out

def option_brief(option, cp: int):
    """
    Grabs relevant information for options
    :param option: "call" or "put"
    :return: filtered dataframe copy from main dataframe
    """
    filtered_indices = option.index[option['strike'] == cp].tolist()

    surrounding_indices = []
    for idx in filtered_indices:
        for i in range(-3, 4):  # Range from -3 to 3
            if 0 <= idx + i < len(option):
                surrounding_indices.append(idx + i)

    surrounding_indices = sorted(set(surrounding_indices))
    filtered_df = option.iloc[surrounding_indices]
    return filtered_df.copy()


def option_seeker(tick: str, weeks: int, option: str):
    f"""
    Looks at current price of strike price options +/- 3 from current price, for {weeks}, on desired {option}
    :param weeks: number of weeks seeking data
    :param option: "call" or "put"
    :return: appended dataframe of option, by weeks, in range of +/- 3 of current price
    """
    ticker = yf.Ticker(tick)
    current_price = int(ticker.info['currentPrice'])


    master_df = None
    op = None

    option_filter = ['strike', 'bid', 'lastPrice', 'ask', 'contractSymbol']

    for day in range(weeks):
        select_day = ticker.options[day]
        counter = day + 1

        if option == "call":
            op = ticker.option_chain(select_day).calls
        if option == "put":
            op = ticker.option_chain(select_day).puts

        filter_call = op[option_filter]

        filtered_options_df = option_brief(filter_call, current_price)

        value_list = []
        value_per_weeks = []

        for i in filtered_options_df['lastPrice']:
            value = (i * 100) / (counter * 5)
            value_per_weeks.append(round(value))

            value2 = (i * 100)
            value_list.append(round(value2))

        filtered_options_df.loc[:, 'Value'] = value_list
        filtered_options_df.loc[:, 'ValuePerweeks'] = value_per_weeks

        # Concatenate the filtered and computed DataFrame to the master DataFrame
        if not filtered_options_df.empty:
            master_df = pd.concat([master_df, filtered_options_df], ignore_index=True)

    return master_df

stocks = ["ARM", "F"]

for stock in stocks:
    print(f"Looking at {stock}")
    print(option_seeker(stock, 3, "put"))
    print("*"*10)
