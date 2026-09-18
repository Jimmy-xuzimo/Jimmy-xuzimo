import datetime, hashlib

PERIOD_TIMES = {
    1: ('08:00', '09:35'),
    2: ('09:55', '11:30'),
    3: ('14:00', '15:35'),
    4: ('15:55', '17:30'),
    5: ('18:30', '20:05'),
    6: ('20:15', '21:50'),
}

COURSES = [
    (0, 2, '艺术概论', '3-5,7,10-18', '七区439(多媒体-中英数字创意学院)', '高宇', '26数媒技术（中英）2班;26网新（中英）2班'),
    (0, 5, '大学生职业发展与就业指导1', '11-13(单)', '未排地点', '朱润秋', '26网新（中英）1-3班'),
    (1, 5, '学科专业导学与生涯规划1', '10-17', '未排地点', '毛金蓉,郭爽', '26网新（中英）1-3班'),
    (1, 3, '大学英语（综合）1', '2-4,7,10-18', '七区441(多媒体-中英数字创意学院)', '王汇雯', '26网新（中英）2班'),
    (2, 2, '大学生心理健康', '2-4,7,10-11', '四区318(北)', '王云', '26网新（中英）1-3班'),
    (2, 2, '大学生心理健康', '12-18', '不安排教室', '王云', '26网新（中英）1-3班'),
    (2, 4, '中国新闻传播大讲堂（线上线下混合课）', '2-5,7,10-12', '未排地点', '毛金蓉', '26网新（中英）1-2班'),
    (2, 5, '军事理论', '8-9', '七区437(多媒体-中英数字创新学院)', '王辉', '26网新（中英）1-2班'),
    (2, 6, '军事理论', '8-9', '七区437(多媒体-中英数字创新学院)', '王辉', '26网新（中英）1-2班'),
    (3, 2, '思想道德与法治', '2-4,6-7,10-18', '七区439(多媒体-中英数字创意学院)', '徐妍', '26网新（中英）1-2班'),
    (3, 4, '体育1', '2-4,6-7,10-18', '乒乓球馆(活动中心114)', '钱凯', '478乒乓球男-1/2026'),
    (4, 2, '数字技术基础与实践', '2-4,6-7,10-18', '二区501(计算机基础实验室3)', '牛艺霏', '26网新（中英）2-3班'),
    (4, 4, '大学英语（综合）1', '2-4,6-7,10-18', '七区440(多媒体-中英数字创意学院)', '王汇雯', '26网新（中英）2班'),
    (4, 5, '形势与政策1', '14-17', '七区437(多媒体-中英数字创新学院)', '赵利群', '26网新（中英）1-2班'),
    (5, 1, '军事理论', '2-5,7,18', '不安排教室', '王辉', '26网新（中英）1-2班'),
    (5, 2, '军事理论', '2-5,7,18', '不安排教室', '王辉', '26网新（中英）1-2班'),
    (5, 2, '大学生心理健康', '6', '四区318(北)', '王云', '26网新（中英）1-3班'),
    (6, 3, '大学英语（综合）1', '3', '七区441(多媒体-中英数字创意学院)', '王汇雯', '26网新（中英）2班'),
]

HOLIDAYS = {
    datetime.date(2026, 9, 25), datetime.date(2026, 9, 26), datetime.date(2026, 9, 27),
    datetime.date(2026, 10, 1), datetime.date(2026, 10, 2), datetime.date(2026, 10, 3),
    datetime.date(2026, 10, 4), datetime.date(2026, 10, 5), datetime.date(2026, 10, 6),
    datetime.date(2026, 10, 7),
    datetime.date(2027, 1, 1),
}

SEMESTER_START = datetime.date(2026, 8, 31)

def parse_weeks(s):
    weeks = set()
    for part in s.split(','):
        part = part.strip()
        is_odd = '单' in part
        is_even = '双' in part
        part = part.replace('(单)', '').replace('（单）', '').replace('(双)', '').replace('（双）', '').replace('周', '').strip()
        if '-' in part:
            a, b = part.split('-')
            for w in range(int(a), int(b) + 1):
                if is_odd and w % 2 == 0: continue
                if is_even and w % 2 == 1: continue
                weeks.add(w)
        else:
            w = int(part)
            if not ((is_odd and w % 2 == 0) or (is_even and w % 2 == 1)):
                weeks.add(w)
    return sorted(weeks)

def escape_ics(text):
    return text.replace('\\', '\\\\').replace(';', '\;').replace(',', '\,').replace('\n', '\\n')

def fmt_dt(d, t):
    return d.strftime('%Y%m%d') + 'T' + t.replace(':', '') + '00'

events = []
for day_idx, period, name, weeks_str, location, teacher, class_info in COURSES:
    weeks = parse_weeks(weeks_str)
    st, et = PERIOD_TIMES[period]
    for wk in weeks:
        d = SEMESTER_START + datetime.timedelta(days=(wk - 1) * 7 + day_idx)
        if d in HOLIDAYS:
            continue
        desc = f'教师: {teacher} | 教学班: {class_info} | 第{wk}周'
        events.append((d, st, et, name, location, desc, wk))

events.sort(key=lambda e: (e[0], e[1]))

lines = []
lines.append('BEGIN:VCALENDAR')
lines.append('VERSION:2.0')
lines.append('PRODID:-//NanJingXiaoBo//Schedule//CN')
lines.append('CALSCALE:GREGORIAN')
lines.append('METHOD:PUBLISH')
lines.append('X-WR-CALNAME:徐子墨的课表 2026-2027第一学期')
lines.append('X-WR-TIMEZONE:Asia/Shanghai')
lines.append('X-APPLE-CALENDAR-COLOR:#FF6B35')
lines.append('BEGIN:VTIMEZONE')
lines.append('TZID:Asia/Shanghai')
lines.append('BEGIN:STANDARD')
lines.append('DTSTART:19700101T000000')
lines.append('TZOFFSETFROM:+0800')
lines.append('TZOFFSETTO:+0800')
lines.append('TZNAME:CST')
lines.append('END:STANDARD')
lines.append('END:VTIMEZONE')

for d, st, et, name, location, desc, wk in events:
    uid = hashlib.md5(f'{d}{st}{name}'.encode()).hexdigest()[:16] + '@schedule'
    lines.append('BEGIN:VEVENT')
    lines.append(f'UID:{uid}')
    lines.append('DTSTAMP:20260908T000000Z')
    lines.append(f'DTSTART;TZID=Asia/Shanghai:{fmt_dt(d, st)}')
    lines.append(f'DTEND;TZID=Asia/Shanghai:{fmt_dt(d, et)}')
    lines.append(f'SUMMARY:{escape_ics(name)}')
    if location and location != '不安排教室' and location != '未排地点' and location != '无':
        lines.append(f'LOCATION:{escape_ics(location)}')
    lines.append(f'DESCRIPTION:{escape_ics(desc)}')
    lines.append('BEGIN:VALARM')
    lines.append('TRIGGER:-PT15M')
    lines.append('ACTION:DISPLAY')
    lines.append(f'DESCRIPTION:{escape_ics(name)} 即将开始')
    lines.append('END:VALARM')
    lines.append('END:VEVENT')

lines.append('END:VCALENDAR')

ics_content = '\r\n'.join(lines) + '\r\n'
with open('schedule.ics', 'w', encoding='utf-8') as f:
    f.write(ics_content)
print(f'Generated {len(events)} events -> schedule.ics')
