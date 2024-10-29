import streamlit as st
import psycopg2
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np


# Connect to the PostgreSQL database
def connect_to_db(dbname, user, password, host, port):
  try:
    conn = psycopg2.connect(dbname=dbname, user=user, password=password, host=host, port=port)
    return conn
  except Exception as e:
    st.error(f"Connection error: {e}")
    return None


# Run queries on PostgrSQL database
def run_query(conn, sql):
  if not conn:
    return

  cursor = conn.cursor()
  cursor.execute(sql)

  return cursor.fetchall(), cursor.description


# Generate find cards SQL
def show_available_listing(country, amenity,rating):
    # Filters based on user selection
    country_filter = f"AND country.Country = '{country}'" if country else ""
    amenity_filter = f"AND amenity.Amenity_level = '{amenity}'" if amenity else ""
    rating_filter = f"AND rating.RatingLevel = '{rating}'" if rating else ""

    # SQL to get available listing
    available_listing_sql = f"""
        SELECT
	listing.Listing_ID,
	listing.Name,
	listing.Description,
	listing.Location,
	property.propertytype,
	bedroom.bedtype,
  price.price,
	bathroom.bathroomtype,
	amenity.amenity_level,
	rating.RatingLevel,
	cancellation.CancellationType
FROM
	listing
INNER JOIN property ON listing.Property_ID = property.Property_ID
INNER JOIN bedroom ON listing.Bedroom_ID = bedroom.Bedroom_ID
INNER JOIN bathroom ON listing.Bathroom_ID = bathroom.Bathroom_ID
INNER JOIN amenity ON listing.Amenity_ID = amenity.amenity_ID
INNER JOIN price ON listing.Price_ID = price.price_id
INNER JOIN review ON listing.listing_id = review.listing_id
INNER JOIN rating ON review.rating_id = rating.rating_id
INNER JOIN cancellation ON listing.Cancellation_ID = cancellation.Cancellation_ID
INNER JOIN country ON listing.Country_ID = country.Country_ID
WHERE listing.Availability = 'Available'
    {country_filter}
    {amenity_filter}
    {rating_filter}

    """
   
    

    return available_listing_sql
  


# def generate_price_history_sql(make, model):

#   price_history_sql = f"""
#     WITH vehicles AS (
#       SELECT vehicle_id, model FROM vehicles WHERE availability = TRUE AND type = 'new'
#     ),
#     vehicle_models AS (
#       SELECT model, make FROM vehicle_models WHERE model = '{model}' AND make = '{make}'
#     ),
#     price_history AS (
#       SELECT vehicle_id, extract(year from price_recorded_date) as year, price FROM price_history
#     )
#     SELECT
#       price_history.year AS year, round(avg(price_history.price)) AS price
#     FROM
#       vehicles JOIN vehicle_models ON vehicles.model = vehicle_models.model
#       JOIN price_history ON vehicles.vehicle_id = price_history.vehicle_id
#     GROUP BY
#       price_history.year
#     ORDER BY
#       price_history.year
#   """

#   return price_history_sql


# Database connection details
dbname = "dmql"
user = "postgres"
password = "Vishal140300"
host = "localhost"
port = 5432

conn = connect_to_db(dbname, user, password, host, port)

st.set_page_config(page_title="Team 67", page_icon="")


st.header("Hotel System")
st.image("https://olirdesigns.com/wp-content/uploads/2021/06/hotel-dora-logo.png", width=100)
search_hotels, _ = st.tabs(["Seach Hotels", "Empty"])

with search_hotels:

# Tabs for Find Cars and Price History
  st.subheader("Find your Hotels")

    # Text input fields for user to enter query parameters
  country = st.selectbox("Country", ["USA", "Canada", "UK", "Australia", "Germany","France", "Italy", "Spain", "China", "India"], key=1)
  amenity = st.selectbox("Amentity", ['Basic', 'Standard', 'Comfort', 'Premium', 'Luxury'], key=2)
  rating = st.selectbox("Rating ", ["Excellent", "Very Good", "Good", "Fair", "Poor"], key=3)


    # Submit button
  if st.button("Show", key=9):
    available_listing = show_available_listing(country, amenity,rating)
    results, description = run_query(conn, available_listing)
    results_df = pd.DataFrame(results, columns=[desc[0] for desc in description])

    st.dataframe(results_df)

# with price_history:
#   # Price History tab content
#   st.subheader("Track Price")

#   # Text input fields for user to enter query parameters
#   make = st.selectbox("Make", ["Honda", "Ford", "Nissan", "Chevrolet", "Toyota"], key=201)

#   if make == "Honda":
#     model = st.selectbox("Model", ["CR-V Hybrid", "HR-V", "Passport", "Pilot", "Ridgeline"], key=202)
#   elif make == "Ford":
#     model = st.selectbox("Model", ["Bronco Sport", "Edge", "F-150", "Maverick", "Mustang Mach-E"], key=203)
#   elif make == "Nissan":
#     model = st.selectbox("Model", ["Altima", "Frontier", "Maxima", "Rouge", "Sentra"], key=204)
#   elif make == "Chevrolet":
#     model = st.selectbox("Model", ["Blazer EV", "Colorado", "Equinox", "Silverado", "Trax"], key=205)
#   elif make == "Toyota":
#     model = st.selectbox("Model", ["Corolla", "Highlander", "RAV4 Hybrid", "Sienna", "Tundra"], key=206)

#   # Submit button
#   if st.button("Show Cars", key=207):
#     price_history_sql = generate_price_history_sql(make, model)
#     results, description = run_query(conn, price_history_sql)
#     results_df = pd.DataFrame(results, columns=[desc[0] for desc in description])

#     fig, ax = plt.subplots()

#     ax.plot(results_df["year"], results_df["price"])
#     st.pyplot(fig)