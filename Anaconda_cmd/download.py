import subprocess


SUCCESS = r'Download successful!'
FAIL = r'Download fail!'


def download(res):
    with open('install.log', 'w+') as f:
        # 迭代输出
        for line in res.stdout.splitlines():
            print(line)
            f.write(line)
            f.write('\n')


if __name__ == '__main__':
    File = r'requirements.txt'
    result = subprocess.run(['python', '-m', 'pip', 'download', '-r', File, '-d', '.'],
                             stdout=subprocess.PIPE, text=True)
    download(result)
