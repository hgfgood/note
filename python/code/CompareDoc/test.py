import difflib
line1 = '''
hgf
is
of
asdasd
'''.strip().splitlines()
line2 = '''
jxn
is
oof
asdasdasda
'''.strip().splitlines()
print type(line2)
d=difflib.Differ()
diff_message = d.compare(line1,line2)
print list(diff_message)

