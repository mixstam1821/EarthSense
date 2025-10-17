#!/bin/bash
# Start Bokeh servers
bokeh serve --show bokeh_apps/app3_mirror.py bokeh_apps/app2_mirror.py bokeh_apps/app1_mirror.py --port=9798 --allow-websocket-origin=localhost:9798 &
# Start FastAPI server
python main.py
