import requests
import time
import random
from faker import Faker
import re
from colorama import Fore, Style, init

init(autoreset=True)
fake = Faker()

def nama():
    art_lines = [
        "   ___  ___            _       _               ______       _   ",
        "  |  \\/  |           | |     | |              | ___ \\     | |  ",
        "  | .  . | ___  _ __ | |_ ___| | _____ ____   | |_/ / ___ | |_ ",
        "  | |\\/| |/ _ \\| '_ \\| __/ _ \\ |/ / __|_  /   | ___ \\/ _ \\| __|",
        "  | |  | | (_) | | | | ||  __/   <\\__ \\/ /    | |_/ / (_) | |_ ",
        "  \\_|  |_|\\___/|_| |_|\\__\\___|_|\\_\\___/___|   \\____/ \\___/ \\__|",
        "                                                                ",
        "                                                                "
    ]

    max_length = max(len(line) for line in art_lines)

    border = '#' * (max_length + 4)

    print(border)
    for line in art_lines:
        print(f"# {line} #")
    print(border)

    print(f"{Fore.GREEN}Terima kasih Telah Menggunakan Bot dari Monteksz Jangan Lupa Bintangnya ^^{Fore.RESET}")
    print(f"{Fore.GREEN}Cek Bot Lainnya di https://github.com/monteksz{Fore.RESET}")
    print(f"{Fore.GREEN}=================================================================================================={Fore.RESET}")

nama()

def get_temp_email_address():
    response = requests.get('https://api.mail.tm/domains')
    if response.status_code != 200:
        print(Fore.RED + Style.BRIGHT + "Gagal mendapatkan domain email.")
        print(Fore.RED + Style.BRIGHT + "Respon:", response.text)
        return None
    data = response.json()
    if not data or 'hydra:member' not in data or len(data['hydra:member']) == 0:
        print(Fore.RED + Style.BRIGHT + "Tidak ada domain email yang tersedia.")
        return None
    domain = data['hydra:member'][0]['domain']
    email_prefix = fake.user_name() + str(random.randint(1000, 9999))
    email_address = f"{email_prefix}@{domain}"
    return email_address

def create_temp_email(email_address):
    response = requests.post('https://api.mail.tm/accounts', json={
        'address': email_address,
        'password': 'password123'
    })
    if response.status_code != 201:
        print(Fore.RED + Style.BRIGHT + "Gagal membuat email sementara.")
        print(Fore.RED + Style.BRIGHT + "Respon:", response.text)
        return None, None, None
    data = response.json()
    return data.get('address'), 'password123', data.get('id')

def get_access_token(email, password):
    response = requests.post('https://api.mail.tm/token', json={
        'address': email,
        'password': password
    })
    if response.status_code != 200:
        print(Fore.RED + Style.BRIGHT + "Gagal mendapatkan token akses.")
        print(Fore.RED + Style.BRIGHT + "Respon:", response.text)
        return None
    return response.json().get('token')

def get_latest_email(token):
    headers = {'Authorization': f'Bearer {token}'}
    response = requests.get('https://api.mail.tm/messages', headers=headers)
    if response.status_code != 200:
        print(Fore.RED + Style.BRIGHT + "Gagal mendapatkan email terbaru.")
        print(Fore.RED + Style.BRIGHT + "Respon:", response.text)
        return None
    messages = response.json().get('hydra:member', [])
    return messages[0] if messages else None

def request_otp(email):
    response = requests.post('https://api.pixelverse.xyz/api/otp/request', json={'email': email})
    return response.status_code == 200

def verify_otp(email, otp):
    response = requests.post('https://api.pixelverse.xyz/api/auth/otp', json={'email': email, 'otpCode': otp})
    if response.status_code in [200, 201]:
        refresh_token_cookie = response.cookies.get('refresh-token')
        data = response.json()
        data['refresh_token'] = refresh_token_cookie
        return data
    else:
        print(Fore.RED + Style.BRIGHT + f"Verifikasi OTP gagal. Status: {response.status_code}, Respon: {response.text}")
    return None

def set_referral(referral_code, access_token):
    headers = {
        'Authorization': access_token,
        'Accept': 'application/json, text/plain, */*',
        'Content-Type': 'application/json',
        'Accept-Encoding': 'gzip, deflate, br, zstd',
        'Accept-Language': 'en-US,en;q=0.9',
        'Cache-Control': 'no-cache',
        'Origin': 'https://dashboard.pixelverse.xyz',
        'Referer': 'https://dashboard.pixelverse.xyz/',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, seperti Gecko) Chrome/126.0.0.0 Safari/537.36'
    }
    referral_url = f'https://api.pixelverse.xyz/api/referrals/set-referer/{referral_code}'
    response = requests.put(referral_url, headers=headers)
    try:
        response_json = response.json()
    except ValueError:
        response_json = None
    return response.status_code, response_json

def extract_otp(text):
    match = re.search(r'\b\d{6}\b', text)
    if match:
        return match.group(0)
    return None

def generate_username():
    username = fake.user_name()[:14]
    while len(username) < 5 or len(username) > 14:
        username = fake.user_name()[:14]
    return username

def update_username_and_bio(access_token):
    url = "https://api.pixelverse.xyz/api/users/@me"
    headers = {
        'Accept': 'application/json, text/plain, */*',
        'Accept-Encoding': 'gzip, deflate, br, zstd',
        'Accept-Language': 'en-US,en;q=0.9',
        'Authorization': access_token,
        'Cache-Control': 'no-cache',
        'Content-Type': 'application/json',
        'Origin': 'https://dashboard.pixelverse.xyz',
        'Referer': 'https://dashboard.pixelverse.xyz/',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, seperti Gecko) Chrome/126.0.0.0 Safari/537.36'
    }
    username = generate_username()
    biography = fake.sentence()
    payload = {
        "updateProfileOptions": {
            "username": username,
            "biography": biography
        }
    }
    response = requests.patch(url, headers=headers, json=payload)
    if response.status_code == 200:
        print(Fore.GREEN + Style.BRIGHT + f"Username berhasil diperbarui menjadi: {username}")
        print(Fore.GREEN + Style.BRIGHT + f"Bio berhasil diperbarui menjadi: {biography}")
    else:
        print(Fore.RED + Style.BRIGHT + f"Gagal memperbarui username. Status: {response.status_code}, Respon: {response.text}")
    return response.status_code == 200

def buy_pet(access_token, pet_id):
    url = f"https://api.pixelverse.xyz/api/pets/{pet_id}/buy"
    headers = {
        'Authorization': access_token,
        'Accept': 'application/json, text/plain, */*',
        'Content-Type': 'application/json',
        'Accept-Encoding': 'gzip, deflate, br, zstd',
        'Accept-Language': 'en-US,en;q=0.9',
        'Cache-Control': 'no-cache',
        'Origin': 'https://dashboard.pixelverse.xyz',
        'Referer': 'https://dashboard.pixelverse.xyz/',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, seperti Gecko) Chrome/126.0.0.0 Safari/537.36'
    }
    response = requests.post(url, headers=headers)
    if response.status_code in [200, 201]:
        print(Fore.GREEN + Style.BRIGHT + "Pet berhasil dibeli!")
        return response.status_code, response.json()
    else:
        print(Fore.RED + Style.BRIGHT + f"Gagal membeli pet. Status: {response.status_code}, Respon: {response.text}")
    return response.status_code, None

def select_pet(access_token, pet_data):
    pet_id = pet_data['id']
    url = f"https://api.pixelverse.xyz/api/pets/user-pets/{pet_id}/select"
    headers = {
        'Authorization': access_token,
        'Accept': 'application/json, text/plain, */*',
        'Content-Type': 'application/json',
        'Accept-Encoding': 'gzip, deflate, br, zstd',
        'Accept-Language': 'en-US,en;q=0.9',
        'Cache-Control': 'no-cache',
        'Origin': 'https://dashboard.pixelverse.xyz',
        'Referer': 'https://dashboard.pixelverse.xyz/',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, seperti Gecko) Chrome/126.0.0.0 Safari/537.36'
    }
    response = requests.post(url, headers=headers)
    if response.status_code == 200:
        print(Fore.GREEN + Style.BRIGHT + "Pet berhasil dipilih!")
        return True
    elif response.status_code == 201:
        print(Fore.GREEN + Style.BRIGHT + "Pet sudah dipilih sebelumnya.")
        return True
    else:
        print(Fore.RED + Style.BRIGHT + f"Gagal memilih pet. Status: {response.status_code}, Respon: {response.text}")
    return False

def claim_daily_reward(access_token):
    url = "https://api.pixelverse.xyz/api/daily-reward/complete"
    headers = {
        'Authorization': access_token,
        'Accept': 'application/json, text/plain, */*',
        'Content-Type': 'application/json',
        'Accept-Encoding': 'gzip, deflate, br, zstd',
        'Accept-Language': 'en-US,en;q=0.9',
        'Cache-Control': 'no-cache',
        'Origin': 'https://dashboard.pixelverse.xyz',
        'Referer': 'https://dashboard.pixelverse.xyz/',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, seperti Gecko) Chrome/126.0.0.0 Safari/537.36'
    }
    response = requests.post(url, headers=headers)
    if response.status_code == 200:
        print(Fore.GREEN + Style.BRIGHT + "Daily reward berhasil diklaim!")
        return True
    elif response.status_code == 201:
        print(Fore.GREEN + Style.BRIGHT + "Daily reward berhasil diklaim!")
        return True
    else:
        print(Fore.RED + Style.BRIGHT + f"Gagal mengklaim daily reward. Status: {response.status_code}, Respon: {response.text}")
    return False

def main():
    referral_code = input("Kode Referral: ")
    jumlah = int(input("Jumlah Referral: "))
    pet_id = "27977f52-997c-45ce-9564-a2f585135ff5"

    for i in range(jumlah):
        email = get_temp_email_address()
        if not email:
            print(Fore.RED + Style.BRIGHT + "Gagal membuat email sementara.")
            return
        
        email, password, account_id = create_temp_email(email)
        if not email:
            print(Fore.RED + Style.BRIGHT + "Gagal membuat email sementara.")
            return

        print(Fore.BLUE + Style.BRIGHT + f"[{i+1}] Email sementara berhasil dibuat: {email}")

        if request_otp(email):
            print(Fore.YELLOW + Style.BRIGHT + "OTP berhasil dikirim!")
        else:
            print(Fore.RED + Style.BRIGHT + "Gagal mengirim permintaan OTP.")
            return

        token = get_access_token(email, password)
        if not token:
            print(Fore.RED + Style.BRIGHT + "Gagal mendapatkan token akses.")
            return

        print(Fore.YELLOW + Style.BRIGHT + "Menunggu email OTP...")
        otp_email = None
        for _ in range(10):
            otp_email = get_latest_email(token)
            if otp_email:
                break
            time.sleep(10)

        if otp_email:
            print(Fore.YELLOW + Style.BRIGHT + "Email OTP diterima!")
            otp_content = otp_email.get('text', otp_email.get('intro', ''))
            otp = extract_otp(otp_content)
            if otp:
                print(Fore.YELLOW + Style.BRIGHT + f"Kode OTP: {otp}")

                verification_result = verify_otp(email, otp)
                if verification_result:
                    access_token = verification_result.get('tokens', {}).get('access')
                    refresh_token = verification_result.get('refresh_token')
                    if access_token:
                        print(Fore.GREEN + Style.BRIGHT + "Sukses mendapat token akses")
                    if refresh_token:
                        print(Fore.GREEN + Style.BRIGHT + "Sukses mendapat refresh token")
                    
                    status_code, referral_response = set_referral(referral_code, access_token)
                    
                    if status_code == 200:
                        referral_status = Fore.CYAN+ Style.BRIGHT + f"[{i+1}] Referral berhasil!"
                    else:
                        referral_status = Fore.RED + Style.BRIGHT + f"[{i+1}] Referral gagal!"
                    
                    update_username_and_bio(access_token)
                    
                    status_code, pet_data = buy_pet(access_token, pet_id)
                    if status_code in [200, 201] and pet_data:
                        if select_pet(access_token, pet_data):
                            if claim_daily_reward(access_token):
                                print(referral_status)
                else:
                    print(Fore.RED + Style.BRIGHT + "Verifikasi OTP gagal.")
            else:
                print(Fore.RED + Style.BRIGHT + "Gagal mengekstrak OTP dari email.")
        else:
            print(Fore.RED + Style.BRIGHT + "Email OTP tidak diterima dalam batas waktu.")

        time.sleep(5)

if __name__ == "__main__":
    main()
