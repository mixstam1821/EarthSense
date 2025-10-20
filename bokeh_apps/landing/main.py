from bokeh.models import Div
from bokeh.io import curdoc

# Empty app - template does all the work
curdoc().title = "EarthSense Home"
curdoc().add_root(Div())