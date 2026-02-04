import sqlite3
import matplotlib.pyplot as plt

# --- SECTION 1: DATABASE SETUP ---
def init_db():
    """Initializes the database and creates the table if it doesn't exist."""
    conn = sqlite3.connect('finance.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS transactions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            type TEXT,      -- 'Income' or 'Expense'
            category TEXT,  -- e.g., Food, Rent, Salary
            amount REAL,
            date TEXT
        )
    ''')
    conn.commit()
    conn.close()

# --- SECTION 2: CORE FUNCTIONS ---
def add_transaction(trans_type, category, amount, date):
    """Adds a new transaction to the database."""
    conn = sqlite3.connect('finance.db')
    cursor = conn.cursor()
    cursor.execute('INSERT INTO transactions (type, category, amount, date) VALUES (?, ?, ?, ?)',
                   (trans_type, category, amount, date))
    conn.commit()
    conn.close()
    print(f"✅ {trans_type} added successfully!")

def view_transactions():
    """Fetches and displays all transactions."""
    conn = sqlite3.connect('finance.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM transactions')
    rows = cursor.fetchall()
    conn.close()

    print("\n--- Transaction History ---")
    print(f"{'ID':<5} {'Type':<10} {'Category':<15} {'Amount':<10} {'Date':<12}")
    print("-" * 55)
    for row in rows:
        print(f"{row[0]:<5} {row[1]:<10} {row[2]:<15} ${row[3]:<10.2f} {row[4]:<12}")
    print("-" * 55)

# --- SECTION 3: VISUALIZATION ---
def visualize_expenses():
    """Generates a pie chart of expenses by category."""
    conn = sqlite3.connect('finance.db')
    cursor = conn.cursor()
    
    # Query: Sum of expenses grouped by category
    cursor.execute('''
        SELECT category, SUM(amount) 
        FROM transactions 
        WHERE type='Expense' 
        GROUP BY category
    ''')
    data = cursor.fetchall()
    conn.close()

    if not data:
        print("⚠️ No expenses to visualize yet.")
        return

    # Prepare data for Matplotlib
    categories = [row[0] for row in data]
    amounts = [row[1] for row in data]

    # Create Pie Chart
    plt.figure(figsize=(8, 6))
    plt.pie(amounts, labels=categories, autopct='%1.1f%%', startangle=140)
    plt.title('Expense Distribution by Category')
    plt.show()

# --- SECTION 4: MAIN MENU LOOP ---
def main():
    init_db()  # Ensure database exists before starting
    
    while True:
        print("\n💰 PERSONAL FINANCE TRACKER 💰")
        print("1. Add Income")
        print("2. Add Expense")
        print("3. View Transactions")
        print("4. Visualize Expenses")
        print("5. Exit")
        
        choice = input("Enter your choice (1-5): ")

        if choice == '1':
            cat = input("Enter Source (e.g., Salary, Freelance): ")
            amt = float(input("Enter Amount: "))
            date = input("Enter Date (YYYY-MM-DD): ")
            add_transaction('Income', cat, amt, date)
            
        elif choice == '2':
            cat = input("Enter Category (e.g., Food, Rent): ")
            amt = float(input("Enter Amount: "))
            date = input("Enter Date (YYYY-MM-DD): ")
            add_transaction('Expense', cat, amt, date)
            
        elif choice == '3':
            view_transactions()
            
        elif choice == '4':
            visualize_expenses()
            
        elif choice == '5':
            print("Goodbye! 👋")
            break
        else:
            print("❌ Invalid choice. Please try again.")

if __name__ == "__main__":
    main()