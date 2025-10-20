"""
FORTH-RTM SSR & GDB evaluation. PhD Thesis: https://www.didaktorika.gr/eadd/handle/10442/59941
Creator: Michael Stamatis, email: mixstam1453@gmail.com
"""
from bokeh.layouts import row, column
from bokeh.plotting import figure, curdoc
from bokeh.transform import linear_cmap, dodge
from bokeh.models import (
    ColumnDataSource,Range1d,
    TableColumn,
    DataTable,
    ColorBar,
    TabPanel,
    InlineStyleSheet,
    Tabs,
    CustomJS,
    CustomJSHover,
    HoverTool,
    Div,
    DatetimeTickFormatter,
    TextAreaInput,
    CrosshairTool,
    Span,
    BoxEditTool,
    FreehandDrawTool,
)
from bokeh.palettes import interp_palette
import numpy as np, pandas as pd, xarray as xr, scipy as sp

tais = InlineStyleSheet(
    css=""" /* Outer container styling */ :host { background: #1a1a1a !important; border-radius: 14px !important; padding: 16px !important; box-shadow: 0 4px 18px #0006 !important; } /* Title label styling */ :host .bk-input-group label, :host .bk-textinput-title { color: #34ffe0 !important; font-size: 1.14em !important; font-family: 'Fira Code', monospace !important; font-weight: bold !important; margin-bottom: 12px !important; letter-spacing: 0.5px !important; text-shadow: 0 2px 12px #34ffe077, 0 1px 3px #222 !important; } /* The textarea input box - changed from input[type="text"] to textarea */ :host textarea { background: #23233c !important; color: #f9fafb !important; border: 2px solid #06b6d4 !important; border-radius: 8px !important; padding: 11px 15px !important; font-size: 1.08em !important; font-family: 'Fira Code', monospace !important; transition: border 0.12s ease, box-shadow 0.12s ease !important; box-shadow: none !important; resize: vertical !important; min-height: 120px !important; } /* On hover/focus: red border with glowing effect */ :host textarea:hover, :host textarea:focus { border-color: #ff3049 !important; box-shadow: 0 0 0 2px #ff304999, 0 0 15px #ff3049bb !important; outline: none !important; } /* Placeholder text */ :host textarea::placeholder { color: #9ca3af !important; opacity: 0.7 !important; font-style: italic !important; } /* Scrollbar styling for webkit browsers */ :host textarea::-webkit-scrollbar { width: 8px !important; } :host textarea::-webkit-scrollbar-track { background: #1a1a2e !important; border-radius: 4px !important; } :host textarea::-webkit-scrollbar-thumb { background: #06b6d4 !important; border-radius: 4px !important; } :host textarea::-webkit-scrollbar-thumb:hover { background: #ff3049 !important; } """
)
tabs_style = InlineStyleSheet(
    css=""" /* Main tabs container */ :host { background: #2d2d2d !important; border-radius: 14px !important; padding: 8px !important; margin: 10px !important; box-shadow: 0 6px 20px rgba(220, 28, 221, 0.4), 0 2px 10px rgba(0, 0, 0, 0.3) !important; border: 1px solid rgba(0, 191, 255, 0.3) !important; } /* Tab navigation bar */ :host .bk-tabs-header { background: transparent !important; border-bottom: 2px solid #00bfff !important; margin-bottom: 8px !important; } /* Individual tab buttons */ :host .bk-tab { background: linear-gradient(135deg, #2d2d2d 0%, #3a3a3a 100%) !important; color: #00bfff !important; border: 1px solid #555 !important; border-radius: 8px 8px 0 0 !important; padding: 12px 20px !important; margin-right: 4px !important; font-family: 'Arial', sans-serif !important; font-weight: 600 !important; font-size: 0.95em !important; text-transform: uppercase !important; letter-spacing: 0.5px !important; transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1) !important; position: relative !important; overflow: hidden !important; } /* Tab hover effect */ :host .bk-tab:hover { background: linear-gradient(135deg, #dc1cdd 0%, #ff1493 100%) !important; color: #ffffff !important; border-color: #dc1cdd !important; box-shadow: 0 4px 15px rgba(220, 28, 221, 0.5) !important; transform: translateY(-2px) !important; } /* Active tab styling */ :host .bk-tab.bk-active { background: linear-gradient(135deg, #00bfff 0%, #0080ff 100%) !important; color: #000000 !important; border-color: #00bfff !important; box-shadow: 0 4px 20px rgba(0, 191, 255, 0.6), inset 0 2px 0 rgba(255, 255, 255, 0.3) !important; transform: translateY(-1px) !important; font-weight: 700 !important; } /* Active tab glow effect */ :host .bk-tab.bk-active::before { content: '' !important; position: absolute !important; top: 0 !important; left: 0 !important; right: 0 !important; bottom: 0 !important; background: linear-gradient(45deg, transparent 30%, rgba(255, 255, 255, 0.1) 50%, transparent 70%) !important; animation: shimmer 2s infinite !important; } @keyframes shimmer { 0% { transform: translateX(-100%); } 100% { transform: translateX(100%); } } /* Tab content area */ :host .bk-tab-content { background: transparent !important; padding: 16px !important; border-radius: 0 0 10px 10px !important; } /* Focus states for accessibility */ :host .bk-tab:focus { outline: 2px solid #00bfff !important; outline-offset: 2px !important; } /* Disabled tab state */ :host .bk-tab:disabled { background: #1a1a1a !important; color: #666 !important; cursor: not-allowed !important; opacity: 0.5 !important; } """
)
from bokeh.models import WMTSTileSource

# colorss=["rgb(16, 94, 0)", "rgb(0, 185, 9)", "rgb(0, 255, 64)","rgb(0, 28, 121)", "rgb(0, 60, 255)","rgb(0, 200, 255)","rgb(255, 0, 0)","rgb(218, 116, 0)","rgb(255, 230, 0)", "rgb(111, 2, 161)", "#ff35a4", "#000000"]
colorss = ["deepskyblue", "orange"]


def cusj():
    num = 1
    return CustomJSHover(
        code=f"""
    special_vars.indices = special_vars.indices.slice(0,{num})
    return special_vars.indices.includes(special_vars.index) ? " " : " hidden "
    """
    )


def hovfun(tltl):
    return (
        """<div @hidden{custom} style="background-color: #fff0eb; padding: 5px; border-radius: 5px; box-shadow: 0px 0px 5px rgba(0,0,0,0.3);">        <font size="3" style="background-color: #fff0eb; padding: 5px; border-radius: 5px;"> """
        + tltl
        + """ <br> </font> </div> <style> :host { --tooltip-border: transparent;  /* Same border color used everywhere */ --tooltip-color: transparent; --tooltip-text: #2f2f2f;} </style> """
    )


curdoc().theme = "dark_minimal"
# curdoc().theme = Theme(filename=r'/home/michael/MEGA/MEGAsync/mike2.json') #C:\Users\michail.stamatis\Desktop\training\PythonProjects\mist\mike2.json
p9 = {"active_scroll": "wheel_zoom"}


def add_extras(p, drawline_width=5, drawalpha=0.4, drawcolor="red", cross=1):
    # box edit tool wants to be first
    sourcebox = ColumnDataSource(
        data=dict(
            x=[0],
            y=[0],
            width=[0],
            height=[0],
            color=["grey"],
            alpha=[0.35],
        ),
        # default_values = dict( color="grey", alpha=0.35, ),
    )
    rbox = p.rect(
        "x", "y", "width", "height", color="color", alpha="alpha", source=sourcebox
    )
    box_tool = BoxEditTool(
        renderers=[rbox],
    )
    p.add_tools(box_tool)

    # draw tool
    rdraw = p.multi_line(
        [], [], line_width=drawline_width, alpha=drawalpha, color=drawcolor
    )
    draw_tool = FreehandDrawTool(renderers=[rdraw], num_objects=100)
    p.add_tools(draw_tool)

    p.add_tools("box_select", "lasso_select", "tap")
    Span_height = Span(
        dimension="height", line_dash="dashed", line_width=2, line_color="#878787"
    )
    Crosshair_Tool = CrosshairTool(overlay=Span_height)
    if cross == 1:
        p.add_tools(Crosshair_Tool)
    if len(p.legend) > 0:
        p.legend.location = "center"
        p.add_layout(p.legend[0], "right")
        p.legend.click_policy = "hide"
        p.legend.label_text_font_size = "13pt"
        # change border and background of legend
        p.legend.border_line_width = 1.5
        p.legend.border_line_color = "black"
        p.legend.border_line_alpha = 0.7
        p.legend.background_fill_alpha = 0.1
        p.legend.background_fill_color = "silver"

    # re-arange y axis when hide a glyph! not works if i set the y_range
    # p.y_range.only_visible = True


# ------ MY DATA -------- #

df = pd.read_csv(
    "data/_DA_FMCX_1984_2018_lat0_-90_lat1_90_lon0_-180_lon1_180_thresalt_0_500_thresagr_0.7__GEBA_ANOMALIES_GLOBE_rf.txt"
)
df["Date"] = pd.to_datetime(df["year"].astype(str) + "-" + df["month"].astype(str))
# df.fillna('-', inplace=True)

df2 = pd.read_csv(
    "data/_AF_FMCX_1984_2018_lat0_-90_lat1_90_lon0_-180_lon1_180_thresalt_0_500_thresagr_0.7__GEBA_FLUXES_GLOBE_rf.txt"
)
df2["Date"] = pd.to_datetime(df2["year"].astype(str) + "-" + df2["month"].astype(str))

df1 = pd.read_csv(
    "data/_AF_FMCX_1984_2018_lat0_-90_lat1_90_lon0_-180_lon1_180_thresalt_0_500_thresagr_0.7__GEBA_FLUXES_GLOBE_eva.txt"
)
df1["slopeA"] = df1["slopeA"] * 120
df1["slopeF"] = df1["slopeF"] * 120
df1["signW"] = ["Yes" if i > 0 else "No" for i in df1["sign"]]
df1b = pd.read_csv(
    "data/_DA_FMCX_1984_2018_lat0_-90_lat1_90_lon0_-180_lon1_180_thresalt_0_500_thresagr_0.7__GEBA_ANOMALIES_GLOBE_eva.txt"
)
df1 = df1.round(3)
df1b = df1b.round(3)

lisa = df1[
    [
        "lon",
        "lat",
        "id",
        "r",
        "bias",
        "bias_pc",
        "rmse",
        "slope",
        "sign",
        "slopeF",
        "slopeA",
    ]
].values.tolist()

# p1: GDB
fmc_ssr = xr.open_dataset(
    "data/FMCX_8418_SurfaceDown_f.nc"
)["SurfaceDown"].sel(time=slice("1984-01-01", "2018-12-31"))
gdbdc = (
    xr.open_dataset(
        "data/__anom_8418_slopes_FMCX8418_SurfaceDown_.nc"
    )["slope"].rename("GDB")
    * 120
)


def crd():
    import cartopy.feature as cf, numpy as np

    # create the list of coordinates separated by nan to avoid connecting the lines
    x_coords = []
    y_coords = []
    for coord_seq in cf.COASTLINE.geometries():
        x_coords.extend([k[0] for k in coord_seq.coords] + [np.nan])
        y_coords.extend([k[1] for k in coord_seq.coords] + [np.nan])

    # x_coords2 = []
    # y_coords2 = []
    # for coord_seq in cf.BORDERS.geometries():
    #     x_coords2.extend([k[0] for k in coord_seq.coords] + [np.nan])
    #     y_coords2.extend([k[1] for k in coord_seq.coords] + [np.nan])
    return (
        x_coords,
        y_coords,
    )  # x_coords2,y_coords2


x_coords, y_coords = [i for i in crd()]
xdates = pd.date_range("1984", "2018-12-31", freq="MS")  # .astype('datetime64[M]')
# ------ The App ------ #

# p1) stations map
latitudes = fmc_ssr.lat.values.tolist()
longitudes = fmc_ssr.lon.values.tolist()
lati = np.repeat(latitudes, len(longitudes))
loni = np.tile(longitudes, len(latitudes))
df1["hidden"] = df1.lat.values


# --- Conversion functions ---
def lon_to_mercator(lon):
    lon = np.array(lon, dtype=np.float64)  # ensure numeric
    return lon * 20037508.34 / 180.0


def lat_to_mercator(lat):
    lat = np.array(lat, dtype=np.float64)
    lat = np.clip(lat, -89.9999, 89.9999)  # avoid infinite values near poles
    return np.log(np.tan((90 + lat) * np.pi / 360.0)) * 20037508.34 / np.pi


# --- Convert your data ---
df1["lon2"] = lon_to_mercator(df1["lon"].values)
df1["lat2"] = lat_to_mercator(df1["lat"].values)
s1 = ColumnDataSource(df1)


# s1 = ColumnDataSource(df1)

# Set up Bokeh figure
# p1 = figure(output_backend="webgl",
#     border_fill_color="#2d2d2d",
#     background_fill_color="#2d2d2d",min_border_bottom=60, min_border_right=170,
#     width=850,
#     height=450,
#     x_range=(-180,180),
#     y_range=(-90,90),
#     title=r"$$Stations' GDB, 1984-2018$$", **p9,styles={'margin-top': '5px','margin-left': '10px','padding': '15px','border-radius': '10px','box-shadow': '0 4px 4px rgb(220, 28, 221,0.5)','background-color': '#2d2d2d'},
# )

# Set up Bokeh figure
p1 = figure(
    x_axis_type="mercator",
    y_axis_type="mercator",
    border_fill_color="#2d2d2d",
    background_fill_color="#2d2d2d",
    min_border_bottom=60,
    min_border_right=170,
    width=850,
    height=450,
    x_range=Range1d(-20118754.34, 20118754.34),
    y_range=Range1d(-15918754.17, 15918754.17),
    title=r"$$Stations' GDB, 1984-2018$$",
    **p9,
    styles={
        "margin-top": "5px",
        "margin-left": "10px",
        "padding": "15px",
        "border-radius": "10px",
        "box-shadow": "0 4px 4px rgb(220, 28, 221,0.5)",
        "background-color": "#2d2d2d",
    },
)


dark_url = "https://basemaps.cartocdn.com/dark_all/{Z}/{X}/{Y}.png" # "http://a.basemaps.cartocdn.com/rastertiles/voyager/{Z}/{X}/{Y}.png"  # "https://basemaps.cartocdn.com/dark_all/{Z}/{X}/{Y}.png"
tile_provider = WMTSTileSource(url=dark_url)
p1.add_tile(tile_provider)



mike2 = (
    "#000063",
    "#123aff",
    "#00aeff",
    "#26fff4",
    "#00ff95",
    "#ffffff",
    "#ffff00",
    "#ff8a15",
    "#ff2a1b",
    "#db0000",
    "#4b0000",
)
bo_mike2 = interp_palette(mike2, 255)

color_mapper = linear_cmap(field_name="slopeA", palette=bo_mike2, low=-35, high=35)

color_bar = ColorBar(
    color_mapper=color_mapper["transform"],
    location=(0, 0),
    title=r"$$Wm^{-2}decade{-1}$$",
    title_standoff=1,
    title_text_baseline="middle",
    title_text_align="right",
    background_fill_alpha=0,
)
p1.add_layout(color_bar, "right")

p11 = p1.scatter(
    x="lon2",
    y="lat2",
    source=s1,
    size=18,
    alpha=0.9,
    color=color_mapper,
    line_color="black",
    line_width=1,
)  # selection_line_color="firebrick",selection_line_width=8,nonselection_fill_alpha=1,
# p12 = p1.line(x = x_coords,y = y_coords, line_width=1, line_color='black')
x_coords_merc = lon_to_mercator(x_coords)
y_coords_merc = lat_to_mercator(y_coords)
# p12 = p1.line(x=x_coords_merc, y=y_coords_merc, line_width=1, line_color='black')


tltl = """<i>Station:</i> <b>@id</b> <br> <i>Latitude:</i> <b>@lat</b><br> <i>Longitude:</i> <b>@lon</b><br> <i>GDB:</i> <b>@slopeA{0.0000}</b> <br> <i>SignAgreement:</i> <b>@signW</b></b>"""
p1.add_tools(
    HoverTool(
        tooltips=hovfun(tltl),
        formatters={"@hidden": cusj()},
        mode="mouse",
        renderers=[p11],
        attachment="left",
        show_arrow=False,
    )
)

add_extras(p1, cross=0)
# p11.selection_glyph = Scatter(size=22, line_color="red", line_width=5)
# p11.nonselection_glyph = None
p1.grid.visible = False

# p2) bar plot

variables = [
    "Jan",
    "Feb",
    "Mar",
    "Apr",
    "May",
    "Jun",
    "Jul",
    "Aug",
    "Sep",
    "Oct",
    "Nov",
    "Dec",
]
yy = ["Model", "Stations"]
forp2 = df2.groupby(["id", "month"]).ssr.mean().reset_index()
forp2b = df2.groupby(["id", "month"]).ssrb.mean().reset_index()

data2 = {
    "variables": variables,
    "Model": [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],  # forp2.iloc[:12,2],
    "Station": [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],  # forp2b.iloc[:12,2],
}
source2 = ColumnDataSource(data=data2)

p2 = figure(
    x_range=variables,
    y_axis_label=r"$$Wm^{-2}$$",
    title=r"$$SSR~Annual~Cycle$$",
    width=850,
    height=490,
    min_border_bottom=60,
    min_border_right=170,
    background_fill_color="#2d2d2d",
    border_fill_color="#2d2d2d",
    styles={
        "margin-top": "10px",
        "margin-left": "10px",
        "padding": "15px",
        "border-radius": "10px",
        "box-shadow": "0 4px 4px rgb(220, 28, 221,0.5)",
        "background-color": "#2d2d2d",
    },
)

p22 = p2.vbar(
    x=dodge("variables", -0.2, range=p2.x_range),
    top="Model",
    source=source2,
    color="deepskyblue",
    hover_line_color="red",
    hover_line_width=3,
    width=0.4,
    legend_label="Model",
    line_color="black",
)

p222 = p2.vbar(
    x=dodge("variables", 0.2, range=p2.x_range),
    top="Station",
    source=source2,
    color="orange",
    hover_line_color="red",
    hover_line_width=3,
    width=0.4,
    legend_label="Station",
    line_color="black",
)

p2.x_range.range_padding = 0.05
p2.xgrid.grid_line_color = None
p2.add_tools(
    HoverTool(
        tooltips="""<div style="background-color: #f0f0f0; padding: 5px; border-radius: 5px; box-shadow: 0px 0px 5px rgba(0,0,0,0.3);">        <font size="3" style="background-color: #f0f0f0; padding: 5px; border-radius: 5px;">
                       <b>@variables</b> <br> 
                       <i>Model:</i> <b>@Model{0.00}</b> <br> 
                        <i>Station:</i> <b>@Station{0.00}</b> <br> 
        </font> </div> <style> :host { --tooltip-border: transparent;  /* Same border color used everywhere */ --tooltip-color: transparent; --tooltip-text: #2f2f2f;} </style> """,
        mode="mouse", point_policy="follow_mouse",
    )
)
add_extras(p2, cross=0)
# p2.legend.location = "center";  p2.add_layout(p2.legend[0], 'right')
# show(p2)


# p3) The Drivers
s3 = ColumnDataSource(data=dict(x=[], model=[], station=[]))
p3 = figure(
    width=1000,
    height=450,
    x_axis_type="datetime",
    x_range=(pd.Timestamp("1984"), pd.Timestamp("2018")),
    border_fill_color="#2d2d2d",
    background_fill_color="#2d2d2d",
    title=r"$$SSR~Model~vs~Station$$",
    y_axis_label=r"$$Wm^{-2}$$",
    **p9,
    min_border_bottom=60,
    min_border_right=170,
    styles={
        "margin-top": "5px",
        "margin-left": "10px",
        "padding": "15px",
        "border-radius": "10px",
        "box-shadow": "0 4px 4px rgb(220, 28, 221,0.5)",
        "background-color": "#2d2d2d",
    },
)
p33 = p3.line(
    "x", "model", source=s3, line_alpha=0, line_width=0
)  # p3.circle('x', 'AC1', source=s3, color='blue',size=0)
p3.xaxis[0].formatter = DatetimeTickFormatter(years="%Y-%m")

s3list = ["model", "station"]
for kk in range(2):
    p3.line(
        "x",
        s3list[kk],
        legend_label=s3list[kk],
        source=s3,
        color=colorss[kk],
        line_width=2,
    )
    # p3.circle('x', s3list[kk],legend_label=s3list[kk], source=s3, color=colorss[kk],size=10)

p3.add_tools(
    HoverTool(
        tooltips="""<div style="background-color: #f0f0f0; padding: 5px; border-radius: 5px; box-shadow: 0px 0px 5px rgba(0,0,0,0.3);">        <font size="3" style="background-color: #f0f0f0; padding: 5px; border-radius: 5px;">
            <b>Monthly SSR Anomalies<br> (1984-2018)</b><br>
            <i>Date:</i> <b>@x{%Y-%m}</b> <br> 
            <i>Model:</i> <b>@model{0.00} Wm<sup>-2</sup></b> <br>
                       <i>Station:</i> <b>@station{0.00} Wm<sup>-2</sup></b> <br>
        </font> </div> <style> :host { --tooltip-border: transparent;  /* Same border color used everywhere */ --tooltip-color: transparent; --tooltip-text: #2f2f2f;} </style> """,
        formatters={"@x": "datetime"},
        mode="vline",
        point_policy="snap_to_data",
        line_policy="none",
        attachment="left",
        show_arrow=False,
        renderers=[p33],
    )
)
add_extras(p3)
# p3.legend.location = "center"
# p3.add_layout(p3.legend[0], 'right')

# p4)

s4 = ColumnDataSource(data=dict(model=[], station=[], hidden=[]))
sss4 = ColumnDataSource(data=dict(x=[], y=[]))
# Set up Bokeh figure
p4 = figure(
    min_border_bottom=110,
    min_border_right=70,
    y_range=(0, 400),
    x_range=(0, 400),
    border_fill_color="#2d2d2d",
    background_fill_color="#2d2d2d",
    y_axis_label=r"$$Model~(Wm^{-2})$$",
    x_axis_label=r"$$Station~(Wm^{-2})$$",
    width=420,
    height=420,
    title=r"$$SSR~Model~vs~Station$$",
    **p9,
    styles={
        "margin-top": "10px",
        "margin-left": "10px",
        "padding": "15px",
        "border-radius": "10px",
        "background-color": "#2d2d2d",
    },
)

p44 = p4.scatter(
    x="station",
    y="model",
    source=s4,
    size=18,
    alpha=0.9,
    color="deepskyblue",
    line_color="black",
    line_width=1,
)
p4.line(x=[0, 400], y=[0, 400], color="grey", line_dash="dashed", line_width=1)
p4.line(x="x", y="y", color="red", line_width=5, source=sss4)


tltl = """<i>Station:</i> <b>@station{0.00} Wm<sup>-2</sup></b> <br> <i>Model:</i> <b>@model{0.00} Wm<sup>-2</sup></b></b>"""
p4.add_tools(
    HoverTool(
        tooltips=hovfun(tltl),
        formatters={"@hidden": cusj()},
        mode="mouse",
        renderers=[p44],
    )
)
add_extras(p4, cross=0)


########
# p4d)

s4d = ColumnDataSource(data=dict(model=[], station=[], hidden=[]))
sss4d = ColumnDataSource(data=dict(x=[], y=[]))
# Set up Bokeh figure
p4d = figure(
    min_border_bottom=110,
    min_border_right=70,
    y_range=(-100, 100),
    x_range=(-100, 100),
    border_fill_color="#2d2d2d",
    background_fill_color="#2d2d2d",
    y_axis_label=r"$$Model~(Wm^{-2})$$",
    x_axis_label=r"$$Station~(Wm^{-2})$$",
    width=420,
    height=420,
    title=r"$$SSR~Model~vs~Station$$",
    **p9,
    styles={
        "margin-top": "10px",
        "margin-left": "10px",
        "padding": "15px",
        "border-radius": "10px",
        "background-color": "#2d2d2d",
    },
)

p44d = p4d.scatter(
    x="station",
    y="model",
    source=s4d,
    size=18,
    alpha=0.9,
    color="lime",
    line_color="black",
    line_width=1,
)
p4d.line(x=[-200, 200], y=[-200, 200], color="grey", line_dash="dashed", line_width=1)
p4d.line(x="x", y="y", color="red", line_width=5, source=sss4d)


tltl = """<i>Station:</i> <b>@station{0.00} Wm<sup>-2</sup></b> <br> <i>Model:</i> <b>@model{0.00} Wm<sup>-2</sup></b></b>"""
p4d.add_tools(
    HoverTool(
        tooltips=hovfun(tltl),
        formatters={"@hidden": cusj()},
        mode="mouse",
        renderers=[p44d],
    )
)
add_extras(p4d, cross=0)
# Combine tabs into a single layout
tabs_layout = Tabs(
    tabs=[
        TabPanel(child=p4, title="SSR Fluxes"),
        TabPanel(child=p4d, title="SSR anomalies"),
    ],
    stylesheets=[tabs_style], styles = {'height':'495px'}
    #    styles={'color':'deepskyblue','margin-top': '10px','margin-left': '10px','padding': '0px','border-radius': '10px','box-shadow': '0 4px 4px rgb(220, 28, 221,0.5)','background-color': '#2d2d2d'}
)

# p5
data5 = dict(
    Metrics=[
        "Name",
        "Lat",
        "Lon",
        "Alt",
        "StartYear",
        "EndYear",
        "N",
        "slope",
        "slope_anom",
        "intercept",
        "intercept_anom",
        "R",
        "Ranom",
        "Bias",
        "Bias %",
        "Rmse",
        "Rmse %",
        "ChangeModel",
        "pv95Model",
        "ChangeStation",
        "pv95Station",
        "Sign Agreement",
    ],
    Values=["-"] * 22,
)
source5 = ColumnDataSource(data5)

columns5 = [
    TableColumn(
        field="Metrics",
        title="Metrics",
    ),
    TableColumn(
        field="Values",
        title="Values",
    ),
]
data_table = DataTable(
    source=source5,
    columns=columns5,
    width=400,
    height=490,
    row_height=19,
    styles={
        "margin-top": "10px",
        "margin-left": "10px",
        "padding": "15px",
        "border-radius": "10px",
        "box-shadow": "0 4px 4px rgb(220, 28, 221,0.5)",
        "background-color": "hsl(0, 13%, 95%)",
        "color": "black",
    },
    background="hsl(0, 13%, 95%)",
)
table_style = InlineStyleSheet(
    css=""" .slick-header-columns { font-family: arial; font-weight: bold; font-size: 12pt; color: #ff0bb6; text-align: right; } .slick-row { font-size: 9pt; font-family: arial; text-align: center; } """
)
data_table.stylesheets = [table_style]

# take some notes
text_area_input = TextAreaInput(
    value=" ", rows=15, cols=150, title="My notes:", stylesheets=[tais]
)
text_area_input.js_on_change(
    "value",
    CustomJS(
        code="""
    console.log('text_area_input: value=' + this.value, this.toString())
"""
    ),
)


# Callback function
def update_timeseries(attr, old, new):

    inde = df1.iloc[new[0], :].id
    clon = df1.iloc[new[0], :].lon
    clat = df1.iloc[new[0], :].lat
    source2.data = dict(
        variables=variables,
        Model=forp2[forp2.id == inde].ssr.values,
        Station=forp2b[forp2b.id == inde].ssrb.values,
    )
    s3.data = dict(
        x=df[df.id == inde].Date.values,
        model=df[df.id == inde].ssr.values,
        station=df[df.id == inde].ssrb.values,
    )
    s4.data = dict(
        model=df2[df2.id == inde].ssr.values,
        station=df2[df2.id == inde].ssrb.values,
        hidden=df2[df2.id == inde].ssrb.values,
    )
    s4d.data = dict(
        model=df[df.id == inde].ssr.values,
        station=df[df.id == inde].ssrb.values,
        hidden=df[df.id == inde].ssrb.values,
    )

    mask = ~np.isnan(df2[df2.id == inde].ssr.values) & ~np.isnan(
        df2[df2.id == inde].ssrb.values
    )
    yy = df2[df2.id == inde].ssr.values[mask]
    xx = df2[df2.id == inde].ssrb.values[mask]
    sl, inter, r, pv, ster = sp.stats.linregress(xx, yy)
    sss4.data = dict(
        x=np.arange(xx.min(), xx.max()), y=sl * np.arange(xx.min(), xx.max()) + inter
    )

    maskd = ~np.isnan(df[df.id == inde].ssr.values) & ~np.isnan(
        df[df.id == inde].ssrb.values
    )
    yyd = df[df.id == inde].ssr.values[maskd]
    xxd = df[df.id == inde].ssrb.values[maskd]
    sld, interd, r, pv, ster = sp.stats.linregress(xxd, yyd)

    sss4d.data = dict(
        x=np.arange(xxd.min(), xxd.max()),
        y=sld * np.arange(xxd.min(), xxd.max()) + interd,
    )

    source5.data = dict(
        Metrics=[
            "Name",
            "Lat",
            "Lon",
            "Alt",
            "StartYear",
            "EndYear",
            "N",
            "slope",
            "slope_anom",
            "intercept",
            "intercept_anom",
            "R",
            "Ranom",
            "Bias",
            "Bias %",
            "Rmse",
            "Rmse %",
            "ChangeModel",
            "pv95Model",
            "ChangeStation",
            "pv95Station",
            "Sign Agreement",
        ],
        Values=[
            df1[df1.id == inde].id.values[0],
            df1[df1.id == inde].lat.values[0],
            df1[df1.id == inde].lon.values[0],
            df2[df2.id == inde].alt.values[0],
            str(df2[df2.id == inde].dropna().Date.values[0])[:4],
            str(df2[df2.id == inde].dropna().Date.values[-1])[:4],
            df1[df1.id == inde].pairs.values[0],
            df1[df1.id == inde].slope.values[0],
            df1b[df1b.id == inde].slope.values[0],
            df1[df1.id == inde].intercept.values[0],
            df1b[df1b.id == inde].intercept.values[0],
            df1[df1.id == inde].r.values[0],
            df1b[df1b.id == inde].r.values[0],
            df1[df1.id == inde].bias.values[0],
            df1[df1.id == inde].bias_pc.values[0],
            df1[df1.id == inde].rmse.values[0],
            df1[df1.id == inde].rrmse.values[0],
            df1[df1.id == inde].slopeF.values[0],
            df1[df1.id == inde].pvF.values[0],
            df1[df1.id == inde].slopeA.values[0],
            df1[df1.id == inde].pvA.values[0],
            df1[df1.id == inde].signW.values[0],
        ],
    )


# Add the callback to the image selection
s1.selected.on_change("indices", update_timeseries)

# Layout
layout = column(
    row(p1, p3),
    row(p2, tabs_layout, data_table),
    row(text_area_input),
    styles={"width": "100%", "height": "150%", "background-color": "#1a1a1a"},
)
curdoc().add_root(layout)
curdoc().title = "FORTH-RTM SSR & GDB Evaluation"
