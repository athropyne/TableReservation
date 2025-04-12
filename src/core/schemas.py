from sqlalchemy import Table, MetaData, Column, Integer, String, ForeignKey, DateTime

metadata = MetaData()
tables = Table(
    "tables",
    metadata,
    Column("id", Integer, primary_key=True, autoincrement=True),
    Column("name", String(20), nullable=False),
    Column("seats", Integer, nullable=False),
    Column("location", String(200), nullable=False),
)

reservations = Table(
    "reservations",
    metadata,
    Column("id", Integer, primary_key=True, autoincrement=True),
    Column("customer_name", String(100), nullable=False),
    Column("table_id", ForeignKey(tables.c.id, onupdate="CASCADE", ondelete="CASCADE"), nullable=False),
    Column("reservation_time", DateTime, nullable=False),
    Column("duration_minutes", Integer, nullable=False)
)
