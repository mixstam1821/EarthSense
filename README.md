# EarthSense

My PhD was made interactive through this free and open-source web app! 
PhD Thesis: Detailed assessment of the global dimming and brightening of the Earth under all-sky and clear sky conditions using modern tools and long-term climate data. https://www.didaktorika.gr/eadd/handle/10442/59941

## Features
1) Explore the surface solar radiation (SSR) produced by radiative transfer calculations. Map, and animate per month the global distribution of SSR. Interact with the spatially averaged timeseries and the annual cycle of SSR.
2) See the evaluation of modelled SSR against ground-truth measurements by the GEBA network. Map with stations, click on them and see the annual cycle, the monthly timeseries, the scatter plot and evaluation metrics between modelled SSR and GEBA stations.
3) Investigate the SSR changes, their causes and their links with other climatic variables.

## Installation

1. Clone the repository:
```bash
git clone https://github.com/mixstam1821/EarthSense.git
cd EarthSense
```

2. Create a virtual environment (optional but recommended):
```bash
python -m venv earthsensevenv
source earthsensevenv/bin/activate  # On Windows: earthsensevenv\Scripts\activate
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

3. Open your browser and navigate to:
```
[http://localhost:9797](http://0.0.0.0:9797/)
```

## Structure

```
EarthSense/
├── data/
│   ├── 10 files downloaded from https://zenodo.org/records/17382343
├── bokeh_apps/
│   ├── app1_mirror.py
│   ├── app2_mirror.py
│   └── app3_mirror.py
├── static/
│   └── css/
│       └── style.css
├── templates/
│   ├── base.html
│   ├── home.html
│   ├── about.html
│   ├── intro.html
│   └── bokeh_app.html
├── main.py
├── requirements.txt
├── start.sh
└── README.md
```


## Contributing

Feel free to submit issues and enhancement requests!
