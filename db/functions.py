from sqlalchemy import select, func, and_
from sqlalchemy.dialects.postgresql import insert


from db.connection import async_session
from db.tables import OrderBookDB


async def save_data(data: list, table):
    async with async_session() as session:
        try:
            stmt = insert(table).values(data)

            await session.execute(stmt)
            await session.commit()
        except Exception as e:
            print(e)


async def calculate_weighted_average(symbol, period):
    async with async_session() as session:
        query = (
            select(func.avg(OrderBookDB.volume * OrderBookDB.price).label("avg_weighted_price"))
            .where(OrderBookDB.symbol == symbol)
            .group_by(OrderBookDB.created_at)
            .order_by(OrderBookDB.created_at.desc())
            .limit(period)
        )

        weighted_avg_volume = await session.execute(query)
        return weighted_avg_volume.scalar()
