import time
from bin.scripts.run import run


def main():
    file = '.'
    while True:
        run(file)
        time.sleep(1)


if __name__ == '__main__':
    main()
