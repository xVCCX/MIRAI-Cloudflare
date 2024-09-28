# Copyright (c) 2024 xVCCX,  All rights reserved
# Required python 3.7 Up

import requests
import json
import sys
import os
import re
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

def tampilkan_banner(account_info=None):

    if account_info and 'name' in account_info:
        # Pisahin email dengan @gmail.com's Account bisa di custom
        email = account_info['name'].split("@gmail.com's Account")[0]
        account_info_str = f"{Fore.MAGENTA}{Style.BRIGHT}Hello, {email}"
    else:
        account_info_str = "Informasi akun tidak tersedia."
    
    banner = f"""
{Fore.CYAN}{Style.BRIGHT}╔═══════════════════════════════════════════════════════╗
║{Fore.YELLOW}{Style.NORMAL}⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣀⣤⣤⣤⣤⣄⡀⠀⠀⠀⠀⠀⠀{Fore.CYAN}{Style.BRIGHT}                              ║
║{Fore.YELLOW}{Style.NORMAL}⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣴⣿⣿⣿⣿⣿⣿⣿⣿⣷⡄⠀⠀  {Fore.WHITE}{Style.BRIGHT}   M I R A I - {Fore.YELLOW}{Style.NORMAL}CLOUDFLARE {Fore.CYAN}{Style.BRIGHT}    ║
║{Fore.YELLOW}{Style.NORMAL}⠀⠀⠀⠀⠀⣠⣴⣶⣤⣼⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡄⠀{Fore.GREEN}{Style.BRIGHT}            CONTROLLER          {Fore.CYAN}{Style.BRIGHT}║                             
║{Fore.YELLOW}{Style.NORMAL}⠀⠀⠀⢀⣸⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡇⠀⣀⡀⠀⠀⠀{Fore.CYAN}{Style.BRIGHT}                           ║
║{Fore.YELLOW}{Style.NORMAL}⠀⣴⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣷⣿⣿⣿⣷⣦⠀      {Fore.RED}Developed by :{Fore.CYAN}{Style.BRIGHT}       ║
║{Fore.YELLOW}{Style.NORMAL}⢸⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡇            {Fore.RED}xVCCX{Fore.CYAN}{Style.BRIGHT}          ║
║{Fore.YELLOW}{Style.NORMAL}⠸⠿⠿⠿⠿⠿⠿⠿⠿⠿⠿⠿⠿⠿⠿⠿⠿⠿⠿⠿⠿⠿⠿⠿⠿⠿⠿⠃{Fore.CYAN}{Style.BRIGHT}                           ║
║                {Fore.RED}{Style.NORMAL}Version : V1.03 BETA{Fore.CYAN}{Style.BRIGHT}                   ║
║                 {account_info_str}                   {Fore.CYAN}{Style.BRIGHT}║
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

def get_account_info():
    result = permintaan_api("GET", f"{BASE_URL}/accounts")
    if result and 'result' in result and result['result']:
        return result['result'][0] 
    return None

def dapatkan_zona(page=1, per_page=20):
    result = permintaan_api("GET", f"{BASE_URL}/zones?page={page}&per_page={per_page}")
    return result if result else None

def tampilkan_daftar_domain(all_zones, current_page, total_pages, per_page):
    start_index = (current_page - 1) * per_page
    end_index = start_index + per_page
    zones_to_display = all_zones[start_index:end_index]

    tabel = buat_tabel_cantik(["No", "Nama Domain"])
    for i, zone in enumerate(zones_to_display, start=start_index + 1):
        tabel.add_row([f"{i}", f"{zone['name']}"])

    print(f"\n{Fore.CYAN}{Style.BRIGHT}Daftar domain (Halaman {current_page} dari {total_pages}):{Style.RESET_ALL}")
    tampilkan_tabel_berwarna(tabel)

def pilih_domain():
    page = 1
    per_page = 20
    all_zones = []

    while True:
        result = dapatkan_zona(page, per_page)
        if not result or 'result' not in result:
            print(f"{Fore.RED}Gagal mengambil daftar domain.{Style.RESET_ALL}")
            return None

        zones = result['result']
        if not zones:
            print(f"{Fore.YELLOW}Tidak ada domain yang ditemukan.{Style.RESET_ALL}")
            return None

        all_zones.extend(zones)
        total_pages = result['result_info']['total_pages']
        current_page = result['result_info']['page']

        tampilkan_daftar_domain(all_zones, current_page, total_pages, per_page)

        while True:
            print(f"\n{Fore.YELLOW}Navigasi: [P]revious, [N]ext, [S]elect domain, [B]ack to menu{Style.RESET_ALL}")
            choice = input(f"{Fore.GREEN}Pilih tindakan: {Style.RESET_ALL}").lower()

            if choice == 'p' and current_page > 1:
                page -= 1
                all_zones = all_zones[:-len(zones)]  # Remove the current page's zones
                break
            elif choice == 'n' and current_page < total_pages:
                page += 1
                break
            elif choice == 's':
                try:
                    index = int(input(f"{Fore.GREEN}Masukkan nomor domain: {Style.RESET_ALL}")) - 1
                    if 0 <= index < len(all_zones):
                        return all_zones[index]
                    else:
                        print(f"{Fore.RED}Nomor domain tidak valid. Silakan coba lagi.{Style.RESET_ALL}")
                except ValueError:
                    print(f"{Fore.RED}Masukkan nomor yang valid.{Style.RESET_ALL}")
            elif choice == 'b':
                return None
            else:
                print(f"{Fore.RED}Pilihan tidak valid. Gunakan P, N, S, atau B.{Style.RESET_ALL}")

def safe_input(prompt, validator=None, error_message=None):
    while True:
        try:
            value = input(prompt)
            if validator and not validator(value):
                raise ValueError(error_message or "Input tidak valid.")
            return value
        except ValueError as e:
            print(f"{Fore.RED}{str(e)}{Style.RESET_ALL}")

def dapatkan_catatan_dns(zone_id):
    result = permintaan_api("GET", f"{BASE_URL}/zones/{zone_id}/dns_records")
    return result.get('result', []) if result else None

def tambah_catatan_dns(zone_id, tipe, nama, konten, proxied= True, ttl=1):
    data = {"type": tipe, "name": nama, "content": konten, "proxied": proxied, "ttl": ttl}
    result = permintaan_api("POST", f"{BASE_URL}/zones/{zone_id}/dns_records", data)
    if result:
        print(f"{Fore.GREEN}Catatan DNS berhasil ditambahkan: {nama}{Style.RESET_ALL}")

def edit_catatan_dns(zone_id, record_id, tipe, nama, konten, proxied= True, ttl=1):
    data = {"type": tipe, "name": nama, "content": konten, "proxied": proxied, "ttl": ttl}
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

def kelola_catatan_dns():
    while True:
        selected_zone = pilih_domain()
        if selected_zone is None:
            return

        while True:
            records = dapatkan_catatan_dns(selected_zone['id'])
            if records:
                dns_table = buat_tabel_cantik(["No", "Nama", "Tipe", "Konten", "Proxied", "TTL"])
                for i, record in enumerate(records, 1):
                    dns_table.add_row([f"{i}", f"{record['name']}", f"{record['type']}", f"{record['content']}", f"{record['proxied']}", f"{record['ttl']}"])
                print(f"\n{Fore.CYAN}{Style.BRIGHT}Catatan DNS untuk {selected_zone['name']}:{Style.RESET_ALL}")
                tampilkan_tabel_berwarna(dns_table)
                print(f"\n{Fore.CYAN}{Style.BRIGHT}Pilih tindakan:{Style.RESET_ALL}")
                print(f"{Fore.GREEN}{Style.BRIGHT}1. Tambah catatan DNS{Style.RESET_ALL}")
                print(f"{Fore.GREEN}{Style.BRIGHT}2. Edit catatan DNS{Style.RESET_ALL}")
                print(f"{Fore.RED}{Style.BRIGHT}3. Hapus catatan DNS{Style.RESET_ALL}")
                print(f"{Fore.RED}{Style.BRIGHT}4. Hapus banyak catatan DNS{Style.RESET_ALL}")
                print(f"{Fore.YELLOW}{Style.BRIGHT}5. Kembali ke pilihan domain{Style.RESET_ALL}")
                print(f"{Fore.YELLOW}{Style.BRIGHT}6. Kembali ke menu utama{Style.RESET_ALL}")
                
                action = safe_input(f"\n{Fore.YELLOW}Masukkan pilihan: {Style.RESET_ALL}",
                                    lambda x: x in ['1', '2', '3', '4', '5', '6'],
                                    "Pilihan tidak valid. Masukkan angka 1-6.")
                
                if action == '1':
                    tipe = input(f"{Fore.GREEN}{Style.BRIGHT}Masukkan tipe catatan DNS: {Style.RESET_ALL}")
                    nama = input(f"{Fore.GREEN}{Style.BRIGHT}Masukkan nama catatan DNS: {Style.RESET_ALL}")
                    konten = input(f"{Fore.GREEN}{Style.BRIGHT}Masukkan konten catatan DNS: {Style.RESET_ALL}")
                    tambah_catatan_dns(selected_zone['id'], tipe, nama, konten)
                elif action == '2':
                    record_index = safe_input(f"{Fore.GREEN}{Style.BRIGHT}Masukkan nomor catatan yang akan diedit: {Style.RESET_ALL}",
                                              lambda x: x.isdigit() and 1 <= int(x) <= len(records),
                                              f"Nomor catatan harus antara 1 dan {len(records)}.")
                    record_index = int(record_index) - 1
                    record = records[record_index]
                    tipe = input(f"{Fore.GREEN}{Style.BRIGHT}Masukkan tipe baru ({record['type']}): {Style.RESET_ALL}") or record['type']
                    nama = input(f"{Fore.GREEN}{Style.BRIGHT}Masukkan nama baru ({record['name']}): {Style.RESET_ALL}") or record['name']
                    konten = input(f"{Fore.GREEN}{Style.BRIGHT}Masukkan konten baru ({record['content']}): {Style.RESET_ALL}") or record['content']
                    edit_catatan_dns(selected_zone['id'], record['id'], tipe, nama, konten)
                elif action == '3':
                    record_index = safe_input(f"{Fore.RED}Masukkan nomor catatan yang akan dihapus: {Style.RESET_ALL}",
                                              lambda x: x.isdigit() and 1 <= int(x) <= len(records),
                                              f"Nomor catatan harus antara 1 dan {len(records)}.")
                    record_index = int(record_index) - 1
                    if hapus_catatan_dns(selected_zone['id'], records[record_index]['id']):
                        print(f"{Fore.GREEN}{Style.BRIGHT}Catatan DNS berhasil dihapus.{Style.RESET_ALL}")
                    else:
                        print(f"{Fore.RED}Gagal menghapus catatan DNS.{Style.RESET_ALL}")
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
                elif action == '6':
                    return
            else:
                print(f"{Fore.YELLOW}Tidak ada catatan DNS ditemukan.{Style.RESET_ALL}")
                break
            
            input(f"\n{Fore.YELLOW}Tekan Enter untuk melanjutkan...{Style.RESET_ALL}")

def toggle_force_https(zone_id, action):
    data = {"value": action}
    result = permintaan_api("PATCH", f"{BASE_URL}/zones/{zone_id}/settings/always_use_https", data)
    if result:
        status = "diaktifkan" if action == "on" else "dinonaktifkan"
        print(f"{Fore.GREEN}Force HTTPS berhasil {status}{Style.RESET_ALL}")

def tampilkan_daftar_domain_dan_status(page=1, per_page=20):
    result = dapatkan_zona(page, per_page)
    if not result or 'result' not in result:
        print(f"{Fore.RED}Gagal mengambil daftar domain.{Style.RESET_ALL}")
        return None, None

    zones = result['result']
    total_pages = result['result_info']['total_pages']
    current_page = result['result_info']['page']

    tabel = buat_tabel_cantik(["No", "Nama Domain", "Status Force HTTPS"])

    for i, zone in enumerate(zones, 1):
        result = permintaan_api("GET", f"{BASE_URL}/zones/{zone['id']}/settings/always_use_https")
        if result:
            status = result['result']['value']
            status_text = 'Aktif' if status == 'on' else 'Nonaktif'
            tabel.add_row([f"{(current_page - 1) * per_page + i}", f"{zone['name']}", f"{status_text}"])
        else:
            tabel.add_row([f"{(current_page - 1) * per_page + i}", f"{zone['name']}", "Gagal memeriksa"])

    print(f"\n{Fore.CYAN}{Style.BRIGHT}Daftar domain dan status Force HTTPS (Halaman {current_page} dari {total_pages}):{Style.RESET_ALL}")
    tampilkan_tabel_berwarna(tabel)

    return current_page, total_pages

def navigasi_halaman(current_page, total_pages):
    while True:
        print(f"\n{Fore.YELLOW}Navigasi: [P]revious, [N]ext, [G]o to page, [B]ack to menu{Style.RESET_ALL}")
        choice = input(f"{Fore.GREEN}Pilih tindakan: {Style.RESET_ALL}").lower()

        if choice == 'p' and current_page > 1:
            return current_page - 1
        elif choice == 'n' and current_page < total_pages:
            return current_page + 1
        elif choice == 'g':
            try:
                page = int(input(f"{Fore.GREEN}Masukkan nomor halaman: {Style.RESET_ALL}"))
                if 1 <= page <= total_pages:
                    return page
                else:
                    print(f"{Fore.RED}Nomor halaman tidak valid.{Style.RESET_ALL}")
            except ValueError:
                print(f"{Fore.RED}Masukkan nomor halaman yang valid.{Style.RESET_ALL}")
        elif choice == 'b':
            return None
        else:
            print(f"{Fore.RED}Pilihan tidak valid. Gunakan P, N, G, atau B.{Style.RESET_ALL}")

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

def kelola_force_https():
    while True:
        selected_zone = pilih_domain()
        if selected_zone is None:
            return

        print(f"\n{Fore.CYAN}{Style.BRIGHT}Force HTTPS untuk {selected_zone['name']}:{Style.RESET_ALL}")
        print(f"{Fore.GREEN}1. Aktifkan Force HTTPS{Style.RESET_ALL}")
        print(f"{Fore.RED}2. Nonaktifkan Force HTTPS{Style.RESET_ALL}")
        print(f"{Fore.YELLOW}3. Kembali ke pilihan domain{Style.RESET_ALL}")
        print(f"{Fore.YELLOW}4. Kembali ke menu utama{Style.RESET_ALL}")

        action = input(f"\n{Fore.YELLOW}Masukkan pilihan: {Style.RESET_ALL}")
        if action == '1':
            toggle_force_https(selected_zone['id'], 'on')
        elif action == '2':
            toggle_force_https(selected_zone['id'], 'off')
        elif action == '3':
            continue
        elif action == '4':
            return
        else:
            print(f"{Fore.RED}Pilihan tidak valid.{Style.RESET_ALL}")

        input(f"\n{Fore.YELLOW}Tekan Enter untuk melanjutkan...{Style.RESET_ALL}")

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
            selected_zone = pilih_domain()
            if selected_zone:
                konfirmasi = input(f"{Fore.YELLOW}Anda yakin ingin menghapus domain {selected_zone['name']}? (y/n): {Style.RESET_ALL}").lower()
                if konfirmasi == 'y':
                    hapus_domain(selected_zone['id'])
                elif konfirmasi == 'n':
                    print(f"{Fore.YELLOW}Penghapusan domain dibatalkan.{Style.RESET_ALL}")
                else:
                    print(f"{Fore.RED}Pilihan tidak valid. Masukkan 'y' atau 'n'.{Style.RESET_ALL}")
        elif sub_pilihan == '3':
            break
        else:
            print(f"{Fore.RED}Pilihan tidak valid.{Style.RESET_ALL}")
        
        input(f"\n{Fore.YELLOW}Tekan Enter untuk melanjutkan...{Style.RESET_ALL}")

def get_page_rules(zone_id):
    result = permintaan_api("GET", f"{BASE_URL}/zones/{zone_id}/pagerules")
    return result.get('result', []) if result else None

def is_valid_url(url):
    regex = re.compile(
        r'^(?:http|ftp)s?://'  # http:// or https://
        r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+(?:[A-Z]{2,6}\.?|[A-Z0-9-]{2,}\.?)|'  # domain...
        r'localhost|'  # localhost...
        r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})'  # ...or ip
        r'(?::\d+)?'  # optional port
        r'(?:/?|[/?]\S+)$', re.IGNORECASE)
    return re.match(regex, url) is not None

def safe_input(prompt, validator=None, error_message=None):
    while True:
        try:
            value = input(prompt)
            if validator and not validator(value):
                raise ValueError(error_message or "Input tidak valid.")
            return value
        except ValueError as e:
            print(f"{Fore.RED}{str(e)}{Style.RESET_ALL}")

def create_page_rule(zone_id, url_pattern, actions):
    data = {
        "targets": [{"target": "url", "constraint": {"operator": "matches", "value": url_pattern}}],
        "actions": actions,
        "status": "active"
    }
    result = permintaan_api("POST", f"{BASE_URL}/zones/{zone_id}/pagerules", data)
    if result:
        print(f"{Fore.GREEN}Page Rule berhasil ditambahkan untuk: {url_pattern}{Style.RESET_ALL}")
    else:
        print(f"{Fore.RED}Gagal menambahkan Page Rule untuk: {url_pattern}{Style.RESET_ALL}")

def update_page_rule(zone_id, rule_id, url_pattern, actions):
    data = {
        "targets": [{"target": "url", "constraint": {"operator": "matches", "value": url_pattern}}],
        "actions": actions,
        "status": "active"
    }
    result = permintaan_api("PUT", f"{BASE_URL}/zones/{zone_id}/pagerules/{rule_id}", data)
    if result:
        print(f"{Fore.GREEN}Page Rule berhasil diperbarui untuk: {url_pattern}{Style.RESET_ALL}")
    else:
        print(f"{Fore.RED}Gagal memperbarui Page Rule untuk: {url_pattern}{Style.RESET_ALL}")

def delete_page_rule(zone_id, rule_id):
    result = permintaan_api("DELETE", f"{BASE_URL}/zones/{zone_id}/pagerules/{rule_id}")
    if result:
        print(f"{Fore.GREEN}Page Rule berhasil dihapus.{Style.RESET_ALL}")
    else:
        print(f"{Fore.RED}Gagal menghapus Page Rule.{Style.RESET_ALL}")

def display_page_rules(zone_id):
    rules = get_page_rules(zone_id)
    if rules:
        table = buat_tabel_cantik(["No", "URL Pattern", "Actions"])
        for i, rule in enumerate(rules, 1):
            url_pattern = rule['targets'][0]['constraint']['value']
            actions = ", ".join([format_action(action) for action in rule['actions']])
            table.add_row([f"{i}", f"{url_pattern}", f"{actions}"])
        print(f"\n{Fore.CYAN}{Style.BRIGHT}Daftar Page Rules:{Style.RESET_ALL}")
        tampilkan_tabel_berwarna(table)
    else:
        print(f"{Fore.YELLOW}Tidak ada Page Rules ditemukan.{Style.RESET_ALL}")

def format_action(action):
    if action['id'] == 'forwarding_url':
        return f"Redirect to: {action['value']['url']} (Status: {action['value']['status_code']})"
    elif action['id'] == 'always_use_https':
        return "Always use HTTPS"
    elif action['id'] == 'cache_level':
        return f"Cache Level: {action['value']}"
    else:
        return f"{action['id']}: {action.get('value', '')}"

def display_page_rule_info():
    print(f"\n{Fore.CYAN}{Style.BRIGHT}Informasi Page Rules:{Style.RESET_ALL}")
    print(f"{Fore.YELLOW}Page Rules memungkinkan Anda mengontrol pengaturan Cloudflare untuk URL tertentu.")
    print("Beberapa contoh penggunaan Page Rules:")
    print("1. Redirect: Mengalihkan satu URL ke URL lain")
    print("2. Always Use HTTPS: Memaksa penggunaan HTTPS untuk URL tertentu")
    print("3. Cache Level: Mengatur level cache untuk URL tertentu")
    print(f"\n{Fore.GREEN}Tip: Gunakan wildcard (*) untuk mencocokkan beberapa URL.{Style.RESET_ALL}")
    print(f"{Fore.GREEN}Contoh: example.com/* akan mencocokkan semua halaman di example.com{Style.RESET_ALL}")

def input_page_rule_actions():
    actions = []
    while True:
        print(f"\n{Fore.CYAN}{Style.BRIGHT}Pilih tipe aksi:{Style.RESET_ALL}")
        print("1. Redirect")
        print("2. Always Use HTTPS")
        print("3. Cache Level")
        print("4. Selesai")
        
        choice = safe_input(f"{Fore.GREEN}Masukkan pilihan (1-4): {Style.RESET_ALL}", 
                            lambda x: x in ['1', '2', '3', '4'],
                            "Pilihan harus antara 1 dan 4.")
        
        if choice == '1':
            destination_url = safe_input(f"{Fore.GREEN}Masukkan URL tujuan redirect: {Style.RESET_ALL}", 
                                         is_valid_url,
                                         "URL tidak valid. Pastikan URL dimulai dengan http:// atau https://")
            status_code = safe_input(f"{Fore.GREEN}Masukkan kode status (301 untuk permanent, 302 untuk temporary): {Style.RESET_ALL}", 
                                     lambda x: x in ['301', '302'],
                                     "Kode status harus 301 atau 302.")
            actions.append({
                "id": "forwarding_url",
                "value": {"url": destination_url, "status_code": int(status_code)}
            })
            print(f"{Fore.GREEN}Redirect berhasil ditambahkan.{Style.RESET_ALL}")
            break  # Exit after setting up redirect
        elif choice == '2':
            actions.append({"id": "always_use_https"})
            print(f"{Fore.GREEN}Always Use HTTPS ditambahkan.{Style.RESET_ALL}")
        elif choice == '3':
            print(f"{Fore.YELLOW}Pilih level cache:{Style.RESET_ALL}")
            print("1. Bypass")
            print("2. Basic")
            print("3. Simplified")
            print("4. Aggressive")
            cache_choice = safe_input(f"{Fore.GREEN}Masukkan pilihan (1-4): {Style.RESET_ALL}", 
                                      lambda x: x in ['1', '2', '3', '4'],
                                      "Pilihan harus antara 1 dan 4.")
            cache_levels = ["bypass", "basic", "simplified", "aggressive"]
            actions.append({"id": "cache_level", "value": cache_levels[int(cache_choice)-1]})
            print(f"{Fore.GREEN}Cache Level berhasil ditambahkan.{Style.RESET_ALL}")
        elif choice == '4':
            if not actions:
                print(f"{Fore.YELLOW}Peringatan: Tidak ada aksi yang dipilih. Page Rule membutuhkan setidaknya satu aksi.{Style.RESET_ALL}")
                continue
            break
    
    return actions

def kelola_page_rules():
    while True:
        selected_zone = pilih_domain()
        if selected_zone is None:
            return
        kelola_page_rules_untuk_zona(selected_zone['id'])

def kelola_page_rules_untuk_zona(zone_id):
    while True:
        try:
            display_page_rules(zone_id)
            display_page_rule_info()
            print(f"\n{Fore.CYAN}{Style.BRIGHT}Pilih tindakan:{Style.RESET_ALL}")
            print(f"{Fore.GREEN}1. Tambah Page Rule{Style.RESET_ALL}")
            print(f"{Fore.GREEN}2. Edit Page Rule{Style.RESET_ALL}")
            print(f"{Fore.RED}3. Hapus Page Rule{Style.RESET_ALL}")
            print(f"{Fore.YELLOW}4. Kembali ke pilihan domain{Style.RESET_ALL}")
            print(f"{Fore.YELLOW}5. Kembali ke menu utama{Style.RESET_ALL}")
            
            action = safe_input(f"\n{Fore.YELLOW}Masukkan pilihan: {Style.RESET_ALL}",
                                lambda x: x in ['1', '2', '3', '4', '5'],
                                "Pilihan harus antara 1 dan 5.")
            
            if action == '1':
                print(f"\n{Fore.CYAN}{Style.BRIGHT}Tambah Page Rule Baru:{Style.RESET_ALL}")
                url_pattern = safe_input(f"{Fore.GREEN}Masukkan URL pattern untuk Page Rule (contoh: example.com/*): {Style.RESET_ALL}", 
                                         lambda x: '*' in x or '/' in x,
                                         "URL pattern harus mengandung '*' atau '/'.")
                actions = input_page_rule_actions()
                if actions:
                    create_page_rule(zone_id, url_pattern, actions)
            elif action == '2':
                rules = get_page_rules(zone_id)
                if rules:
                    rule_index = safe_input(f"{Fore.GREEN}Masukkan nomor Page Rule yang akan diedit: {Style.RESET_ALL}", 
                                            lambda x: x.isdigit() and 1 <= int(x) <= len(rules),
                                            f"Nomor Page Rule harus antara 1 dan {len(rules)}.")
                    rule_index = int(rule_index) - 1
                    rule = rules[rule_index]
                    print(f"\n{Fore.CYAN}{Style.BRIGHT}Edit Page Rule:{Style.RESET_ALL}")
                    url_pattern = safe_input(f"{Fore.GREEN}Masukkan URL pattern baru ({rule['targets'][0]['constraint']['value']}): {Style.RESET_ALL}", 
                                             lambda x: x == '' or '*' in x or '/' in x,
                                             "URL pattern harus mengandung '*' atau '/', atau biarkan kosong untuk tidak mengubah.")
                    url_pattern = url_pattern or rule['targets'][0]['constraint']['value']
                    actions = input_page_rule_actions()
                    if actions:
                        update_page_rule(zone_id, rule['id'], url_pattern, actions)
                else:
                    print(f"{Fore.YELLOW}Tidak ada Page Rules untuk diedit.{Style.RESET_ALL}")
            elif action == '3':
                rules = get_page_rules(zone_id)
                if rules:
                    rule_index = safe_input(f"{Fore.RED}Masukkan nomor Page Rule yang akan dihapus: {Style.RESET_ALL}", 
                                            lambda x: x.isdigit() and 1 <= int(x) <= len(rules),
                                            f"Nomor Page Rule harus antara 1 dan {len(rules)}.")
                    rule_index = int(rule_index) - 1
                    confirm = safe_input(f"{Fore.YELLOW}Anda yakin ingin menghapus Page Rule ini? (y/n): {Style.RESET_ALL}", 
                                         lambda x: x.lower() in ['y', 'n'],
                                         "Masukkan 'y' untuk ya atau 'n' untuk tidak.")
                    if confirm.lower() == 'y':
                        delete_page_rule(zone_id, rules[rule_index]['id'])
                    else:
                        print(f"{Fore.YELLOW}Penghapusan Page Rule dibatalkan.{Style.RESET_ALL}")
                else:
                    print(f"{Fore.YELLOW}Tidak ada Page Rules untuk dihapus.{Style.RESET_ALL}")
            elif action == '4':
                break
            elif action == '5':
                return
        except Exception as e:
            print(f"{Fore.RED}Terjadi kesalahan: {str(e)}{Style.RESET_ALL}")
        
        input(f"\n{Fore.YELLOW}Tekan Enter untuk melanjutkan...{Style.RESET_ALL}")

def purge_cache(zone_id):
    url = f"{BASE_URL}/zones/{zone_id}/purge_cache"
    data = {"purge_everything": True}
    result = permintaan_api("POST", url, data)
    if result and result.get('success'):
        print(f"{Fore.GREEN}Cache berhasil dibersihkan.{Style.RESET_ALL}")
    else:
        print(f"{Fore.RED}Gagal membersihkan cache.{Style.RESET_ALL}")

def kelola_cache():
    while True:
        selected_zone = pilih_domain()
        if selected_zone is None:
            return

        print(f"\n{Fore.CYAN}{Style.BRIGHT}Kelola Cache untuk {selected_zone['name']}:{Style.RESET_ALL}")
        print(f"{Fore.GREEN}1. Bersihkan Semua Cache{Style.RESET_ALL}")
        print(f"{Fore.YELLOW}2. Kembali ke Menu Utama{Style.RESET_ALL}")

        action = input(f"\n{Fore.YELLOW}Masukkan pilihan: {Style.RESET_ALL}")
        if action == '1':
            purge_cache(selected_zone['id'])
        elif action == '2':
            return
        else:
            print(f"{Fore.RED}Pilihan tidak valid.{Style.RESET_ALL}")

        input(f"\n{Fore.YELLOW}Tekan Enter untuk melanjutkan...{Style.RESET_ALL}")

def kelola_development_mode():
    page = 1
    per_page = 20

    while True:
        bersihkan_layar()
        print(f"{Fore.CYAN}{Style.BRIGHT}Kelola Development Mode{Style.RESET_ALL}")
        
        result = dapatkan_zona(page, per_page)
        if not result or 'result' not in result:
            print(f"{Fore.RED}Gagal mengambil daftar domain.{Style.RESET_ALL}")
            return

        zones = result['result']
        total_pages = result['result_info']['total_pages']
        current_page = result['result_info']['page']

        tabel = buat_tabel_cantik(["No", "Nama Domain", "Status Development Mode"])

        for i, zone in enumerate(zones, 1):
            dev_mode_status = get_development_mode_status(zone['id'])
            status_text = 'Aktif' if dev_mode_status == 'on' else 'Nonaktif'
            tabel.add_row([f"{(current_page - 1) * per_page + i}", f"{zone['name']}", f"{status_text}"])

        print(f"\n{Fore.CYAN}{Style.BRIGHT}Daftar domain dan Development Mode (Halaman {current_page} dari {total_pages}):{Style.RESET_ALL}")
        tampilkan_tabel_berwarna(tabel)

        print(f"\n{Fore.YELLOW}Pilihan:{Style.RESET_ALL}")
        print(f"{Fore.GREEN}1-{len(zones)}. Pilih domain untuk toggle Development Mode{Style.RESET_ALL}")
        print(f"{Fore.MAGENTA}B. Bulk Toggle Development Mode{Style.RESET_ALL}")
        if current_page > 1:
            print(f"{Fore.YELLOW}P. Halaman Sebelumnya{Style.RESET_ALL}")
        if current_page < total_pages:
            print(f"{Fore.YELLOW}N. Halaman Selanjutnya{Style.RESET_ALL}")
        print(f"{Fore.YELLOW}0. Kembali ke Menu Utama{Style.RESET_ALL}")

        choice = input(f"\n{Fore.YELLOW}Masukkan pilihan: {Style.RESET_ALL}").lower()

        if choice == '0':
            return
        elif choice == 'b':
            bulk_toggle_development_mode(zones)
        elif choice == 'p' and current_page > 1:
            page -= 1
        elif choice == 'n' and current_page < total_pages:
            page += 1
        elif choice.isdigit() and 1 <= int(choice) <= len(zones):
            selected_zone = zones[int(choice) - 1]
            toggle_development_mode(selected_zone['id'])
        else:
            print(f"{Fore.RED}Pilihan tidak valid. Silakan coba lagi.{Style.RESET_ALL}")

        input(f"\n{Fore.YELLOW}Tekan Enter untuk melanjutkan...{Style.RESET_ALL}")


def bulk_toggle_development_mode(zones):
    print(f"\n{Fore.CYAN}{Style.BRIGHT}Bulk Toggle Development Mode{Style.RESET_ALL}")
    print(f"{Fore.YELLOW}Masukkan nomor domain yang ingin di-toggle (pisahkan dengan koma) atau 'all' untuk semua domain:{Style.RESET_ALL}")
    selection = input().lower()

    if selection == 'all':
        selected_zones = zones
    else:
        indices = [int(idx.strip()) - 1 for idx in selection.split(',') if idx.strip().isdigit()]
        selected_zones = [zones[i] for i in indices if 0 <= i < len(zones)]

    if not selected_zones:
        print(f"{Fore.RED}Tidak ada domain yang dipilih.{Style.RESET_ALL}")
        return

    for zone in selected_zones:
        toggle_development_mode(zone['id'])

    print(f"{Fore.GREEN}Bulk toggle Development Mode selesai.{Style.RESET_ALL}")

def toggle_development_mode(zone_id):
    url = f"{BASE_URL}/zones/{zone_id}/settings/development_mode"
    
    result = permintaan_api("GET", url)
    if not result or 'result' not in result:
        print(f"{Fore.RED}Gagal mendapatkan status Development Mode.{Style.RESET_ALL}")
        return

    current_status = result['result']['value']
    new_status = 'on' if current_status == 'off' else 'off'

    data = {"value": new_status}
    result = permintaan_api("PATCH", url, data)
    
    if result and result.get('success'):
        status_text = "diaktifkan" if new_status == 'on' else "dinonaktifkan"
        print(f"{Fore.GREEN}Development Mode berhasil {status_text}.{Style.RESET_ALL}")
        if new_status == 'on':
            print(f"{Fore.YELLOW}Perhatian: Development Mode akan otomatis nonaktif setelah 3 jam.{Style.RESET_ALL}")
    else:
        print(f"{Fore.RED}Gagal mengubah status Development Mode.{Style.RESET_ALL}")

def get_development_mode_status(zone_id):
    url = f"{BASE_URL}/zones/{zone_id}/settings/development_mode"
    result = permintaan_api("GET", url)
    if result and 'result' in result:
        return result['result']['value']
    return "Unknown"

def get_under_attack_mode_status(zone_id):
    url = f"{BASE_URL}/zones/{zone_id}/settings/security_level"
    result = permintaan_api("GET", url)
    if result and 'result' in result:
        return result['result']['value']
    return "Unknown"

def toggle_under_attack_mode(zone_id):
    url = f"{BASE_URL}/zones/{zone_id}/settings/security_level"

    current_status = get_under_attack_mode_status(zone_id)

    new_status = "under_attack" if current_status != "under_attack" else "medium"

    data = {"value": new_status}
    result = permintaan_api("PATCH", url, data)
    
    if result and result.get('success'):
        status_text = "diaktifkan" if new_status == "under_attack" else "dinonaktifkan"
        print(f"{Fore.GREEN}Mode Under Attack berhasil {status_text}.{Style.RESET_ALL}")
    else:
        print(f"{Fore.RED}Gagal mengubah status Mode Under Attack.{Style.RESET_ALL}")

def kelola_under_attack_mode():
    page = 1
    per_page = 20

    while True:
        bersihkan_layar()
        print(f"{Fore.CYAN}{Style.BRIGHT}Kelola Mode Under Attack{Style.RESET_ALL}")
        
        result = dapatkan_zona(page, per_page)
        if not result or 'result' not in result:
            print(f"{Fore.RED}Gagal mengambil daftar domain.{Style.RESET_ALL}")
            return

        zones = result['result']
        total_pages = result['result_info']['total_pages']
        current_page = result['result_info']['page']

        tabel = buat_tabel_cantik(["No", "Nama Domain", "Status Under Attack Mode"])

        for i, zone in enumerate(zones, 1):
            status = get_under_attack_mode_status(zone['id'])
            status_text = 'Aktif' if status == "under_attack" else 'Nonaktif'
            tabel.add_row([f"{(current_page - 1) * per_page + i}", f"{zone['name']}", f"{status_text}"])

        print(f"\n{Fore.CYAN}{Style.BRIGHT}Daftar domain dan Under Attack Mode (Halaman {current_page} dari {total_pages}):{Style.RESET_ALL}")
        tampilkan_tabel_berwarna(tabel)

        print(f"\n{Fore.YELLOW}Pilihan:{Style.RESET_ALL}")
        print(f"{Fore.GREEN}1-{len(zones)}. Pilih domain untuk toggle Mode Under Attack{Style.RESET_ALL}")
        print(f"{Fore.MAGENTA}B. Bulk Toggle Under Attack Mode{Style.RESET_ALL}")
        if current_page > 1:
            print(f"{Fore.YELLOW}P. Halaman Sebelumnya{Style.RESET_ALL}")
        if current_page < total_pages:
            print(f"{Fore.YELLOW}N. Halaman Selanjutnya{Style.RESET_ALL}")
        print(f"{Fore.YELLOW}0. Kembali ke Menu Utama{Style.RESET_ALL}")

        choice = input(f"\n{Fore.YELLOW}Masukkan pilihan: {Style.RESET_ALL}").lower()

        if choice == '0':
            return
        elif choice == 'b':
            bulk_toggle_under_attack_mode(zones)
        elif choice == 'p' and current_page > 1:
            page -= 1
        elif choice == 'n' and current_page < total_pages:
            page += 1
        elif choice.isdigit() and 1 <= int(choice) <= len(zones):
            selected_zone = zones[int(choice) - 1]
            toggle_under_attack_mode(selected_zone['id'])
        else:
            print(f"{Fore.RED}Pilihan tidak valid. Silakan coba lagi.{Style.RESET_ALL}")

        input(f"\n{Fore.YELLOW}Tekan Enter untuk melanjutkan...{Style.RESET_ALL}")

def bulk_toggle_under_attack_mode(zones):
    print(f"\n{Fore.CYAN}{Style.BRIGHT}Bulk Toggle Under Attack Mode{Style.RESET_ALL}")
    print(f"{Fore.YELLOW}Masukkan nomor domain yang ingin di-toggle (pisahkan dengan koma) atau 'all' untuk semua domain:{Style.RESET_ALL}")
    selection = input().lower()

    if selection == 'all':
        selected_zones = zones
    else:
        indices = [int(idx.strip()) - 1 for idx in selection.split(',') if idx.strip().isdigit()]
        selected_zones = [zones[i] for i in indices if 0 <= i < len(zones)]

    if not selected_zones:
        print(f"{Fore.RED}Tidak ada domain yang dipilih.{Style.RESET_ALL}")
        return

    for zone in selected_zones:
        toggle_under_attack_mode(zone['id'])

    print(f"{Fore.GREEN}Bulk toggle Under Attack Mode selesai.{Style.RESET_ALL}")

def get_security_level(zone_id):
    url = f"{BASE_URL}/zones/{zone_id}/settings/security_level"
    result = permintaan_api("GET", url)
    if result and 'result' in result:
        return result['result']['value']
    return "Unknown"

def set_security_level(zone_id, level):
    url = f"{BASE_URL}/zones/{zone_id}/settings/security_level"
    data = {"value": level}
    result = permintaan_api("PATCH", url, data)
    
    if result and result.get('success'):
        print(f"{Fore.GREEN}Security Level berhasil diubah ke {level}.{Style.RESET_ALL}")
    else:
        print(f"{Fore.RED}Gagal mengubah Security Level.{Style.RESET_ALL}")

def kelola_security_level():
    page = 1
    per_page = 20
    total_domains = 0

    while True:
        bersihkan_layar()
        print(f"{Fore.CYAN}{Style.BRIGHT}Kelola Security Level{Style.RESET_ALL}")
        
        try:
            result = dapatkan_zona(page, per_page)
            if not result or 'result' not in result:
                raise Exception("Gagal mengambil daftar domain.")

            zones = result['result']
            total_pages = result['result_info']['total_pages']
            current_page = result['result_info']['page']
            total_domains = result['result_info']['total_count']

            tabel = buat_tabel_cantik(["No", "Nama Domain", "Security Level"])

            start_index = (page - 1) * per_page + 1
            for i, zone in enumerate(zones, start_index):
                try:
                    status = get_security_level(zone['id'])
                    tabel.add_row([f"{i}", f"{zone['name']}", f"{status}"])
                except Exception as e:
                    tabel.add_row([f"{i}", f"{zone['name']}", f"Error: {str(e)}"])

            print(f"\n{Fore.CYAN}{Style.BRIGHT}Daftar domain dan Security Level (Halaman {current_page} dari {total_pages}, Total Domain: {total_domains}):{Style.RESET_ALL}")
            tampilkan_tabel_berwarna(tabel)

            print(f"\n{Fore.YELLOW}Pilihan:{Style.RESET_ALL}")
            print(f"{Fore.GREEN}1-{len(zones)}. Pilih domain untuk mengubah Security Level{Style.RESET_ALL}")
            print(f"{Fore.MAGENTA}B. Bulk Update Security Level{Style.RESET_ALL}")
            if current_page > 1:
                print(f"{Fore.YELLOW}P. Halaman Sebelumnya{Style.RESET_ALL}")
            if current_page < total_pages:
                print(f"{Fore.YELLOW}N. Halaman Selanjutnya{Style.RESET_ALL}")
            print(f"{Fore.YELLOW}0. Kembali ke Menu Utama{Style.RESET_ALL}")

            choice = input(f"\n{Fore.YELLOW}Masukkan pilihan: {Style.RESET_ALL}").lower()

            if choice == '0':
                return
            elif choice == 'b':
                bulk_update_security_level(zones, start_index)
            elif choice == 'p' and current_page > 1:
                page -= 1
            elif choice == 'n' and current_page < total_pages:
                page += 1
            elif choice.isdigit() and 1 <= int(choice) <= len(zones):
                selected_zone = zones[int(choice) - start_index]
                ubah_security_level(selected_zone['id'])
            else:
                raise ValueError("Pilihan tidak valid.")

        except Exception as e:
            print(f"{Fore.RED}Terjadi kesalahan: {str(e)}{Style.RESET_ALL}")

        input(f"\n{Fore.YELLOW}Tekan Enter untuk melanjutkan...{Style.RESET_ALL}")


def bulk_update_security_level(zones, start_index):
    print(f"\n{Fore.CYAN}{Style.BRIGHT}Bulk Update Security Level{Style.RESET_ALL}")
    print(f"{Fore.YELLOW}Masukkan nomor domain yang ingin diupdate (pisahkan dengan koma) atau 'all' untuk semua domain:{Style.RESET_ALL}")
    selection = input().lower()

    try:
        if selection == 'all':
            selected_zones = zones
        else:
            indices = [int(idx.strip()) - start_index for idx in selection.split(',') if idx.strip().isdigit()]
            selected_zones = [zones[i] for i in range(len(zones)) if i in indices]

        if not selected_zones:
            raise ValueError("Tidak ada domain yang dipilih.")

        print(f"\n{Fore.CYAN}{Style.BRIGHT}Pilih Security Level untuk update:{Style.RESET_ALL}")
        print(f"{Fore.GREEN}1. Essentially Off{Style.RESET_ALL}")
        print(f"{Fore.GREEN}2. Low{Style.RESET_ALL}")
        print(f"{Fore.GREEN}3. Medium{Style.RESET_ALL}")
        print(f"{Fore.GREEN}4. High{Style.RESET_ALL}")
        print(f"{Fore.GREEN}5. Under Attack{Style.RESET_ALL}")

        level_choice = input(f"\n{Fore.YELLOW}Masukkan pilihan (1-5): {Style.RESET_ALL}")
        levels = {
            "1": "essentially_off",
            "2": "low",
            "3": "medium",
            "4": "high",
            "5": "under_attack"
        }

        if level_choice not in levels:
            raise ValueError("Pilihan Security Level tidak valid.")

        new_level = levels[level_choice]
        for zone in selected_zones:
            set_security_level(zone['id'], new_level)
        print(f"{Fore.GREEN}Bulk update selesai.{Style.RESET_ALL}")

    except Exception as e:
        print(f"{Fore.RED}Terjadi kesalahan saat bulk update: {str(e)}{Style.RESET_ALL}")

def ubah_security_level(zone_id):
    levels = {
        "1": "essentially_off",
        "2": "low",
        "3": "medium",
        "4": "high",
        "5": "under_attack"
    }
    
    print(f"\n{Fore.CYAN}{Style.BRIGHT}Pilih Security Level:{Style.RESET_ALL}")
    print(f"{Fore.GREEN}1. Essentially Off{Style.RESET_ALL}")
    print(f"{Fore.GREEN}2. Low{Style.RESET_ALL}")
    print(f"{Fore.GREEN}3. Medium{Style.RESET_ALL}")
    print(f"{Fore.GREEN}4. High{Style.RESET_ALL}")
    print(f"{Fore.GREEN}5. Under Attack{Style.RESET_ALL}")

    choice = input(f"\n{Fore.YELLOW}Masukkan pilihan (1-5): {Style.RESET_ALL}")

    if choice in levels:
        set_security_level(zone_id, levels[choice])
    else:
        print(f"{Fore.RED}Pilihan tidak valid.{Style.RESET_ALL}")



def tampilkan_menu():
    print()
    
    table = buat_tabel_cantik(["No", "Menu"])
    table.add_row(["1", "List Domain & SSL Status                        "])
    table.add_row(["2", "Kelola DNS"])
    table.add_row(["3", "Force HTTPS/SSL"])
    table.add_row(["4", "Kelola domain"])
    table.add_row(["5", "Kelola Page Rules"])
    table.add_row(["6", "Purge Cache"])
    table.add_row(["7", "Development Mode"])
    table.add_row(["8", "Under Attack Mode (Aktifkan Kalau lagi Kena DDOS)"])
    table.add_row(["9", "DDOS SHIELD Level"])
    table.add_row(["10", "Keluar"])
    print(f"\n{Fore.CYAN}{Style.BRIGHT}MENU UTAMA:{Style.RESET_ALL}")
    tampilkan_tabel_berwarna(table)

def main():
    if not periksa_autentikasi():
        print(f"{Fore.RED}Silakan periksa API Token Anda dan coba lagi.{Style.RESET_ALL}")
        sys.exit(1)

    account_info = get_account_info()

    while True:
        bersihkan_layar()
        tampilkan_banner(account_info)
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
                kelola_page_rules()
            elif pilihan == '6':
                kelola_cache()
            elif pilihan == '7':
                kelola_development_mode() 
            elif pilihan == '8':
                kelola_under_attack_mode() 
            elif pilihan == '9':
                kelola_security_level() 
            elif pilihan == '10':
                print(f"{Fore.GREEN}ADIOS!{Style.RESET_ALL}")
                break
            else:
                print(f"{Fore.RED}Pilihan tidak valid. Silakan coba lagi.{Style.RESET_ALL}")

            input(f"\n{Fore.YELLOW}Tekan Enter untuk melanjutkan...{Style.RESET_ALL}")

        except KeyboardInterrupt:
            print(f"\n{Fore.RED}Session Terminated.{Style.RESET_ALL}")
            break
        except Exception as e:
            print(f"{Fore.RED}Terjadi kesalahan: {e}{Style.RESET_ALL}")
            input(f"\n{Fore.YELLOW}Tekan Enter untuk melanjutkan...{Style.RESET_ALL}")

if __name__ == "__main__":
    main()
