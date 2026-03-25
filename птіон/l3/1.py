import os
import sys

def dirsize(path):
    """Функція, що повертає розмір однієї директорії (каталогу)"""
    size = 0
    for root, dirs, files in os.walk(path):
        size += sum(os.path.getsize(os.path.join(root, name)) for name in files)
    return size

def dirslist(directory):
    """Функція, що повертає список пар (каталог, розмір)"""
    dir_list = os.listdir(directory)
    dirs_sizes = []

    for dir in dir_list:
        path = os.path.join(directory, dir)

        if os.path.isdir(path):
            dirs_sizes.append((path, dirsize(path)))

    dirs_sizes.sort(reverse=True, key=lambda x: x[1])
    return dirs_sizes

if __name__ == '__main__':
    if len(sys.argv) == 1:
        directory = input('Input directory name: ')
    else:
        directory = sys.argv[1]
        
    dirs_sizes = dirslist(directory)

    # 1. Створюємо окремий каталог для файлу
    output_dir = "output_results"
    if not os.path.exists(output_dir):
        os.mkdir(output_dir)

    output_file_path = os.path.join(output_dir, 'dirslist.txt')

    # 2. Зберігаємо оригінальний стандартний вивід
    original_stdout = sys.stdout

    # 3. Перенаправляємо вивід у файл
    with open(output_file_path, 'w', encoding='utf-8') as f:
        sys.stdout = f
        
        # Усі ці принти тепер записуватимуться безпосередньо у dirslist.txt
        for _ in dirs_sizes:
            print(f'directory: {_[0]}, size: {_[1]}')

    # 4. Відновлюємо стандартний вивід у консоль
    sys.stdout = original_stdout
    print(f"Готово! Результати збережено у: {output_file_path}")