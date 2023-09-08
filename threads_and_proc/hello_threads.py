import time
import threading


def main():
    threads = [threading.Thread(target=greeter, args=('Vasya', 3), daemon=True),
               threading.Thread(target=greeter, args=('Petya', 4), daemon=True),
               threading.Thread(target=greeter, args=('Masha', 2), daemon=True)]
    [thread.start() for thread in threads]
    print('main')
    [thread.join() for thread in threads]
    print('done')


def greeter(name, times):
    for _ in range(times):
        print(f'Hello {name}')
        time.sleep(1)


if __name__ == '__main__':
    main()
