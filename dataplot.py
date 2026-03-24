import pandas as pd
import matplotlib.pyplot as plt
import os

# =====================================
# 1. SET DOMAIN NAME (change this once)
# =====================================
domain_name = "stayconnectedplumbing"

# Folder name
folder_name = f"{domain_name}_seo_reports"

# Create folder automatically
if not os.path.exists(folder_name):
    os.makedirs(folder_name)

# =====================================
# 2. LOAD CSV FILE
# =====================================
file_path = "keywords.csv"   # your uploaded CSV
df = pd.read_csv(file_path)

# =====================================
# 3. DETECT DATE COLUMNS AUTOMATICALLY
# =====================================
ranking_columns = [col for col in df.columns if "." in col or "-" in col]
ranking_columns = sorted(ranking_columns, reverse=True)

latest = ranking_columns[0]
previous = ranking_columns[1]

# Convert ranking columns to numbers
for col in ranking_columns:
    df[col] = pd.to_numeric(df[col], errors='coerce')

# =====================================
# 4. EXTRACT SUBURB FROM KEYWORD
# =====================================
df["Suburb"] = df["New Keywords"].apply(lambda x: str(x).split()[-1].capitalize())

# =====================================
# 5. KEYWORD GROWTH TREND CHART
# =====================================
avg_rank_by_date = []

for col in ranking_columns:
    avg_rank = df[col].mean()
    avg_rank_by_date.append(avg_rank)

plt.figure()
plt.plot(ranking_columns, avg_rank_by_date)
plt.title("Keyword Ranking Growth Trend")
plt.xlabel("Date")
plt.ylabel("Average Ranking Position")
plt.xticks(rotation=45)

# SAVE IMAGE
trend_path = f"{folder_name}/{domain_name}_keyword-trend.png"
plt.savefig(trend_path, bbox_inches="tight")
plt.close()

# =====================================
# 6. SUBURB PERFORMANCE SCORE
# =====================================
def score(row):
    if row <= 3:
        return 100
    elif row <= 10:
        return 70
    elif row <= 20:
        return 40
    elif row <= 50:
        return 20
    else:
        return 5

df["SEO Score"] = df[latest].apply(score)

suburb_score = df.groupby("Suburb")["SEO Score"].mean().sort_values(ascending=False)

# BAR CHART
plt.figure()
suburb_score.head(15).plot(kind="bar")
plt.title("Suburb SEO Strength Score")
plt.xlabel("Suburb")
plt.ylabel("SEO Score")
plt.xticks(rotation=40)

# SAVE IMAGE
suburb_path = f"{folder_name}/{domain_name}_suburb-score.png"
plt.savefig(suburb_path, bbox_inches="tight")
plt.close()

# =====================================
# 7. RANKING DISTRIBUTION PIE CHART
# =====================================
top3 = df[df[latest] <= 3].shape[0]
top10 = df[(df[latest] > 3) & (df[latest] <= 10)].shape[0]
top20 = df[(df[latest] > 10) & (df[latest] <= 20)].shape[0]
others = df[df[latest] > 20].shape[0]

labels = ["Top 3", "Top 10", "Top 20", "Not Ranking Well"]
sizes = [top3, top10, top20, others]

plt.figure()
plt.pie(sizes, labels=labels, autopct="%1.1f%%")
plt.title("Keyword Ranking Distribution")

# SAVE IMAGE
pie_path = f"{folder_name}/{domain_name}_ranking-pie.png"
plt.savefig(pie_path, bbox_inches="tight")
plt.close()

# =====================================
# 8. PRIORITY KEYWORDS REPORT
# =====================================
priority_keywords = df[
    (df[latest] > 5) & 
    (df[latest] <= 20)
].sort_values(by=latest)

priority_path = f"{folder_name}/{domain_name}_priority_keywords.csv"
priority_keywords.to_csv(priority_path, index=False)

# =====================================
# 9. BEST IMPROVED KEYWORDS
# =====================================
df["Improvement"] = df[previous] - df[latest]
best_growth = df.sort_values(by="Improvement", ascending=False)

growth_path = f"{folder_name}/{domain_name}_best_growth_keywords.csv"
best_growth.to_csv(growth_path, index=False)

# =====================================
# DONE MESSAGE
# =====================================
print("\nAll reports saved successfully in folder:")
print(folder_name)