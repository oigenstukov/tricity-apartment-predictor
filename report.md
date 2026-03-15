# Trójmiasto Apartment Price Prediction — Report

**Author:** Evgeny Podskrebkin  
**Date:** March 2026

---

## 1. Project Overview
This project demonstrates a complete machine learning pipeline for predicting apartment prices in Trójmiasto (Gdańsk, Gdynia, Sopot). The workflow includes data scraping, cleaning, analysis, model training, and deployment as a web application.

## 2. Data Description
- **Source:** adresowo.pl (scraped in March 2026)
- **Number of records:** 595 
- **Main features:** city, area (m²), number of rooms, price, price per m², etc.

## 3. Key Visualizations
- **Histogram of apartment areas**
  
  ![Area Histogram](plots/area_histogram.png)
  
  _Shows the distribution of apartment sizes._

- **Boxplot of prices by city**
  
  ![Boxplot](plots/price_boxplot_by_city.png)
  
  _Compares price ranges in Gdańsk, Gdynia, Sopot._

- **Scatter plot: Area vs Price**
  
  ![Scatter](plots/area_vs_price_scatter.png)
  
  _Visualizes the relationship between area and price._

## 4. Model Results
- **Algorithm:** RandomForestRegressor
- **R² score:** 0.4605
- **Residuals plot:**
  
  ![Residuals](plots/residuals_plot.png)

## 5. Web Application
- The Streamlit app allows users to enter apartment parameters and get a price estimate with a comparison to the market.
- Example screenshot:
  
  ![App Screenshot](plots/app_example.png)

## 6. Conclusions
- The model provides reasonable price estimates for apartments in Trójmiasto.
- The pipeline is fully automated and can be easily updated with new data.

---
