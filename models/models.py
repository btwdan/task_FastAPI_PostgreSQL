from sqlalchemy import MetaData, Integer, String, ForeignKey, Table, Column, Float

metadata = MetaData()

comic = Table(
    "comic",
    metadata,
    Column('id', Integer, primary_key=True),
    Column('title', String, nullable=False),
    Column('author', String, nullable=False),
    Column('rating', Float, default=0.0)
)

rating = Table(
    "rating",
    metadata,
    Column("id", Integer, primary_key=True),
    Column("comic_id", Integer, ForeignKey("comic.id")),
    Column("user_id", Integer, nullable=False),
    Column("VALUE", Integer, nullable=False)
)