""" 
Exploration of FORTH-RTM SSR (1984-2018). PhD Thesis: https://www.didaktorika.gr/eadd/handle/10442/59941
Creator: Michael Stamatis, email: mixstam1453@gmail.com
"""

from bokeh.layouts import row, column
from bokeh.plotting import figure, curdoc
from bokeh.models import (
    ColumnDataSource,
    TapTool,
    MultiChoice,
    CustomJSHover,
    FactorRange,
    LegendItem,
    LinearColorMapper,
    CustomJS,
    Scatter,
    HoverTool,
    Div,
    DatetimeTickFormatter,
    TextAreaInput,
    DatetimeTickFormatter,
    CrosshairTool,
    HoverTool,
    Span,
    Legend,
    BoxEditTool,
    FreehandDrawTool,
    InlineStyleSheet,
    ColorBar,
    Slider,
    Button,
)
from bokeh.palettes import interp_palette, Turbo256
from bokeh.transform import factor_cmap

import numpy as np, pandas as pd, xarray as xr, scipy as sp
from bokeh.models import TextInput

tais = InlineStyleSheet(
    css=""" /* Outer container styling */ :host { background: #1a1a1a !important; border-radius: 14px !important; padding: 16px !important; box-shadow: 0 4px 18px #0006 !important; } /* Title label styling */ :host .bk-input-group label, :host .bk-textinput-title { color: #34ffe0 !important; font-size: 1.14em !important; font-family: 'Fira Code', monospace !important; font-weight: bold !important; margin-bottom: 12px !important; letter-spacing: 0.5px !important; text-shadow: 0 2px 12px #34ffe077, 0 1px 3px #222 !important; } /* The textarea input box - changed from input[type="text"] to textarea */ :host textarea { background: #23233c !important; color: #f9fafb !important; border: 2px solid #06b6d4 !important; border-radius: 8px !important; padding: 11px 15px !important; font-size: 1.08em !important; font-family: 'Fira Code', monospace !important; transition: border 0.12s ease, box-shadow 0.12s ease !important; box-shadow: none !important; resize: vertical !important; min-height: 120px !important; } /* On hover/focus: red border with glowing effect */ :host textarea:hover, :host textarea:focus { border-color: #ff3049 !important; box-shadow: 0 0 0 2px #ff304999, 0 0 15px #ff3049bb !important; outline: none !important; } /* Placeholder text */ :host textarea::placeholder { color: #9ca3af !important; opacity: 0.7 !important; font-style: italic !important; } /* Scrollbar styling for webkit browsers */ :host textarea::-webkit-scrollbar { width: 8px !important; } :host textarea::-webkit-scrollbar-track { background: #1a1a2e !important; border-radius: 4px !important; } :host textarea::-webkit-scrollbar-thumb { background: #06b6d4 !important; border-radius: 4px !important; } :host textarea::-webkit-scrollbar-thumb:hover { background: #ff3049 !important; } """
)
base_variables = """ :host { /* CSS Custom Properties for easy theming */ --primary-color: #8b5cf6; --secondary-color: #06b6d4; --background-color: #1f2937; --surface-color: #343838; --text-color: #f9fafb; --accent-color: #f59e0b; --danger-color: #ef4444; --success-color: #10b981; --border-color: #4b5563; --hover-color: #6366f1; background: none !important; } """
button_style = InlineStyleSheet(
    css=base_variables
    + """ :host button { background: linear-gradient(135deg, var(--primary-color), var(--secondary-color)) !important; color: white !important; border: none !important; border-radius: 6px !important; padding: 10px 20px !important; font-size: 14px !important; font-weight: 600 !important; cursor: pointer !important; transition: all 0.2s ease !important; box-shadow: 0 2px 4px rgba(0,0,0,0.1) !important; } :host button:hover { transform: translateY(-1px) !important; box-shadow: 0 4px 8px rgba(0,0,0,0.2) !important; background: linear-gradient(135deg, var(--hover-color), var(--primary-color)) !important; } :host button:active { transform: translateY(0) !important; box-shadow: 0 2px 4px rgba(0,0,0,0.1) !important; } :host button:disabled { background: #6b7280 !important; cursor: not-allowed !important; transform: none !important; box-shadow: none !important; } """
)
slider_style = InlineStyleSheet(
    css=""" /* Host: set the widget's container background */ :host { background: #16161e !important;   /* even darker than black for modern dark UI */ border-radius: 12px !important; padding: 12px !important; box-shadow: 0 4px 12px #0006 !important; } /* Slider title */ :host .bk-slider-title { color: #00ffe0 !important;     /* bright cyan for the title */ font-size: 1.2em !important; font-weight: bold !important; letter-spacing: 1px !important; font-family: 'Fira Code', 'Consolas', 'Menlo', monospace !important; margin-bottom: 14px !important; text-shadow: 0 2px 12px #00ffe099; } /* Track (background) */ :host .noUi-base, :host .noUi-target { background: #23233c !important; border: 1px solid #2a3132 !important; } /* Filled portion */ :host .noUi-connect { background: linear-gradient(90deg, #00ffe0 10%, #d810f7 90%) !important; box-shadow: 0 0 12px #00ffe099; border-radius: 12px !important; } /* Handle */ :host .noUi-handle { background: #343838 !important; border: 2px solid #00ffe0 !important; border-radius: 50%; width: 20px; height: 20px; } /* Handle hover/focus */ :host .noUi-handle:hover, :host .noUi-handle:focus { border-color: #ff2a68 !important; box-shadow: 0 0 10px #ff2a6890; } /* Tooltip */ :host .noUi-tooltip { background: #343838 !important; color: #00ffe0 !important; font-family: 'Consolas', monospace; border-radius: 6px; border: 1px solid #00ffe0; } """
)
multi_style = InlineStyleSheet(
    css=""" /* Outer widget container */ :host { background: #181824 !important; border-radius: 14px !important; padding: 16px !important; box-shadow: 0 4px 20px #0008 !important; } /* Title styling */ :host .bk-input-group label, :host .bk-multichoice-title { color: #00ffe0 !important; font-size: 1.18em !important; font-family: 'Fira Code', monospace; font-weight: bold !important; margin-bottom: 10px !important; letter-spacing: 1px !important; text-shadow: 0 2px 12px #00ffe088, 0 1px 4px #181824; } /* The input field when closed */ :host .choices__inner { background: #23233c !important; color: #f9fafb !important; border: 2px solid #06b6d4 !important; border-radius: 8px !important; font-size: 1.05em !important; transition: border 0.1s, box-shadow 0.1s; box-shadow: none !important; } /* Glow on hover/focus of input */ :host .choices__inner:hover, :host .choices__inner:focus-within { border-color: #ff3049 !important; box-shadow: 0 0 0 2px #ff304999, 0 0 16px #ff3049cc !important; outline: none !important; } /* Dropdown list */ :host .choices__list--dropdown { background: #181824 !important; border: 1.5px solid #06b6d4 !important; border-radius: 8px !important; box-shadow: 0 10px 32px #000c !important; } /* Items in the dropdown */ :host .choices__item--choice { color: #f9fafb !important; padding: 12px 16px !important; transition: all 0.15s; border-bottom: 1px solid #28284666 !important; } :host .choices__item--choice:hover { background: #8b5cf6 !important; color: #1f2937 !important; } /* Active selected items in the box */ :host .choices__item--selectable { background: linear-gradient(90deg, #ffb028 20%, #ff4f4f 100%) !important; color: #181824 !important; border-radius: 6px !important; font-weight: 600 !important; margin: 2px 4px !important; padding: 6px 14px !important; box-shadow: 0 1px 6px #0005; } """
)
colorss = [
    "rgb(16, 94, 0)",
    "rgb(0, 185, 9)",
    "rgb(0, 255, 64)",
    "rgb(0, 28, 121)",
    "rgb(0, 60, 255)",
    "rgb(0, 200, 255)",
    "rgb(255, 0, 0)",
    "rgb(218, 116, 0)",
    "rgb(255, 230, 0)",
    "rgb(111, 2, 161)",
    "#ff35a4",
    "#000000",
]
textinput_css = InlineStyleSheet(
    css=""" /* Outer container styling */ :host { background: #181824 !important; border-radius: 14px !important; padding: 12px !important; box-shadow: 0 4px 18px #0006 !important; } /* Title label styling */ :host .bk-input-group label, :host .bk-textinput-title { color: #34ffe0 !important; font-size: 1.14em !important; font-family: 'Fira Code', monospace; font-weight: bold !important; margin-bottom: 12px !important; letter-spacing: 0.5px !important; text-shadow: 0 2px 12px #34ffe077, 0 1px 3px #222; } /* The input box */ :host input[type="text"] { background: #23233c !important; color: #f9fafb !important; border: 2px solid #06b6d4 !important; border-radius: 8px !important; padding: 11px 15px !important; font-size: 1.08em !important; transition: border 0.12s, box-shadow 0.12s; box-shadow: none !important; } /* On hover/focus: red border with glowing effect */ :host input[type="text"]:hover, :host input[type="text"]:focus { border-color: #ff3049 !important; box-shadow: 0 0 0 2px #ff304999, 0 0 15px #ff3049bb !important; outline: none !important; } /* Placeholder text */ :host input[type="text"]::placeholder { color: #9ca3af !important; opacity: 0.7 !important; font-style: italic !important; } """
)

lat_min_input = TextInput(
    title="Lat Min",
    value="-90",
    width=100,
    height=80,
    stylesheets=[textinput_css],
    styles={"margin-left": "40px"},
)
lat_max_input = TextInput(
    title="Lat Max",
    value="90",
    width=100,
    height=80,
    stylesheets=[textinput_css],
    styles={"margin-left": "40px"},
)
lon_min_input = TextInput(
    title="Lon Min",
    value="-180",
    width=100,
    height=80,
    stylesheets=[textinput_css],
    styles={"margin-left": "40px"},
)
lon_max_input = TextInput(
    title="Lon Max",
    value="180",
    width=100,
    height=80,
    stylesheets=[textinput_css],
    styles={"margin-left": "40px"},
)
apply_button = Button(
    label="Apply Region",
    width=120,
    stylesheets=[button_style],
    styles={"margin-left": "40px"},
)


p9 = {"active_scroll": "wheel_zoom"}
curdoc().theme = "dark_minimal"


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
        # default_values=dict(
        #     color="grey",
        #     alpha=0.35,
        # ),
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

    # re-arange y axis when hide a glyph! not works if i set the y_range
    # p.y_range.only_visible = True


# ------ MY DATA -------- #
# p1: GDB
fmc_ssr_full = (
    xr.open_dataset("data/FMCX_8418_SurfaceDown_f.nc")[
        "SurfaceDown"
    ]
    .sel(time=slice("1984-01-01", "2018-12-31"))
    # .fillna(0)
)

fmc_ssr_full = xr.where(
    (fmc_ssr_full.time.dt.year == 1985) & (fmc_ssr_full.time.dt.month == 2),
    np.nan,
    fmc_ssr_full,
)

# initialize fmc_ssr with the full dataset (will be updated later)
fmc_ssr = fmc_ssr_full


gdbdc = (
    xr.open_dataset(
        "data/__anom_8418_slopes_FMCX8418_SurfaceDown_.nc"
    )["slope"].rename("GDB")
    * 120
)
anom_fmc_ssr0 = fmc_ssr.groupby("time.month") - fmc_ssr.groupby("time.month").mean(
    "time"
)
ts_fmc_ssr = anom_fmc_ssr0.weighted(np.cos(np.deg2rad(anom_fmc_ssr0.lat))).mean(
    ("lat", "lon")
)  # .groupby('time.year').mean('time')
anom_fmc_ssr = ts_fmc_ssr
anomTS = anom_fmc_ssr.values
xdates = ts_fmc_ssr.time.values
geomask = "data/forth_361x576_land_see_mask.nc"

i = fmc_ssr
g = xr.open_dataset(geomask)
land = i / g.topo
n9 = xr.where(land == np.inf, np.nan, land)
SSR_land = xr.where(n9 == -np.inf, np.nan, n9)
i = fmc_ssr
g = xr.open_dataset(geomask)
ocean = i / np.abs(g.topo - 1)
n99 = xr.where(ocean == np.inf, np.nan, ocean)
SSR_ocean = xr.where(n99 == -np.inf, np.nan, n99)


forssrmeanGLOBE = [
    np.nanmean(fmc_ssr.values[i, :, :]) for i in range(len(fmc_ssr.time))
]
forssrmeanLAND = [
    np.nanmean(SSR_land.values[i, :, :]) for i in range(len(fmc_ssr.time))
]
forssrmeanOCEAN = [
    np.nanmean(SSR_ocean.values[i, :, :]) for i in range(len(fmc_ssr.time))
]


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

# ------ The App ------ #

# p1) GDB
latitudes = fmc_ssr.lat.values.tolist()
longitudes = fmc_ssr.lon.values.tolist()
lati = np.repeat(latitudes, len(longitudes))
loni = np.tile(longitudes, len(latitudes))
s1 = ColumnDataSource(
    data={
        "image": [fmc_ssr.mean("time").values],
        "latitudes": [lati],
        "longitudes": [loni],
    }
)

# Set up Bokeh figure
p1 = figure(
    output_backend="webgl",
    border_fill_color="#2d2d2d",
    background_fill_color="#2d2d2d",
    width=845,
    min_border_bottom=10,
    min_border_right=80,
    toolbar_location="below",
    height=445,
    x_range=(min(longitudes), max(longitudes)),
    y_range=(min(latitudes), max(latitudes)),
    title=r"$$FMC-RTM~SSR, 1984-2018$$",
    **p9,
    styles={
        "margin-top": "12px",
        "margin-left": "-848px",
        "padding": "0px",
        "border-radius": "10px",
        "background-color": "#2d2d2d",
    },
)
p1_ = figure(
    width=850,
    height=450,
    styles={
        "margin-top": "10px",
        "margin-left": "100px",
        "border-radius": "10px",
        "padding": "15px",
        "box-shadow": "0 3px 3px #06ffcd",
        "background-color": "#2d2d2d",
    },
)
p1_.border_fill_color = "#2d2d2d"
p1_.toolbar_location = None


color_mapper = LinearColorMapper(palette=Turbo256, low=40, high=390)
color_bar = ColorBar(
    color_mapper=color_mapper,
    location=(0, 0),
    title=r"$$Wm^{-2}$$",
    title_standoff=1,
    title_text_baseline="middle",
    title_text_align="right",
    background_fill_alpha=0,
)
p1.add_layout(color_bar, "right")

# # Add custom text (label) at specific (x, y) coordinates
# label = Label( text=r"$$Wm^{-2}decade^{-1}$$", x=150, y=130, x_units="screen", y_units="screen", )
# p1.add_layout(label)

# Display the temperature data using the image renderer
p11 = p1.image(
    image="image",
    color_mapper=color_mapper,
    x=min(longitudes),
    y=min(latitudes),
    dw=max(longitudes) - min(longitudes),
    dh=max(latitudes) - min(latitudes),
    source=s1,
)
p12 = p1.line(x=x_coords, y=y_coords, line_width=1, line_color="black")

p1.add_tools(
    HoverTool(
        tooltips="""<div style="background-color: #f0f0f0; padding: 5px; border-radius: 5px; box-shadow: 0px 0px 5px rgba(0,0,0,0.3);">        <font size="3" style="background-color: #f0f0f0; padding: 5px; border-radius: 5px;">
            <i>Lon:</i> <b>@longitudes{0.000}<sup>o</sup></b> <br> 
            <i>Lat:</i> <b>@latitudes{0.000}<sup>o</sup></b> <br>
            <i>SSR:</i> <b>@image{0.000} Wm<sup>-2</sup></b> <br>
        </font> </div> <style> :host { --tooltip-border: transparent;  /* Same border color used everywhere */ --tooltip-color: transparent; --tooltip-text: #2f2f2f;} </style> """,
        mode="mouse",
        renderers=[p11],
    )
)
add_extras(p1, cross=0)
tap_tool = p1.select(type=TapTool)
tap_tool.mode = "replace"

s3 = ColumnDataSource(data=dict(x=xdates, y=anomTS, hidden=anomTS))
p3 = figure(
    width=1000,
    height=450,
    x_axis_type="datetime",
    x_range=(pd.Timestamp("1984"), pd.Timestamp("2018")),
    border_fill_color="#2d2d2d",
    background_fill_color="#2d2d2d",
    min_border_bottom=10,
    min_border_right=80,
    y_range=(-13, 13),
    title=r"$$SSR~Deseasonalized~Anomalies~1984-2018$$",
    y_axis_label=r"$$Wm^{-2}$$",
    **p9,
    styles={
        "margin-top": "10px",
        "margin-left": "10px",
        "padding": "15px",
        "border-radius": "10px",
        "box-shadow": "0 9px 14px #06ffcd",
        "background-color": "#2d2d2d",
    },
)
p333 = p3.line("x", "y", source=s3, line_alpha=1, line_width=1, color="#06ffcd9a")
p33 = p3.scatter("x", "y", source=s3, color="#06ffcd", line_color="black", size=13)
p3.xaxis[0].formatter = DatetimeTickFormatter(years="%Y-%m")
p33.selection_glyph = Scatter(
    size=19, fill_color="blue", line_color="red", line_width=4
)
p33.nonselection_glyph = None
p333.nonselection_glyph = None

tltl = """
            <i>Date:</i> <b>@x{%Y-%m}</b> <br> 
            <i>SSR anom:</i> <b>@y{0.00} Wm<sup>-2</sup></b> """

p3.add_tools(
    HoverTool(
        tooltips=hovfun(tltl),
        formatters={"@x": "datetime", "@hidden": cusj()},
        mode="vline",
        point_policy="snap_to_data",
        line_policy="none",
        attachment="left",
        show_arrow=False,
        renderers=[p33],
    )
)

add_extras(p3)


annu = (
    fmc_ssr.weighted(np.cos(np.deg2rad(fmc_ssr.lat)))
    .mean(("lat", "lon"))
    .groupby("time.month")
    .mean("time")
    .values
)
NHannu = (
    fmc_ssr.sel(lat=slice(0, 90))
    .weighted(np.cos(np.deg2rad(fmc_ssr.sel(lat=slice(0, 90)).lat)))
    .mean(("lat", "lon"))
    .groupby("time.month")
    .mean("time")
    .values
)
SHannu = (
    fmc_ssr.sel(lat=slice(-90, 0))
    .weighted(np.cos(np.deg2rad(fmc_ssr.sel(lat=slice(-90, 0)).lat)))
    .mean(("lat", "lon"))
    .groupby("time.month")
    .mean("time")
    .values
)

fruits = [
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
years = ["GL", "NH", "SH"]
year_to_category = {"GL": "GL", "NH": "NH", "SH": "SH"}
categories = ["GL", "NH", "SH"]  # Only three categories

data = {"fruits": fruits, "GL": annu, "NH": NHannu, "SH": SHannu}

palette = ["grey", "#5fc7fb", "#e84d60"]


x = [(fruit, year) for fruit in fruits for year in years]
counts = sum(zip(data["GL"], data["NH"], data["SH"]), ())  # Like an hstack
categories_mapped = [year_to_category[year] for fruit in fruits for year in years]

san = ColumnDataSource(data=dict(x=x, counts=counts, category=categories_mapped))

annual = figure(
    x_range=FactorRange(*x),
    width=800,
    height=450,
    border_fill_color="#2d2d2d",
    background_fill_color="#2d2d2d",
    min_border_bottom=100,
    min_border_right=80,
    title=r"$$SSR~Annual~Cycle~1984-2018$$",
    y_axis_label=r"$$Wm^{-2}$$",
    **p9,
    styles={
        "margin-top": "10px",
        "margin-left": "10px",
        "padding": "15px",
        "border-radius": "10px",
        "box-shadow": "0 9px 14px #06ffcd",
        "background-color": "#2d2d2d",
    },
)
annual333 = annual.vbar(
    x="x",
    top="counts",
    source=san,
    hover_line_color="lime",
    hover_line_width=2,
    line_width=1,
    width=0.9,
    border_radius=3,
    line_color="black",
    fill_color=factor_cmap("category", palette=palette, factors=categories),
)

annual.y_range.start = 0
annual.x_range.range_padding = 0
annual.xaxis.major_label_orientation = 1
annual.xgrid.grid_line_color = None
annual.xaxis.major_label_text_alpha = 0.0
annual.xaxis.major_label_text_font_size = "1px"

# Manually create the legend
legend_items = [
    LegendItem(label=label, renderers=[annual333], index=i)
    for i, label in enumerate(categories)
]
legend = Legend(items=legend_items, location="center", orientation="horizontal")
annual.add_layout(legend, "below")

legend.location = (300, 370)
# annual.add_layout(legend, 'below')
# annual.legend.click_policy = "hide"
# p.add_layout(legend, 'right')
annual.add_tools(
    HoverTool(
        tooltips="""<div style="background-color: #f0f0f0; padding: 5px; border-radius: 5px; box-shadow: 0px 0px 5px rgba(0,0,0,0.3);">        <font size="3" style="background-color: #f0f0f0; padding: 5px; border-radius: 5px;">
            <i>Month:</i> <b>@x</b> <br> 

            <i>SSR:</i> <b>@counts{0.00} Wm<sup>-2</sup></b> <br>

        </font> </div> <style> :host { --tooltip-border: transparent;  /* Same border color used everywhere */ --tooltip-color: transparent; --tooltip-text: #2f2f2f;} </style> """,
        mode="mouse",point_policy="follow_mouse",
        renderers=[annual333],
    )
)
add_extras(annual,cross=0)

####
anlat = fmc_ssr.weighted(np.cos(np.deg2rad(fmc_ssr.lat))).mean(
    ("lon", "time")
)  # ts_fmc_ssr.groupby('time.month').mean('time').values
sanlat = ColumnDataSource(data=dict(x=[], y=[]))
annualx = figure(
    y_range=(min(anlat.lat.values), max(anlat.lat.values)),
    width=400,
    height=450,
    border_fill_color="#2d2d2d",
    background_fill_color="#2d2d2d",
    min_border_bottom=60,
    min_border_right=80,
    title=r"$$SSR~Latitudinal~means$$",
    x_axis_label=r"$$Wm^{-2}$$",
    y_axis_label=r"$$Latitude (^{o})$$",
    **p9,
    styles={
        "margin-top": "10px",
        "margin-left": "10px",
        "padding": "15px",
        "border-radius": "10px",
        "box-shadow": "0 4px 4px #06ffcd67",
        "background-color": "#2d2d2d",
    },
)
annual3331 = annualx.line(
    x="x", y="y", source=sanlat, line_color="deepskyblue", line_width=2
)

annualx.add_tools(
    HoverTool(
        tooltips="""<div style="background-color: #f0f0f0; padding: 5px; border-radius: 5px; box-shadow: 0px 0px 5px rgba(0,0,0,0.3);">        <font size="3" style="background-color: #f0f0f0; padding: 5px; border-radius: 5px;">
            <i>lat:</i> <b>@y{0.00} <sup>o</sup></b> <br> 

            <i>SSR:</i> <b>@x{0.00} Wm<sup>-2</sup></b> <br>
        </font> </div> <style> :host { --tooltip-border: transparent;  /* Same border color used everywhere */ --tooltip-color: transparent; --tooltip-text: #2f2f2f;} </style> """,
        mode="mouse",
        renderers=[annual3331],
    )
)
add_extras(annualx)

IID = fmc_ssr.time.values.astype("datetime64[D]").astype("str").tolist()

# display text
div2 = Div(
    text=f"""
    <div style="background-color: #fff1c0; padding: 1px; border-radius: 3px; box-shadow: 3px 3px 4px #06ffcd;margin-left: 6px">
        <p style='font-family:Arial;font-size: 17px;  color: #343434;'>
<b>date</b>: 1984-2018
<br> <b>mean SSR</b>: {np.nanmean(fmc_ssr.values[:, :, :]):.2f} Wm<sup>-2</sup>
<br> <b>mean land SSR</b>: {np.nanmean(SSR_land.values[:, :, :]):.2f} Wm<sup>-2</sup>
<br> <b>mean ocean SSR</b>: {np.nanmean(SSR_ocean.values[:, :, :]):.2f} Wm<sup>-2</sup>
</p>
    </div>
                """,
    height=30,
    width=400,
    styles={"margin-left": "11px"},
)
# take some notes
text_area_input = TextAreaInput(
    value=" ",
    rows=20,
    cols=150,
    title="My notes:",
    stylesheets=[tais],
    styles={"margin-top": "30px"},
)
time_select = MultiChoice(
    title="Select Dates:",
    value=[],
    options=IID,
    width=300,
    max_items=1,
    styles={"color": "silver", "margin-left": "15px"},
    stylesheets=[multi_style],
)

meanfmc = fmc_ssr.mean("time")
# Create a year slider
slider = Slider(
    start=0,
    end=420,
    step=1,
    value=0,
    title="Date",
    styles={"color": "#ffdf6b", "margin-left": "12px"},
    stylesheets=[slider_style],
)
slider.js_on_change(
    "value",
    CustomJS(
        code=f"""
    console.log('slider: date=' + this.value, this.toString())
"""
    ),
)


# --- ADD callback to update dataset & recompute analysis ---


def apply_region():
    global fmc_ssr, anom_fmc_ssr, anomTS, xdates
    global forssrmeanGLOBE, forssrmeanLAND, forssrmeanOCEAN

    try:
        lat_min = float(lat_min_input.value)
        lat_max = float(lat_max_input.value)
        lon_min = float(lon_min_input.value)
        lon_max = float(lon_max_input.value)

        # subset the dataset from the full globe
        fmc_ssr = fmc_ssr_full.sel(
            lat=slice(lat_min, lat_max), lon=slice(lon_min, lon_max)
        )

        # recompute anomalies
        anom_fmc_ssr0 = fmc_ssr.groupby("time.month") - fmc_ssr.groupby(
            "time.month"
        ).mean("time")
        ts_fmc_ssr = anom_fmc_ssr0.weighted(np.cos(np.deg2rad(anom_fmc_ssr0.lat))).mean(
            ("lat", "lon")
        )
        anom_fmc_ssr = ts_fmc_ssr
        anomTS = anom_fmc_ssr.values
        xdates = ts_fmc_ssr.time.values

        # recompute land/ocean separation
        g = xr.open_dataset(geomask)
        land = fmc_ssr / g.topo
        SSR_land = xr.where((land == np.inf) | (land == -np.inf), np.nan, land)
        ocean = fmc_ssr / np.abs(g.topo - 1)
        SSR_ocean = xr.where((ocean == np.inf) | (ocean == -np.inf), np.nan, ocean)

        forssrmeanGLOBE = [
            np.nanmean(fmc_ssr.values[i, :, :]) for i in range(len(fmc_ssr.time))
        ]
        forssrmeanLAND = [
            np.nanmean(SSR_land.values[i, :, :]) for i in range(len(fmc_ssr.time))
        ]
        forssrmeanOCEAN = [
            np.nanmean(SSR_ocean.values[i, :, :]) for i in range(len(fmc_ssr.time))
        ]

        # update figure ranges
        p1.x_range.start = lon_min
        p1.x_range.end = lon_max
        p1.y_range.start = lat_min
        p1.y_range.end = lat_max

        # update map source & reposition image glyph
        latitudes = fmc_ssr.lat.values.tolist()
        longitudes = fmc_ssr.lon.values.tolist()
        lati = np.repeat(latitudes, len(longitudes))
        loni = np.tile(longitudes, len(latitudes))

        regional_mean = fmc_ssr.mean("time")

        s1.data = {
            "image": [regional_mean.values],
            "latitudes": [lati],
            "longitudes": [loni],
        }

        # 🔥 Fix: update the image plot extents
        p11.glyph.x = float(longitudes[0])
        p11.glyph.y = float(latitudes[0])
        p11.glyph.dw = float(longitudes[-1] - longitudes[0])
        p11.glyph.dh = float(latitudes[-1] - latitudes[0])

        # update timeseries plot & reset y_range auto
        s3.data = dict(x=xdates, y=anomTS, hidden=anomTS)
        if len(anomTS) > 0:
            p3.y_range.start = float(np.nanmin(anomTS)) - 1
            p3.y_range.end = float(np.nanmax(anomTS)) + 1

        # recompute annual cycle
        annu = (
            fmc_ssr.weighted(np.cos(np.deg2rad(fmc_ssr.lat)))
            .mean(("lat", "lon"))
            .groupby("time.month")
            .mean("time")
            .values
        )
        NHannu = (
            fmc_ssr.sel(lat=slice(0, 90))
            .weighted(np.cos(np.deg2rad(fmc_ssr.sel(lat=slice(0, 90)).lat)))
            .mean(("lat", "lon"))
            .groupby("time.month")
            .mean("time")
            .values
        )
        SHannu = (
            fmc_ssr.sel(lat=slice(-90, 0))
            .weighted(np.cos(np.deg2rad(fmc_ssr.sel(lat=slice(-90, 0)).lat)))
            .mean(("lat", "lon"))
            .groupby("time.month")
            .mean("time")
            .values
        )

        counts = sum(zip(annu, NHannu, SHannu), ())
        categories_mapped = ["GL", "NH", "SH"] * 12
        san.data = dict(
            x=[(m, y) for m in fruits for y in years],
            counts=counts,
            category=categories_mapped,
        )

        # recompute latitudinal mean
        anlat = fmc_ssr.weighted(np.cos(np.deg2rad(fmc_ssr.lat))).mean(("lon", "time"))
        sanlat.data = dict(x=anlat.values, y=anlat.lat.values)

        # update info box with region
        div2.text = f"""
        <div style="background-color: #fff1c0; padding: 1px; border-radius: 3px;
             margin-left: 11px; box-shadow: 3px 3px 4px #06ffcd92">
          <p style='font-family:Arial;font-size: 17px; color: #343434;'>
          <b>date</b>: 1984-2018<br>
          <b>mean SSR</b>: {np.nanmean(fmc_ssr.values[:, :, :]):.2f} Wm<sup>-2</sup><br>
          <b>mean land SSR</b>: {np.nanmean(SSR_land.values[:, :, :]):.2f} Wm<sup>-2</sup><br>
          <b>mean ocean SSR</b>: {np.nanmean(SSR_ocean.values[:, :, :]):.2f} Wm<sup>-2</sup><br>
          <b>region</b>: Lat [{lat_min}, {lat_max}], Lon [{lon_min}, {lon_max}]
          </p>
        </div>
        """

        print(f"✅ Region updated: Lat {lat_min}..{lat_max}, Lon {lon_min}..{lon_max}")

    except Exception as e:
        print("❌ Invalid input for region filter:", e)


apply_button.on_click(apply_region)


# define the callback function to animate the slider when clicking the button
def animate_update():
    year = slider.value + 1
    if year > 420:
        year = 0
    slider.value = year


# create global variable for callback
callback_animate = None


# define the callback function for clicking the button
def animate():
    global callback_animate
    if button.label == "► Play":
        button.label = "❚❚ Pause"
        callback_animate = curdoc().add_periodic_callback(animate_update, 200)
    else:
        button.label = "► Play"
        curdoc().remove_periodic_callback(callback_animate)


# create the button and set on-click callback
button = Button(label="► Play", width=60, stylesheets=[button_style])
button.on_click(animate)


def update_timeseries3(attr, old, new):
    indd = IID.index(new[0])
    s1.data = {
        "image": [fmc_ssr.values[indd, :, :]],
        "latitudes": [lati],
        "longitudes": [loni],
    }
    anlatx = (
        fmc_ssr.isel(time=indd).weighted(np.cos(np.deg2rad(fmc_ssr.lat))).mean(("lon"))
    )  # ts_fmc_ssr.groupby('time.month').mean('time').values
    sanlat.data = {
        "y": anlatx.lat.values,
        "x": anlatx.values,
    }

    div2.text = f"""
    <div style="background-color: #fff1c0; padding: 1px; border-radius: 3px;margin-left: 11px; box-shadow: 3px 3px 4px #06ffcd92">
        <p style='font-family:Arial;font-size: 17px;  color: #343434;'>
<b>date</b>: {new[0]}<br> <b>mean SSR</b>: {forssrmeanGLOBE[indd]:.2f} Wm<sup>-2</sup>
<br> <b>mean land SSR</b>: {forssrmeanLAND[indd]:.2f} Wm<sup>-2</sup>
<br> <b>mean ocean SSR</b>: {forssrmeanOCEAN[indd]:.2f} Wm<sup>-2</sup>

</p>
    </div>
"""


def update_timeseries(attr, old, new):
    s1.data = {
        "image": [fmc_ssr.values[new, :, :]],
        "latitudes": [lati],
        "longitudes": [loni],
    }

    anlatx = (
        fmc_ssr.isel(time=new).weighted(np.cos(np.deg2rad(fmc_ssr.lat))).mean(("lon"))
    )  # ts_fmc_ssr.groupby('time.month').mean('time').values

    sanlat.data = {
        "y": anlatx.lat.values,
        "x": anlatx.values,
    }

    div2.text = f"""
    <div style="background-color: #fff1c0; padding: 1px; border-radius: 3px; box-shadow: 3px 3px 4px rgba(0, 242, 255, 0.2));margin-left: 11px;">
        <p style='font-family:Arial;font-size: 17px;  color: #343434;'>
<b>date</b>: {xdates[new].astype("datetime64[M]")}<br> <b>mean SSR</b>: {forssrmeanGLOBE[new]:.2f} Wm<sup>-2</sup>
<br> <b>mean land SSR</b>: {forssrmeanLAND[new]:.2f} Wm<sup>-2</sup>
<br> <b>mean ocean SSR</b>: {forssrmeanOCEAN[new]:.2f} Wm<sup>-2</sup>

</p>
    </div>
"""


# Callback function
def update_timeseries2(attr, old, new):
    s1.data = {
        "image": [fmc_ssr.values[new[0], :, :]],
        "latitudes": [lati],
        "longitudes": [loni],
    }

    anlatx = (
        fmc_ssr.isel(time=new[0])
        .weighted(np.cos(np.deg2rad(fmc_ssr.lat)))
        .mean(("lon"))
    )  # ts_fmc_ssr.groupby('time.month').mean('time').values

    sanlat.data = {
        "y": anlatx.lat.values,
        "x": anlatx.values,
    }

    div2.text = f"""
    <div style="background-color: #fff1c0; padding: 1px; border-radius: 3px;margin-left: 11px; box-shadow: 3px 3px 4px #06ffcd92">
        <p style='font-family:Arial;font-size: 17px;  color: #343434;'>
<b>date</b>: {xdates[new[0]].astype("datetime64[M]")}<br> <b>mean SSR</b>: {forssrmeanGLOBE[new[0]]:.2f} Wm<sup>-2</sup>
<br> <b>mean land SSR</b>: {forssrmeanLAND[new[0]]:.2f} Wm<sup>-2</sup>
<br> <b>mean ocean SSR</b>: {forssrmeanOCEAN[new[0]]:.2f} Wm<sup>-2</sup>


</p>
    </div>
"""


# Add the callback to the image selection
s3.selected.on_change("indices", update_timeseries2)


def update_timeseries4(attr, old, new):
    new = [int(i / 3) for i in new]


    s1.data = {
        "image": [
            fmc_ssr.sel(time=fmc_ssr.time.dt.month == new[0] + 1)
            .mean("time")
            .values[:, :]
        ],  # [new[0], :, :]],
        "latitudes": [lati],
        "longitudes": [loni],
    }

    anlatx = (
        fmc_ssr.sel(time=fmc_ssr.time.dt.month == new[0] + 1)
        .mean("time")
        .weighted(np.cos(np.deg2rad(fmc_ssr.lat)))
        .mean(("lon"))
    )  # ts_fmc_ssr.groupby('time.month').mean('time').values

    sanlat.data = {
        "y": anlatx.lat.values,
        "x": anlatx.values,
    }

    forco = fmc_ssr.sel(time=fmc_ssr.time.dt.month == new[0] + 1).mean("time")

    i = forco
    g = xr.open_dataset(geomask)
    land = i / g.topo
    n9 = xr.where(land == np.inf, np.nan, land)
    SSR_landforco = xr.where(n9 == -np.inf, np.nan, n9)
    i = forco
    g = xr.open_dataset(geomask)
    ocean = i / np.abs(g.topo - 1)
    n99 = xr.where(ocean == np.inf, np.nan, ocean)
    SSR_oceanforco = xr.where(n99 == -np.inf, np.nan, n99)

    forssrmeanGLOBEforco = [np.nanmean(forco.values[:, :])]
    forssrmeanLANDforco = [np.nanmean(SSR_landforco.values[:, :])]
    forssrmeanOCEANforco = [np.nanmean(SSR_oceanforco.values[:, :])]
    div2.text = f"""
    <div style="background-color: #fff1c0; padding: 1px; border-radius: 3px;margin-left: 11px; box-shadow: 3px 3px 4px #06ffcd92">
        <p style='font-family:Arial;font-size: 17px;  color: #343434;'>
<b>date</b>: {fruits[new[0]]}<br> <b>mean SSR</b>: {forssrmeanGLOBEforco[0]:.2f} Wm<sup>-2</sup>
<br> <b>mean land SSR</b>: {forssrmeanLANDforco[0]:.2f} Wm<sup>-2</sup>
<br> <b>mean ocean SSR</b>: {forssrmeanOCEANforco[0]:.2f} Wm<sup>-2</sup>


</p>
    </div>
"""


san.selected.on_change("indices", update_timeseries4)


# Attach the update_plot callback to slider
slider.on_change("value", update_timeseries)
time_select.on_change("value", update_timeseries3)

layout = column(
    row(
        column(
            lat_min_input, lat_max_input, lon_min_input, lon_max_input, apply_button
        ),
        row(p1_, p1),
        annualx,
        column(slider, button, time_select, div2),
    ),
    row(p3, annual),
    row(text_area_input),
    styles={"background-color": "#1a1a1a", "width": "100%", "height": "200%"},
)
curdoc().add_root(layout)
# show(layout)
curdoc().title = "FORTH-RTM SSR"
