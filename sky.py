import math, svgwrite, sys, time


class Sky():
    prefix = 'hip'
    font_size = 12
    font_family = 'monospace'
    star_r = [255, 203, 162, 129, 103, 82, 65, 52, 41, 33, 26, 21, 17, 13, 11, 8]
    area_l2 = [3, 9, 15, 21, 27, 32, 36, 40, 43, 45, 47, 48]
    f1 = {}
    f2 = {}
    f3 = {}
    star = {}
    line = []

    def __init__(self, r=400, tyc=False):
        self.time_start = time.time()
        self.image_r = r
        if tyc:
            for i in range(16):
                self.star_r[i] = self.star_r[i] * r * 0.00015
        else:
            for i in range(16):
                if i < 9:
                    self.star_r[i] = self.star_r[i] * r * 0.000045
                else:
                    self.star_r[i] = self.star_r[8]

    def init_area(self, fid=0, alpha_min=0, alpha_center=0, alpha_max=360, delta_min=0, delta_center=90, delta_max=90, x=0.9, mag_max=6, tyc=False):
        file_name = 'tyc{:04}'.format(fid) if tyc else 'hip{:03}'.format(fid)
        self.g = svgwrite.Drawing('svg\\' + file_name + '.svg', (self.image_r * 2, self.image_r * 2), profile='tiny', debug=False)
        self.alpha0 = math.radians(alpha_center)
        self.delta0 = math.radians(delta_center)
        self.alpha_center = alpha_center
        self.delta_center = delta_center
        self.alpha_max = alpha_max
        self.delta_max = delta_max
        self.alpha_min = alpha_min
        self.delta_min = delta_min
        self.mag_max = mag_max
        self.sphere_r = self.image_r * x
        self.g.add(self.g.rect((0, 0), (self.image_r * 2, self.image_r * 2), fill='none', stroke='black', stroke_width='2'))

    def read_frame_hip(self):
        r = open('frame_hip.csv', 'r')
        src = r.read()
        r.close
        rows = src.split('\n')
        for row in rows:
            d = row.split(',')
            fid = int(d[0])
            pid = int(d[1])
            l = int(d[2])
            alpha_min = float(d[3])
            alpha_max = float(d[4])
            delta_min = float(d[5])
            delta_max = float(d[6])
            x = float(d[7])
            if l == 0:self.fs = [0, alpha_min, 180, alpha_max, delta_min, -90, delta_max, x]
            if l == 1:self.fn = [0, alpha_min, 0, alpha_max, delta_min, 90, delta_max, x]
            if l == 2:self.f1[fid] = [pid, alpha_min, (alpha_min + alpha_max) / 2, alpha_max, delta_min, (delta_min + delta_max) / 2, delta_max, x]
            if l == 3:self.f2[fid] = [pid, alpha_min, (alpha_min + alpha_max) / 2, alpha_max, delta_min, (delta_min + delta_max) / 2, delta_max, x]

    def read_frame_tyc(self):
        r = open('frame_tyc.csv', 'r')
        src = r.read()
        r.close
        rows = src.split('\n')
        for row in rows:
            d = row.split(',')
            fid = int(d[0])
            pid = int(d[1])
            alpha_min = float(d[2])
            alpha_max = float(d[3])
            delta_min = float(d[4])
            delta_max = float(d[5])
            x = float(d[6])
            self.f3[fid] = [pid, alpha_min, (alpha_min + alpha_max) / 2, alpha_max, delta_min, (delta_min + delta_max) / 2, delta_max, x]

    def read_line(self):
        r = open('line.csv', 'r')
        src = r.read()
        r.close
        rows = src.split('\n')
        for row in rows:
            d = row.split(',')
            self.line.append([float(d[1]), float(d[2]), float(d[3]), float(d[4])])

    def read_star(self, tyc=False):
        r = open('hip_basic.csv', 'r')
        src = r.read()
        r.close
        rows = src.split('\n')
        for row in rows:
            d = row.split(',')
            self.star[d[0]] = [float(d[1]), float(d[2]), int(d[3])]
        if tyc:
            r = open('tyc_basic.csv', 'r')
            src = r.read()
            r.close
            rows = src.split('\n')
            for row in rows:
                d = row.split(',')
                k = d[0] + '_' + d[1] + '_' + d[2]
                self.star[k] = [float(d[3]), float(d[4]), int(d[5])]

    def read_star_tyc(self):
        self.star_hip = {}
        for i in range(16):
            self.star_hip[i] = {}
        r = open('hip_basic.csv', 'r')
        src = r.read()
        r.close
        rows = src.split('\n')
        for row in rows:
            d = row.split(',')
            self.star_hip[int(d[3])][d[0]] = [float(d[1]), float(d[2])]
        self.star_tyc = {}
        for i in range(9537):
            self.star_tyc[i] = {}
            for j in range(16):
                self.star_tyc[i][j] = {}
        r = open('tyc_basic.csv', 'r')
        src = r.read()
        r.close
        rows = src.split('\n')
        for row in rows:
            d = row.split(',')
            k = d[1] + '_' + d[2]
            self.star_tyc[int(d[0]) - 1][int(d[5])][k] = [float(d[3]), float(d[4])]

    def save_img(self):
        self.g.save()

    def draw_star(self):
        for v in self.star.values():
            alpha = v[0]
            delta = v[1]
            mag = v[2]
            if self.in_alpha(alpha) and self.in_delta(delta) and mag < self.mag_max:
                x, y = self.xy(math.radians(alpha), math.radians(delta))
                self.g.add(self.g.circle((x, y), self.star_r[mag], fill='black', stroke='white', stroke_width='0.25'))

    def draw_star_tyc(self, fid):
        for k, p in self.star_hip.items():
            for v in p.values():
                alpha = v[0]
                delta = v[1]
                if self.in_alpha(alpha) and self.in_delta(delta):
                    x, y = self.xy(math.radians(alpha), math.radians(delta))
                    self.g.add(self.g.circle((x, y), self.star_r[k], fill='black', stroke='white', stroke_width='0.25'))
        for k, p in self.star_tyc[fid].items():
            for v in p.values():
                alpha = v[0]
                delta = v[1]
                x, y = self.xy(math.radians(alpha), math.radians(delta))
                self.g.add(self.g.circle((x, y), self.star_r[k], fill='black', stroke='white', stroke_width='0.25'))

    def draw_constellation_lines(self):
        for v in self.line:
            alpha1 = v[0]
            delta1 = v[1]
            alpha2 = v[2]
            delta2 = v[3]
            if self.in_alpha(alpha1) and self.in_alpha(alpha2) and self.in_delta(delta1) and self.in_delta(delta2):
                x1, y1 = self.xy(math.radians(alpha1), math.radians(delta1))
                x2, y2 = self.xy(math.radians(alpha2), math.radians(delta2))
                self.g.add(self.g.line((x1, y1), (x2, y2), fill='none', stroke='green', stroke_opacity='0.5', stroke_width='1.5'))

    def draw_alpha_lines(self, d=15):
        for alpha_i in range(int(360 / d)):
            alpha = alpha_i * d
            if self.in_alpha(alpha):
                self.draw_alpha_line(math.radians(alpha), 'silver')

    def draw_alpha_line(self, alpha=0, color='silver'):
        p = []
        x, y = self.xy(alpha, math.radians(self.delta_min))
        p.append([x, y])
        for delta_d in range(1441):
            delta = delta_d * 0.125 - 90
            if delta > self.delta_min and delta < self.delta_max:
                x, y = self.xy(alpha, math.radians(delta))
                p.append([x, y])
        x, y = self.xy(alpha, math.radians(self.delta_max))
        p.append([x, y])
        self.g.add(self.g.polyline(p, fill='none', stroke=color, stroke_width='0.5', stroke_opacity='0.5'))

    def draw_alpha_text(self, d=15):
        delta_str = math.radians(self.delta_max) if self.delta_min < 0 else math.radians(self.delta_min)
        for alpha_i in range(int(360 / d)):
            alpha = alpha_i * d
            if self.in_alpha(alpha):
                str_alpha = self.str_hh(alpha) if d >= 15 else self.str_hhmm(alpha)
                x, y = self.xy(math.radians(alpha), delta_str)
                self.g.add(self.g.text(str_alpha, (x, y), fill='gray', fill_opacity='0.5', font_size=self.font_size, font_family=self.font_family))

    def draw_delta_lines(self, d=10):
        for delta_i in range(int(180 / d) + 1):
            delta = delta_i * d - 90
            if self.in_delta(delta):
                self.draw_delta_line(math.radians(delta), 'silver')

    def draw_delta_line(self, delta=0, color='silver'):
        p = []
        x, y = self.xy(math.radians(self.alpha_min), delta)
        p.append([x, y])
        for alpha_d in range(2881):
            alpha = alpha_d * 0.125
            if alpha > self.alpha_min and alpha < self.alpha_max:
                x, y = self.xy(math.radians(alpha), delta)
                p.append([x, y])
        x, y = self.xy(math.radians(self.alpha_max), delta)
        p.append([x, y])
        self.g.add(self.g.polyline(p, fill='none', stroke=color, stroke_width='0.5', stroke_opacity='0.5'))

    def draw_delta_text(self, d=10):
        alpha_str = math.radians(self.alpha_max)
        for delta_i in range(int(180 / d) + 1):
            delta = delta_i * d - 90
            if self.in_delta(delta):
                str_delta = self.str_deg(delta)
                x, y = self.xy(alpha_str, math.radians(delta))
                self.g.add(self.g.text(str_delta, (x, y), fill='gray', fill_opacity='0.5', font_size=self.font_size, font_family=self.font_family))

    def draw_frame(self, top=True, right=True, bottom=True, left=True):
        if top:self.draw_delta_line(math.radians(self.delta_max), 'black')
        if right:self.draw_alpha_line(math.radians(self.alpha_min), 'black')
        if bottom:self.draw_delta_line(math.radians(self.delta_min), 'black')
        if left:self.draw_alpha_line(math.radians(self.alpha_max), 'black')

    def draw_frame_link(self, fid, alpha_min, alpha_max, delta_min, delta_max, file_name, color):
        p = []
        alpha_min_rad = math.radians(alpha_min)
        alpha_max_rad = math.radians(alpha_max)
        delta_min_rad = math.radians(delta_min)
        delta_max_rad = math.radians(delta_max)
        x, y = self.xy((alpha_min_rad + alpha_max_rad) / 2, (delta_min_rad + delta_max_rad) / 2)
        self.g.add(self.g.text(str(fid), (x, y), fill=color, fill_opacity='0.7', font_size=self.font_size, font_family=self.font_family))
        x, y = self.xy(alpha_min_rad, delta_min_rad)
        p.append([x, y])
        for alpha_d in range(2881):
            alpha = alpha_d * 0.125
            if alpha > alpha_min and alpha < alpha_max:
                x, y = self.xy(math.radians(alpha), delta_min_rad)
                p.append([x, y])
        x, y = self.xy(alpha_max_rad, delta_min_rad)
        p.append([x, y])
        for delta_d in range(1441):
            delta = delta_d * 0.125 - 90
            if delta > delta_min and delta < delta_max:
                x, y = self.xy(alpha_max_rad, math.radians(delta))
                p.append([x, y])
        x, y = self.xy(alpha_max_rad, delta_max_rad)
        p.append([x, y])
        for alpha_d in range(2881):
            alpha = 360 - alpha_d * 0.125
            if alpha > alpha_min and alpha < alpha_max:
                x, y = self.xy(math.radians(alpha), delta_max_rad)
                p.append([x, y])
        x, y = self.xy(alpha_min_rad, delta_max_rad)
        p.append([x, y])
        for delta_d in range(1441):
            delta = 90 - delta_d * 0.125
            if delta > delta_min and delta < delta_max:
                x, y = self.xy(alpha_min_rad, math.radians(delta))
                p.append([x, y])
        link = self.g.add(self.g.a(file_name + '.svg', target='_self'))
        link.add(self.g.polygon(p, stroke=color, stroke_opacity='0.7', stroke_width='0.5', fill=color, fill_opacity='0'))

    def draw_header_link(self, fid, l):
        if l == 0 or l == 1:
            v = self.fs
            text = 'No.1 ' + self.str_hh(v[1]) + ' ' + self.str_hh(v[3]) + ' ' + self.str_deg(v[4]) + self.str_deg(v[6])
            if l == 0:
                self.g.add(self.g.text('> ' + text, (self.font_size, self.font_size * 2), fill='black', font_size=self.font_size, font_family=self.font_family))
            else:
                link = self.g.add(self.g.a(self.prefix + '001.svg', target='_self'))
                link.add(self.g.text(text, (self.font_size, self.font_size * 2), fill='black', font_size=self.font_size, font_family=self.font_family))
            v = self.fn
            text = 'No.2 ' + self.str_hh(v[1]) + ' ' + self.str_hh(v[3]) + ' ' + self.str_deg(v[4]) + self.str_deg(v[6])
            if l == 1:
                self.g.add(self.g.text('> ' + text, (self.font_size, self.font_size * 3), fill='black', font_size=self.font_size, font_family=self.font_family))
            else:
                link = self.g.add(self.g.a(self.prefix + '002.svg', target='_self'))
                link.add(self.g.text(text, (self.font_size, self.font_size * 3), fill='black', font_size=self.font_size, font_family=self.font_family))
        elif l == 2:
            v = self.f1[fid]
            text = '> No.' + str(fid) + ' ' + self.str_hhmm(v[1]) + ' ' + self.str_hhmm(v[3]) + ' ' + self.str_deg(v[4]) + self.str_deg(v[6])
            self.g.add(self.g.text(text, (self.font_size, self.font_size * 3), fill='black', font_size=self.font_size, font_family=self.font_family))
            pid = v[0]
            if pid == 1:
                v = self.fs
            elif pid == 2:
                v = self.fn
            text = 'No.' + str(pid) + ' ' + self.str_hh(v[1]) + ' ' + self.str_hh(v[3]) + ' ' + self.str_deg(v[4]) + self.str_deg(v[6])
            link = self.g.add(self.g.a(self.prefix + '{:03}'.format(pid) + '.svg', target='_self'))
            link.add(self.g.text(text, (self.font_size, self.font_size * 2), fill='black', font_size=self.font_size, font_family=self.font_family))
        elif l == 3:
            v = self.f2[fid]
            text = '>> No.' + str(fid) + ' ' + self.str_hhmm(v[1]) + ' ' + self.str_hhmm(v[3]) + ' ' + self.str_deg(v[4]) + self.str_deg(v[6])
            self.g.add(self.g.text(text, (self.font_size, self.font_size * 4), fill='black', font_size=self.font_size, font_family=self.font_family))
            pid = v[0]
            v = self.f1[pid]
            text = '> No.' + str(pid) + ' ' + self.str_hhmm(v[1]) + ' ' + self.str_hhmm(v[3]) + ' ' + self.str_deg(v[4]) + self.str_deg(v[6])
            link = self.g.add(self.g.a(self.prefix + '{:03}'.format(pid) + '.svg', target='_self'))
            link.add(self.g.text(text, (self.font_size, self.font_size * 3), fill='black', font_size=self.font_size, font_family=self.font_family))
            pid = v[0]
            if pid == 1:
                v = self.fs
            elif pid == 2:
                v = self.fn
            text = 'No.' + str(pid) + ' ' + self.str_hh(v[1]) + ' ' + self.str_hh(v[3]) + ' ' + self.str_deg(v[4]) + self.str_deg(v[6])
            link = self.g.add(self.g.a(self.prefix + '{:03}'.format(pid) + '.svg', target='_self'))
            link.add(self.g.text(text, (self.font_size, self.font_size * 2), fill='black', font_size=self.font_size, font_family=self.font_family))

    def draw_header_tyc(self, fid):
        v = self.f3[fid]
        text = 'No.' + str(fid) + ' ' + self.str_hhmm(v[1]) + ' ' + self.str_hhmm(v[3]) + ' ' + self.str_deg(v[4]) + self.str_deg(v[6])
        self.g.add(self.g.text(text, (self.font_size, self.font_size * 2), fill='black', font_size=self.font_size, font_family=self.font_family))

    def draw_legend(self, tyc=False):
        i_max = 17 if tyc else 9
        for i in range(self.mag_max if self.mag_max < i_max else i_max):
            x = i * self.image_r * 0.09 + self.star_r[0] * 1.75 - i * i * 0.8
            y = self.image_r * 2 - self.star_r[0] * 1.75
            self.g.add(self.g.add(self.g.circle((x, y), self.star_r[i], fill='black', stroke='white', stroke_width='0.25')))
            s = str(i + 1)
            if i > 8:x = x - self.font_size * 0.25
            self.g.add(self.g.text(s, (x - self.font_size * 0.25, y - self.star_r[0] - self.font_size * 0.5), fill='black', font_size=self.font_size, font_family=self.font_family))

    def alpha_d(self, deg=0):
        d = abs(deg)
        if d < 50:
            d = 1.25
        elif d < 60:
            d = 2.5
        elif d < 65:
            d = 3.75
        elif d < 75:
            d = 5
        elif d < 80:
            d = 7.5
        else:
            d = 15
        return d

    def in_alpha(self, alpha=0):
        return True if alpha >= self.alpha_min and alpha <= self.alpha_max else False

    def in_delta(self, delta=0):
        return True if delta >= self.delta_min and delta <= self.delta_max else False

    def str_hh(self, deg=0):
        h = int(deg / 15)
        return '{:02}'.format(h) + 'h'

    def str_hhmm(self, deg=0):
        hf = deg / 15
        h = int(hf)
        m = round((hf - h) * 60)
        return '{:02}'.format(h) + 'h' + '{:02}'.format(m) + 'm'

    def str_deg(self, deg=0):
        return '{:+02}'.format(deg) + '\u00b0'

    def xy(self, alpha, delta):
        k = self.sphere_r / (1 + math.sin(self.delta0) * math.sin(delta) + math.cos(self.delta0) * math.cos(delta) * math.cos(alpha - self.alpha0))
        x = -k * math.cos(delta) * math.sin(alpha - self.alpha0) + self.image_r
        y = -k * (math.cos(self.delta0) * math.sin(delta) - math.sin(self.delta0) * math.cos(delta) * math.cos(alpha - self.alpha0)) + self.image_r
        return x, y

    def print_progress(self, i=0, n=0):
        sys.stdout.write('\r%d/%d' % (i, n))
        sys.stdout.flush()

    def print_time(self):
        print('\n{:.3f}'.format(time.time() - self.time_start) + '[s]')
