<!-- PROJECT LOGO -->
<br />
<div align="center">
  <h3 align="center">Mirai Cloudflare Controller</h3>

  <p align="center">
    Tool Cloudflare yang kuat dan mudah digunakan
    <br />
  </p>
</div>

![image](https://github.com/user-attachments/assets/9517e382-8111-447b-af9e-6378c48a1dfb)

Mirai Cloudflare Controller adalah alat manajemen DNS Cloudflare yang kuat dan mudah digunakan, dirancang untuk memudahkan pengelolaan domain dan konfigurasi DNS melalui antarmuka command-line.

Fitur utama:
* Daftar domain dan status SSL
* Manajemen catatan DNS (tambah, edit, hapus)
* Pengaturan Force HTTPS/SSL
* Manajemen domain (tambah, hapus)
* Antarmuka berwarna dan mudah dibaca
* Operasi async untuk kinerja yang lebih baik


### Dibangun Dengan

* https://www.python.org/
* https://cloudflare.com

### Dibutuhkan

* Python 3.7+
* Akun Cloudflare dengan API Token

### Instalasi

1. Dapatkan API Token dari [https://dash.cloudflare.com/profile/api-tokens](https://dash.cloudflare.com/profile/api-tokens)
Pastikan sesuai dengan kebutuhan. Karena tools masih dalam pengembangan ini saya centang semua.   
![image](https://github.com/user-attachments/assets/5e443bb5-55bb-4e98-9862-1f5715db0f4b)

3. Klone repositori
   ```sh
   git clone https://github.com/xVCCX/Mirai-Cloudflare.git
   cd Mirai-Cloudflare
   ```
4. Buat lingkungan virtual (opsional tapi direkomendasikan)
   ```sh
   python -m venv venv
   source venv/bin/activate  # Untuk Unix atau MacOS
   .venv\Scripts\activate  # Untuk Windows
   ```
5. Instal paket yang diperlukan
   ```sh
   pip install -r requirements.txt
   ```
6. Buat file `.env` di direktori utama dan tambahkan API Token Anda
   ```
   CLOUDFLARE_API_TOKEN=token_kamu_disini
   ```

## Penggunaan

Jalankan skrip dengan perintah:

```sh
python mirai.py
```

Setelah itu tinggal pilih opsi yang anda inginkan . Fungsi akan terus update selama projek ini dikembangkan.

## Roadmap

- [x] Manajemen catatan DNS dasar
- [x] Pengaturan Force HTTPS
- [x] Tambah dan hapus domain  
- [ ] Dukungan untuk manajemen Page Rules
- [ ] Cloudflare Workers

## Lisensi

Didistribusikan di bawah Lisensi MIT. Lihat `LICENSE.txt` untuk informasi lebih lanjut.

## Ucapan Terima Kasih

* [Cloudflare API Documentation](https://developers.cloudflare.com/api/)
* [Python Requests Library](https://docs.python-requests.org/en/latest/)
