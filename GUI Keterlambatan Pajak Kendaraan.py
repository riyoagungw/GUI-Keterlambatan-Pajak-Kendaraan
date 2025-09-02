import tkinter as tk
from tkinter import ttk, messagebox
import pandas as pd

def simulasi_keterlambatan_tabel(PKB, Opsen, SWDKLLJ, denda_swdklj_flat, max_bulan=24):
    data = {
        "Bulan": [],
        "Denda PKB+Opsen (2% per bulan)": [],
        "Denda SWDKLLJ": [],
        "Total Bayar (PKB+Opsen+SWDKLLJ+Denda)": []
    }
    total_PKB_opsen = PKB + Opsen
    for bulan in range(1, max_bulan+1):
        persen_denda = min(2*bulan, 48)
        denda_PKB_opsen = total_PKB_opsen * (persen_denda/100)
        total_bayar = PKB + Opsen + SWDKLLJ + denda_PKB_opsen + denda_swdklj_flat
        data["Bulan"].append(bulan)
        data["Denda PKB+Opsen (2% per bulan)"].append(round(denda_PKB_opsen))
        data["Denda SWDKLLJ"].append(round(denda_swdklj_flat))
        data["Total Bayar (PKB+Opsen+SWDKLLJ+Denda)"].append(round(total_bayar))
    return pd.DataFrame(data)

def hitung_simulasi():
    try:
        PKB = float(entry_PKB.get())
        Opsen = float(entry_Opsen.get())
        SWDKLLJ = float(entry_SWDKLJ.get())
        denda_swdklj_flat = float(entry_DendaSW.get())
        global df_simulasi
        df_simulasi = simulasi_keterlambatan_tabel(PKB, Opsen, SWDKLLJ, denda_swdklj_flat)
        tampilkan_tabel(df_simulasi)
        jenis = combo_jenis.get().replace(" ", "_")
        df_simulasi.to_excel(f"Simulasi_{jenis}.xlsx", index=False)
        messagebox.showinfo("Sukses", f"Tabel simulasi berhasil dibuat dan disimpan ke Simulasi_{jenis}.xlsx")
    except ValueError:
        messagebox.showerror("Error", "Masukkan angka valid!")

def tampilkan_tabel(df):
    for row in tree.get_children():
        tree.delete(row)
    for _, row in df.iterrows():
        tree.insert("", "end", values=(row["Bulan"],
                                       f"Rp {row['Denda PKB+Opsen (2% per bulan)']:,}",
                                       f"Rp {row['Denda SWDKLLJ']:,}",
                                       f"Rp {row['Total Bayar (PKB+Opsen+SWDKLLJ+Denda)']:,}"))

def filter_bulan():
    try:
        bulan = int(entry_FilterBulan.get())
        if 1 <= bulan <= 24:
            df_filter = df_simulasi[df_simulasi["Bulan"] == bulan]
            tampilkan_tabel(df_filter)
        else:
            messagebox.showerror("Error", "Bulan harus antara 1-24")
    except ValueError:
        messagebox.showerror("Error", "Masukkan angka valid untuk bulan")

def set_swdklj_default(event):
    jenis = combo_jenis.get()
    if jenis == "Motor":
        entry_SWDKLJ.delete(0, tk.END)
        entry_SWDKLJ.insert(0, "35000")
        entry_DendaSW.delete(0, tk.END)
        entry_DendaSW.insert(0, "32000")
    elif jenis == "Mobil Penumpang":
        entry_SWDKLJ.delete(0, tk.END)
        entry_SWDKLJ.insert(0, "143000")
        entry_DendaSW.delete(0, tk.END)
        entry_DendaSW.insert(0, "100000")
    elif jenis == "Mobil Barang":
        entry_SWDKLJ.delete(0, tk.END)
        entry_SWDKLJ.insert(0, "163000")
        entry_DendaSW.delete(0, tk.END)
        entry_DendaSW.insert(0, "100000")

# ===== GUI =====
root = tk.Tk()
root.title("Simulasi Keterlambatan PKB + Opsen + SWDKLLJ (Motor & Mobil)")
root.geometry("800x500")

frame_input = tk.Frame(root)
frame_input.pack(pady=10)

tk.Label(frame_input, text="Jenis Kendaraan:").grid(row=0, column=0, sticky="w")
combo_jenis = ttk.Combobox(frame_input, values=["Motor", "Mobil Penumpang", "Mobil Barang"])
combo_jenis.grid(row=0, column=1)
combo_jenis.bind("<<ComboboxSelected>>", set_swdklj_default)

tk.Label(frame_input, text="PKB Pokok:").grid(row=1, column=0, sticky="w")
entry_PKB = tk.Entry(frame_input)
entry_PKB.grid(row=1, column=1)

tk.Label(frame_input, text="Opsen PKB:").grid(row=2, column=0, sticky="w")
entry_Opsen = tk.Entry(frame_input)
entry_Opsen.grid(row=2, column=1)

tk.Label(frame_input, text="SWDKLLJ:").grid(row=3, column=0, sticky="w")
entry_SWDKLJ = tk.Entry(frame_input)
entry_SWDKLJ.grid(row=3, column=1)

tk.Label(frame_input, text="Denda SWDKLLJ (flat):").grid(row=4, column=0, sticky="w")
entry_DendaSW = tk.Entry(frame_input)
entry_DendaSW.grid(row=4, column=1)

tk.Button(frame_input, text="Hitung Simulasi", command=hitung_simulasi).grid(row=5, column=0, columnspan=2, pady=10)

frame_filter = tk.Frame(root)
frame_filter.pack(pady=5)
tk.Label(frame_filter, text="Filter Bulan:").pack(side="left")
entry_FilterBulan = tk.Entry(frame_filter, width=5)
entry_FilterBulan.pack(side="left", padx=5)
tk.Button(frame_filter, text="Filter", command=filter_bulan).pack(side="left")

frame_table = tk.Frame(root)
frame_table.pack(fill="both", expand=True)

scrollbar = tk.Scrollbar(frame_table)
scrollbar.pack(side="right", fill="y")

tree = ttk.Treeview(frame_table, columns=("Bulan", "Denda PKB+Opsen", "Denda SWDKLLJ", "Total Bayar"), show="headings", yscrollcommand=scrollbar.set)
tree.heading("Bulan", text="Bulan")
tree.heading("Denda PKB+Opsen", text="Denda PKB+Opsen")
tree.heading("Denda SWDKLLJ", text="Denda SWDKLLJ")
tree.heading("Total Bayar", text="Total Bayar")
tree.column("Bulan", width=80, anchor="center")
tree.column("Denda PKB+Opsen", width=180, anchor="e")
tree.column("Denda SWDKLLJ", width=150, anchor="e")
tree.column("Total Bayar", width=180, anchor="e")
tree.pack(fill="both", expand=True)
scrollbar.config(command=tree.yview)

root.mainloop()
