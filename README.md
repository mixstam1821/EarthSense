# EarthSense

My PhD was made interactive through this free and open-source web app! 

PhD Thesis: Detailed assessment of the global dimming and brightening of the Earth under all-sky and clear sky conditions using modern tools and long-term climate data. 
https://www.didaktorika.gr/eadd/handle/10442/59941

## Features

<a href="#" style="pointer-events:none; cursor:default;">
  <img src="https://img.shields.io/badge/EarthSense1-deepskyblue" alt="EarthSense1" width="130">
</a>

Explore the surface solar radiation (SSR) produced by radiative transfer calculations. Map and animate per month the global distribution of SSR. Interact with the spatially averaged timeseries and the annual cycle of SSR.
In the timeseries, you can click on a point, which is the deseasonalized SSR anomaly and corresponds to a specific time stamp. Then the Map will show the global distribution of SSR on this date. Use the slider or the dropdown menu to choose the date, and the play button to animate the Map. The abr plot shows the annual cycle of SSR for the globe and for the Northern and Southern Hemispheres. Click on the bar and you will get the average SSR for this month on the Map. If you reload the App you will get the total annual average of SSR, as it was in the begining. Please note that when you run this app live in the Hugging Face (see the link below), it will take arounf half a minute to load due to the large data.


<a href="#" style="pointer-events:none; cursor:default;">
  <img src="https://img.shields.io/badge/EarthSense2-gold" alt="EarthSense2" width="130">
</a>

See the evaluation of modelled SSR against ground-truth measurements by the GEBA network. There is a map with stations showing the SSR changes of the stations. Click on them and see the annual cycle, the monthly timeseries, the scatter plot and evaluation metrics between modelled SSR (near the stations) and GEBA stations.


<a href="#" style="pointer-events:none; cursor:default;">
  <img src="https://img.shields.io/badge/EarthSense3-pink" alt="EarthSense3" width="130">
</a>

Investigate the SSR changes, their causes and their links with other climatic variables. The map is showing the global distribution of SSR changes. Click or select a rectangular area, and you will get the contributions to the estimated SSR changes of the atmospheric input to the model parameters, in the bar plots. On the top right, you will get the normalized low-pass filtered data of the annual timeseries of the input to the model parameters, as well as the SSR. The timeseries below show the normalized low-pass filtered data of the annual timeseries of various climatic variables and SSR. The table summarizes the trends and their significance, as well as the Pearson and Spearman correlation coefficients between the annual time series of climatic variables and the SSR.


## Live 
<a href="https://mixstam1453-earthsense.hf.space/landing" target="_blank" rel="noopener noreferrer">
  <img src="https://img.shields.io/badge/%20Open%20in%20Spaces-purple" alt="EarthSense" width="170">
</a>

## Demo
Here’s how **EarthSense** looks in action 👇  

![Demo](assets/ES1.gif)
![Demo](assets/ES2.gif)
![Demo](assets/ES3.gif)
![Demo](assets/ES4.gif)
![Demo](assets/ES5.gif)

## Installation

1. Clone the repository:
```bash
git clone https://github.com/mixstam1821/EarthSense.git
cd EarthSense
```
2. Download the data:
   ```bash
   chmod +x download_data.sh
   ./download_data.sh
   ```
   
   -OR-
   
   Download it manually:
   a) Go here https://zenodo.org/records/17382343
   b) Find and click "Download all"
   c) A zip file around 930MB will be downloaded.
   d) Extract them inside EarthSense/data/ directory.
   
3. Create a virtual environment (optional but recommended):
```bash
python -m venv earthsensevenv
source earthsensevenv/bin/activate  # On Windows: earthsensevenv\Scripts\activate
```

4. Install dependencies:
```bash
pip install -r requirements.txt
```

5. Make the start script executable:
```bash
chmod +x start.sh
```

6. Start all servers using the start script:
```bash
./start.sh
```

7. Open your browser and navigate to:
```
http://0.0.0.0:7860/landing
```

-OR-

Use Docker:

1. Clone the repository:
```bash
git clone https://github.com/mixstam1821/EarthSense.git
cd EarthSense
```
2. Download the data:
   ```bash
   chmod +x download_data.sh
   ./download_data.sh
   ```
   
   -OR-
   
   Download it manually:
   a) Go here https://zenodo.org/records/17382343
   b) Find and click "Download all"
   c) A zip file around 930MB will be downloaded.
   d) Extract them inside EarthSense/data/ directory.

3. Build the Docker image (the dot . means "current folder")
```bash
docker build -t earthsense .
```

4. Run the container and expose port 7860
```bash
docker run -p 7860:7860 earthsense
```

5. Open your browser and navigate to:
```
http://0.0.0.0:7860/landing
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
├── requirements.txt
├── start.sh
└── README.md
```


## Contributing

Feel free to submit issues and enhancement requests!
