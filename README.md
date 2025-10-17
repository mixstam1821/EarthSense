# Bokeh FastAPI Dashboard

A modern dashboard application combining Bokeh's interactive visualizations with FastAPI's high-performance backend, featuring a beautiful dark theme.

## Features

- Interactive Scatter Plot with customizable distributions
- Dynamic Line Plot with time series data
- Customizable Heatmap with multiple color palettes
- Dark theme for comfortable viewing
- Responsive design
- FastAPI backend
- Modern UI with gradient accents

## Installation

1. Clone the repository:
```bash
git clone <repository-url>
cd bokeh-fastapi-dashboard/app
```

2. Create a virtual environment (optional but recommended):
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

## Running the Application

1. Make the start script executable:
```bash
chmod +x start.sh
```

2. Start all servers using the start script:
```bash
./start.sh
```

This will start:
- Bokeh server for Scatter Plot on port 5006
- Bokeh server for Line Plot on port 5007
- Bokeh server for Heatmap on port 5008
- FastAPI server on port 8000

3. Open your browser and navigate to:
```
http://localhost:8000
```

## Structure

```
app/
├── bokeh_apps/
│   ├── scatter_app.py
│   ├── line_app.py
│   └── heatmap_app.py
├── static/
│   └── css/
│       └── style.css
├── templates/
│   ├── base.html
│   ├── home.html
│   ├── about.html
│   └── bokeh_app.html
├── main.py
├── requirements.txt
├── start.sh
└── README.md
```

## Customization

- Modify the theme colors in `static/css/style.css`
- Add new Bokeh applications in the `bokeh_apps` directory
- Customize the layout in the template files

## Contributing

Feel free to submit issues and enhancement requests!
