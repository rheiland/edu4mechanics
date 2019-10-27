 
# This file is auto-generated from a Python script that parses a PhysiCell configuration (.xml) file.
#
# Edit at your own risk.
#
import os
from ipywidgets import Label,Text,Checkbox,Button,HBox,VBox,FloatText,IntText,BoundedIntText,BoundedFloatText,Layout,Box
    
class UserTab(object):

    def __init__(self):
        
        micron_units = Label('micron')   # use "option m" (Mac, for micro symbol)

        constWidth = '180px'
        tab_height = '500px'
        stepsize = 10

        #style = {'description_width': '250px'}
        style = {'description_width': '25%'}
        layout = {'width': '400px'}

        name_button_layout={'width':'25%'}
        widget_layout = {'width': '15%'}
        units_button_layout ={'width':'15%'}
        desc_button_layout={'width':'45%'}

        param_name1 = Button(description='circle_radius', disabled=True, layout=name_button_layout)
        param_name1.style.button_color = 'lightgreen'

        self.circle_radius = FloatText(
          value=20,
          step=1,
          style=style, layout=widget_layout)

        param_name2 = Button(description='persistence_time', disabled=True, layout=name_button_layout)
        param_name2.style.button_color = 'tan'

        self.persistence_time = FloatText(
          value=0,
          step=0.01,
          style=style, layout=widget_layout)

        param_name3 = Button(description='migration_speed', disabled=True, layout=name_button_layout)
        param_name3.style.button_color = 'lightgreen'

        self.migration_speed = FloatText(
          value=5,
          step=0.1,
          style=style, layout=widget_layout)

        param_name4 = Button(description='migration_bias', disabled=True, layout=name_button_layout)
        param_name4.style.button_color = 'tan'

        self.migration_bias = FloatText(
          value=0.6,
          step=0.1,
          style=style, layout=widget_layout)

        param_name5 = Button(description='number_of_cells', disabled=True, layout=name_button_layout)
        param_name5.style.button_color = 'lightgreen'

        self.number_of_cells = IntText(
          value=5,
          step=0.1,
          style=style, layout=widget_layout)

        param_name6 = Button(description='adhesion_strength', disabled=True, layout=name_button_layout)
        param_name6.style.button_color = 'tan'

        self.adhesion_strength = FloatText(
          value=0.5,
          step=0.1,
          style=style, layout=widget_layout)

        param_name7 = Button(description='repulsion_strength', disabled=True, layout=name_button_layout)
        param_name7.style.button_color = 'lightgreen'

        self.repulsion_strength = FloatText(
          value=0.5,
          step=0.1,
          style=style, layout=widget_layout)

        param_name8 = Button(description='rel_max_adhesion_dist', disabled=True, layout=name_button_layout)
        param_name8.style.button_color = 'tan'

        self.rel_max_adhesion_dist = FloatText(
          value=1.25,
          step=0.1,
          style=style, layout=widget_layout)

        units_button1 = Button(description='micron', disabled=True, layout=units_button_layout) 
        units_button1.style.button_color = 'lightgreen'
        units_button2 = Button(description='min', disabled=True, layout=units_button_layout) 
        units_button2.style.button_color = 'tan'
        units_button3 = Button(description='micron/min', disabled=True, layout=units_button_layout) 
        units_button3.style.button_color = 'lightgreen'
        units_button4 = Button(description='', disabled=True, layout=units_button_layout) 
        units_button4.style.button_color = 'tan'
        units_button5 = Button(description='', disabled=True, layout=units_button_layout) 
        units_button5.style.button_color = 'lightgreen'
        units_button6 = Button(description='', disabled=True, layout=units_button_layout) 
        units_button6.style.button_color = 'tan'
        units_button7 = Button(description='', disabled=True, layout=units_button_layout) 
        units_button7.style.button_color = 'lightgreen'
        units_button8 = Button(description='', disabled=True, layout=units_button_layout) 
        units_button8.style.button_color = 'tan'

        desc_button1 = Button(description='circle radius on which we create cells', disabled=True, layout=desc_button_layout) 
        desc_button1.style.button_color = 'lightgreen'
        desc_button2 = Button(description='mean persistence time', disabled=True, layout=desc_button_layout) 
        desc_button2.style.button_color = 'tan'
        desc_button3 = Button(description='migration speed', disabled=True, layout=desc_button_layout) 
        desc_button3.style.button_color = 'lightgreen'
        desc_button4 = Button(description='migration bias parameter (0=random)', disabled=True, layout=desc_button_layout) 
        desc_button4.style.button_color = 'tan'
        desc_button5 = Button(description='# of cells to create', disabled=True, layout=desc_button_layout) 
        desc_button5.style.button_color = 'lightgreen'
        desc_button6 = Button(description='', disabled=True, layout=desc_button_layout) 
        desc_button6.style.button_color = 'tan'
        desc_button7 = Button(description='', disabled=True, layout=desc_button_layout) 
        desc_button7.style.button_color = 'lightgreen'
        desc_button8 = Button(description='', disabled=True, layout=desc_button_layout) 
        desc_button8.style.button_color = 'tan'

        row1 = [param_name1, self.circle_radius, units_button1, desc_button1] 
        row2 = [param_name2, self.persistence_time, units_button2, desc_button2] 
        row3 = [param_name3, self.migration_speed, units_button3, desc_button3] 
        row4 = [param_name4, self.migration_bias, units_button4, desc_button4] 
        row5 = [param_name5, self.number_of_cells, units_button5, desc_button5] 
        row6 = [param_name6, self.adhesion_strength, units_button6, desc_button6] 
        row7 = [param_name7, self.repulsion_strength, units_button7, desc_button7] 
        row8 = [param_name8, self.rel_max_adhesion_dist, units_button8, desc_button8] 

        box_layout = Layout(display='flex', flex_flow='row', align_items='stretch', width='100%')
        box1 = Box(children=row1, layout=box_layout)
        box2 = Box(children=row2, layout=box_layout)
        box3 = Box(children=row3, layout=box_layout)
        box4 = Box(children=row4, layout=box_layout)
        box5 = Box(children=row5, layout=box_layout)
        box6 = Box(children=row6, layout=box_layout)
        box7 = Box(children=row7, layout=box_layout)
        box8 = Box(children=row8, layout=box_layout)

        self.tab = VBox([
          box1,
          box2,
          box3,
          box4,
          box5,
          # box6,
          # box7,
          # box8,
        ])

    # Populate the GUI widgets with values from the XML
    def fill_gui(self, xml_root):
        uep = xml_root.find('.//microenvironment_setup')  # find unique entry point
        vp = []   # pointers to <variable> nodes
        if uep:
            for var in uep.findall('variable'):
                vp.append(var)

        uep = xml_root.find('.//user_parameters')  # find unique entry point
        self.circle_radius.value = float(uep.find('.//circle_radius').text)
        self.persistence_time.value = float(uep.find('.//persistence_time').text)
        self.migration_speed.value = float(uep.find('.//migration_speed').text)
        self.migration_bias.value = float(uep.find('.//migration_bias').text)
        self.number_of_cells.value = int(uep.find('.//number_of_cells').text)
        # self.adhesion_strength.value = float(uep.find('.//adhesion_strength').text)
        # self.repulsion_strength.value = float(uep.find('.//repulsion_strength').text)
        # self.rel_max_adhesion_dist.value = float(uep.find('.//rel_max_adhesion_dist').text)


    # Read values from the GUI widgets to enable editing XML
    def fill_xml(self, xml_root):
        uep = xml_root.find('.//microenvironment_setup')  # find unique entry point
        vp = []   # pointers to <variable> nodes
        if uep:
            for var in uep.findall('variable'):
                vp.append(var)

        uep = xml_root.find('.//user_parameters')  # find unique entry point
        uep.find('.//circle_radius').text = str(self.circle_radius.value)
        uep.find('.//persistence_time').text = str(self.persistence_time.value)
        uep.find('.//migration_speed').text = str(self.migration_speed.value)
        uep.find('.//migration_bias').text = str(self.migration_bias.value)
        uep.find('.//number_of_cells').text = str(self.number_of_cells.value)
        # uep.find('.//adhesion_strength').text = str(self.adhesion_strength.value)
        # uep.find('.//repulsion_strength').text = str(self.repulsion_strength.value)
        # uep.find('.//rel_max_adhesion_dist').text = str(self.rel_max_adhesion_dist.value)
