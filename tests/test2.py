from time import sleep
from threading import Thread


def mainthread():
    print('How are you?')
    sleep(1)
    print('Are you fine?')
    sleep(1)
    print('Thats great')


def otherthread():
    print('This should be written to our stdout')
    sleep(1.5)
    print('Is it?')
    print('А ЕСЛИ ТАК?')


Thread(target=otherthread).start()
mainthread()
