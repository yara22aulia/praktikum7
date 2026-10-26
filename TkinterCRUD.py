import tkinter as tk
from tkinter import messagebox
import sqlite3

# Membuat database
conn = sqlite3.connect("nilai_siswa.db")
cursor = conn.cursor()

# Membuat tabel
cursor.execute("""
CREATE TABLE IF NOT EXISTS nilai_siswa (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nama_siswa TEXT NOT NULL,
    biologi REAL NOT NULL,
    fisika REAL NOT NULL,
    inggris REAL NOT NULL,
    prediksi_fakultas TEXT NOT NULL
)
""")
conn.commit()


# Fungsi submit nilai
def submit_nilai():
    nama = entry_nama.get().strip()

    try:
        biologi = float(entry_biologi.get())
        fisika = float(entry_fisika.get())
        inggris = float(entry_inggris.get())
    except ValueError:
        messagebox.showerror(
            "Error",
            "Nama dan semua nilai harus diisi dengan benar!"
        )
        return

    if nama == "":
        messagebox.showwarning("Peringatan", "Nama siswa harus diisi!")
        return

    if not all(0 <= n <= 100 for n in [biologi, fisika, inggris]):
        messagebox.showwarning(
            "Peringatan",
            "Nilai harus antara 0 sampai 100!"
        )
        return

    nilai_tertinggi = max(biologi, fisika, inggris)

    if [biologi, fisika, inggris].count(nilai_tertinggi) > 1:
        messagebox.showwarning(
            "Nilai Seri",
            "Nilai tertinggi sama. Silakan periksa kembali nilai."
        )
        return

    if biologi == nilai_tertinggi:
        prediksi = "Kedokteran"
    elif fisika == nilai_tertinggi:
        prediksi = "Teknik"
    else:
        prediksi = "Bahasa"

    cursor.execute("""
        INSERT INTO nilai_siswa
        (nama_siswa, biologi, fisika, inggris, prediksi_fakultas)
        VALUES (?, ?, ?, ?, ?)
    """, (nama, biologi, fisika, inggris, prediksi))

    conn.commit()

    hasil_label.config(
        text=f"Nama: {nama}\n"
             f"Biologi: {biologi:g} | Fisika: {fisika:g} | "
             f"Inggris: {inggris:g}\n"
             f"Prediksi Fakultas: {prediksi}"
    )

    messagebox.showinfo(
        "Berhasil",
        f"Data {nama} berhasil disimpan ke database!"
    )


# Membuat jendela utama
root = tk.Tk()
root.title("Aplikasi Prediksi Fakultas")
root.geometry("500x450")
root.configure(bg="#f0f4f7")

# Judul
judul = tk.Label(
    root,
    text="Aplikasi Prediksi Fakultas",
    font=("Helvetica", 16, "bold"),
    bg="#f0f4f7",
    fg="#333333"
)
judul.pack(pady=20)

# Frame input
input_frame = tk.Frame(root, bg="#f0f4f7")
input_frame.pack(pady=10)

# Nama siswa
tk.Label(
    input_frame, text="Nama Siswa:",
    font=("Helvetica", 12), bg="#f0f4f7"
).grid(row=0, column=0, sticky="w", padx=10, pady=8)

entry_nama = tk.Entry(input_frame, width=25)
entry_nama.grid(row=0, column=1, padx=10, pady=8)
entry_nama.insert(0, "Yara")

# Nilai Biologi
tk.Label(
    input_frame, text="Nilai Biologi:",
    font=("Helvetica", 12), bg="#f0f4f7"
).grid(row=1, column=0, sticky="w", padx=10, pady=8)

entry_biologi = tk.Entry(input_frame, width=25)
entry_biologi.grid(row=1, column=1, padx=10, pady=8)
entry_biologi.insert(0, "95")

# Nilai Fisika
tk.Label(
    input_frame, text="Nilai Fisika:",
    font=("Helvetica", 12), bg="#f0f4f7"
).grid(row=2, column=0, sticky="w", padx=10, pady=8)

entry_fisika = tk.Entry(input_frame, width=25)
entry_fisika.grid(row=2, column=1, padx=10, pady=8)
entry_fisika.insert(0, "80")

# Nilai Inggris
tk.Label(
    input_frame, text="Nilai Inggris:",
    font=("Helvetica", 12), bg="#f0f4f7"
).grid(row=3, column=0, sticky="w", padx=10, pady=8)

entry_inggris = tk.Entry(input_frame, width=25)
entry_inggris.grid(row=3, column=1, padx=10, pady=8)
entry_inggris.insert(0, "85")

# Tombol submit
submit_button = tk.Button(
    root,
    text="Submit Nilai",
    command=submit_nilai,
    font=("Helvetica", 12, "bold"),
    bg="#3333cc",
    fg="white",
    width=15
)
submit_button.pack(pady=15)

# Hasil prediksi
hasil_label = tk.Label(
    root,
    text="Hasil Prediksi: -",
    font=("Helvetica", 12),
    bg="#f0f4f7",
    fg="blue",
    justify="center"
)
hasil_label.pack(pady=10)


# Menutup aplikasi
def tutup_aplikasi():
    conn.close()
    root.destroy()


root.protocol("WM_DELETE_WINDOW", tutup_aplikasi)
root.mainloop()