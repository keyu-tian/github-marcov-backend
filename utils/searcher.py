import argparse
import os

from colorama import Fore


def walk_check(dirname, key):
    project_root_path = os.getcwd()
    lines = 0
    for path, dirs, files in os.walk(dirname):
        if any(s in path for s in ['__pycache__', 'migrations', 'frontend']):
            continue
        temp_cwd = os.getcwd()
        os.chdir(path)
        for f_name in files:
            if not f_name.endswith('.py'):
                continue
            with open(f_name, encoding='utf-8') as fp:
                contains = []
                for i, line in enumerate(fp):
                    lines += 1
                    if key in line:
                        contains.append(i+1)
                if len(contains) == 0:
                    continue
                rel_path = os.path.join(os.path.relpath(os.getcwd(), project_root_path), f_name)
                print(f'`{key}` found in  {rel_path:30s}:  [line {str(contains).strip("[]")}]')
                # print(f''
                #       + Fore.GREEN + f'`{key}`' + Fore.RESET + ' found in '
                #       + Fore.CYAN + f' {f_name:20s}' + Fore.RESET + ': '
                #       + Fore.BLUE + f'[line {str(lines).strip("[]")}]' + Fore.RESET)
        os.chdir(temp_cwd)
        
    if dirname in ['.', './', '.\\']:
        print(f'\n[total lines of MarCov-19 backend: {lines}]')


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('dir', type=str, default='.')
    parser.add_argument('key', type=str, default=None)
    args = parser.parse_args()
    # if args.key is None:
    #     args.key = input('please input the key: ')
    walk_check(args.dir, args.key)
