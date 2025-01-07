# Имя входного и выходного файлов
input_file = "channels_full.txt"
output_file = "channels_packed.txt"

# Читаем строки из файла, обрабатываем и сортируем
with open(input_file, "r", encoding="utf-8") as file:
    # Читаем строки, удаляем пробелы и переводим в нижний регистр для обработки
    lines = file.readlines()
    unique_lines = sorted(set(line.strip().lower() for line in lines))  # Уникальные строки, сортируем по нижнему регистру

# Записываем результат в новый файл, возвращая оригинальный регистр
with open(output_file, "w", encoding="utf-8") as file:
    file.writelines(f"{line}\n" for line in unique_lines)

print(f"Сортированный файл без дубликатов записан в {output_file}")