import base64
f = open("cipher.txt","rb")
a = f.readline().strip()
while True:
	a = base64.b64decode(a)
	if b"dctf{" in a:
		print(a)
		break
