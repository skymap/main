def print_area(f, pid, alpha_min, alpha_max, delta_min, delta_max):
    for k, v in f.items():
        if v[0] >= alpha_min and v[0] <= alpha_max and v[1] >= delta_min and v[1] <= delta_max:
            print(k + ',' + pid + ',4,' + '{:.3f}'.format(alpha_min) + ',' + '{:.3f}'.format(alpha_max) + ',' + '{:.3f}'.format(delta_min) + ',' + '{:.3f}'.format(delta_max) + ',30')


r = open('index.csv', 'r')
src = r.read()
r.close
f = {}
rows = src.split('\n')
for row in rows:
    v = row.split(',')
    f[v[0]] = [float(v[1]), float(v[2])]
r = open('frame_tmp.csv', 'r')
src = r.read()
r.close
rows = src.split('\n')
for row in rows:
    v = row.split(',')
    pid = v[0]
    alpha_min_src = float(v[1])
    alpha_max_src = float(v[2])
    delta_min_src = float(v[3])
    delta_max_src = float(v[4])
    d = int(v[5])
    alpha_d = (alpha_max_src - alpha_min_src) / d
    delta_d = (delta_max_src - delta_min_src) / d
    for delta_i in range(d):
        delta_min = delta_d * delta_i + delta_min_src
        delta_max = delta_d * (delta_i + 1) + delta_min_src
        for alpha_i in range(d):
            alpha_min = alpha_d * alpha_i + alpha_min_src
            alpha_max = alpha_d * (alpha_i + 1) + alpha_min_src
            print_area(f, pid, alpha_min, alpha_max, delta_min, delta_max)
