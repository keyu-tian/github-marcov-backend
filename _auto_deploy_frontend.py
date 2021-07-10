import os

import colorama


def main():
    colorama.init(autoreset=True)
    os.chdir('frontend')
    newist_zip = sorted(filter(lambda s: s.endswith('.zip'), os.listdir()), key=os.path.getatime)[-1]
    print(colorama.Fore.GREEN + '[newist_zip]: ' + colorama.Fore.WHITE + newist_zip)
    os.system(f'rm -rf dist; unzip "{newist_zip}" >/dev/null 2>&1')
    

if __name__ == '__main__':
    main()
