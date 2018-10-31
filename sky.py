import math, svgwrite


class Sky():
    font_family = 'monospace'
    star_r = [255, 203, 162, 129, 103, 82, 65, 52, 41, 33, 26, 21, 17, 13, 11, 8]
    area_l2 = [3, 9, 15, 21, 27, 32, 36, 40, 43, 45, 47, 48]
    hip = {}
    line = []
            
    def init_area(self, alpha_min=0, alpha_center=0, alpha_max=360, delta_min=0, delta_center=90, delta_max=90, mag_max=6, r=400, x=0.9):
        self.g = svgwrite.Drawing('map_' + str(alpha_center) + '_' + str(delta_center) + '.svg', profile='tiny')
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
                self.g.add(self.g.line((x1, y1), (x2, y2), fill='none', stroke='#9c9'))

    def draw_alpha_lines(self, d=15):
        for alpha_i in range(int(360 / d)):
            alpha = alpha_i * d
            if self.in_alpha(alpha):
                self.draw_alpha_line(math.radians(alpha), '#eee')

    def draw_alpha_line(self, alpha=0, color='#ccc'):
        p = []
        for delta_d in range(1441):
            delta = delta_d * 0.125 - 90
            if delta >= self.delta_min and delta <= self.delta_max:
                x, y = self.xy(alpha, math.radians(delta))
                p.append([x, y])
        self.g.add(self.g.polyline(p, fill='none', stroke=color))

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
                self.draw_delta_line(math.radians(delta), '#eee')

    def draw_delta_line(self, delta=0, color='#ccc'):
        p = []
        for alpha_d in range(2881):
            alpha = alpha_d * 0.125
            if alpha >= self.alpha_min and alpha <= self.alpha_max:
                x, y = self.xy(math.radians(alpha), delta)
                p.append([x, y])
        self.g.add(self.g.polyline(p, fill='none', stroke=color))

    def draw_delta_text(self, d=10):
        alpha_str = math.radians(self.alpha_max)
        for delta_i in range(int(180 / d) + 1):
            delta = delta_i * d - 90
            if self.in_delta(delta):
                str_delta = '{:+02}'.format(delta) + '\u00b0'
                x, y = self.xy(alpha_str, math.radians(delta))
                self.g.add(self.g.text(str_delta, (x - self.font_r * 0.6, y - self.font_r * 0.2), fill='black', font_size=self.font_size, font_family=self.font_family))

    def draw_frame(self, top=True, right=True, bottom=True, left=True):
        if top:self.draw_delta_line(math.radians(self.delta_max), '#ccc')
        if right:self.draw_alpha_line(math.radians(self.alpha_min), '#ccc')
        if bottom:self.draw_delta_line(math.radians(self.delta_min), '#ccc')
        if left:self.draw_alpha_line(math.radians(self.alpha_max), '#ccc')
        
    def draw_legend(self):
        self.g.add(self.g.rect((self.image_r * 0.02, self.image_r * 1.88), (self.mag_max * self.image_r * 0.06 + self.image_r * 0.04, self.image_r * 0.1), fill='#eee', stroke='none'))
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
        m = int((hf - h) * 60)
        return '{:02}'.format(h) + 'h' + '{:02}'.format(m) + 'm'

    def xy(self, alpha, delta):
        k = self.sphere_r / (1 + math.sin(self.delta0) * math.sin(delta) + math.cos(self.delta0) * math.cos(delta) * math.cos(alpha - self.alpha0))
        x = -k * math.cos(delta) * math.sin(alpha - self.alpha0) + self.image_r
        y = -k * (math.cos(self.delta0) * math.sin(delta) - math.sin(self.delta0) * math.cos(delta) * math.cos(alpha - self.alpha0)) + self.image_r
        return x, y
