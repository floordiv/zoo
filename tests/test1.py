# import subprocess
#
#
# with subprocess.Popen(('python3', 'test2.py'), stdout=subprocess.PIPE, stderr=subprocess.PIPE) as proc:
#     while True:
#         out = proc.stdout.read(1)
#
#         if out == b'' and proc.poll() is not None:
#             break
#
#         print(out.decode(), end='')
#
# print('\nProcess finished with return-code', proc.returncode)
from time import sleep


print('hello')
sleep(5)
print('I am just a test')
sleep(5)
print('So, don\'t be so angry, if something went wrong')
