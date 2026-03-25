import pandas as pd
import matplotlib.pyplot as plt
import os

# =====================================
# 1. DOMAIN NAME
# =====================================
domain_name = "seo_project"

folder_name = f"{domain_name}_visual_reports"

if not os.path.exists(folder_name):
    os.makedirs(folder_name)

# =====================================
# 2. LOAD CSV
# =====================================
file_path = "keywords.csv"
df = pd.read_csv(file_path)

# =====================================
# 3. AUTO DETECT DATE COLUMNS
# =====================================
date_columns = []

for col in df.columns:
    if any(char.isdigit() for char in col):
        date_columns.append(col)

date_columns = sorted(date_columns, reverse=True)

latest = date_columns[0]
previous = date_columns[1]

# =====================================
# 4. CLEAN RANK DATA
# =====================================
def clean_rank(value):
    if pd.isna(value):
        return 101
    
    value = str(value).strip().lower()

    if value in ["not in 100", "-", "", "na", "n/a"]:
        return 101

    try:
        return int(value)
    except:
        return 101

for col in date_columns:
    df[col] = df[col].apply(clean_rank)

# =====================================
# 5. OVERALL SEO GROWTH TREND
# =====================================
avg_rank = []

for col in date_columns:
    avg_rank.append(df[col].mean())

plt.figure()
plt.plot(date_columns, avg_rank)
plt.title("SEO Keyword Growth Trend")
plt.xlabel("Date")
plt.ylabel("Average Ranking Position")
plt.xticks(rotation=45)

plt.savefig(f"{folder_name}/seo_growth_trend.png", bbox_inches="tight")
plt.close()

# =====================================
# 6. TOP WINNING KEYWORDS (Top 20)
# =====================================
top_keywords = df.sort_values(by=latest).head(20)

plt.figure()
plt.barh(top_keywords["Keywords"], top_keywords[latest])
plt.title("Top Performing Keywords")
plt.xlabel("Ranking Position")
plt.ylabel("Keywords")

plt.savefig(f"{folder_name}/top_keywords.png", bbox_inches="tight")
plt.close()

# =====================================
# 7. EASY WIN KEYWORDS (Rank 5–20)
# =====================================
easy_win = df[(df[latest] > 5) & (df[latest] <= 20)]
easy_win = easy_win.sort_values(by=latest).head(20)

plt.figure()
plt.barh(easy_win["Keywords"], easy_win[latest])
plt.title("Easy SEO Win Keywords (Optimize These First)")
plt.xlabel("Ranking Position")
plt.ylabel("Keywords")

plt.savefig(f"{folder_name}/easy_win_keywords.png", bbox_inches="tight")
plt.close()

# =====================================
# 8. KEYWORDS LOSING RANK
# =====================================
df["Drop"] = df[latest] - df[previous]

losing_keywords = df.sort_values(by="Drop", ascending=False).head(20)

plt.figure()
plt.barh(losing_keywords["Keywords"], losing_keywords["Drop"])
plt.title("Keywords Losing Ranking (Needs Fix)")
plt.xlabel("Ranking Drop")
plt.ylabel("Keywords")

plt.savefig(f"{folder_name}/losing_keywords.png", bbox_inches="tight")
plt.close()

# =====================================
# 9. SEO STRENGTH DISTRIBUTION
# =====================================
top3 = df[df[latest] <= 3].shape[0]
top10 = df[(df[latest] > 3) & (df[latest] <= 10)].shape[0]
top20 = df[(df[latest] > 10) & (df[latest] <= 20)].shape[0]
others = df[df[latest] > 20].shape[0]

labels = ["Top 3", "Top 10", "Top 20", "Not Ranking"]
sizes = [top3, top10, top20, others]

plt.figure()
plt.pie(sizes, labels=labels, autopct="%1.1f%%")
plt.title("SEO Keyword Strength Distribution")

plt.savefig(f"{folder_name}/seo_strength_distribution.png", bbox_inches="tight")
plt.close()

# =====================================
# DONE
# =====================================
print("\nAll SEO Visual Reports Generated Successfully!")
print("Check folder:", folder_name)