from sky import Sky
s = Sky(400)
alpha = (6 + 45 / 60 + 08.917 / 3600) * 15
delta = -16 - 42 / 60 - 58.02 / 3600
s.read_frame_tyc()
fid = s.id_frame_tyc(alpha, delta)
print(fid)
