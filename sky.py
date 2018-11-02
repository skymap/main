import math, svgwrite


class Sky():
    font_family = 'monospace'
    star_r = [255, 203, 162, 129, 103, 82, 65, 52, 41, 33, 26, 21, 17, 13, 11, 8]
    area_l2 = [3, 9, 15, 21, 27, 32, 36, 40, 43, 45, 47, 48]
    f1 = {}
    f2 = {}
    hip = {}
    line = []
            
    def init_area(self, pid=0, alpha_min=0, alpha_center=0, alpha_max=360, delta_min=0, delta_center=90, delta_max=90, x=0.9, mag_max=6, r=400):
        self.g = svgwrite.Drawing('svg\skymap_' + str(int(pid)) + '_' + str(int(alpha_center)) + '_' + str(int(delta_center)) + '.svg', (r * 2, r * 2), profile='tiny', debug=False)
        self.alpha0 = math.radians(alpha_center)
        self.delta0 = math.radians(delta_center)
        self.alpha_center = alpha_center
        self.delta_center = delta_center
        self.alpha_max = alpha_max
        self.delta_max = delta_max
        self.alpha_min = alpha_min
        self.delta_min = delta_min
        self.mag_max = mag_max
        self.image_r = r
        self.sphere_r = r * x
        self.font_r = r * 0.03
        self.font_size = str(int(self.font_r)) + 'px'

    def init_star_r(self, x=0.01):
        for i in range(16):
            self.star_r[i] = self.star_r[i] * x

    def read_frame(self):
        r = open('frame.csv', 'r')
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

    def read_line(self):
        r = open('line.csv', 'r')
        src = r.read()
        r.close
        rows = src.split('\n')
        for row in rows:
            d = row.split(',')
            self.line.append([float(d[1]), float(d[2]), float(d[3]), float(d[4])])

    def read_hip(self):
        r = open('hip_basic.csv', 'r')
        src = r.read()
        r.close
        rows = src.split('\n')
        for row in rows:
            d = row.split(',')
            self.hip[d[0]] = [float(d[1]), float(d[2]), int(d[3])]

    def save_img(self):
        self.g.save()

    def draw_star_hip(self):
        for v in self.hip.values():
            alpha = v[0]
            delta = v[1]
            mag = v[2]
            if self.in_alpha(alpha) and self.in_delta(delta) and mag < self.mag_max:
                x, y = self.xy(math.radians(alpha), math.radians(delta))
                self.g.add(self.g.circle((x, y), self.star_r[mag], fill='black', stroke='none'))

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
        self.g.add(self.g.polyline(p, fill='none', stroke=color, stroke_width='1'))

    def draw_alpha_text(self, d=15):
        delta_str = math.radians(self.delta_max) if self.delta_min < 0 else math.radians(self.delta_min)
        for alpha_i in range(int(360 / d)):
            alpha = alpha_i * d
            if self.in_alpha(alpha):
                str_alpha = self.str_hh(alpha) if d >= 15 else self.str_hhmm(alpha)
                x, y = self.xy(math.radians(alpha), delta_str)
                self.g.add(self.g.text(str_alpha, (x - self.font_r * 0.6, y + self.font_r), fill='black', font_size=self.font_size, font_family=self.font_family))

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
        self.g.add(self.g.polyline(p, fill='none', stroke=color, stroke_width='1'))

    def draw_delta_text(self, d=10):
        alpha_str = math.radians(self.alpha_max)
        for delta_i in range(int(180 / d) + 1):
            delta = delta_i * d - 90
            if self.in_delta(delta):
                str_delta = '{:+02}'.format(delta) + '\u00b0'
                x, y = self.xy(alpha_str, math.radians(delta))
                self.g.add(self.g.text(str_delta, (x - self.font_r * 0.6, y - self.font_r * 0.2), fill='black', font_size=self.font_size, font_family=self.font_family))

    def draw_frame(self, top=True, right=True, bottom=True, left=True):
        if top:self.draw_delta_line(math.radians(self.delta_max), 'black')
        if right:self.draw_alpha_line(math.radians(self.alpha_min), 'black')
        if bottom:self.draw_delta_line(math.radians(self.delta_min), 'black')
        if left:self.draw_alpha_line(math.radians(self.alpha_max), 'black')

    def draw_frame_link(self, pid, alpha_min, alpha_max, delta_min, delta_max):
        p = []
        alpha_min_rad = math.radians(alpha_min)
        alpha_max_rad = math.radians(alpha_max)
        delta_min_rad = math.radians(delta_min)
        delta_max_rad = math.radians(delta_max)
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
        link = self.g.add(self.g.a('skymap_' + str(int(pid)) + '_' + str(int((alpha_max + alpha_min) / 2)) + '_' + str(int((delta_max + delta_min) / 2)) + '.svg', target='_self'))
        link.add(self.g.polygon(p, stroke='blue', stroke_opacity='0.5', stroke_width='0.5', fill='white', fill_opacity='0'))

    def draw_legend(self):
        # self.g.add(self.g.rect((self.image_r * 0.02, self.image_r * 1.88), (self.mag_max * self.image_r * 0.06 + self.image_r * 0.04, self.image_r * 0.1), fill='silver', fill_opacity='0.5', stroke='none'))
        for i in range(self.mag_max):
            x = i * self.image_r * 0.06 + self.image_r * 0.07
            y = self.image_r * 1.95
            self.g.add(self.g.add(self.g.circle((x, y), self.star_r[i], fill='black', stroke='none')))
            s = str(i + 1)
            self.g.add(self.g.text(s, (x - self.font_r * 0.2, y - self.font_r * 0.8), fill='black', font_size=self.font_size, font_family=self.font_family))

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

    def xy(self, alpha, delta):
        k = self.sphere_r / (1 + math.sin(self.delta0) * math.sin(delta) + math.cos(self.delta0) * math.cos(delta) * math.cos(alpha - self.alpha0))
        x = -k * math.cos(delta) * math.sin(alpha - self.alpha0) + self.image_r
        y = -k * (math.cos(self.delta0) * math.sin(delta) - math.sin(self.delta0) * math.cos(delta) * math.cos(alpha - self.alpha0)) + self.image_r
        return x, y
