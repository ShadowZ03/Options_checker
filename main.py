import pandas as pd
import yfinance as yf
import mailer
import time
from datetime import datetime, timedelta
import const
import holidays

debug = const.debug


def is_business_day():
    today = datetime.now().date()
    return today.weekday() < 5 and today not in holidays.country_holidays('US')


class seeker:
    def __init__(self, stock):
        self.stockTicker = stock.upper()
        self.yhTicker = yf.Ticker(self.stockTicker)

    def option_brief(self, option, cp: int):
        """
        Grabs relevant information for options
        :param option: "call" or "put"
        :return: filtered dataframe copy from main dataframe v
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

    def option_seeker(self, weeks: int, option: str):
        f"""
        Looks at current price of strike price options +/- 3 from current price, for {weeks}, on desired {option}
        :param weeks: number of weeks seeking data
        :param option: "call" or "put"
        :return: appended dataframe of option, by weeks, in range of +/- 3 of current price
        """

        current_price = int(self.yhTicker.info['currentPrice'])

        master_df = None
        op = None

        option_filter = ['strike', 'bid', 'lastPrice', 'ask', 'contractSymbol']

        for day in range(weeks):
            select_day = self.yhTicker.options[day]
            counter = day + 1

            if option == "call":
                op = self.yhTicker.option_chain(select_day).calls
            if option == "put":
                op = self.yhTicker.option_chain(select_day).puts

            filter_call = op[option_filter]

            filtered_options_df = self.option_brief(filter_call, current_price)

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
            if debug:
                print(master_df)

            # articles = news_seeker(tick)
        return master_df

    def news_seeker(self, yhfTick) -> str:
        """
        Function to grab news for a designated ticker
        :param tick: stock ticker
        :return: string of Title and link for that article
        """

        news_yf = yhfTick.news
        links = ""

        for article in news_yf:
            if self.stockTicker in article["title"].upper():
                links = f"{links}" + f"{article['title']}" + "\n"
                links = f"{links}" + f"{article['link']}" + "\n" + "\n"

        if debug:
            print(links)

        return links

    def wait_until_start(self, start_time):
        now = datetime.now()
        start_dt = datetime.combine(now.date(), start_time)

        # If start time is before the current time, start the next day
        if start_dt < now:
            start_dt += timedelta(days=1)

        wait_seconds = (start_dt - now).total_seconds()
        print(f"Waiting for {wait_seconds} seconds until start time...")
        time.sleep(wait_seconds)

    def scheduler(self):
        # for stock in stocks:
        print(f"Looking at: {self.yhTicker.info['symbol']}")
        print("*" * 10)

        print(f"Generating Email for: {self.yhTicker.info['symbol']}")
        subject = f"OPTIONS BRIEF - {self.yhTicker.info['symbol']}"
        body = f"""This is a test email sent from Python.\n 
                            ***** Call *****
                        {self.option_seeker(3, "call").to_string()}
                        \n
                            ***** Put *****
                        {self.option_seeker(3, "put").to_string()}
                        \n

                           **** NEWS ****
                        {self.news_seeker(self.yhTicker)}
                        """
        to_email = const.gmail_email  # Replace with recipient's email

        mailer.send_email(subject, body, to_email)


if __name__ == "__main__":

    list = ["ARM", "F"]
    if is_business_day():
        i = 0
        while i <= 5:

            for l in list:
                x = seeker(l)
                x.scheduler()
            time.sleep(60 * 60)  # Run the job every hour
        else:
            print("Today is a holiday or weekend, skipping job.")
            subject = f"Not Working Day"
            body = "This is a test email sent from Python."
            to_email = const.gmail_email  # Replace with recipient's email
            mailer.send_email(subject, body, to_email)
