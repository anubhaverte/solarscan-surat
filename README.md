# SolarScan Surat

**Mapping unrealized rooftop solar potential in Surat, Gujarat, using computer vision and geospatial analysis grounded in real government energy data.**

---

## Overview

Most rooftops in Indian cities sit unused for solar generation, despite strong year-round irradiance. This project builds an end-to-end pipeline that takes raw aerial imagery of a real Surat neighborhood and produces, per rooftop:

- Whether solar panels are already installed
- If not, an estimated month-by-month energy generation potential (in kWh), grounded in Gujarat's actual seasonal solar irradiance — not a flat, generic assumption

The goal is a reusable template: the same pipeline could, in principle, be pointed at any Indian city with public satellite imagery and open government solar data.

## How it works

```
Aerial imagery
      │
      ├──────────────────────┐
      ▼                      ▼
Building footprint      Solar panel
extraction (SAM)         detection
                        (YOLOv8, fine-tuned)
      │                      │
      └──────────┬───────────┘
                 ▼
        Spatial matching
       (GeoPandas — which
      panels sit on which
           rooftops)
                 ▼
       Potential calculation
    (grounded in NITI Aayog's
   15-year monthly insolation
        data for Surat)
                 ▼
        Per-rooftop results:
      has_panel / potential kWh
```

**1. Building footprint extraction**
Meta's Segment Anything Model (SAM), run in automatic mask-generation mode, segments every distinct object in the aerial imagery. A custom filtering layer (size, shape, and spectral thresholds) isolates real building footprints from roads, vegetation, and background noise.

**2. Solar panel detection**
A YOLOv8 model, fine-tuned on a curated aerial solar panel dataset, detects existing installations directly from the same imagery.

**3. Spatial matching**
Detected panels are matched to their underlying rooftop polygon using point-in-polygon and centroid-based spatial joins in GeoPandas, classifying each rooftop as "has solar" or "unrealized potential."

**4. Grounded potential calculation**
For every rooftop without solar, potential generation is estimated using:
- A standard rooftop solar capacity benchmark (kWp per unit area), consistent with figures used in Indian rooftop solar policy
- 15-year monthly average solar insolation for Surat district, sourced directly from [NITI Aayog's ICED energy data portal](https://iced.niti.gov.in/energy/fuel-sources/solar/irradiance)
- A standard system performance ratio, accounting for real-world losses (inverter efficiency, soiling, temperature derating)

This produces a full 12-month generation curve per rooftop, reflecting Gujarat's real seasonal solar variation rather than a single static number.

## Tech stack

| Component | Tool |
|---|---|
| Building segmentation | Meta Segment Anything Model (SAM) |
| Object detection | YOLOv8 (Ultralytics), fine-tuned |
| Geospatial processing | GeoPandas, Shapely, Rasterio |
| Potential modeling | Custom, grounded in NITI Aayog irradiance data |
| Backend | FastAPI |
| Frontend | Leaflet.js |
| Training environment | Google Colab (T4 GPU) |

## Data sources

- Aerial satellite imagery of a defined Surat study area
- [Roboflow Universe](https://universe.roboflow.com) — aerial solar panel detection dataset (fine-tuning)
- [NITI Aayog ICED](https://iced.niti.gov.in/energy/fuel-sources/solar/irradiance) — monthly solar insolation data, Surat district, 15-year average

## Results

- Rooftops mapped across a defined Surat neighborhood
- Existing solar installations identified and separated from unrealized potential
- Month-by-month generation potential (kWh) calculated per rooftop, reflecting Gujarat's actual seasonal irradiance curve

## Known limitations

- **Georeferencing drift:** tile corner coordinates were derived from map-service URL parameters rather than independently verified against ground truth, causing minor spatial misalignment between tiles when overlaid on satellite basemaps. Rooftop *shapes and areas* are internally consistent and verified; absolute geographic placement has a small, uneven offset currently being corrected.
- **Detection scope:** the current study area covers a single neighborhood, not the full city — chosen deliberately to keep the pipeline demonstrable and fully verifiable within project scope.
- **Panel matching:** spatial matching between independently-derived detection and segmentation layers is inherently approximate; a portion of detected panels remain ambiguously or unmatched due to small georeferencing offsets rather than detection failure.

## Status

Core detection, spatial matching, and potential-calculation pipeline is complete and verified. Backend and frontend integration is in progress; georeferencing refinement is ongoing.

## Motivation

Built as an independent project to explore how computer vision and open geospatial data can be combined to answer a locally grounded, practically useful question — and as a foundation for deeper work in geospatial AI and remote sensing.
