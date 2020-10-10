import db_functions as db

def print_hi(name):
    sql = db.SQLInjection()
    print(sql("""
        SELECT * from "User" Limit 2
    """))

if __name__ == '__main__':
    print_hi('PyCharm')

