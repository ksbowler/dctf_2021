from Crypto.Util.number import *
from functools import reduce
from operator import mul
from itertools import combinations
import sys
import socket, struct, telnetlib
from string import ascii_letters, digits
from random import SystemRandom
from math import ceil, log
from signal import signal, alarm, SIGALRM
from tqdm import tqdm

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


def decrypt(enc,table):
	message = list(enc)
	pt = list(enc)
	rounds = int(2 * ceil(log(len(message), 2)))
	for r in range(rounds-1,-1,-1):
		if r < rounds-1:
			ppt = ["a" for _ in range(len(pt))]
			for j in range(len(pt)):
				if j%2 == 0:
					ppt[j] = pt[len(pt)//2+j//2]
				else:
					ppt[j] = pt[j//2]
			
			pt = ppt
		ppt = []
		for j in range(len(pt)):
			ppt.append(table[pt[j]])
		pt = ppt
	return ''.join(pt)


ALPHABET = ascii_letters + digits + "_!@#$%.'\"+:;<=}{"
l = len(ALPHABET)
#HOSTはIPアドレスでも可
HOST, PORT = "dctf1-chall-sp-box.westeurope.azurecontainer.io", 8888
while True:
	s, f = sock(HOST, PORT)
	read_until(f)
	enc = read_until(f).strip()
	b1 = []
	bef = "a"
	#b1.append(bef)
	for i in tqdm(range(l//2)):
		read_until(f,"> ")
		s.send(bef.encode()+b"\n")
		read_until(f)
		recv_m = read_until(f).strip()
		b1.append(recv_m[-1])
		bef = b1[-1]

	#assert list(set(b1)) == l//2
	print("b1")
	print(b1)
	if len(list(set(b1))) != l//2:
		print("NG b1 :",len(list(set(b1))))
		s.close()
		continue
	if b1[-1] != "a":
		print("NG b1 because the last is not a")
		s.close()
		continue

	b2 = []
	for x in ALPHABET:
		if x in b1: continue
		bef = x
		print("b2",x)
		break
#b2.append(bef)
	for i in tqdm(range(l//2)):
		#bef = b2[-1]
		read_until(f,"> ")
		s.send(bef.encode()+b"\n")
		read_until(f)
		recv_m = read_until(f).strip()
		b2.append(recv_m[-1])
		bef = b2[-1]

	#assert list(set(b2)) == l//2
	print("b2")
	print(b2)
	if len(list(set(b2))) != l//2:
		print("NG b2 :",len(list(set(b2))))
		s.close()
		continue

	rev_table = {}
	for j in range(len(b2)):
		rev_table[b1[j]] = b2[j]
		rev_table[b2[j]] = b1[(j+1)%len(b1)]
	table = {}
	for k,v in rev_table.items():
 		table[v] = k
	print(decrypt(enc,table))

	s.close()
	break
#read_untilの使い方
#返り値があるのでprintするか、何かの変数に入れる
#1行読む：read_until(f)
#特定の文字まで読む：read_until(f,"input")
#配列に格納する：recv_m = read_until(f).split() or .strip()

#サーバーに何か送るとき
#s.send(b'1\n') : 1を送っている
#バイト列で送ること。str->bytesにするには、変数の後に.encode()
#必ず改行を入れること。終了ポイントが分からなくなる。ex) s.send(flag.encode() + b'\n')

