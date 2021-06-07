from Crypto.Util.number import *
from functools import reduce
from operator import mul
from itertools import combinations
import sys
import socket, struct, telnetlib
from Crypto.Cipher import DES3
from time import time
from binascii import hexlify

# --- common funcs ---
def sock(remoteip, remoteport):
	s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	s.connect((remoteip, remoteport))
	return s, s.makefile('rw')

def read_until(f, delim='\n'):
	data = ''
	while not data.endswith(delim):
		data += f.read(1)
	return data

	
#HOSTはIPアドレスでも可
HOST, PORT = "dctf-chall-just-take-your-time.westeurope.azurecontainer.io", 9999
s, f = sock(HOST, PORT)
read_until(f)
recv_m = read_until(f).split()
x = int(recv_m[0])*int(recv_m[2])
s.send(str(x).encode()+b"\n")
tim = int(time()) #UNIXTIMEの取得
print(read_until(f))
enc = read_until(f).strip()
print(enc)
print("time: ",tim)
for _ in range(3):
	key = str(tim).zfill(16).encode("utf-8") #keyの設定
	cipher = DES3.new(key, DES3.MODE_CFB, b"00000000")
	pt = cipher.decrypt(long_to_bytes(int(enc,16)))
	s.send(pt+b"\n")
	recv_m = read_until(f).strip()
	if "guess" in recv_m:
		#はずれ
		tim += 1
	else:
		#あたり
		break 
while True: print(read_until(f))

#read_untilの使い方
#返り値があるのでprintするか、何かの変数に入れる
#1行読む：read_until(f)
#特定の文字まで読む：read_until(f,"input")
#配列に格納する：recv_m = read_until(f).split() or .strip()

#サーバーに何か送るとき
#s.send(b'1\n') : 1を送っている
#バイト列で送ること。str->bytesにするには、変数の後に.encode()
#必ず改行を入れること。終了ポイントが分からなくなる。ex) s.send(flag.encode() + b'\n')

