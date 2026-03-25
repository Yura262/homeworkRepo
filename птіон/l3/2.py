import os
import datetime
import sys
import tarfile
import shutil

def archivesubdirs(backupdir):
    """Функція для архівації всіх підкаталогів та їх подальшого видалення"""
    backupdir = os.path.normpath(backupdir) 
    
    # Якщо каталогу бекапів ще немає, створюємо його і виходимо
    if not os.path.exists(backupdir):
        os.makedirs(backupdir, exist_ok=True)
        return

    lst = os.listdir(backupdir)

    for name in lst:
        full_name = os.path.join(backupdir, name)

        if os.path.isdir(full_name):
            try:
                # Архівуємо
                with tarfile.open(full_name + '.tar.gz', 'w:gz') as tf:
                    # arcname=name гарантує, що в архіві буде папка, а не повний шлях C:\...
                    tf.add(full_name, arcname=name)
                
                # Використовуємо shutil для миттєвого видалення каталогу з усім вмістом
                shutil.rmtree(full_name)
            except Exception as e:
                print('Помилка архівації/видалення', name, e, sep='\n')

def getbackupname(backupdir):
    """Функція, що повертає ім’я нового каталогу з поточної дати та часу."""
    dt = datetime.datetime.now()
    dirname = dt.strftime('%Y%m%d_%H%M%S')
    return os.path.join(backupdir, dirname)

def backupdirectories(directories, backupdir):
    """Функція, що зберігає файли із зазначених каталогів у каталозі backup"""
    archivesubdirs(backupdir)  # Архівуємо попередні версії

    toparent = getbackupname(backupdir)
    os.makedirs(toparent, exist_ok=True)

    for src_dir in directories:
        src_dir = os.path.normpath(src_dir)
        
        if not os.path.exists(src_dir):
            print(f'Каталог "{src_dir}" не знайдено. Пропускаємо.')
            continue
            
        last_dir_name = os.path.split(src_dir)[-1]
        dest_dir = os.path.join(toparent, last_dir_name)
        
        try:
            # shutil.copytree автоматично створює цільову директорію і копіює все туди
            shutil.copytree(src_dir, dest_dir)
            print(f'Скопійовано: {src_dir} -> {dest_dir}')
        except Exception as e:
            print(f'Пропущено директорію {src_dir}.\n', e)

if __name__ == '__main__':
    if len(sys.argv) < 3:
        backupdir = input('Введіть backup-каталог: ').strip(' \'"')
        user_input = input("Введіть імена каталогів для бекапу через кому:\n")
        directories = [d.strip(' \'"') for d in user_input.split(",") if d.strip()]
    else:
        backupdir = sys.argv[1]
        directories = sys.argv[2:]
        
    backupdirectories(directories, backupdir)