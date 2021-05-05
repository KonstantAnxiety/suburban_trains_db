# suburban_trains_db
## SQLAlchemy guide
### Quickstart
```python
from sqlalchemy import create_engine

db_string = "postgresql://user:password@hostname/database_name"

db = create_engine(db_string)

# Create 
db.execute("CREATE TABLE IF NOT EXISTS films (title text, director text, year text)")  
db.execute("INSERT INTO films (title, director, year) VALUES ('Doctor Strange', 'Scott Derrickson', '2016')")

# Read
result_set = db.execute("SELECT * FROM films")  
for r in result_set:  
    print(r)

# Update
db.execute("UPDATE films SET title='Some2016Film' WHERE year='2016'")

# Delete
db.execute("DELETE FROM films WHERE year='2016'")  
```
### Exceptions
Here we should use Base Exceptions Class to catch all exceptions (or read [it](https://docs.sqlalchemy.org/en/14/core/exceptions.html) for all kinds of excepetions).<br/>
Example:
```python
from sqlalchemy import exc
try:
    result_set = db.execute("SELECT * FROM couriers")
    for r in result_set:
        print(r)
except exc.SQLAlchemyError as err:
    print(err)
```
Result:
```
psycopg2.errors.UndefinedTable) ОШИБКА:  отношение "couriers" не существует
LINE 1: SELECT * FROM couriers
                      ^

[SQL: SELECT * FROM couriers]
(Background on this error at: http://sqlalche.me/e/14/f405)
```
