import re
import os


EMAIL_REGEX = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
DATE_REGEX = r'^\d{2}\.\d{2}\.\d{4}$'
PHONE_REGEX = r'^\+?38?0?\s?\(?\d{2}\)?[\s-]?\d{3}[\s-]?\d{2,4}[\s-]?\d{2}$'

def normalize_phone(phone: str) -> str:
    """Приводить телефон до єдиного формату +38 (0XX) XXX-XX-XX"""
    digits = re.sub(r'\D', '', phone)
    if digits.startswith('38'):
        digits = digits[2:]
    if digits.startswith('8'):
        digits = digits[1:]
    if digits.startswith('0'):
        digits = digits[1:]
    
    if len(digits) == 9:
        digits = '0' + digits
        
    return f"+38 ({digits[0:3]}) {digits[3:6]}-{digits[6:8]}-{digits[8:10]}"

def process_employees(file_list):
    valid_data = []
    log_data = []

    for file_path in file_list:
        if not os.path.exists(file_path):
            continue
            
        with open(file_path, 'r', encoding='utf-8') as f:
            for line_no, line in enumerate(f, 1):
                parts = [p.strip() for p in line.split(',')]
                if len(parts) < 6:
                    log_data.append(f"FILE: {file_path}, LINE: {line_no} | Error: Missing fields | DATA: {line}")
                    continue

                name, surname, dob, phone, email, pos = parts
                
                is_valid = (re.match(DATE_REGEX, dob) and 
                            re.match(EMAIL_REGEX, email) and 
                            re.match(PHONE_REGEX, phone))

                if is_valid:
                    norm_phone = normalize_phone(phone)
                    valid_entry = f"{name}, {surname}, {dob}, {norm_phone}, {email}, {pos} | ORIGIN: {file_path}, LINE: {line_no}"
                    valid_data.append(valid_entry)
                else:
                    log_data.append(f"FILE: {file_path}, LINE: {line_no} | Error: Validation failed | DATA: {line}")

    with open('valid_employees.txt', 'w', encoding='utf-8') as f:
        f.write('\n'.join(valid_data))
    
    with open('invalid_log.log', 'w', encoding='utf-8') as f:
        f.write('\n'.join(log_data))






import re
import pickle
from datetime import datetime, timedelta

# Пароль: мін 12 символів, 1 літера, 1 цифра, 1 спецсимвол
PASSWORD_STRICT = r'^(?=.*[a-zA-Z])(?=.*\d)(?=.*[.,?!@#$%^&*()_+={}\[\]|\\:;"\'<>,/~`-]).{12,}$'

def process_clients(filename):
    old_clients = []
    bad_passwords = []
    to_notify = []
    
    one_year_ago = datetime.now() - timedelta(days=365)

    with open(filename, 'r', encoding='utf-8') as f:
        for line in f:
            # Припускаємо формат: id, username, password, email, last_login
            parts = [p.strip() for p in line.strip().split(',')]
            if len(parts) < 5: continue
            
            client_id, user, pwd, email, last_login = parts
            login_date = datetime.strptime(last_login, '%Y-%m-%d')

            client_info = {
                'id': client_id,
                'user': user,
                'pwd': pwd,
                'email': email,
                'last_login': last_login
            }

            # 1. Перевірка дати входу (> 1 року тому)
            if login_date < one_year_ago:
                old_clients.append(client_info)
            else:
                # 3. Система сповіщення (зайшли менше року тому)
                to_notify.append(email)

            # 2. Перевірка пароля
            if not re.match(PASSWORD_STRICT, pwd):
                bad_passwords.append(client_info)

    # Збереження у pickle
    with open('inactive_clients.pkl', 'wb') as f:
        pickle.dump(old_clients, f)
        
    with open('weak_passwords.pkl', 'wb') as f:
        pickle.dump(bad_passwords, f)

    # Вивід сповіщень
    print("--- Система сповіщення про оновлення паролю ---")
    for email in to_notify:
        print(f"Надсилання листа на {email}: Будь ласка, оновіть свій пароль згідно з новими стандартами безпеки!")


process_employees(['employees.txt'])
process_clients('clients.txt')