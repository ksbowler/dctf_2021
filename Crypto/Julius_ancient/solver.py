enc = "rq7t{7vH_rFH_vI6_pHH1_qI67}"

table = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789"
assert len(table) == 62

for i in enc:
	if i in table:
		e = table.index(i)
		print(table[(e-14)%62],end="")
	else:
		print(i,end="")
print()


