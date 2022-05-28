import sqlite3

with sqlite3.connect('Sneakbot.db', check_same_thread=False) as database:
    database.row_factory = sqlite3.Row
    cursor = database.cursor()
    cursor.execute("""CREATE TABLE IF NOT EXISTS sneakers_database (id INTEGER,image TEXT, name TEXT, price_usd TEXT,
         price_rub TEXT, size TEXT, color TEXT, style_code TEXT, regions TEXT, link TEXT, date Text)""")
    cursor.execute("""CREATE TABLE IF NOT EXISTS jordans_database (id INTEGER,image TEXT, name TEXT, price_usd TEXT,
             price_rub TEXT, size TEXT, color TEXT, style_code TEXT, regions TEXT, link TEXT, date Text)""")
    cursor.execute("""CREATE TABLE IF NOT EXISTS yeezys_database (id INTEGER,image TEXT, name TEXT, price_usd TEXT,
             price_rub TEXT, size TEXT, color TEXT, style_code TEXT, regions TEXT, link TEXT, date Text)""")
    database.commit()


def save_data(sneakers, name):
    id = 1
    for sneaker in sneakers:
        sql_insert = f"INSERT INTO '{name}' (id ,image, name, price_usd, price_rub, size," \
                     f" color, style_code, regions, link, date) " \
                     f"VALUES ({id},'{sneaker.image}', '{sneaker.name}', " \
                     f"'{sneaker.price_usd}', '{sneaker.price_rub}', '{sneaker.size}'," \
                     f"'{sneaker.color}', '{sneaker.style_code}', '{sneaker.regions}', '{sneaker.link}', " \
                     f"'{sneaker.drop_date}');"
        id += 1
        print(sql_insert)
        cursor.execute(f"""{sql_insert}""")
        database.commit()


def delete_data(name):
    cursor.execute(f"""DELETE FROM '{name}'""")
    database.commit()


def get_count_notes(name):
    cursor.execute(f"""SELECT * FROM '{name}'""")
    rows = cursor.fetchall()
    return len(rows)


def get_table(start_point, end_point, name):
    cursor.execute(f"""SELECT * FROM '{name}' WHERE id > {start_point} and id <= {end_point}""")
    return cursor
