import pandas as pd

# Create sample dataset
data = {
    "Employee": ["A", "B", "C", "D", "E"],
    "Department": ["IT", "HR", "IT", "Finance", "HR"],
    "Salary": [50000, 45000, 60000, 55000, 48000]
}

df = pd.DataFrame(data)

# Show dataset
print("Dataset:")
print(df)

# Average salary
print("\nAverage Salary:", df["Salary"].mean())

# Group by department
print("\nAverage Salary by Department:")
print(df.groupby("Department")["Salary"].mean())