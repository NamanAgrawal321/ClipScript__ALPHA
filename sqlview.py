from sqlalchemy import create_engine, inspect, text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# SQLite डेटाबेस फाइल का पथ
DB_PATH = 'clipscript_sqlalchemy.db'  # या 'clipscript.db'

# Engine बनाएं
engine = create_engine(f'sqlite:///{DB_PATH}')

# Inspector बनाएं
inspector = inspect(engine)

# सभी टेबल्स की सूची प्राप्त करें
table_names = inspector.get_table_names()
print("डेटाबेस में मौजूद टेबल्स:", table_names)

# प्रत्येक टेबल के कॉलम्स और डेटा देखें
for table_name in table_names:
    print(f"\nटेबल: {table_name}")
    columns = inspector.get_columns(table_name)
    for column in columns:
        print(f"  - {column['name']} ({column['type']})")
    
    # टेबल से डेटा प्राप्त करें (पहले 5 रो)
    with engine.connect() as connection:
        # text() फंक्शन का उपयोग करें
        result = connection.execute(text(f"SELECT * FROM {table_name} LIMIT 5"))
        rows = result.fetchall()
        print(f"\n{table_name} के पहले 5 रो:")
        for row in rows:
            print("  ", row)