from PIL import Image, ImageDraw, ImageFont
import math


class sky:
    color = {'black':(0, 0, 0), 'white':(255, 255, 255), 'gray':(204, 204, 204), 'light_gray':(238, 238, 238), 'green':(153, 204, 153)}
    font_name = 'AdobeHeitiStd-Regular.otf'
    star_r16 = [255, 203, 162, 129, 103, 82, 65, 52, 41, 33, 26, 21, 17, 13, 11, 8]

    def __init__(self, alpha_min=0, alpha_center=0, alpha_max=360, delta_min=0, delta_center=90, delta_max=90, mag_max=6, c=0.9, r=15000):
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
        self.sphere_r = r * c
        self.font = ImageFont.truetype(self.font_name, int(r * 0.03))
        self.img = Image.new('RGB', (r * 2, r * 2), self.color['white'])
        self.draw = ImageDraw.Draw(self.img)
        l = len(self.star_r16)
        self.star_r = list(range(l))
        for i in range(l):
            self.star_r.append(self.star_r16[i] * r * 0.00004)

    def save_img(self, r=600, prefix='sky'):
        self.img = self.img.resize((r, r), Image.LANCZOS)
        self.img.save(prefix + str(r) + '.png')

    def draw_star_hip(self):
        r = open('hip_basic.csv', 'r')
        src = r.read()
        r.close
        rows = src.split('\n')
        for row in rows:
            d = row.split(',')
            alpha = float(d[1])
            delta = float(d[2])
            mag = int(d[3])
            if self.in_alpha(alpha) and self.in_delta(delta) and mag < self.mag_max:
                r = self.star_r16[mag]
                x, y = self.xy(math.radians(alpha), math.radians(delta))
                self.draw.ellipse((x - r, y - r, x + r, y + r), self.color['black'])

    def draw_constellation_lines(self):
        r = open('line.csv', 'r')
        src = r.read()
        r.close
        rows = src.split('\n')
        for row in rows:
            d = row.split(',')
            alpha1 = float(d[1])
            delta1 = float(d[2])
            alpha2 = float(d[3])
            delta2 = float(d[4])
            if self.in_alpha(alpha1) and self.in_alpha(alpha2) and self.in_delta(delta1) and self.in_delta(delta2):
                x1, y1 = self.xy(math.radians(alpha1), math.radians(delta1))
                x2, y2 = self.xy(math.radians(alpha2), math.radians(delta2))
                self.draw.line((x1, y1, x2, y2), self.color['green'], 20)

    def draw_alpha_lines(self, d=15):
        delta_str = math.radians(self.delta_max + d / 5) if self.delta_min < 0 else math.radians(self.delta_min - d / 5)
        for alpha_i in range(int(360 / d)):
            alpha = alpha_i * d
            if self.in_alpha(alpha):
                alpha_str = self.str_hh(alpha) if d >= 15 else self.str_hhmm(alpha)
                alpha = math.radians(alpha)
                x, y = self.xy(alpha, delta_str)
                w, h = self.font.getsize(alpha_str)
                self.draw.text((x - w / 2, y - h / 2), alpha_str, self.color['gray'], self.font)
                self.draw_alpha_line(alpha, 'gray')

    def draw_alpha_line(self, alpha=0, color_name=''):
        for delta_d in range(1448):
            delta1 = delta_d * 0.125 - 90
            delta2 = delta_d * 0.125 - 89.875
            if delta1 >= self.delta_min and delta2 <= self.delta_max:
                x1, y1 = self.xy(alpha, math.radians(delta1))
                x2, y2 = self.xy(alpha, math.radians(delta2))
                self.draw.line((x1, y1, x2, y2), self.color[color_name], 10)

    def draw_delta_lines(self, d=10):
        alpha_str = math.radians(self.alpha_max)
        for delta_i in range(int(180 / d) + 1):
            delta = delta_i * d - 90
            if self.in_delta(delta):
                str_delta = '{:+02}'.format(delta) + '\u00b0'
                delta = math.radians(delta)
                x, y = self.xy(alpha_str, delta)
                w, h = self.font.getsize(str_delta)
                self.draw.text((x - w / 2, y - h / 2), str_delta, self.color['gray'], self.font)
                self.draw_delta_line(delta, 'gray')

    def draw_delta_line(self, delta=0, color_name=''):
        for alpha_d in range(360):
            alpha1 = alpha_d
            alpha2 = alpha_d + 1
            if alpha1 >= self.alpha_min and alpha2 <= self.alpha_max:
                x1, y1 = self.xy(math.radians(alpha1), delta)
                x2, y2 = self.xy(math.radians(alpha2), delta)
                self.draw.line((x1, y1, x2, y2), self.color[color_name], 10)

    def draw_frame(self, top=True, right=True, bottom=True, left=True):
        if top:self.draw_delta_line(math.radians(self.delta_max), 'black')
        if right:self.draw_alpha_line(math.radians(self.alpha_min), 'black')
        if bottom:self.draw_delta_line(math.radians(self.delta_min), 'black')
        if left:self.draw_alpha_line(math.radians(self.alpha_max), 'black')
        
    def draw_legend(self):
        self.draw.rectangle((self.image_r * 0.02, self.image_r * 1.88, self.mag_max * self.image_r * 0.06 + self.image_r * 0.04, self.image_r * 1.98), self.color['light_gray'])
        for i in range(self.mag_max):
            r = self.star_r16[i]
            x = i * self.image_r * 0.06 + self.image_r * 0.06
            y = self.image_r * 1.95
            self.draw.ellipse((x - r, y - r, x + r, y + r), self.color['black'])
            s = str(i + 1)
            w, h = self.font.getsize(s)
            self.draw.text((x - w / 2, y - h * 2), s, self.color['black'], self.font)

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
        x = k * math.cos(delta) * math.sin(alpha - self.alpha0) + self.image_r
        y = k * (math.cos(self.delta0) * math.sin(delta) - math.sin(self.delta0) * math.cos(delta) * math.cos(alpha - self.alpha0)) + self.image_r
        return x, y
