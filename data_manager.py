# data_manager.py
import pandas as pd

# Item verileri: item_name, price (float/int), date (datetime)
df_items = pd.DataFrame(columns=['item_name', 'price', 'date'])

# Stok verileri: item_name, stock (int)
df_stock = pd.DataFrame(columns=['item_name', 'stock'])

def init_data():
    """
    İsterseniz başlangıçta bazı örnek veriler ekleyebilirsiniz veya
    bu fonksiyon boş kalıp sonradan doldurulabilir.
    """
    global df_items, df_stock
    # Örnek eklemeler:
    # df_items = pd.DataFrame([
    #     {'item_name': 'Kutsama Kağıdı', 'price': 1200000, 'date': pd.to_datetime('2025-01-29')},
    #     {'item_name': 'Ejderha Tanrısı Suyu', 'price': 350000, 'date': pd.to_datetime('2025-01-30')}
    # ])
    # df_stock = pd.DataFrame([
    #     {'item_name': 'Kutsama Kağıdı', 'stock': 10},
    #     {'item_name': 'Ejderha Tanrısı Suyu', 'stock': 5}
    # ])
    pass  # Şimdilik boş bırakıyoruz


# data_manager.py
import pandas as pd

# Item verileri: item_name, price (float/int), date (datetime)
df_items = pd.DataFrame(columns=['item_name', 'price', 'date'])

# Stok verileri: item_name, stock (int)
df_stock = pd.DataFrame(columns=['item_name', 'stock'])


def init_data():
    """
    İsterseniz başlangıçta bazı örnek veriler ekleyebilirsiniz veya
    bu fonksiyon boş kalıp sonradan doldurulabilir.
    """
    global df_items, df_stock
    # Örnek eklemeler:
    # df_items = pd.DataFrame([
    #     {'item_name': 'Kutsama Kağıdı', 'price': 1200000, 'date': pd.to_datetime('2025-01-29')},
    #     {'item_name': 'Ejderha Tanrısı Suyu', 'price': 350000, 'date': pd.to_datetime('2025-01-30')}
    # ])
    # df_stock = pd.DataFrame([
    #     {'item_name': 'Kutsama Kağıdı', 'stock': 10},
    #     {'item_name': 'Ejderha Tanrısı Suyu', 'stock': 5}
    # ])
    pass  # Şimdilik boş bırakıyoruz


def load_items_csv(filepath):
    """
    df_items'e veri yükler.
    Kolonlar: item_name, price, date (gg.aa.yyyy veya benzer)
    """
    global df_items
    temp_df = pd.read_csv(filepath)
    # Date parse etme
    if 'date' in temp_df.columns:
        temp_df['date'] = pd.to_datetime(temp_df['date'], format="%d.%m.%Y", errors='coerce')
    # Price'ı ister float ister int parse edebilirsiniz
    # Veya CSV'de "1.200.000 Yang" formatındaysa önce parse etmeniz gerekir.

    df_items = temp_df.copy()


def save_items_csv(filepath):
    """
    df_items'i CSV'ye kaydeder. Tarih ve fiyat formatını ayarlayabilirsiniz.
    """
    global df_items
    df_to_save = df_items.copy()
    # Tarih sütununu gg.aa.yyyy'ye dönüştür
    if 'date' in df_to_save.columns and pd.api.types.is_datetime64_any_dtype(df_to_save['date']):
        df_to_save['date'] = df_to_save['date'].dt.strftime('%d.%m.%Y')
    df_to_save.to_csv(filepath, index=False)


def load_stock_csv(filepath):
    """
    df_stock'a veri yükler.
    Kolonlar: item_name, stock
    """
    global df_stock
    temp_df = pd.read_csv(filepath)
    df_stock = temp_df.copy()


def save_stock_csv(filepath):
    """
    df_stock'u CSV'ye kaydeder.
    """
    global df_stock
    df_stock.to_csv(filepath, index=False)
