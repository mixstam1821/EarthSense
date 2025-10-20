#!/bin/bash
#!/bin/bash
echo "🚀 Starting Bokeh multi-app server..."

bokeh serve \
    bokeh_apps/landing \
    bokeh_apps/intro \
    bokeh_apps/about \
    bokeh_apps/app1_mirror.py \
    bokeh_apps/app2_mirror.py \
    bokeh_apps/app3_mirror.py \
    --allow-websocket-origin="*" \
    --port 7860 \
    --address 0.0.0.0 \
    --session-token-expiration=86400000
