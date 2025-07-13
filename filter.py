import pandas as pd

# Load the CSV file (replace with your filename if different)
input_file = "sales-data.csv"
output_file = "output.csv"

# Read the CSV into a DataFrame
df = pd.read_csv(input_file)

# Remove rows where square footage is 0 or missing to avoid division errors
df = df[df["sq__ft"] > 0]

# Calculate price per square foot for each property
df["price_per_sqft"] = df["price"] / df["sq__ft"]

# Calculate the average price per square foot
avg_price_per_sqft = df["price_per_sqft"].mean()

# Filter properties with price per sqft less than the average
filtered_df = df[df["price_per_sqft"] < avg_price_per_sqft]

# Write the filtered data to a new CSV file
filtered_df.to_csv(output_file, index=False)

print(f"Filtered data saved to: {output_file}")
