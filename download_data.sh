#!/usr/bin/env bash
set -e  # exit on any error

# Folder where to place data
DATA_DIR="data"

# Ensure data directory exists
mkdir -p "$DATA_DIR"

# Change to that directory
cd "$DATA_DIR"

echo "Downloading EarthSense dataset from Zenodo..."

# Base Zenodo record URL
ZENODO_BASE="https://zenodo.org/records/17382343/files"

# List of files (as given in the Zenodo record)
FILES=(
  "__anom_8418_slopes_FMCX8418_SurfaceDown_.nc"
  "FMCX_8418_SurfaceDown_f.nc"
  "FMCX_8418_drivers_we1.nc"
  "FMCX_8418_impac1.nc"
  "contributions_all_1984-2018_.nc"
  "forth_361x576_land_see_mask.nc"
  "_AF_FMCX_1984_2018_lat0_-90_lat1_90_lon0_-180_lon1_180_thresalt_0_500_thresagr_0.7__GEBA_FLUXES_GLOBE_eva.txt"
  "_AF_FMCX_1984_2018_lat0_-90_lat1_90_lon0_-180_lon1_180_thresalt_0_500_thresagr_0.7__GEBA_FLUXES_GLOBE_rf.txt"
  "_DA_FMCX_1984_2018_lat0_-90_lat1_90_lon0_-180_lon1_180_thresalt_0_500_thresagr_0.7__GEBA_ANOMALIES_GLOBE_eva.txt"
  "_DA_FMCX_1984_2018_lat0_-90_lat1_90_lon0_-180_lon1_180_thresalt_0_500_thresagr_0.7__GEBA_ANOMALIES_GLOBE_rf.txt"
)

for fname in "${FILES[@]}"; do
  url="${ZENODO_BASE}/${fname}"
  echo "-> Downloading ${fname} ..."
  curl -L -o "${fname}" "${url}"
done

echo "Download complete. Files are placed in $(pwd)."
