# from .models import ThongKe
# # from ImageLabellingTool.models import LabelClass
# from django.http import JsonResponse
# from dateutil.relativedelta import relativedelta
# from django.utils import timezone
# import datetime
# import polars as pl


# TIMEPEELOADER = 60 # Thời gian lấy dữ liệu mới, đơn vị giây

# DFSALARY = None
# LASTGETSALARY = None # Thời gian lấy dữ liệu cuối cùng
# def getSalary():
#     global DFSALARY, LASTGETSALARY
#     print(LASTGETSALARY, timezone.now())
#     if not LASTGETSALARY is None and (timezone.now() - LASTGETSALARY).total_seconds() < TIMEPEELOADER:
#         return DFSALARY
#     print('Get Salary')
#     df= {
#         'thang': [],
#         'luong': [],
#     }
#     for s in ThongKe.objects.all():
#         df['thang'].append(s.month)
#         df['luong'].append(s.luong)
#     df = pl.DataFrame(df)
#     DFSALARY = df
#     LASTGETSALARY = timezone.now()
#     return df

# # LABELCLASS = {}
# # def getLabelClass(id):
# #     global LABELCLASS
# #     if id in LABELCLASS:
# #         return LABELCLASS[id]
# #     label = LabelClass.objects.get(id=id)
# #     LABELCLASS[id] = label
# #     return label

# def chart_summary(request):
#     """ CHART SUMMARY OF ROI MANAGEMENT : CHARTJS
#     - Theo nhãn ROI bằng màu
#     - Trục x: thời gian trong 30 ngày gần nhất
#     - Trục y: số lượng ROI
#     """
#     df = getSalary().clone()
#     # Get 12 months ago
#     now = timezone.now()
#     months = 12
#     start_month = now - relativedelta(months = months) 
#     # Filter by month
#     for i in range(months):
#         end_month = start_month + relativedelta(months=1)  
#         df = df.filter((pl.col('created_at') >= start_month) & (pl.col('created_at') <= end_month))
#         start_month = start_month + relativedelta(months=1)
#     # Chuyển đổi kiểu dữ liệu thời gian thành tháng
#     df = df.with_columns(pl.col('created_at').strftime('%Y-%m'))
#     # Group by luong and thang
#     df = df.groupby(['luong', 'thang']).agg(pl.count('id').alias('count'))
#     # print(df)
#     df= df.to_dict(as_series= False)
#     # print(df)
#     # chartjs
#     # truc x: 12 thang gan nhat, i+1 vi bat dau tu thang hien tai
#     labels = [(start_month + relativedelta(months=i)).strftime('%Y-%m') for i in range(months)]
    
#     # truc y: so luong luong theo thang
#     data = {}
#     for i in range(len(df['luong'])):
#         luong = df['luong'][i]
#         month = df['thang'][i].strftime('%Y-%m')
#         count = df['count'][i]
#         if not luong in data:
#             data[luong] = {}
#         data[luong][month] = count

#     chart_data= {
#         'labels': labels,
#         'title': {
#             'text': 'Lương của nhân viên trong 12 tháng',
#             'display': True,
#             'color': '#000000',
#             'font': { 
#                 'size': 20,
#                 'family': 'Arial',
#                 'weight': 'bold'
#             },
#         },
#         'x_label': {
#             'text': 'Tháng',
#             'display': True,
#             'color': '#000000',
#             'font': { 
#                 'size': 15,
#                 'family': 'Arial',
#                 'weight': 'bold'
#             },
#         },
#         'y_label': {
#             'text': 'Lương',
#             'display': True,
#             'color': '#000000',
#             'font': { 
#                 'size': 15,
#                 'family': 'Arial',
#                 'weight': 'bold'
#             },
#         },
#         'x_ticks': {
#             'font': { 
#                 'size': 10,
#             },
#         },
#         'y_ticks': {
#             'stepSize': 1,
#             'font': { 
#                 'size': 10,
#             },
#         },
#         'datasets': [{
#                 'label': luong,
#                 'data': [data[luong].get(month, 0) for month in months],
#                 'backgroundColor': '#000000',
#                 'borderColor': '#000000',
#                 'borderWidth': 2,
#                 'fill': False,
#                 'type': 'line',
#             } for luong in data],
#     }
#     return JsonResponse(chart_data, status=200)

   
# # def chart_label_by_group(request):
# #     # ?group=group_name
# #     group= request.GET.get('group', None)
# #     if group is None:
# #         return JsonResponse({"error": "Missing group"}, status=400)
# #     """
# #     - Trục x: label name
# #     - Trục y: số lượng ROI
# #     """
# #     df= getROIs().clone()
# #     # label_id in group
# #     labels = LabelClass.objects.filter(group__group_name=group).values_list('id', flat=True)
# #     labels = list(labels)
# #     # Filter by label_id
# #     # print(labels)
# #     df = df.filter(pl.col('label').is_in(labels))
# #     # Group by label
# #     df = df.groupby('label').agg(pl.count('id').alias('count'))
# #     df= df.to_dict(as_series= False)
# #     # print(df)
# #     # chartjs
# #     data= {
# #         'labels': [getLabelClass(label_id).name for label_id in df['label']],
# #         'datasets': [{
# #             'label': 'Number of ROIs',
# #             'data': df['count'],
# #             'backgroundColor': [getLabelClass(label_id).default_colour for label_id in df['label']],
# #             'borderColor': [getLabelClass(label_id).default_colour for label_id in df['label']],
# #             'borderWidth': 2,
# #             'fill': False,
# #         }],
# #         'title': {
# #             'text': 'Number of ROIs by label name in group {}'.format(group),
# #             'display': True,
# #             'color': '#000000',
# #             'font': { 
# #                 'size': 20,
# #                 'family': 'Arial',
# #                 'weight': 'bold'
# #             },
# #         },
# #     }
# #     return JsonResponse(data, status=200)

# # def chart_label_type_by_group(request):
# #     #?group=group_name
# #     group= request.GET.get('group', None)
# #     if group is None:
# #         return JsonResponse({"error": "Missing group"}, status=400)
    
# #     """
# #     - Trục x: label type
# #     - Trục y: số lượng ROI
# #     """
# #     df= getROIs().clone()
# #     # label_id in group
# #     labels = LabelClass.objects.filter(group__group_name=group).values_list('id', flat=True)
# #     labels = list(labels)
# #     # Filter by label_id
# #     # print(labels)
# #     df = df.filter(pl.col('label').is_in(labels))
# #     # Group by label_type
# #     df = df.groupby('type').agg(pl.count('id').alias('count'))
# #     df= df.to_dict(as_series= False)
# #     # print(df)
# #     # chartjs
# #     data= {
# #         'labels': df['type'],
# #         'datasets': [{
# #             'label': 'Number of ROIs',
# #             'data': df['count'],
# #             # 'backgroundColor': ['#FF6384', '#36A2EB', '#FFCE56'],
# #             # 'borderColor': ['#FF6384', '#36A2EB', '#FFCE56'],
# #             'borderWidth': 2,
# #             'fill': False,
# #             'type': 'bar',
# #         }],
# #         'title': {
# #             'text': 'Number of ROIs by label type in group {}'.format(group),
# #             'display': True,
# #             'color': '#000000',
# #             'font': { 
# #                 'size': 20,
# #                 'family': 'Arial',
# #                 'weight': 'bold'
# #             },
# #         },
# #         'x_label': {
# #             'text': 'Label type',
# #             'display': True,
# #             'color': '#000000',
# #             'font': { 
# #                 'size': 15,
# #                 'family': 'Arial',
# #                 'weight': 'bold'
# #             },
# #         },
# #         'y_label': {
# #             'text': 'Number of ROIs',
# #             'display': True,
# #             'color': '#000000',
# #             'font': { 
# #                 'size': 15,
# #                 'family': 'Arial',
# #                 'weight': 'bold'
# #             },
# #         },
# #         'x_ticks': {
# #             'font': { 
# #                 'size': 10,
# #             },
# #         },
# #         'y_ticks': {
# #             'stepSize': 1,
# #             'font': { 
# #                 'size': 10,
# #             },
# #         },
# #     }
# #     return JsonResponse(data, status=200)