import openpyxl
from pyproj import Transformer
from math import degrees, atan2
from numpy import cross, asarray
from numpy.linalg import norm

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
        print('... headers found')
        for value in values:
            value = value.split(',')

            description = value[4]
            x_design = float(value[6])
            y_design = float(value[5])
            z_design = 0 if "N/A" == value[7] else float(value[7])
            x_field = float(value[23])
            y_field = float(value[22])
            z_field = 0 if "N/A" == value[24] else float(value[24])

            latlng_design = proj_to_wgs84.transform(x_design, y_design)
            latlng_field = proj_to_wgs84.transform(x_field, y_field)
            result.append(


                {
                    "pile_id": description,
                    "lat_design": latlng_design[0],
                    "lng_design": latlng_design[1],
                    "lat_field": latlng_field[0],
                    "lng_field": latlng_field[1],
                    "x_field": x_field,
                    "y_field": y_field,
                    "z_field": z_field,
                    "x_design": x_design,
                    "y_design": y_design,
                    "z_design": z_design,
                })
    return result


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


def get_distance(group, key='_field'):
    x = (group[0]['x' + key] - group[1]['x' + key])
    y = (group[0]['y' + key] - group[1]['y' + key])
    return (x**2 + y**2)**(1/2)


def group_angle_error(group):
    d1 = get_distance(group[0:2])
    d2 = get_distance(group[1:3])
    h1 = group[0]['z_field'] - group[1]['z_field']
    h2 = group[2]['z_field'] - group[1]['z_field']
    ang1 = degrees(atan2(h1, d1))
    ang2 = degrees(atan2(h2, d2))
    return round(abs(ang1+ang2), 3)


def group_x_error(group):
    p1 = asarray((group[0]['x_field'], group[0]['y_field']))
    p2 = asarray((group[1]['x_field'], group[1]['y_field']))
    p3 = asarray((group[2]['x_field'], group[2]['y_field']))
    d = norm(cross(p2-p1, p1-p3))/norm(p2-p1)
    return round(d, 3)


def group_y_error(group):
    d1 = get_distance(group[0:2])
    d2 = get_distance(group[1:3])
    return [round(d1, 3), round(d2, 3)]


def group_y_diff(group):
    d1 = get_distance(group[0:2], '_design')
    d2 = get_distance(group[1:3], '_design')
    return [round(d1, 3), round(d2, 3)]


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
        # print(row['order'], row['x_design'], row['y_design'])
        # make sets of 3 and for the middle element add the group error
        rows = sorted(rows, key=lambda x: x['order'])

        for i in range(len(rows)):
            if i+3 > len(rows):
                break
            angle_error = group_angle_error(rows[i:i+3])
            x_error = group_x_error(rows[i:i+3])
            y_error = group_y_error(rows[i:i+3])
            y_diff = group_y_diff(rows[i:i+3])
            rows[i+1]['angle_g_error'] = angle_error
            rows[i+1]['x_g_error'] = x_error
            rows[i+1]['y_g_error'] = [
                round(abs(y_diff[0] - y_error[0]), 3),
                round(abs(y_diff[1] - y_error[1]), 3)
            ]

        ordered_samples += rows
    return(ordered_samples)


def format_file(filedir, epsg=2275):
    print('... reading file')
    r = xlsx_to_rows(filedir)

    print('... creating projections')
    create_projs(epsg)

    print('... reading columns')
    samples = rows_to_json(r)
    print('...found:', len(samples))

    columns = get_columns(samples)
    return give_order(samples, columns)
