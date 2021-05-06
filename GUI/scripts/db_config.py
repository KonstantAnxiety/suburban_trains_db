from sqlalchemy import create_engine

# db_connect = "postgresql://user:password@hostname/database_name"
# TODO change to own.
db_connect = "postgresql://postgres:12345@localhost:5432/suburban_trains"
db = create_engine(db_connect)
