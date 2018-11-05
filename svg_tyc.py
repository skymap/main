from sky import Sky
s = Sky(400, True)
s.read_frame_tyc()
s.print_time()
s.read_star_tyc()
s.print_time()
i = 0
n = len(s.f3)
for k, v in s.f3.items():
    d = s.alpha_d(v[5])
    s.init_area(k, v[1], v[2], v[3], v[4], v[5], v[6], v[7], 16, True)
    s.draw_alpha_lines(d)
    s.draw_delta_lines(1)
    s.draw_frame(True, True, True, True)
    s.draw_star_tyc(int(k - 1))
    s.draw_legend(True)
    s.draw_alpha_text(d)
    s.draw_delta_text(1)
    s.draw_header_tyc(k)
    s.save_img()
    i = i + 1
    s.print_progress(i, n)
s.print_time()
