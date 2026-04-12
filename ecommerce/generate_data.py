import json
import random
import os
from datetime import timedelta
from faker import Faker
from sqlalchemy import create_engine, text

# --- ЗАВАНТАЖЕННЯ КОНФІГУРАЦІЇ ---
def load_config(file_path='config.json'):
    with open(file_path, 'r') as f:
        return json.load(f)

config = load_config()

# Розпаковуємо параметри
db_cfg = config['database']
path_cfg = config['paths']
limits = config['generation_limits']

# Використовуємо змінні з конфігу
DB_URL_ROOT = f"mysql+pymysql://{db_cfg['user']}:{db_cfg['password']}@{db_cfg['host']}:{db_cfg['port']}/"
DB_URL_APP  = f"{DB_URL_ROOT}{db_cfg['name']}"
WEB_EVENTS_PATH = path_cfg['web_events_path']

# Константи генерації
N_CUSTOMERS = limits['n_customers']
N_PRODUCTS  = limits['n_products']
N_ORDERS    = limits['n_orders']
N_EVENTS    = limits['n_events']

fake = Faker()
random.seed(42)
Faker.seed(42)

# ... (ваш DDL та функції gen_customers, gen_products залишаються без змін) ...

def main():
    # Створення бази даних
    engine_root = create_engine(DB_URL_ROOT)
    with engine_root.connect() as conn:
        conn.execute(text(f"CREATE DATABASE IF NOT EXISTS {db_cfg['name']}"))
        conn.commit()
    
    engine = create_engine(DB_URL_APP)

    print("⏳ Створення таблиць у MySQL...")
    with engine.connect() as conn:
        # Тут я використовую DDL, який ви надали раніше
        for stmt in DDL.strip().split(";"):
            if stmt.strip():
                conn.execute(text(stmt))
        conn.commit()

    print("⏳ Заповнення MySQL даними...")
    with engine.connect() as conn:
        # Customers
        cust_data = gen_customers(N_CUSTOMERS)
        conn.execute(text("INSERT INTO customers (first_name, last_name, email, country, city, created_at) "
                          "VALUES (:first_name, :last_name, :email, :country, :city, :created_at)"), cust_data)
        
        # Products
        prod_data = gen_products(N_PRODUCTS)
        conn.execute(text("INSERT INTO products (name, category, price, stock, created_at) "
                          "VALUES (:name, :category, :price, :stock, :created_at)"), prod_data)
        
        cust_ids = [r[0] for r in conn.execute(text("SELECT customer_id FROM customers")).fetchall()]
        prod_info = {r[0]: float(r[1]) for r in conn.execute(text("SELECT product_id, price FROM products")).fetchall()}
        conn.commit()

        # Orders, Items & Payments (ваша логіка без змін)
        print("⏳ Генеруємо замовлення...")
        for _ in range(N_ORDERS):
            ordered_at = fake.date_time_between(start_date="-60d")
            status = random.choice(ORDER_STATUSES)
            res = conn.execute(text("INSERT INTO orders (customer_id, status, ordered_at) VALUES (:c, :s, :dt)"),
                               {"c": random.choice(cust_ids), "s": status, "dt": ordered_at})
            oid = res.lastrowid
            
            total_amt = 0
            for _ in range(random.randint(1, 3)):
                pid = random.choice(list(prod_info.keys()))
                price = prod_info[pid]
                qty = random.randint(1, 5)
                total_amt += price * qty
                conn.execute(text("INSERT INTO order_items (order_id, product_id, quantity, unit_price) "
                                  "VALUES (:oid, :pid, :qty, :up)"),
                             {"oid": oid, "pid": pid, "qty": qty, "up": price})
            
            conn.execute(text("INSERT INTO payments (order_id, method, status, amount, paid_at) "
                              "VALUES (:oid, :m, 'paid', :amt, :dt)"),
                         {"oid": oid, "m": random.choice(PAYMENT_METHODS), "amt": total_amt, "dt": ordered_at})
        conn.commit()

    # Створення JSON файлу з подіями
    print(f"⏳ Генеруємо {WEB_EVENTS_PATH}...")
    # Перевіряємо, чи існує папка, якщо ні — створюємо
    os.makedirs(os.path.dirname(WEB_EVENTS_PATH), exist_ok=True)
    
    events = []
    for i in range(N_EVENTS):
        events.append({
            "event_id": i + 1,
            "user_id": random.choice(cust_ids),
            "event_type": random.choice(EVENT_TYPES),
            "timestamp": fake.date_time_between(start_date="-30d").isoformat(),
            "device": random.choice(["mobile", "desktop", "tablet"]),
            "browser": random.choice(["Chrome", "Safari", "Firefox"])
        })
    
    with open(WEB_EVENTS_PATH, "w") as f:
        json.dump(events, f, indent=2)

    print("✅ Все готово!")

if __name__ == "__main__":
    main()
