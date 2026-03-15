import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

INPUT_CSV = "data/mieszkania_trojmiasto_clean.csv"

# Load cleaned data
df = pd.read_csv(INPUT_CSV)

# Basic statistics
mean_price = df["price"].mean()
median_price = df["price"].median()
mean_area = df["area"].mean()
median_area = df["area"].median()
mean_price_per_m2 = df["price_per_m2"].mean()
median_price_per_m2 = df["price_per_m2"].median()

print("Basic statistics:")
print(f"Mean price: {mean_price:.2f} zł")
print(f"Median price: {median_price:.2f} zł")
print(f"Mean area: {mean_area:.2f} m²")
print(f"Median area: {median_area:.2f} m²")
print(f"Mean price per m²: {mean_price_per_m2:.2f} zł/m²")
print(f"Median price per m²: {median_price_per_m2:.2f} zł/m²")

# Histogram of apartment areas
fig_area_hist = px.histogram(df, x="area", nbins=30, title="Distribution of Apartment Areas (m²)")
fig_area_hist.write_html("plots/area_histogram.html")

# Boxplot of prices by city
df["city"] = df["city"].str.capitalize()
fig_box = px.box(df, x="city", y="price", title="Apartment Prices by City")
fig_box.write_html("plots/price_boxplot_by_city.html")

# Scatter plot: area vs price
fig_scatter = px.scatter(df, x="area", y="price", color="city", title="Area vs Price", labels={"area": "Area (m²)", "price": "Price (zł)"})
fig_scatter.write_html("plots/area_vs_price_scatter.html")

# Ranking of cities by average price per m²
city_ranking = df.groupby("city")["price_per_m2"].mean().sort_values(ascending=False)
fig_bar = px.bar(city_ranking, x=city_ranking.index, y=city_ranking.values, labels={"x": "City", "y": "Average Price per m² (zł)"}, title="Average Price per m² by City")
fig_bar.write_html("plots/price_per_m2_ranking.html")

# Pie chart for share of listings by city
city_counts = df["city"].value_counts()
fig_pie = px.pie(names=city_counts.index, values=city_counts.values, title="Share of Listings by City")
fig_pie.write_html("plots/listings_share_pie.html")

print("Plots saved to 'plots/' directory.")
