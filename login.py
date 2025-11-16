import sqlite3

def login_account(username, password):
    conn = sqlite3.connect("users.db")
    c = conn.cursor()

    # Cari user berdasarkan username
    c.execute("SELECT password, score FROM users WHERE username = ?", (username,))
    result = c.fetchone()

    # Jika username tidak ditemukan
    if not result:
        conn.close()
        return "Username tidak ditemukan, silahkan lakukan pendaftaran akun"

    stored_password = result[0]
    current_score = result[1]

    if current_score is None:
        c.execute("UPDATE users SET score = 0 WHERE username = ?", (username,))
        conn.commit()

    # Jika password tidak cocok
    if stored_password != password:
        conn.close()
        return "Username atau password salah"

    conn.close()
    return "Login berhasil"
