# -*- coding: utf-8 -*-
"""
Created on Wed Jul 17 19:50:02 2019

@author: seoleary
"""
from ipywidgets import widgets, interact
from IPython.display import display
%matplotlib inline
import numpy as np
import matplotlib.pyplot as plt
caption = widgets.Label(value = 'Please choose your Company and Risk Lenses')

a = widgets.Text(
    value='',
    placeholder='Type your company',
    description='Company:',
    disabled=False
)

risk_lenses = ['Cyber', 'Foreign','Business', 'Economic']

items = [widgets.Checkbox(
    value=False,
    description=x,
    disabled=False
)for x in risk_lenses]

left_box = widgets.VBox([items[0], items[1]])
right_box = widgets.VBox([items[2], items[3]])
boxes = widgets.HBox([left_box, right_box])

b = widgets.Button(description = 'Search')

output = widgets.Output()


display(caption,a,boxes, b, output)

def on_button_clicked(b):
    with output:
        print("Searching for "+a.value+" with risks: ",', '.join([items[i].description for i in range(len(items)) if items[i].value ==True]))

b.on_click(on_button_clicked)