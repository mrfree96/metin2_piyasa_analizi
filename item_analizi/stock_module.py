# stock_module.py
import tkinter as tk
from tkinter import messagebox, filedialog
import pandas as pd

from data_manager import df_stock, load_stock_csv, save_stock_csv


def open_stock_window(root):
    """
    Yeni bir Toplevel penceresi açarak stok işlemlerini gösterir.
    root: ana pencere (Tk) referansı
    """
    global df_stock

    stock_window = tk.Toplevel(root)
    stock_window.title("Stok Takibi")
    stock_window.geometry("400x300")

    frame_csv = tk.LabelFrame(stock_window, text="Stok CSV İşlemleri", padx=5, pady=5)
    frame_csv.pack(fill="x", padx=5, pady=5)

    btn_load = tk.Button(frame_csv, text="Load Stok CSV", command=lambda: load_stok_file(text_stock))
    btn_load.pack(side="left", padx=5)
    btn_save = tk.Button(frame_csv, text="Save Stok CSV", command=lambda: save_stok_file())
    btn_save.pack(side="left", padx=5)

    frame_form = tk.LabelFrame(stock_window, text="Stok Ekle/Güncelle", padx=5, pady=5)
    frame_form.pack(fill="x", padx=5, pady=5)

    lbl_item = tk.Label(frame_form, text="Item Adı:")
    lbl_item.grid(row=0, column=0, sticky="w")
    entry_item_name = tk.Entry(frame_form, width=15)
    entry_item_name.grid(row=0, column=1, padx=5)

    lbl_stock = tk.Label(frame_form, text="Stok Adedi:")
    lbl_stock.grid(row=1, column=0, sticky="w")
    entry_stock_val = tk.Entry(frame_form, width=15)
    entry_stock_val.grid(row=1, column=1, padx=5)

    btn_add = tk.Button(frame_form, text="Ekle/Güncelle",
                        command=lambda: add_stock_item(entry_item_name, entry_stock_val, text_stock))
    btn_add.grid(row=2, column=0, columnspan=2, pady=5)

    frame_list = tk.LabelFrame(stock_window, text="Stok Listesi", padx=5, pady=5)
    frame_list.pack(fill="both", expand=True, padx=5, pady=5)

    text_stock = tk.Text(frame_list, width=40, height=8)
    text_stock.pack(fill="both", expand=True)

    # Silme için de benzer bir form ekleyebilirsiniz
    frame_delete = tk.LabelFrame(stock_window, text="Stok Sil", padx=5, pady=5)
    frame_delete.pack(fill="x", padx=5, pady=5)

    lbl_delete = tk.Label(frame_delete, text="Silinecek Item:")
    lbl_delete.grid(row=0, column=0)
    entry_delete_item = tk.Entry(frame_delete, width=15)
    entry_delete_item.grid(row=0, column=1, padx=5)
    btn_delete_stok = tk.Button(frame_delete, text="Sil",
                                command=lambda: delete_stock_item(entry_delete_item, text_stock))
    btn_delete_stok.grid(row=0, column=2, padx=5)

    show_stock_items(text_stock)  # Açılır açılmaz stokları göster


def load_stok_file(text_widget):
    filepath = filedialog.askopenfilename(
        title="Stok CSV Dosyası Seçiniz",
        filetypes=[("CSV Files", "*.csv"), ("All Files", "*.*")]
    )
    if not filepath:
        return
    load_stock_csv(filepath)  # data_manager fonksiyonu
    messagebox.showinfo("Bilgi", "Stok CSV yüklendi.")
    show_stock_items(text_widget)


def save_stok_file():
    filepath = filedialog.asksaveasfilename(
        title="Stok CSV Kaydet",
        defaultextension=".csv",
        filetypes=[("CSV Files", "*.csv"), ("All Files", "*.*")]
    )
    if not filepath:
        return
    save_stock_csv(filepath)  # data_manager fonksiyonu
    messagebox.showinfo("Bilgi", "Stok CSV kaydedildi.")


def add_stock_item(entry_item_name, entry_stock_val, text_widget):
    global df_stock
    item_name = entry_item_name.get().strip()
    stock_str = entry_stock_val.get().strip()

    if not item_name or not stock_str:
        messagebox.showwarning("Uyarı", "Item adı ve stok adedi giriniz!")
        return
    try:
        stock_val = int(stock_str)
    except ValueError:
        messagebox.showerror("Hata", "Stok değeri sayı olmalı!")
        return

    # Güncelle veya ekle
    mask = df_stock['item_name'] == item_name
    if mask.any():
        df_stock.loc[mask, 'stock'] = stock_val
        messagebox.showinfo("Bilgi", f"{item_name} stoğu güncellendi: {stock_val}")
    else:
        new_row = pd.DataFrame([[item_name, stock_val]], columns=['item_name', 'stock'])
        df_stock = pd.concat([df_stock, new_row], ignore_index=True)
        messagebox.showinfo("Bilgi", f"{item_name} stoğu eklendi: {stock_val}")

    entry_item_name.delete(0, tk.END)
    entry_stock_val.delete(0, tk.END)
    show_stock_items(text_widget)


def show_stock_items(text_widget):
    global df_stock
    text_widget.delete("1.0", tk.END)
    if df_stock.empty:
        text_widget.insert(tk.END, "Henüz stok yok.\n")
        return
    for _, row in df_stock.iterrows():
        text_widget.insert(tk.END, f"Item: {row['item_name']} - Stok: {row['stock']}\n")


def delete_stock_item(entry_delete_item, text_widget):
    global df_stock
    item_to_delete = entry_delete_item.get().strip()
    if not item_to_delete:
        messagebox.showwarning("Uyarı", "Silmek için item adı giriniz.")
        return

    if item_to_delete not in df_stock['item_name'].values:
        messagebox.showinfo("Bilgi", f"{item_to_delete} adlı stok kaydı bulunamadı.")
        return

    df_stock = df_stock[df_stock['item_name'] != item_to_delete]
    messagebox.showinfo("Bilgi", f"'{item_to_delete}' silindi.")
    entry_delete_item.delete(0, tk.END)
    show_stock_items(text_widget)
