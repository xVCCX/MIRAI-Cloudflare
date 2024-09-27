# Copyright (c) 2024 xVCCX,  All rights reserved
# Required python 3.7 Up

import requests
import json
import sys
import os
import time
from colorama import init, Fore, Back, Style
from dotenv import load_dotenv
from prettytable import PrettyTable
from concurrent.futures import ThreadPoolExecutor, as_completed

# Inisialisasi colorama dan load environment variables
init(autoreset=True)
load_dotenv()

API_TOKEN = os.getenv("CLOUDFLARE_API_TOKEN")
if not API_TOKEN:
    raise ValueError("Token API Cloudflare tidak ditemukan. Harap atur variabel lingkungan CLOUDFLARE_API_TOKEN.")

BASE_URL = "https://api.cloudflare.com/client/v4"

headers = {
    "Authorization": f"Bearer {API_TOKEN}",
    "Content-Type": "application/json"
}

def bersihkan_layar():
    os.system('cls' if os.name == 'nt' else 'clear')

def tampilkan_banner():
    banner = f"""
{Fore.CYAN}{Style.BRIGHT}╔═══════════════════════════════════════════════════════╗
║{Fore.YELLOW}{Style.NORMAL}⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣀⣤⣤⣤⣤⣄⡀⠀⠀⠀⠀⠀⠀{Fore.CYAN}{Style.BRIGHT}                              ║
║{Fore.YELLOW}{Style.NORMAL}⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣴⣿⣿⣿⣿⣿⣿⣿⣿⣷⡄⠀⠀  {Fore.WHITE}{Style.BRIGHT}   M I R A I - {Fore.YELLOW}{Style.NORMAL}CLOUDFLARE {Fore.CYAN}{Style.BRIGHT}    ║
║{Fore.YELLOW}{Style.NORMAL}⠀⠀⠀⠀⠀⣠⣴⣶⣤⣼⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡄⠀{Fore.GREEN}            CONTROLLER          {Fore.CYAN}{Style.BRIGHT}║                             
║{Fore.YELLOW}{Style.NORMAL}⠀⠀⠀⢀⣸⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡇⠀⣀⡀⠀⠀⠀{Fore.CYAN}{Style.BRIGHT}                           ║
║{Fore.YELLOW}{Style.NORMAL}⠀⣴⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣷⣿⣿⣿⣷⣦⠀      {Fore.RED}Developed by :{Fore.CYAN}{Style.BRIGHT}       ║
║{Fore.YELLOW}{Style.NORMAL}⢸⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡇            {Fore.RED}xVCCX{Fore.CYAN}{Style.BRIGHT}          ║
║{Fore.YELLOW}{Style.NORMAL}⠸⠿⠿⠿⠿⠿⠿⠿⠿⠿⠿⠿⠿⠿⠿⠿⠿⠿⠿⠿⠿⠿⠿⠿⠿⠿⠿⠃{Fore.CYAN}{Style.BRIGHT}                           ║
║                {Fore.WHITE}{Style.NORMAL}Version : V1.01 BETA{Fore.CYAN}{Style.BRIGHT}                   ║
╚═══════════════════════════════════════════════════════╝{Style.RESET_ALL}
    """
    print(banner)

def tampilkan_info():
    print(f"{Fore.CYAN}{Style.BRIGHT}Peringatan! Hati-Hati saat menggunakan Semua Fitur ini!{Style.RESET_ALL}")
    print(f"{Fore.CYAN}{Style.BRIGHT}Pastikan sudah mengerti dasar menggunakan Cloudflare sebelum mencoba fitur dibawah ini.{Style.RESET_ALL}")

def buat_tabel_cantik(nama_kolom):
    tabel = PrettyTable()
    tabel.field_names = nama_kolom
    for field in nama_kolom:
        tabel.align[field] = "l"
    tabel.border = True
    tabel.header = True
    tabel.header_style = "upper"
    return tabel

def tampilkan_tabel_berwarna(tabel):
    lines = tabel.get_string().splitlines()
    colored_lines = []
    for i, line in enumerate(lines):
        if i == 0 or i == len(lines) - 1:  # Baris atas dan bawah tabel
            colored_lines.append(f"{Fore.YELLOW}{Style.BRIGHT}{line}{Style.RESET_ALL}")
        elif i == 1 or i == 2:  # Baris header dan pemisah header
            colored_line = f"{Fore.YELLOW}{Style.BRIGHT}{line[0]}{Style.RESET_ALL}"
            colored_line += f"{Fore.YELLOW}{Style.BRIGHT}{line[1:-1]}{Style.RESET_ALL}"
            colored_line += f"{Fore.YELLOW}{Style.BRIGHT}{line[-1]}{Style.RESET_ALL}"
            colored_lines.append(colored_line)
        else:
            # Warnai hanya karakter pertama dan terakhir dari setiap baris
            colored_line = f"{Fore.YELLOW}{Style.BRIGHT}{line[0]}{Style.RESET_ALL}"
            colored_line += line[1:-1]  # Bagian tengah tetap putih
            colored_line += f"{Fore.YELLOW}{Style.BRIGHT}{line[-1]}{Style.RESET_ALL}"
            colored_lines.append(colored_line)
    print("\n".join(colored_lines))

def animasi_loading():
    animasi = [
        f"{Fore.RED}[{Fore.YELLOW}        {Fore.RED}]",
        f"{Fore.RED}[{Fore.YELLOW}=       {Fore.RED}]",
        f"{Fore.RED}[{Fore.YELLOW}==      {Fore.RED}]",
        f"{Fore.RED}[{Fore.GREEN}===     {Fore.RED}]",
        f"{Fore.RED}[{Fore.GREEN}====    {Fore.RED}]",
        f"{Fore.RED}[{Fore.CYAN}=====   {Fore.RED}]",
        f"{Fore.RED}[{Fore.CYAN}======  {Fore.RED}]",
        f"{Fore.RED}[{Fore.BLUE}======= {Fore.RED}]",
        f"{Fore.RED}[{Fore.BLUE}========{Fore.RED}]",
        f"{Fore.RED}[{Fore.MAGENTA} ======={Fore.RED}]",
        f"{Fore.RED}[{Fore.MAGENTA}  ======{Fore.RED}]",
        f"{Fore.RED}[{Fore.WHITE}   ====={Fore.RED}]",
        f"{Fore.RED}[{Fore.WHITE}    ===={Fore.RED}]",
        f"{Fore.RED}[{Fore.YELLOW}     ==={Fore.RED}]",
        f"{Fore.RED}[{Fore.YELLOW}      =={Fore.RED}]",
        f"{Fore.RED}[{Fore.GREEN}       ={Fore.RED}]",
    ]
    idx = 0
    while True:
        print(f"\r{Fore.CYAN}Memproses {animasi[idx % len(animasi)]}", end="")
        sys.stdout.flush()
        idx += 1
        yield

def dengan_loading(func):
    def wrapper(*args, **kwargs):
        loading = animasi_loading()
        result = None
        try:
            with ThreadPoolExecutor(max_workers=1) as executor:
                future = executor.submit(func, *args, **kwargs)
                while not future.done():
                    next(loading)
                    time.sleep(0.1)
                result = future.result()
        finally:
            print("\r" + " " * 30, end="\r")  # Bersihkan animasi loading
        return result
    return wrapper

@dengan_loading
def permintaan_api(metode, url, data=None):
    try:
        if metode == "GET":
            response = requests.get(url, headers=headers)
        elif metode == "POST":
            response = requests.post(url, headers=headers, json=data)
        elif metode == "PUT":
            response = requests.put(url, headers=headers, json=data)
        elif metode == "PATCH":
            response = requests.patch(url, headers=headers, json=data)
        elif metode == "DELETE":
            response = requests.delete(url, headers=headers)
        else:
            raise ValueError(f"Metode HTTP tidak valid: {metode}")
        
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"{Fore.RED}Kesalahan API: {e}{Style.RESET_ALL}")
        return None

def periksa_autentikasi():
    result = permintaan_api("GET", f"{BASE_URL}/user/tokens/verify")
    if result:
        print(f"{Fore.GREEN}Autentikasi berhasil!{Style.RESET_ALL}")
        return True
    return False

def dapatkan_zona():
    result = permintaan_api("GET", f"{BASE_URL}/zones")
    return result.get('result', []) if result else None

def dapatkan_catatan_dns(zone_id):
    result = permintaan_api("GET", f"{BASE_URL}/zones/{zone_id}/dns_records")
    return result.get('result', []) if result else None

def tambah_catatan_dns(zone_id, tipe, nama, konten, ttl=1):
    data = {"type": tipe, "name": nama, "content": konten, "ttl": ttl}
    result = permintaan_api("POST", f"{BASE_URL}/zones/{zone_id}/dns_records", data)
    if result:
        print(f"{Fore.GREEN}Catatan DNS berhasil ditambahkan: {nama}{Style.RESET_ALL}")

def edit_catatan_dns(zone_id, record_id, tipe, nama, konten, ttl=1):
    data = {"type": tipe, "name": nama, "content": konten, "ttl": ttl}
    result = permintaan_api("PUT", f"{BASE_URL}/zones/{zone_id}/dns_records/{record_id}", data)
    if result:
        print(f"{Fore.GREEN}Catatan DNS berhasil diperbarui: {nama}{Style.RESET_ALL}")

def hapus_catatan_dns(zone_id, record_id):
    result = permintaan_api("DELETE", f"{BASE_URL}/zones/{zone_id}/dns_records/{record_id}")
    return result is not None

def hapus_banyak_catatan_dns(zone_id, record_ids):
    for record_id in record_ids:
        if hapus_catatan_dns(zone_id, record_id):
            print(f"{Fore.GREEN}Catatan DNS dengan ID {record_id} berhasil dihapus.{Style.RESET_ALL}")
        else:
            print(f"{Fore.RED}Gagal menghapus catatan DNS dengan ID {record_id}.{Style.RESET_ALL}")

def toggle_force_https(zone_id, action):
    data = {"value": action}
    result = permintaan_api("PATCH", f"{BASE_URL}/zones/{zone_id}/settings/always_use_https", data)
    if result:
        status = "diaktifkan" if action == "on" else "dinonaktifkan"
        print(f"{Fore.GREEN}Force HTTPS berhasil {status}{Style.RESET_ALL}")

def tampilkan_daftar_domain_dan_status():
    zones = dapatkan_zona()
    if not zones:
        print(f"{Fore.RED}Gagal mengambil daftar domain.{Style.RESET_ALL}")
        return

    tabel = buat_tabel_cantik(["No", "Nama Domain", "Status Force HTTPS"])

    for i, zone in enumerate(zones, 1):
        result = permintaan_api("GET", f"{BASE_URL}/zones/{zone['id']}/settings/always_use_https")
        if result:
            status = result['result']['value']
            status_text = 'Aktif' if status == 'on' else 'Nonaktif'
            tabel.add_row([f"{i}", f"{zone['name']}", f"{status_text}"])
        else:
            tabel.add_row([f"{i}", f"{zone['name']}", "Gagal memeriksa"])

    print(f"\n{Fore.CYAN}{Style.BRIGHT}Daftar domain dan status Force HTTPS:{Style.RESET_ALL}")
    tampilkan_tabel_berwarna(tabel)

def tambah_domain_baru():
    while True:
        nama_domain = input(f"{Fore.GREEN}{Style.BRIGHT}Masukkan nama domain baru (atau 'kembali' untuk kembali): {Style.RESET_ALL}")
        if nama_domain.lower() == 'kembali':
            return
        
        konfirmasi = input(f"{Fore.YELLOW}Anda yakin ingin menambahkan domain {nama_domain}? (y/n): {Style.RESET_ALL}").lower()
        if konfirmasi == 'y':
            data = {"name": nama_domain, "jump_start": True}
            result = permintaan_api("POST", f"{BASE_URL}/zones", data)
            if result:
                print(f"{Fore.GREEN}Domain baru berhasil ditambahkan: {nama_domain}{Style.RESET_ALL}")
                print(f"{Fore.YELLOW}Nameserver untuk pointing:{Style.RESET_ALL}")
                for ns in result['result'].get('name_servers', []):
                    print(f"  {Fore.CYAN}- {ns}{Style.RESET_ALL}")
            else:
                print(f"{Fore.RED}Gagal menambahkan domain baru: {nama_domain}{Style.RESET_ALL}")
            break
        elif konfirmasi == 'n':
            print(f"{Fore.YELLOW}Penambahan domain dibatalkan.{Style.RESET_ALL}")
        else:
            print(f"{Fore.RED}Pilihan tidak valid. Masukkan 'y' atau 'n'.{Style.RESET_ALL}")

def hapus_domain(zone_id):
    result = permintaan_api("DELETE", f"{BASE_URL}/zones/{zone_id}")
    if result:
        print(f"{Fore.GREEN}Domain berhasil dihapus.{Style.RESET_ALL}")
    else:
        print(f"{Fore.RED}Gagal menghapus domain.{Style.RESET_ALL}")

def hapus_domain_menu():
    zones = dapatkan_zona()
    if zones:
        while True:
            zone_table = buat_tabel_cantik(["No", "Nama Domain"])
            for i, zone in enumerate(zones, 1):
                zone_table.add_row([f"{i}", f"{zone['name']}"])
            print(f"\n{Fore.CYAN}{Style.BRIGHT}Pilih domain untuk dihapus:{Style.RESET_ALL}")
            tampilkan_tabel_berwarna(zone_table)
            print(f"{Fore.YELLOW}0. Kembali ke menu sebelumnya{Style.RESET_ALL}")
            
            try:
                selected_index = int(input(f"\n{Fore.YELLOW}Masukkan pilihan: {Style.RESET_ALL}"))
                if selected_index == 0:
                    break
                if 1 <= selected_index <= len(zones):
                    selected_zone = zones[selected_index - 1]
                    konfirmasi = input(f"{Fore.YELLOW}Anda yakin ingin menghapus domain {selected_zone['name']}? (y/n): {Style.RESET_ALL}").lower()
                    if konfirmasi == 'y':
                        hapus_domain(selected_zone['id'])
                        break
                    elif konfirmasi == 'n':
                        print(f"{Fore.YELLOW}Penghapusan domain dibatalkan.{Style.RESET_ALL}")
                    else:
                        print(f"{Fore.RED}Pilihan tidak valid. Masukkan 'y' atau 'n'.{Style.RESET_ALL}")
                else:
                    print(f"{Fore.RED}Pilihan tidak valid. Silakan coba lagi.{Style.RESET_ALL}")
            except ValueError:
                print(f"{Fore.RED}Masukkan nomor yang valid.{Style.RESET_ALL}")
    else:
        print(f"{Fore.RED}Tidak ada domain yang tersedia.{Style.RESET_ALL}")

def kelola_catatan_dns():
    zones = dapatkan_zona()
    if zones:
        while True:
            print(f"\n{Fore.CYAN}{Style.BRIGHT}Pilih domain untuk mengelola catatan DNS:{Style.RESET_ALL}")
            zone_table = buat_tabel_cantik(["No", "Nama Domain"])
            for i, zone in enumerate(zones, 1):
                zone_table.add_row([f"{i}", f"{zone['name']}"])
            tampilkan_tabel_berwarna(zone_table)
            print(f"{Fore.YELLOW}0. Kembali ke menu utama{Style.RESET_ALL}")
            
            try:
                selected_index = int(input(f"\n{Fore.YELLOW}Masukkan pilihan: {Style.RESET_ALL}")) - 1
                if selected_index == -1:
                    break
                if 0 <= selected_index < len(zones):
                    selected_zone = zones[selected_index]
                    records = dapatkan_catatan_dns(selected_zone['id'])
                    if records:
                        while True:
                            dns_table = buat_tabel_cantik(["No", "Nama", "Tipe", "Konten"])
                            for i, record in enumerate(records, 1):
                                dns_table.add_row([f"{i}", 
                                                   f"{record['name']}", 
                                                   f"{record['type']}", 
                                                   f"{record['content']}"])
                            print(f"\n{Fore.CYAN}{Style.BRIGHT}Catatan DNS untuk {selected_zone['name']}:{Style.RESET_ALL}")
                            tampilkan_tabel_berwarna(dns_table)
                            
                            print(f"\n{Fore.CYAN}{Style.BRIGHT}Pilih tindakan:{Style.RESET_ALL}")
                            print(f"{Fore.GREEN}{Style.BRIGHT}1. Tambah catatan DNS{Style.RESET_ALL}")
                            print(f"{Fore.GREEN}{Style.BRIGHT}2. Edit catatan DNS{Style.RESET_ALL}")
                            print(f"{Fore.RED}{Style.BRIGHT}3. Hapus catatan DNS{Style.RESET_ALL}")
                            print(f"{Fore.RED}{Style.BRIGHT}4. Hapus banyak catatan DNS{Style.RESET_ALL}")
                            print(f"{Fore.YELLOW}{Style.BRIGHT}5. Kembali ke pilihan domain{Style.RESET_ALL}")
                            
                            action = input(f"\n{Fore.YELLOW}Masukkan pilihan: {Style.RESET_ALL}")
                            
                            if action == '1':
                                tipe = input(f"{Fore.GREEN}{Style.BRIGHT}Masukkan tipe catatan DNS: {Style.RESET_ALL}")
                                nama = input(f"{Fore.GREEN}{Style.BRIGHT}Masukkan nama catatan DNS: {Style.RESET_ALL}")
                                konten = input(f"{Fore.GREEN}{Style.BRIGHT}Masukkan konten catatan DNS: {Style.RESET_ALL}")
                                tambah_catatan_dns(selected_zone['id'], tipe, nama, konten)
                            elif action == '2':
                                record_index = int(input(f"{Fore.GREEN}{Style.BRIGHT}Masukkan nomor catatan yang akan diedit: {Style.RESET_ALL}")) - 1
                                if 0 <= record_index < len(records):
                                    record = records[record_index]
                                    tipe = input(f"{Fore.GREEN}{Style.BRIGHT}Masukkan tipe baru ({record['type']}): {Style.RESET_ALL}") or record['type']
                                    nama = input(f"{Fore.GREEN}{Style.BRIGHT}Masukkan nama baru ({record['name']}): {Style.RESET_ALL}") or record['name']
                                    konten = input(f"{Fore.GREEN}{Style.BRIGHT}Masukkan konten baru ({record['content']}): {Style.RESET_ALL}") or record['content']
                                    edit_catatan_dns(selected_zone['id'], record['id'], tipe, nama, konten)
                                else:
                                    print(f"{Fore.RED}Nomor catatan tidak valid.{Style.RESET_ALL}")
                            elif action == '3':
                                record_index = int(input(f"{Fore.RED}Masukkan nomor catatan yang akan dihapus: {Style.RESET_ALL}")) - 1
                                if 0 <= record_index < len(records):
                                    if hapus_catatan_dns(selected_zone['id'], records[record_index]['id']):
                                        print(f"{Fore.GREEN}{Style.BRIGHT}Catatan DNS berhasil dihapus.{Style.RESET_ALL}")
                                    else:
                                        print(f"{Fore.RED}Gagal menghapus catatan DNS.{Style.RESET_ALL}")
                                else:
                                    print(f"{Fore.RED}Nomor catatan tidak valid.{Style.RESET_ALL}")
                            elif action == '4':
                                record_indices = input(f"{Fore.RED}Masukkan nomor-nomor catatan yang akan dihapus (pisahkan dengan koma): {Style.RESET_ALL}").split(',')
                                record_ids = []
                                for index in record_indices:
                                    try:
                                        index = int(index.strip()) - 1
                                        if 0 <= index < len(records):
                                            record_ids.append(records[index]['id'])
                                        else:
                                            print(f"{Fore.RED}Nomor catatan {index+1} tidak valid.{Style.RESET_ALL}")
                                    except ValueError:
                                        print(f"{Fore.RED}Input tidak valid: {index}{Style.RESET_ALL}")
                                if record_ids:
                                    hapus_banyak_catatan_dns(selected_zone['id'], record_ids)
                            elif action == '5':
                                break
                            else:
                                print(f"{Fore.RED}Pilihan tidak valid.{Style.RESET_ALL}")
                            
                            records = dapatkan_catatan_dns(selected_zone['id'])
                    else:
                        print(f"{Fore.YELLOW}Tidak ada catatan DNS ditemukan.{Style.RESET_ALL}")
                else:
                    print(f"{Fore.RED}Pilihan tidak valid. Silakan coba lagi.{Style.RESET_ALL}")
            except ValueError:
                print(f"{Fore.RED}Masukkan nomor yang valid.{Style.RESET_ALL}")
    else:
        print(f"{Fore.RED}Tidak ada domain yang tersedia.{Style.RESET_ALL}")

def kelola_force_https():
    zones = dapatkan_zona()
    if zones:
        while True:
            zone_table = buat_tabel_cantik(["No", "Nama Domain"])
            for i, zone in enumerate(zones, 1):
                zone_table.add_row([f"{i}", f"{zone['name']}"])
            print(f"\n{Fore.CYAN}{Style.BRIGHT}Pilih domain untuk mengelola Force HTTPS:{Style.RESET_ALL}")
            tampilkan_tabel_berwarna(zone_table)
            print(f"{Fore.YELLOW}0. Kembali ke menu utama{Style.RESET_ALL}")
            
            try:
                selected_index = int(input(f"\n{Fore.YELLOW}Masukkan pilihan: {Style.RESET_ALL}")) - 1
                if selected_index == -1:
                    break
                if 0 <= selected_index < len(zones):
                    selected_zone = zones[selected_index]
                    action = input(f"{Fore.CYAN}{Style.BRIGHT}Pilih tindakan (on/off): {Style.RESET_ALL}").lower()
                    if action in ['on', 'off']:
                        toggle_force_https(selected_zone['id'], action)
                    else:
                        print(f"{Fore.RED}Tindakan tidak valid. Pilih 'on' atau 'off'.{Style.RESET_ALL}")
                else:
                    print(f"{Fore.RED}Pilihan tidak valid. Silakan coba lagi.{Style.RESET_ALL}")
            except ValueError:
                print(f"{Fore.RED}Masukkan nomor yang valid.{Style.RESET_ALL}")
    else:
        print(f"{Fore.RED}Tidak ada domain yang tersedia.{Style.RESET_ALL}")

def kelola_domain():
    while True:
        domain_menu = buat_tabel_cantik(["No", "Aksi"])
        domain_menu.add_row(["1", "Tambah domain baru"])
        domain_menu.add_row(["2", "Hapus domain"])
        domain_menu.add_row(["3", "Kembali ke menu utama"])
        print(f"\n{Fore.CYAN}{Style.BRIGHT}KELOLA DOMAIN:{Style.RESET_ALL}")
        tampilkan_tabel_berwarna(domain_menu)

        sub_pilihan = input(f"{Fore.YELLOW}Pilih tindakan: {Style.RESET_ALL}")

        if sub_pilihan == '1':
            tambah_domain_baru()
        elif sub_pilihan == '2':
            hapus_domain_menu()
        elif sub_pilihan == '3':
            break
        else:
            print(f"{Fore.RED}Pilihan tidak valid.{Style.RESET_ALL}")
        
        input(f"\n{Fore.YELLOW}Tekan Enter untuk melanjutkan...{Style.RESET_ALL}")

def tampilkan_menu():
    table = buat_tabel_cantik(["No", "Menu"])
    table.add_row(["1", "List Domain & SSL Status                        "])
    table.add_row(["2", "Kelola DNS"])
    table.add_row(["3", "Force HTTPS/SSL"])
    table.add_row(["4", "Kelola domain"])
    table.add_row(["5", "Keluar"])
    print(f"\n{Fore.CYAN}{Style.BRIGHT}MENU UTAMA:{Style.RESET_ALL}")
    tampilkan_tabel_berwarna(table)

def main():
    if not periksa_autentikasi():
        print(f"{Fore.RED}Silakan periksa API Token Anda dan coba lagi.{Style.RESET_ALL}")
        sys.exit(1)

    while True:
        bersihkan_layar()
        tampilkan_banner()
        tampilkan_info()
        tampilkan_menu()

        try:
            pilihan = input(f"\n{Fore.YELLOW}Masukkan pilihan: {Style.RESET_ALL}")

            if pilihan == '1':
                tampilkan_daftar_domain_dan_status()
            elif pilihan == '2':
                kelola_catatan_dns()
            elif pilihan == '3':
                kelola_force_https()
            elif pilihan == '4':
                kelola_domain()
            elif pilihan == '5':
                print(f"{Fore.GREEN}Terima kasih telah menggunakan Cloudflare DNS Manager. Sampai jumpa!{Style.RESET_ALL}")
                break
            else:
                print(f"{Fore.RED}Pilihan tidak valid. Silakan coba lagi.{Style.RESET_ALL}")

            input(f"\n{Fore.YELLOW}Tekan Enter untuk melanjutkan...{Style.RESET_ALL}")

        except Exception as e:
            print(f"{Fore.RED}Terjadi kesalahan: {e}{Style.RESET_ALL}")
            input(f"\n{Fore.YELLOW}Tekan Enter untuk melanjutkan...{Style.RESET_ALL}")

if __name__ == "__main__":
    main()
