# item_module.py
import tkinter as tk
from tkinter import messagebox
import matplotlib.pyplot as plt
import pandas as pd
from data_manager import df_items  # DataFrame'i buradan alıyoruz
from data_manager import save_items_csv, load_items_csv  # Gerekirse kullanırız
# item_module.py
from datetime import datetime
from data_manager import df_items


def add_item(entry_item_name, entry_price, text_result=None):
    """
    (GÜNCELLENDİ) Tarihi otomatik olarak bugünün tarihi alır.
    """
    global df_items

    item_name = entry_item_name.get().strip()
    price_str = entry_price.get().strip()

    if not item_name or not price_str:
        messagebox.showwarning("Uyarı", "Lütfen item adı ve fiyat bilgilerini giriniz!")
        return

    # Noktalı formatı parse:
    cleaned_price = price_str.replace(".", "")
    try:
        price_val = float(cleaned_price)
    except ValueError:
        messagebox.showerror("Hata", "Fiyat geçersiz (örn. 1.200.000)!")
        return

    # Otomatik tarih: (Sadece gün bilgisi mi, yoksa saat de mi tutacaksınız?)
    # Eğer sadece günü tutmak isterseniz:
    # date_val = pd.to_datetime('today').normalize()
    # Saat/dakika vs. dahil bugünkü tam zamanı tutmak isterseniz:
    date_val = pd.to_datetime(datetime.now())

    new_record = {
        'item_name': item_name,
        'price': price_val,
        'date': date_val
    }
    df_items = pd.concat([df_items, pd.DataFrame([new_record])], ignore_index=True)

    messagebox.showinfo("Bilgi", f"'{item_name}' kaydı eklendi (Tarih: {date_val.strftime('%d.%m.%Y')}).")

    # Temizle
    entry_item_name.delete(0, tk.END)
    entry_price.delete(0, tk.END)

    if text_result:
        show_all_items(text_result)


def show_all_items(text_widget):
    global df_items
    text_widget.delete("1.0", tk.END)
    if df_items.empty:
        text_widget.insert(tk.END, "Henüz veri yok.\n")
        return
    df_sorted = df_items.sort_values(by='date')
    for _, row in df_sorted.iterrows():
        d_str = row['date'].strftime('%d.%m.%Y %H:%M') if not pd.isnull(row['date']) else "Belirsiz"
        text_widget.insert(tk.END, f"Tarih: {d_str}, Item: {row['item_name']}, Fiyat: {row['price']}\n")


def search_item(entry_search, text_result):
    """
    Arama kutusuna girilen item adını df_items'te arar, sonucu text_result'a yazar.
    """
    global df_items
    search_key = entry_search.get().strip()
    text_result.delete("1.0", tk.END)

    if df_items.empty:
        text_result.insert(tk.END, "Henüz veri yok.\n")
        return
    if not search_key:
        text_result.insert(tk.END, "Lütfen arama yapmak için bir item adı giriniz.\n")
        return

    mask = df_items['item_name'].str.contains(search_key, case=False, na=False)
    result = df_items[mask].sort_values(by='date')

    if result.empty:
        text_result.insert(tk.END, f"'{search_key}' için eşleşme yok.\n")
    else:
        item_names = ", ".join(result['item_name'].unique())
        text_result.insert(tk.END, f"{item_names} arama sonuçları:\n\n")
        for _, row in result.iterrows():
            d_str = row['date'].strftime('%d.%m.%Y') if not pd.isnull(row['date']) else "Belirsiz"
            text_result.insert(tk.END, f"Tarih: {d_str}, {row['item_name']}, Fiyat: {row['price']}\n")


def plot_item(entry_search):
    """
    Aranan itema ait fiyat grafiğini matplotlib ile çizer.
    """
    global df_items
    search_key = entry_search.get().strip()
    if df_items.empty:
        messagebox.showwarning("Uyarı", "Önce veri yüklemeli veya eklemelisiniz.")
        return
    if not search_key:
        messagebox.showwarning("Uyarı", "Grafik için item adı giriniz.")
        return

    mask = df_items['item_name'].str.contains(search_key, case=False, na=False)
    result = df_items[mask].sort_values(by='date')
    if result.empty:
        messagebox.showinfo("Bilgi", f"'{search_key}' için veri yok.")
        return

    # Direkt float sakladığımızı varsayıyoruz
    plt.figure(figsize=(7, 4))
    plt.plot(result['date'], result['price'], marker='o', linestyle='-', color='blue')
    plt.title(f"{search_key} Fiyat Değişimi")
    plt.xlabel("Tarih")
    plt.ylabel("Fiyat (Yang)")
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.show()


def delete_item(entry_delete):
    """
    df_items'ten belirli bir item adını siler.
    """
    global df_items
    item_to_delete = entry_delete.get().strip()
    if not item_to_delete:
        messagebox.showwarning("Uyarı", "Silmek için bir item adı giriniz.")
        return
    if item_to_delete not in df_items['item_name'].values:
        messagebox.showinfo("Bilgi", f"'{item_to_delete}' adlı item bulunamadı.")
        return

    df_items = df_items[df_items['item_name'] != item_to_delete]
    messagebox.showinfo("Bilgi", f"'{item_to_delete}' başarıyla silindi.")
    entry_delete.delete(0, tk.END)
