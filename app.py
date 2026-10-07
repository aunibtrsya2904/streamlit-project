import streamlit as st
import pandas as pd
from datetime import date
from budget_module import (
    calculate_remaining_budget,
    check_budget_status,
    StudentExpenseTracker
)

st.set_page_config(page_title="Student Budget Dashboard", layout="wide")

st.title("🎓 Student Monthly Budget Tracker")
st.caption("Urus perbelanjaan bulanan pelajar dengan mudah dan teratur.")

# Inisialisasi session state untuk simpan senarai perbelanjaan
if "expenses" not in st.session_state:
    st.session_state.expenses = []

# --- SIDEBAR: MAKLUMAT PELAJAR & BAJET ---
with st.sidebar:
    st.header("⚙️️ Profil & Bajet")
    student_name = st.text_input("Nama Pelajar:", placeholder="cth: Ahmad")
    monthly_budget_input = st.text_input("Bajet Bulanan (RM):", value="500.00")
    
    if st.button("Reset Semua Rekod"):
        st.session_state.expenses = []
        st.rerun()

# --- VALIDASI AWAL ---
budget_val = 0.0
is_budget_valid = False
try:
    budget_val = float(monthly_budget_input)
    if budget_val > 0 and student_name.strip() != "":
        is_budget_valid = True
    else:
        st.sidebar.warning("Sila masukkan nama dan bajet yang sah (> 0).")
except ValueError:
    st.sidebar.error("Bajet bulanan mestilah dalam bentuk nombor.")

tracker = StudentExpenseTracker(student_name=student_name, monthly_budget=budget_val)

# --- BAHAGIAN INPUT PERBELANJAAN (FORM) ---
st.subheader("➕ Tambah Perbelanjaan")
with st.form("expense_form", clear_on_submit=True):
    col1, col2, col3 = st.columns([2, 2, 2])
    with col1:
        item_name = st.text_input("Perkara / Item:", placeholder="cth: Nasi Kandar")
    with col2:
        category = st.selectbox(
            "Kategori:",
            ["Food", "Transport", "Books & Study Material", "Entertainment", "Bills", "Other"]
        )
    with col3:
        expense_amount_input = st.text_input("Jumlah (RM):", placeholder="cth: 12.50")
    
    submitted = st.form_submit_button("Rekod Perbelanjaan")

    # Exception Handling & Validasi Input (Memenuhi kriteria f)
    if submitted:
        try:
            if not is_budget_valid:
                st.error("Error: Pastikan profil nama dan bajet di sidebar telah diisi dengan sah dahulu.")
            elif item_name.strip() == "" or expense_amount_input.strip() == "":
                st.error("Error: Sila isi semua ruangan (Nama item dan jumlah tidak boleh kosong).")
            else:
                amount = float(expense_amount_input)
                if amount <= 0:
                    st.error("Error: Jumlah perbelanjaan mestilah lebih daripada RM 0.")
                else:
                    # Tambah ke senarai rekod
                    st.session_state.expenses.append({
                        "item": item_name,
                        "category": category,
                        "amount": amount,
                        "date": str(date.today())
                    })
                    st.success(f"Berjaya direkod: {item_name} (RM {amount:.2f})")
        except ValueError:
            st.error("Error: Nilai jumlah perbelanjaan mesti nombor yang sah.")
        except Exception as e:
            st.error(f"Ralat luar jangka: {e}")

# --- PAPARAN DASHBOARD / HASIL ---
total_spent = tracker.calculate_total_expenses(st.session_state.expenses)
remaining = calculate_remaining_budget(budget_val, total_spent)
status = check_budget_status(remaining, budget_val)

st.markdown("---")
st.subheader(f"📊 Ringkasan Kewangan: {student_name if student_name else '-'}")

# Metrik Interaktif (KPI cards)
kpi1, kpi2, kpi3 = st.columns(3)
kpi1.metric("Jumlah Bajet", f"RM {budget_val:.2f}")
kpi2.metric("Jumlah Dibelanjakan", f"RM {total_spent:.2f}")
kpi3.metric("Baki Bajet", f"RM {remaining:.2f}", delta=f"{remaining:.2f}")

# Progress Bar Penggunaan Bajet
percent_used = tracker.get_budget_percentage(total_spent)
st.write(f"Kadar Penggunaan Bajet: **{percent_used * 100:.1f}%**")
st.progress(percent_used)

# Status Alert Box
if status == "Over Budget":
    st.error("🚨 Status: Over Budget! Anda telah melebihi peruntukan bajet bulanan.")
elif status == "Almost Exceeded":
    st.warning("⚠️ Status: Almost Exceeded! Baki bajet anda tinggal kurang daripada 20%.")
else:
    st.success("✅ Status: Within Budget. Perbelanjaan anda terkawal.")

# Senarai Transaksi & Graf Kategori
if len(st.session_state.expenses) > 0:
    col_table, col_chart = st.columns([3, 2])
    df = pd.DataFrame(st.session_state.expenses)

    with col_table:
        st.write("📋 **Senarai Transaksi**")
        st.dataframe(df, use_container_width=True)

    with col_chart:
        st.write("📈 **Pecahan Mengikut Kategori**")
        category_data = df.groupby("category")["amount"].sum()
        st.bar_chart(category_data)
else:
    st.info("Belum ada perbelanjaan direkodkan. Masukkan perbelanjaan di atas untuk melihat analitik.")