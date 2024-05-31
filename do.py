def main():
    file = '.'
    while True:
        run(file)
        time.sleep(1)


if __name__ == '__main__':
    print('正在加载……')
    import time
    from bin.scripts.run import run
    main()
