from Payroll.models import NguoiLD, BangLuong
from django.http import JsonResponse
from dateutil.relativedelta import relativedelta
from django.utils import timezone
import datetime
import polars as pl


TIMEPEELOADER = 60 # Thời gian lấy dữ liệu mới, đơn vị giây

DFSALARY = None
LASTGETSALARY = None # Thời gian lấy dữ liệu cuối cùng
def getSalary(mnv):
    # global DFSALARY, LASTGETSALARY
    # # print(LASTGETSALARY, timezone.now())
    # if not LASTGETSALARY is None and (timezone.now() - LASTGETSALARY).total_seconds() < TIMEPEELOADER:
    #     return DFSALARY
    # print('Get Salary')
    df= {
        # 'mnv' : [],
        'thang': [],
        'luong': [],
    }
    nguoild = NguoiLD.objects.filter(mnv = mnv).first()

    for s in BangLuong.objects.filter(mnv=nguoild):
        df['thang'].append(s.month)
        df['luong'].append(s.luong)

    df = pl.DataFrame(df)
    # print(df)
    # DFSALARY = df
    # LASTGETSALARY = timezone.now()
    return df

def get_employees(request):
    """ Lấy danh sách người lao động gồm mnv và tên
    """
    result= {
        "data": []
    }
    nguoild = NguoiLD.objects.all().values_list('mnv', 'name')
    for (mnv, name) in nguoild:
        result['data'].append({
            "mnv": mnv,
            "name": name,
        })
    return JsonResponse(result, status=200)



def chart_summary(request, mnv):
    """ CHART SUMMARY OF Luong : CHARTJS
    - Theo lương bằng màu
    - Trục x: thời gian trong 12 tháng gần nhất
    - Trục y: lương
    """
    df = getSalary(mnv).clone()
    
    # Get 12 months ago
    now = timezone.now()
    months = 12
    start_month = now - relativedelta(months = months) 
    df= df.to_dict(as_series= False)
    # chartjs
    # truc x: 12 thang gan nhat, i+1 vi bat dau tu thang hien tai
    labels = [(start_month + relativedelta(months=i+1)).strftime('%Y-%m') for i in range(months)]
    
    
    # truc y: so luong luong theo thang
    data = {}
    for label in labels:
        year, month = map(int, label.split('-'))
        if month in df['thang']:
            index = df['thang'].index(month)
            data[label] = df['luong'][index]
        
        
    chart_data= {
        'labels': labels,
        'title': {
            'text': 'Lương của nhân viên {} trong 12 tháng gần nhất'.format(mnv),
            'display': True,
            'color': '#000000',
            'font': { 
                'size': 20,
                'family': 'Arial',
                'weight': 'bold'
            },
        },
        'x_label': {
            'text': 'Tháng',
            'display': True,
            'color': '#000000',
            'font': { 
                'size': 15,
                'family': 'Arial',
                'weight': 'bold'
            },
        },
        'y_label': {
            'text': 'Lương',
            'display': True,
            'color': '#000000',
            'font': { 
                'size': 15,
                'family': 'Arial',
                'weight': 'bold'
            },
        },
        'x_ticks': {
            'font': { 
                'size': 10,
            },
        },
        'y_ticks': {
            'stepSize': 1,
            'font': { 
                'size': 10,
            },
        },
        'datasets': [{
                'label': '{}'.format(mnv),
                'data': data,
                'backgroundColor': '#777777',
                'borderColor': '#777777',
                'borderWidth': 2,
                'fill': False,
                'type': 'bar',
            }],
    }
    return JsonResponse(chart_data, status=200)

def chart_summary_all(request):
    """ CHART SUMMARY OF Luong : CHARTJS
    - Theo lương bằng màu
    - Trục x: thời gian trong 12 tháng gần nhất
    - Trục y: lương
    """
    emp = NguoiLD.objects.all()
    emp_list_data = []

    for i in range(len(emp)):
        e=emp[i].mnv
        mnv = e
        df1 = getSalary(mnv)
        now = timezone.now()
        months = 12
        start_month = now - relativedelta(months = months) 
        df= df1.to_dict(as_series= False)
        # print(d)
        # chartjs
        # truc x: 12 thang gan nhat, i+1 vi bat dau tu thang hien tai
        labels = [(start_month + relativedelta(months=i+1)).strftime('%Y-%m') for i in range(months)]
    
    
        # truc y: so luong luong theo thang
        data = {}
        for label in labels:
            year, month = map(int, label.split('-'))
            if month in df['thang']:
                index = df['thang'].index(month)
                data[label] = df['luong'][index]

        emp_list_data.append({
                'mnv': mnv,
                'data': data  
            })
    
    emp_chart_data= {
        'labels' : labels,
        'title' : {
            'text': 'Lương của tất cả nhân viên trong 12 tháng gần nhất',
            'display': True,
            'color': '#000000',
            'font': { 
                'size': 20,
                'family': 'Arial',
                'weight': 'bold'
            },
        },
        'x_label': {
            'text': 'Tháng',
            'display': True,
            'color': '#000000',
            'font': { 
                'size': 15,
                'family': 'Arial',
                'weight': 'bold'
            },
        },
        'y_label': {
            'text': 'Lương',
            'display': True,
            'color': '#000000',
            'font': { 
                'size': 15,
                'family': 'Arial',
                'weight': 'bold'
            },
        },
        'x_ticks': {
            'font': { 
                'size': 10,
            },
        },
        'y_ticks': {
            'stepSize': 1,
            'font': { 
                'size': 10,
            },
        },
        'datasets': [{
                'label': emp_data['mnv'],
                'data': emp_data['data'],
                'backgroundColor': (color := random()), 
                'borderColor': color, 
                'borderWidth': 2,
                'fill': False,
                'type': 'bar',
            } for emp_data in emp_list_data],
    }
    return JsonResponse(emp_chart_data, status=200)

from random import randint
def random():
    return "#" + str(randint(100000,999999))

def getGiolam(mnv):
    df={
        'thang' : [],
        'giolam' : [],
    }
    nguoild = NguoiLD.objects.filter(mnv = mnv).first()
    for s in BangLuong.objects.filter(mnv=nguoild):
        df['thang'].append(s.month)
        df['giolam'].append(s.sogio)
    df = pl.DataFrame(df)
    DFSALARY = df
    LASTGETSALARY = timezone.now()
    return df

def chart_giolam(request, mnv):
    df = getGiolam(mnv).clone()
    # Get 12 months ago
    now = timezone.now()
    months = 12
    start_month = now - relativedelta(months = months) 
    df= df.to_dict(as_series= False)
    # chartjs
    # truc x: 12 thang gan nhat, i+1 vi bat dau tu thang hien tai
    labels = [(start_month + relativedelta(months=i+1)).strftime('%Y-%m') for i in range(months)]

    data = {}

    for label in labels:
        year, month = map(int, label.split('-'))
        if month in df['thang']:
            index = df['thang'].index(month)
            data[label] = df['giolam'][index]

    chart_data= {
        'labels': labels,
        'title': {
            'text': 'Giờ của nhân viên {} trong 12 tháng gần nhất'.format(mnv),
            'display': True,
            'color': '#000000',
            'font': { 
                'size': 20,
                'family': 'Arial',
                'weight': 'bold'
            },
        },
        'x_label': {
            'text': 'Tháng',
            'display': True,
            'color': '#000000',
            'font': { 
                'size': 15,
                'family': 'Arial',
                'weight': 'bold'
            },
        },
        'y_label': {
            'text': 'Giờ làm',
            'display': True,
            'color': '#000000',
            'font': { 
                'size': 15,
                'family': 'Arial',
                'weight': 'bold'
            },
        },
        'x_ticks': {
            'font': { 
                'size': 10,
            },
        },
        'y_ticks': {
            'stepSize': 1,
            'font': { 
                'size': 10,
            },
        },
        'datasets': [{
                'label': '{}'.format(mnv),
                'data': data,
                'backgroundColor': '#777777',
                'borderColor': '#777777',
                'borderWidth': 2,
                'fill': False,
                'type': 'bar',
            }],
    }
    return JsonResponse(chart_data, status=200)

def chart_giolam_all(request):
    """ CHART SUMMARY OF Luong : CHARTJS
    - Theo lương bằng màu
    - Trục x: thời gian trong 12 tháng gần nhất
    - Trục y: lương
    """
    emp = NguoiLD.objects.all()
    emp_list_data = []

    for i in range(len(emp)):
        e=emp[i].mnv
        mnv = e
        df1 = getGiolam(mnv)#.clone()
        now = timezone.now()
        months = 12
        start_month = now - relativedelta(months = months) 
        df= df1.to_dict(as_series= False)
        # print(d)
        # chartjs
        # truc x: 12 thang gan nhat, i+1 vi bat dau tu thang hien tai
        labels = [(start_month + relativedelta(months=i+1)).strftime('%Y-%m') for i in range(months)]
    
    
        # truc y: so luong luong theo thang
        data = {}
        for label in labels:
            year, month = map(int, label.split('-'))
            if month in df['thang']:
                index = df['thang'].index(month)
                data[label] = df['giolam'][index]

        emp_list_data.append({
                'mnv': mnv,
                'data': data  
            })
    
    emp_chart_data= {
        'labels' : labels,
        'title' : {
            'text': 'Thời gian làm việc của tất cả nhân viên trong 12 tháng gần nhất',
            'display': True,
            'color': '#000000',
            'font': { 
                'size': 20,
                'family': 'Arial',
                'weight': 'bold'
            },
        },
        'x_label': {
            'text': 'Tháng',
            'display': True,
            'color': '#000000',
            'font': { 
                'size': 15,
                'family': 'Arial',
                'weight': 'bold'
            },
        },
        'y_label': {
            'text': 'Giờ làm',
            'display': True,
            'color': '#000000',
            'font': { 
                'size': 15,
                'family': 'Arial',
                'weight': 'bold'
            },
        },
        'x_ticks': {
            'font': { 
                'size': 10,
            },
        },
        'y_ticks': {
            'stepSize': 1,
            'font': { 
                'size': 10,
            },
        },
        'datasets': [{
                'label': emp_data['mnv'],
                'data': emp_data['data'],
                'backgroundColor': (color:= random()), 
                'borderColor': color, 
                'borderWidth': 2,
                'fill': False,
                'type': 'bar',
            } for emp_data in emp_list_data],
    }
    return JsonResponse(emp_chart_data, status=200)
