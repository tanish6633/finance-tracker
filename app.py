import streamlit as st
import sqlite3
import pandas as pd
import matplotlib.pyplot as plt

# --- PAGE SETUP ---
st.set_page_config(page_title="Personal Finance Tracker", page_icon="💰")
st.title("💰 Personal Finance Tracker")

# --- DATABASE MANAGEMENT ---
def init_db():
    conn = sqlite3.connect('finance.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS transactions
                 (id INTEGER PRIMARY KEY, type TEXT, category TEXT, amount REAL, date TEXT)''')
    conn.commit()
    conn.close()

def add_data(t_type, category, amount, date):
    conn = sqlite3.connect('finance.db')
    c = conn.cursor()
    c.execute('INSERT INTO transactions(type, category, amount, date) VALUES (?,?,?,?)', 
              (t_type, category, amount, date))
    conn.commit()
    conn.close()
    st.success(f"✅ Added {category} to database!")

def get_data():
    conn = sqlite3.connect('finance.db')
    df = pd.read_sql_query("SELECT * FROM transactions", conn)
    conn.close()
    return df

# Initialize DB
init_db()

# --- SIDEBAR: ADD TRANSACTION ---
st.sidebar.header("Add New Transaction")
with st.sidebar.form("entry_form", clear_on_submit=True):
    t_type = st.selectbox("Type", ["Income", "Expense"])
    category = st.text_input("Category (e.g., Salary, Food)")
    amount = st.number_input("Amount", min_value=0.0, format="%.2f")
    date = st.date_input("Date")
    submitted = st.form_submit_button("Save Transaction")
    
    if submitted:
        if category and amount > 0:
            add_data(t_type, category, amount, str(date))
        else:
            st.warning("⚠️ Please fill in all fields.")

# --- MAIN DASHBOARD ---
df = get_data()

if not df.empty:
    # 1. Summary Metrics
    total_income = df[df['type'] == 'Income']['amount'].sum()
    total_expense = df[df['type'] == 'Expense']['amount'].sum()
    balance = total_income - total_expense

    col1, col2, col3 = st.columns(3)
    col1.metric("Total Income", f"₹{total_income:,.2f}")
    col2.metric("Total Expense", f"₹{total_expense:,.2f}")
    col3.metric("Remaining Balance", f"₹{balance:,.2f}")

    st.divider()

    # 2. Visualization (Pie Chart)
    st.subheader("📊 Expense Breakdown")
    expense_df = df[df['type'] == 'Expense']
    
    if not expense_df.empty:
        fig, ax = plt.subplots()
        expense_by_cat = expense_df.groupby('category')['amount'].sum()
        ax.pie(expense_by_cat, labels=expense_by_cat.index, autopct='%1.1f%%', startangle=90)
        ax.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.
        st.pyplot(fig)
    else:
        st.info("No expenses recorded yet.")

    st.divider()

    # 3. Recent Transactions (Data Table)
    st.subheader("📝 Recent Transactions")
    st.dataframe(df.sort_values(by="date", ascending=False), use_container_width=True)

    # Option to Delete Data
    if st.checkbox("Show Delete Options"):
        delete_id = st.number_input("Enter ID to delete", min_value=1, step=1)
        if st.button("Delete Record"):
            conn = sqlite3.connect('finance.db')
            c = conn.cursor()
            c.execute("DELETE FROM transactions WHERE id=?", (delete_id,))
            conn.commit()
            conn.close()
            st.rerun()

else:
    st.info("👋 Welcome! Use the sidebar to add your first transaction.")