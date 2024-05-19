# from .models import ThongKe
from Payroll.models import NguoiLD, BangLuong
# from ImageLabellingTool.models import LabelClass
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
        # df['mnv'].append(s.mnv)
        # print(s.month)
        df['thang'].append(s.month) #4
        # print(s.luong)
        df['luong'].append(s.luong) #1000000
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
    year = int(now.year)
    months = 12
    start_month = now - relativedelta(months = months) 
    df= df.to_dict(as_series= False)
    # chartjs
    # truc x: 12 thang gan nhat, i+1 vi bat dau tu thang hien tai
    labels = [(start_month + relativedelta(months=i+1)).strftime('%Y-%m') for i in range(months)]
    
    
    # truc y: so luong luong theo thang
    data = {}
    for i in range(len(df['thang'])):
        month = str(year) + "-" + str(df['thang'][i])
        luong = df['luong'][i]
        data[month] = luong
        
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
                'backgroundColor': '#000000',
                'borderColor': '#000000',
                'borderWidth': 2,
                'fill': False,
                'type': 'line',
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
        year = int(now.year)
        months = 12
        start_month = now - relativedelta(months = months) 
        d= df1.to_dict(as_series= False)
        # print(d)
        # chartjs
        # truc x: 12 thang gan nhat, i+1 vi bat dau tu thang hien tai
        labels = [(start_month + relativedelta(months=i+1)).strftime('%Y-%m') for i in range(months)]
    
    
        # truc y: so luong luong theo thang
        data = {}
        for i in range(len(df1['thang'])):
            month = str(year) + "-" + str(df1['thang'][i])
            luong = df1['luong'][i]
            data[month] = luong
        # print(data)
            # Thực hiện thống kê lương cho nhân viên hiện tại
            # Tương tự như trong hàm chart_summary trước đó

            # Thêm dữ liệu thống kê vào danh sách all_chart_data
        emp_list_data.append({
                'mnv': mnv,
                'data': data  
            })
    # print(emp_list_data[data])
    
    emp_chart_data= {
        # 'labels' : labels,
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
                'backgroundColor': random(), 
                'borderColor': random(), 
                'borderWidth': 2,
                'fill': False,
                'type': 'line',
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
    year = int(now.year)
    months = 12
    start_month = now - relativedelta(months = months) 
    d= df.to_dict(as_series= False)
    # chartjs
    # truc x: 12 thang gan nhat, i+1 vi bat dau tu thang hien tai
    labels = [(start_month + relativedelta(months=i+1)).strftime('%Y-%m') for i in range(months)]

    data = {}
    for i in range(len(df['thang'])):
        month = str(year) + "-" + str(df['thang'][i])
        giolam = df['giolam'][i]
        data[month] = giolam
        # count = df['count'][i]
        # data[month] = count
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
                'backgroundColor': '#000000',
                'borderColor': '#000000',
                'borderWidth': 2,
                'fill': False,
                'type': 'line',
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
        # print(e, 'ehjghghgfgdgfchgdgfh')
        mnv = e
        df1 = getGiolam(mnv)#.clone()
        # print(df1)
        now = timezone.now()
        year = int(now.year)
        months = 12
        start_month = now - relativedelta(months = months) 
        d= df1.to_dict(as_series= False)
        # print(d)
        # chartjs
        # truc x: 12 thang gan nhat, i+1 vi bat dau tu thang hien tai
        labels = [(start_month + relativedelta(months=i+1)).strftime('%Y-%m') for i in range(months)]
    
    
        # truc y: so luong luong theo thang
        data = {}
        for i in range(len(df1['thang'])):
            month = str(year) + "-" + str(df1['thang'][i])
            giolam = df1['giolam'][i]
            data[month] = giolam
        # print(data)
            # Thực hiện thống kê lương cho nhân viên hiện tại
            # Tương tự như trong hàm chart_summary trước đó

            # Thêm dữ liệu thống kê vào danh sách all_chart_data
        emp_list_data.append({
                'mnv': mnv,
                'data': data  
            })
    # print(emp_list_data[data])
    
    emp_chart_data= {
        # 'labels' : labels,
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
                'backgroundColor': random(), 
                'borderColor': random(), 
                'borderWidth': 2,
                'fill': False,
                'type': 'line',
            } for emp_data in emp_list_data],
    }
    return JsonResponse(emp_chart_data, status=200)
