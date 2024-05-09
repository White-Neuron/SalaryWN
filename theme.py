# theme
from admin_interface.models import Theme
try:
    theme= Theme.objects.get(id=2)
    theme.delete()
except:
    pass
theme = Theme(
    id= 2,
    name='White Neuron',
    title='WN Payroll System',
    active= True,
    title_visible=True,
    favicon='favicon/WhiteNeuron.jpg',
    logo= 'logo/WN.png',
    logo_max_height= 45,
    logo_visible=True,
    css_header_background_color='#ffffff', # white
    title_color='#000000', # black
    css_header_link_color='#000000', # màu nền của các link trong header
    css_module_background_color='#000000', # màu nền của các module
    css_module_link_hover_color='#000000', # màu nền của các link khi hover
    css_save_button_background_color='#000000', # màu nền của nút save
    show_inlines_as_tabs= True,
)
theme.save()