import asyncio

import pandas as pd
import websockets
import json

from config import CONFIG
from telegram import bot
from transform import create_dataframes, get_current_price, calculate_volume
from db.functions import save_data, calculate_weighted_average
from db.tables import OrderBookDB


async def extract_order_book_data(symbol):
    url = "wss://stream.binance.com:9443/ws"
    stream = f"{symbol.lower()}@depth20"
    async with websockets.connect(f"{url}/{stream}") as websocket:

        last_last_updated = 0
        while True:
            try:
                data = await websocket.recv()
                order_book = json.loads(data)

                bid_df, ask_df = create_dataframes(order_book)

                current_price = get_current_price(bid_df, ask_df)
                volume = calculate_volume(bid_df, ask_df, current_price)
                last_updated = order_book["lastUpdateId"]

                bid_df["type"] = "bid"
                ask_df["type"] = "ask"

                order_book_df = pd.concat(
                    [bid_df, ask_df],
                    axis=0
                ).reset_index(drop=True)

                order_book_df["full_volume"] = volume
                order_book_df["last_updated_id"] = str(last_updated)
                order_book_df["symbol"] = symbol

                if last_updated > last_last_updated:
                    await save_data(order_book_df.to_dict(orient="records"), OrderBookDB)

                avg_period_value = await calculate_weighted_average(symbol, CONFIG["period"])
                avg_cur_value = sum(order_book_df["price"] * order_book_df["volume"]) / order_book_df.shape[0]

                deviation = abs(avg_cur_value - avg_period_value)

                if deviation > CONFIG["threshold"]:
                    message = f"Deviation detected for {symbol}. Latest volume: {avg_cur_value}, Weighted average volume: {avg_period_value}."
                    bot.send_message(CONFIG["telegram_chat_id"], message)

                last_last_updated = last_updated

            except websockets.ConnectionClosed:
                print(f"Connection closed for {symbol}, reconnecting...")
                break


async def extract_script():
    symbols = CONFIG["coins"]
    tasks = [asyncio.create_task(extract_order_book_data(symbol)) for symbol in symbols]
    await asyncio.gather(*tasks)


if __name__ == "__main__":

    asyncio.run(extract_script())
