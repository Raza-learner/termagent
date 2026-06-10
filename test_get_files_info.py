from functions.get_files_info import get_files_info

def print_line(directory,result):
    try:
        if directory == '.':
            print(f'Result for current directory:')
        else:
            print(f'Result for {directory} directory:')
        print(f"{result} \n")
    except Exception as e:
            return f'Error{e}'

print_line(".",get_files_info("calculator", "."))
print_line("pkg",get_files_info("calculator", "pkg"))
print_line("/bin",get_files_info("calculator", "../"))
print_line("../",get_files_info("calculator", "main.py"))
