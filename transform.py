from typing import Tuple

import pandas as pd


def create_dataframes(data: dict) -> Tuple[pd.DataFrame, pd.DataFrame]:
    bids, asks = data['bids'], data['asks']

    bid_df = pd.DataFrame(data=bids, columns=['price', 'volume'])
    ask_df = pd.DataFrame(data=asks, columns=['price', 'volume'])

    bid_df = bid_df.astype({'price': 'float64', 'volume': 'float64'})
    ask_df = ask_df.astype({'price': 'float64', 'volume': 'float64'})

    return bid_df, ask_df


def get_current_price(bids, asks) -> float:
    return (bids.iloc[0]['price'] + asks.iloc[0]['price']) / 2


def calculate_volume(bids, asks, current_price):
    # Calculate prices at +2% and -2% from the current price
    price_2_percent_above = current_price * 1.02
    price_2_percent_below = current_price * 0.98

    # Filter orders within +2% and -2% from the current price
    bid_orders_within_range = bids[
        (bids['price'] >= price_2_percent_below) & (bids['price'] <= price_2_percent_above)]
    ask_orders_within_range = asks[
        (asks['price'] >= price_2_percent_below) & (asks['price'] <= price_2_percent_above)]

    volume = bid_orders_within_range['volume'].sum() + ask_orders_within_range['volume'].sum()

    return volume
