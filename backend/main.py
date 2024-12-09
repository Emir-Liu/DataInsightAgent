
import os
from dotenv import load_dotenv

load_dotenv()

print(f'environment:')
for key, value in os.environ.items():
    print(f'{key}: {value}')


if __name__ == '__main__':
    print(f'开始执行主程序')
    