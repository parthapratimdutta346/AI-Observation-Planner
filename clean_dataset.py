import pandas as pd

# Load dataset
df = pd.read_csv("astronomy_master_kb.csv")

print("Before:", len(df))

# Remove duplicates
df = df.drop_duplicates(
    subset=["Object_Name", "Category"],
    keep="first"
)

print("After:", len(df))

# Save cleaned file
df.to_csv(
    "astronomy_master_kb.csv",
    index=False
)

print("Duplicates removed successfully.")