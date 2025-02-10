# main.py
import tkinter as tk
from tkinter import filedialog, messagebox

# data_manager (içindeki df_items, df_stock, init_data, load_items_csv, save_items_csv, load_stock_csv, save_stock_csv fonksiyonlarını varsayıyoruz)
from data_manager import init_data, load_items_csv, save_items_csv, load_stock_csv, save_stock_csv

# item_module (item ekleme, arama, silme, grafik fonksiyonları)
import item_module

# stock_module (stok takibi pencere fonksiyonu, load/save stok fonksiyonları)
import stock_module

def main():
    # (Opsiyonel) Başlangıç verileri yüklemek istiyorsanız data_manager’da init_data fonksiyonunu kullanabilirsiniz
    init_data()

    root = tk.Tk()
    root.title("Metin2 Piyasa Uygulaması (Modüler)")
    root.geometry("800x600")

    # Program kapatılırken otomatik kaydetme sormak için:
    root.protocol("WM_DELETE_WINDOW", lambda: on_closing(root))

    # === Üst Frame: CSV İşlemleri (Items) ===
    frame_csv = tk.LabelFrame(root, text="Item CSV İşlemleri", padx=5, pady=5)
    frame_csv.pack(fill="x", padx=5, pady=5)

    btn_load_items = tk.Button(
        frame_csv, text="Load Items CSV",
        command=lambda: load_items_via_dialog()
    )
    btn_load_items.pack(side="left", padx=5)

    btn_save_items = tk.Button(
        frame_csv, text="Save Items CSV",
        command=lambda: save_items_via_dialog()
    )
    btn_save_items.pack(side="left", padx=5)

    # === Orta Frame: Arama / Grafik ===
    frame_search = tk.LabelFrame(root, text="Item Arama / Grafik", padx=5, pady=5)
    frame_search.pack(fill="both", expand=True, padx=5, pady=5)

    lbl_search = tk.Label(frame_search, text="Item Adı:")
    lbl_search.grid(row=0, column=0, sticky="w")
    entry_search = tk.Entry(frame_search, width=30)
    entry_search.grid(row=0, column=1, padx=5)

    btn_search_item = tk.Button(
        frame_search,
        text="Ara",
        command=lambda: item_module.search_item(entry_search, text_result)
    )
    btn_search_item.grid(row=0, column=2, padx=5)

    btn_plot_item = tk.Button(
        frame_search,
        text="Grafik",
        command=lambda: item_module.plot_item(entry_search)
    )
    btn_plot_item.grid(row=0, column=3, padx=5)

    text_result = tk.Text(frame_search, width=80, height=15)
    text_result.grid(row=1, column=0, columnspan=4, padx=5, pady=5)

    # === Alt Frame: Item Ekle / Sil ===
    frame_add = tk.LabelFrame(root, text="Yeni Item Ekle / Sil", padx=5, pady=5)
    frame_add.pack(fill="x", padx=5, pady=5)

    lbl_item_name = tk.Label(frame_add, text="Item Adı:")
    lbl_item_name.grid(row=0, column=0, sticky="w")
    entry_item_name = tk.Entry(frame_add, width=20)
    entry_item_name.grid(row=0, column=1, padx=5)

    lbl_price = tk.Label(frame_add, text="Fiyat (örn. 1.200.000):")
    lbl_price.grid(row=1, column=0, sticky="w")
    entry_price = tk.Entry(frame_add, width=20)
    entry_price.grid(row=1, column=1, padx=5)

    # Artık tarih otomatik alındığı için entry_date alanı eklemiyoruz!

    btn_add_item = tk.Button(
        frame_add,
        text="Add Item",
        # item_module.add_item otomatik tarih alacak, bu yüzden entry_date pas geçiyoruz
        command=lambda: item_module.add_item(entry_item_name, entry_price, text_result)
    )
    btn_add_item.grid(row=2, column=0, columnspan=2, pady=5)

    # --- Silme ---
    lbl_delete = tk.Label(frame_add, text="Silinecek Item Adı:")
    lbl_delete.grid(row=3, column=0, sticky="w")
    entry_delete = tk.Entry(frame_add, width=20)
    entry_delete.grid(row=3, column=1, padx=5)

    btn_delete_item = tk.Button(
        frame_add,
        text="Delete Item",
        command=lambda: item_module.delete_item(entry_delete)
    )
    btn_delete_item.grid(row=4, column=0, columnspan=2, pady=5)

    # === Stok Takibi Butonu ===
    btn_stock = tk.Button(
        root,
        text="Stok Takibi Penceresi",
        command=lambda: stock_module.open_stock_window(root)
    )
    btn_stock.pack(pady=10)

    root.mainloop()


def on_closing(root):
    """
    Pencere kapanırken kullanıcıya kaydetme isteyip istemediğini sorar.
    Evet -> items.csv ve stock.csv'ye kaydedip kapanır
    Hayır -> kaydetmeden kapanır
    İptal -> kapanma iptal edilir
    """
    answer = messagebox.askyesnocancel(
        "Programı Kapat",
        "Değişiklikleri kaydetmek ister misiniz?\n\n"
        "Evet: Kaydet ve Kapat\nHayır: Kaydetmeden Kapat\nİptal: Vazgeç"
    )
    if answer is None:
        # 'Cancel' (İptal)
        return  # Kapatma işlemini iptal eder
    elif answer:
        # 'Yes' -> Kaydet
        # items.csv ve stock.csv olarak sabit dosyalara yazıyoruz
        save_items_csv("items.csv")
        save_stock_csv("stock.csv")
        root.destroy()
    else:
        # 'No' -> Kaydetmeden kapat
        root.destroy()


def load_items_via_dialog():
    """
    Kullanıcının seçtiği CSV dosyasından item verilerini yükler (df_items).
    """
    filepath = filedialog.askopenfilename(
        title="Items CSV Seçiniz",
        filetypes=[("CSV Files", "*.csv"), ("All Files", "*.*")]
    )
    if not filepath:
        return
    load_items_csv(filepath)
    messagebox.showinfo("Bilgi", f"Items CSV Yüklendi: {filepath}")


def save_items_via_dialog():
    """
    Kullanıcının seçeceği konuma item verilerini kaydeder (df_items).
    """
    filepath = filedialog.asksaveasfilename(
        title="Items CSV Kaydet",
        defaultextension=".csv",
        filetypes=[("CSV Files", "*.csv"), ("All Files", "*.*")]
    )
    if not filepath:
        return
    save_items_csv(filepath)
    messagebox.showinfo("Bilgi", f"Items CSV Kaydedildi: {filepath}")


if __name__ == "__main__":
    main()