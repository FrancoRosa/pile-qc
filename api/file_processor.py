import openpyxl
from pyproj import Transformer
from math import degrees, atan2
from numpy import cross, asarray
from numpy.linalg import norm

FILE = 'EdSan Pile Report WO 7.26.21.xlsx'
DIR = '/home/fx/Upwork/pile-qc/api/'

global wgs84_to_proj, proj_to_wgs84


def xlsx_to_rows(filename):
    xlsx = openpyxl.load_workbook(filename)
    sheet = xlsx.active
    data = sheet.rows
    result = []
    for row in data:
        newrow = ''
        l = list(row)
        for i in range(len(l)):
            if i == len(l) - 1:
                newrow += str(l[i].value)
            else:
                newrow += str(l[i].value) + ','
        result.append(newrow)
    return result


def create_projs(epsg_code=6588):
    global wgs84_to_proj, proj_to_wgs84
    wgs84_to_proj = Transformer.from_crs(
        'epsg:4326', 'epsg:%s' % epsg_code)
    proj_to_wgs84 = Transformer.from_crs(
        'epsg:%s' % epsg_code, 'epsg:4326')


def rows_to_json(rows):
    result = []
    headers = rows[0]
    values = rows[1:]
    if 'Folder,Folder,Folder,Name,Description,Design N,Design E,Design Z,Design Azimuth,Design Dip,Machine,Start Date Time,Start Date,Start Time,Stop Date Time,Stop Date,Stop Time,Start N,Start E,Start Z,Start Azimuth,Start Dip,End N,End E,End Z,End Azimuth,End Dip,N Error,Forward/Back Error,E Error,Left/Right Error,Z Error,Azimuth Error(Twist),Dip Error,N/S Plumb,E/W Plumb' in headers:
        print('headers found')
        for value in values:
            value = value.split(',')

            description = value[4]
            x_design = float(value[6])
            y_design = float(value[5])
            z_design = 0 if "N/A" == value[7] else float(value[7])
            x_field = float(value[22])
            y_field = float(value[23])
            z_field = 0 if "N/A" == value[7] else float(value[24])

            latlng_design = proj_to_wgs84.transform(x_design, y_design)
            latlng_field = proj_to_wgs84.transform(x_field, y_field)
            result.append(


                {
                    "pile_id": description,
                    # "lat_design": latlng_design[0],
                    # "lng_design": latlng_design[1],
                    # "lat_field": latlng_field[0],
                    # "lng_field": latlng_field[1],
                    "x_field": x_field,
                    "y_field": y_field,
                    "z_field": z_field,
                    "x_design": x_design,
                    "y_design": y_design,
                    "z_design": z_design,
                })
    return result


# r = xlsx_to_rows(DIR+FILE)
# create_projs()
# data = rows_to_json(r)
# samples = data[:40]


samples = [
    {'pile_id': '24.S2.R10.A Red . Black', 'x_field': 2160939.034, 'y_field': 6519811.613,
        'z_field': 2553.46, 'x_design': 6519811.628, 'y_design': 2160939.031, 'z_design': 2553.443},
    {'pile_id': '24.S2.R10.B Red', 'x_field': 2160909.406, 'y_field': 6519811.61,
        'z_field': 2553.937, 'x_design': 6519811.628, 'y_design': 2160909.42, 'z_design': 2553.948},
    {'pile_id': '24.S2.R10.C Red', 'x_field': 2160879.805, 'y_field': 6519811.602,
        'z_field': 2554.394, 'x_design': 6519811.628, 'y_design': 2160879.809, 'z_design': 2554.39},
    {'pile_id': '24.S2.R10.D Red', 'x_field': 2160850.204, 'y_field': 6519811.625,
        'z_field': 2554.781, 'x_design': 6519811.628, 'y_design': 2160850.198, 'z_design': 2554.819},
    {'pile_id': '24.S2.R10.E Blue', 'x_field': 2160820.596, 'y_field': 6519811.63,
        'z_field': 2555.266, 'x_design': 6519811.628, 'y_design': 2160820.586, 'z_design': 2555.243},
    {'pile_id': '24.S2.R10.G Green . Black', 'x_field': 2160762.837, 'y_field': 6519811.626,
        'z_field': 2556.108, 'x_design': 6519811.628, 'y_design': 2160762.84, 'z_design': 2556.089},
    {'pile_id': '24.S2.R10.H Blue', 'x_field': 2160734.719, 'y_field': 6519811.654,
        'z_field': 2556.529, 'x_design': 6519811.628, 'y_design': 2160734.704, 'z_design': 2556.501},
    {'pile_id': '24.S2.R10.I Blue . Black', 'x_field': 2160709.244, 'y_field': 6519811.622,
        'z_field': 2556.889, 'x_design': 6519811.628, 'y_design': 2160709.23, 'z_design': 2556.876},
    {'pile_id': '24.S2.R10.J Red . Black', 'x_field': 2160683.746, 'y_field': 6519811.636,
        'z_field': 2557.259, 'x_design': 6519811.628, 'y_design': 2160683.756, 'z_design': 2557.24},
    {'pile_id': '24.S2.R11.A Red . Black', 'x_field': 2160939.497, 'y_field': 6519829.631,
        'z_field': 2553.569, 'x_design': 6519829.628, 'y_design': 2160939.514, 'z_design': 2553.568},
    {'pile_id': '24.S2.R11.B Red', 'x_field': 2160909.895, 'y_field': 6519829.638,
        'z_field': 2554.086, 'x_design': 6519829.628, 'y_design': 2160909.902, 'z_design': 2554.073},
    {'pile_id': '24.S2.R11.D Red', 'x_field': 2160850.681, 'y_field': 6519829.632,
        'z_field': 2554.962, 'x_design': 6519829.628, 'y_design': 2160850.68, 'z_design': 2554.942},
    {'pile_id': '24.S2.R11.E Blue', 'x_field': 2160821.06, 'y_field': 6519829.611,
        'z_field': 2555.379, 'x_design': 6519829.628, 'y_design': 2160821.069, 'z_design': 2555.373},
    {'pile_id': '24.S2.R11.F Blue', 'x_field': 2160791.469, 'y_field': 6519829.621,
        'z_field': 2555.833, 'x_design': 6519829.628, 'y_design': 2160791.458, 'z_design': 2555.809},
    {'pile_id': '24.S2.R11.G Green . Black', 'x_field': 2160763.319, 'y_field': 6519829.634,
        'z_field': 2556.25, 'x_design': 6519829.628, 'y_design': 2160763.322, 'z_design': 2556.228},
    {'pile_id': '24.S2.R11.H Blue', 'x_field': 2160735.197, 'y_field': 6519829.687,
        'z_field': 2556.667, 'x_design': 6519829.628, 'y_design': 2160735.187, 'z_design': 2556.645},
    {'pile_id': '24.S2.R11.I Blue . Black', 'x_field': 2160709.738, 'y_field': 6519829.63,
        'z_field': 2557.04, 'x_design': 6519829.628, 'y_design': 2160709.713, 'z_design': 2557.023},
    {'pile_id': '24.S2.R11.J Red . Black', 'x_field': 2160684.216, 'y_field': 6519829.603,
        'z_field': 2557.408, 'x_design': 6519829.628, 'y_design': 2160684.239, 'z_design': 2557.393},
    {'pile_id': '24.S2.R12.A Red . Black', 'x_field': 2160940.004, 'y_field': 6519847.607,
        'z_field': 2553.714, 'x_design': 6519847.628, 'y_design': 2160939.996, 'z_design': 2553.701},
    {'pile_id': '24.S2.R12.B Red', 'x_field': 2160910.376, 'y_field': 6519847.634,
        'z_field': 2554.232, 'x_design': 6519847.628, 'y_design': 2160910.385, 'z_design': 2554.198},
    {'pile_id': '24.S2.R12.C Red', 'x_field': 2160880.785, 'y_field': 6519847.619,
        'z_field': 2554.638, 'x_design': 6519847.628, 'y_design': 2160880.774, 'z_design': 2554.625},
    {'pile_id': '24.S2.R12.D Red', 'x_field': 2160851.162, 'y_field': 6519847.644,
        'z_field': 2555.053, 'x_design': 6519847.628, 'y_design': 2160851.162, 'z_design': 2555.042},
    {'pile_id': '24.S2.R12.E Blue', 'x_field': 2160821.567, 'y_field': 6519847.602,
        'z_field': 2555.476, 'x_design': 6519847.628, 'y_design': 2160821.551, 'z_design': 2555.458},
    {'pile_id': '24.S2.R12.F Blue', 'x_field': 2160791.917, 'y_field': 6519847.636,
        'z_field': 2555.898, 'x_design': 6519847.628, 'y_design': 2160791.94, 'z_design': 2555.877},
    {'pile_id': '24.S2.R12.G Green . Black', 'x_field': 2160763.773, 'y_field': 6519847.678,
        'z_field': 2556.321, 'x_design': 6519847.628, 'y_design': 2160763.805, 'z_design': 2556.287},
    {'pile_id': '24.S2.R12.H Blue', 'x_field': 2160735.658, 'y_field': 6519847.625,
        'z_field': 2556.689, 'x_design': 6519847.628, 'y_design': 2160735.669, 'z_design': 2556.688},
    {'pile_id': '24.S2.R12.I Blue . Black', 'x_field': 2160710.213, 'y_field': 6519847.629,
        'z_field': 2557.05, 'x_design': 6519847.628, 'y_design': 2160710.195, 'z_design': 2557.058},
    {'pile_id': '24.S2.R12.J Red . Black', 'x_field': 2160684.731, 'y_field': 6519847.647,
        'z_field': 2557.408, 'x_design': 6519847.628, 'y_design': 2160684.721, 'z_design': 2557.427},
    {'pile_id': '24.S2.R13.A Red . Black', 'x_field': 2160940.472, 'y_field': 6519865.627,
        'z_field': 2553.828, 'x_design': 6519865.628, 'y_design': 2160940.478, 'z_design': 2553.833},
    {'pile_id': '24.S2.R13.B Red', 'x_field': 2160910.875, 'y_field': 6519865.634,
        'z_field': 2554.304, 'x_design': 6519865.628, 'y_design': 2160910.867, 'z_design': 2554.294},
    {'pile_id': '24.S2.R13.C Red', 'x_field': 2160881.254, 'y_field': 6519865.636,
        'z_field': 2554.709, 'x_design': 6519865.628, 'y_design': 2160881.256, 'z_design': 2554.709},
    {'pile_id': '24.S2.R13.D Red', 'x_field': 2160851.645, 'y_field': 6519865.637,
        'z_field': 2555.145, 'x_design': 6519865.628, 'y_design': 2160851.645, 'z_design': 2555.118},
    {'pile_id': '24.S2.R13.E Blue', 'x_field': 2160822.052, 'y_field': 6519865.642,
        'z_field': 2555.505, 'x_design': 6519865.628, 'y_design': 2160822.033, 'z_design': 2555.518},
    {'pile_id': '24.S2.R13.F Blue', 'x_field': 2160792.444, 'y_field': 6519865.64,
        'z_field': 2555.921, 'x_design': 6519865.628, 'y_design': 2160792.422, 'z_design': 2555.927},
    {'pile_id': '24.S2.R13.G Green . Black', 'x_field': 2160764.43, 'y_field': 6519865.645,
        'z_field': 2556.324, 'x_design': 6519865.628, 'y_design': 2160764.287, 'z_design': 2556.32},
    {'pile_id': '24.S2.R13.H Blue', 'x_field': 2160736.156, 'y_field': 6519865.626,
        'z_field': 2556.734, 'x_design': 6519865.628, 'y_design': 2160736.151, 'z_design': 2556.71},
    {'pile_id': '24.S2.R13.I Blue . Black', 'x_field': 2160710.642, 'y_field': 6519865.644,
        'z_field': 2557.083, 'x_design': 6519865.628, 'y_design': 2160710.677, 'z_design': 2557.068},
    {'pile_id': '24.S2.R13.J Red . Black', 'x_field': 2160685.202, 'y_field': 6519865.638,
        'z_field': 2557.445, 'x_design': 6519865.628, 'y_design': 2160685.203, 'z_design': 2557.431},
    {'pile_id': '24.S2.R14.A Red . Black', 'x_field': 2160940.978, 'y_field': 6519883.684,
        'z_field': 2553.877, 'x_design': 6519883.628, 'y_design': 2160940.961, 'z_design': 2553.867},
    {'pile_id': '24.S2.R14.B Red', 'x_field': 2160911.359, 'y_field': 6519883.633, 'z_field': 2554.341,
        'x_design': 6519883.628, 'y_design': 2160911.349, 'z_design': 2554.322}
]


def unique(list1):
    unique_list = []
    for x in list1:
        if x not in unique_list:
            unique_list.append(x)
    return unique_list


def get_columns(samples):
    eastern_coords = list(map(lambda x: x['x_design'], samples))
    eastern_coords = unique(eastern_coords)
    eastern_coords.sort()
    return eastern_coords


def get_distance(group):
    x = (group[0]['x_field'] - group[1]['x_field'])
    y = (group[0]['y_field'] - group[1]['y_field'])
    return (x**2 + y**2)**(1/2)


def group_angle_error(group):
    d1 = get_distance(group[0:2])
    d2 = get_distance(group[1:3])
    h1 = group[0]['z_field'] - group[1]['z_field']
    h2 = group[2]['z_field'] - group[1]['z_field']
    ang1 = degrees(atan2(h1, d1))
    ang2 = degrees(atan2(h2, d2))
    return 180-ang1-ang2


def group_x_error(group):
    p1 = asarray((group[0]['x_field'], group[0]['y_field']))
    p2 = asarray((group[1]['x_field'], group[1]['y_field']))
    p3 = asarray((group[2]['x_field'], group[2]['y_field']))
    d = norm(cross(p2-p1, p1-p3))/norm(p2-p1)
    return d


def group_y_error(group):
    d1 = get_distance(group[0:2])
    d2 = get_distance(group[1:3])
    return [d1, d2]


def give_order(samples, eastern_coords):
    ordered_samples = []
    for column in eastern_coords:
        rows = list(filter(lambda x: x['x_design'] == column, samples))

        rows_y = list(map(lambda x: x['y_design'], rows))
        rows_y.sort(reverse=True)
        for row in rows:
            row['order'] = [
                eastern_coords.index(row['x_design']),
                rows_y.index(row['y_design'])
            ]
            print(row['order'], row['x_design'], row['y_design'])
        # make sets of 3 and for the middle element add the group error
        for i in range(len(rows)):
            if i+3 > len(rows):
                break
            angle_error = group_angle_error(rows[i:i+3])
            x_error = group_x_error(rows[i:i+3])
            y_error = group_y_error(rows[i:i+3])
            rows[i+1]['angle_g_error'] = angle_error
            rows[i+1]['x_g_error'] = x_error
            rows[i+1]['y_g_error'] = y_error

        ordered_samples += rows
    return(ordered_samples)


columns = get_columns(samples)
new_samples = give_order(samples, columns)

for s in new_samples:
    if 'angle_g_error' in s:
        print(s['order'], ':', s['angle_g_error'])
    else:
        print(s['order'])
