import os
import filecmp
import math

def levenshtein_dist(a, b):   # вычисляет расстояние Левенштейна, имеет асимтотику по рамяти O(min(длина(y), длина(x))), по времени O(длина(y) * длина(x))
    n, m = len(a), len(b)
    if n > m:
        # убедимся что n <= m, чтобы использовать минимум памяти O(min(n, m))
        a, b = b, a
        n, m = m, n
    current_row = range(n + 1)
    for i in range(1, m + 1):
        previous_row, current_row = current_row, [i] + [0] * n
        for j in range(1, n + 1):
            add = previous_row[j] + 1
            delete = current_row[j - 1] + 1
            change = previous_row[j - 1]
            if a[j - 1] != b[i - 1]:
                change += 1
            current_row[j] = min(add, min(delete, change))
    return current_row[n]

def lcs_length(x, y):  # длина наибольшей общей подпоследовательности, имеет асимтотику по рамяти O(длина y), по времени O(длина(y) * длина(x))
    curr = [0]*(1 + len(y))
    for x_elem in x:
        prev = curr[:]
        for y_i, y_elem in enumerate(y):
            if x_elem == y_elem:
                curr[y_i + 1] = prev[y_i] + 1
                continue
            curr[y_i + 1] = max(curr[y_i], prev[y_i + 1])
    return curr

def get_files(directory):
    files = []
    for root, _, filenames in os.walk(directory):
        for filename in filenames:
            files.append(os.path.join(root, filename))
    return files
    
def calculate_similarity(file1, file2, mode='lev_dist'):
    result = 0
    with open(file1, 'rb') as f1, open(file2, 'rb') as f2:  # 'rb' только чтение, открываем файлы в бинарном виде
        content1 = f1.read()
        content2 = f2.read()
        
        max_length = max(len(content1), len(content2))
        
        if 'lcs' == mode:
            result = lcs_length(content1, content2) / max_length
            
        if 'lev_dist' == mode:
            result = 1 - levenshtein_dist(content1, content2) / max_length
        
        '''
        if '...' == mode:   другой метод сравнения
            similarty = ...
        '''
        
        return result
          
def compare_directories(dir1, dir2, similarity_criterion):
    identical_files = []             # список идентичных файлов
    similar_files = []               # список схожих файлов
    exist_sim_file1 = set()          # файлы из директории 2, у которых есть схожий или идентичный файл из директория 1
    missing_files_dir1 = set()       # файлы из директории 2, отсутствующие в директории 1 
    missing_files_dir2 = set()       # файлы из директории 1, отсутствующие в директории 2
    
    files_dir1 = get_files(dir1)
    files_dir2 = get_files(dir2)
    
    for file1 in files_dir1:
        found_identical = False
        found_similar = False
        
        for file2 in files_dir2:
            if filecmp.cmp(file1, file2):
                identical_files.append((file1, file2))
                exist_sim_file1.add(file2)
                found_identical = True
                continue
            
            similarity = calculate_similarity(file1, file2)
            if similarity >= similarity_criterion:
                similar_files.append((file1, file2, similarity))
                exist_sim_file1.add(file2)
                found_similar = True
        
        if not found_identical and not found_similar:
            missing_files_dir2.add(file1)
    
    for file2 in files_dir2:
        if file2 not in exist_sim_file1:
            missing_files_dir1.add(file2)
            
    return identical_files, similar_files, missing_files_dir2, missing_files_dir1


if __name__ == '__main__':
    dir1 = str(input("Введите путь к первой директории: "))
    dir2 = str(input("Введите путь ко второй директории: "))
    similarity_criterion = int(input("Введите минимальный процент сходства: ")) / 100
    
    identical_files, similar_files, missing_files_dir2, missing_files_dir1 = compare_directories(dir1, dir2, similarity_criterion)

    print("Идентичные файлы:")
    for file_pair in identical_files:
        print(f"{file_pair[0]} - {file_pair[1]}")
    
    print("Похожие файлы:")
    for file_info in similar_files:
        print(f"{file_info[0]} - {file_info[1]} - {file_info[2]*100}%")
    
    print("Файлы, отсутствующие в директории 2:")
    for file in missing_files_dir2:
        print(file)
    
    print("Файлы, отсутствующие в директории 1:")
    for file in missing_files_dir1:
        print(file)

