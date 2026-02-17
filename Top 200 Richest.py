import pandas as pd 
import matplotlib.pyplot as plt 
import seaborn as sns 
import numpy as np
import requests
from bs4 import BeautifulSoup
import time


df= pd.read_csv("Top 200 Richest Person in the World.csv",encoding="latin-1")
print(df.head())
print(df.info())
print(df.describe())

print(df['Networth'])
df['Networth'] = df['Networth'].str.replace('$','').str.replace('B','').astype(float)
print(df['Networth'].dtype)

print(df.isnull().sum())

print(df['Country'].value_counts().head(5))
print(df['Industry'].value_counts().head(5))

plt.figure(figsize=(12,6))
sns.histplot(df['Age'], bins=15 , kde=True,color="blue")
plt.title("Distribution of Age")
plt.ylabel("The People Count")
plt.show()

top_countries = df['Country'].value_counts().head(10)
print(top_countries)
sns.barplot(x=top_countries.values, y=top_countries.index)
plt.title("Top Countries by Billionaires")
plt.ylabel("Name Of Top Countries")
plt.show()

top_industries = df['Industry'].value_counts().head(10)
print(top_industries)
sns.barplot(x=top_industries.values, y=top_industries.index)
plt.title("Top Industries by Billionaires")
plt.ylabel("Name Of Top Industries")
plt.show()

sns.scatterplot(x='Age', y='Networth', data=df)
plt.title("Networth vs Age Scatter Plot")
plt.ylabel("Networth")
plt.xlabel("Age")
plt.show()

sns.scatterplot(x='Industry', y='Networth', data=df)
plt.title("Networth vs Industry Scatter Plot")
plt.ylabel("Networth")
plt.xlabel("Industry")
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()

avg_country = df.groupby('Country')['Networth'].mean().sort_values(ascending=False).head(10)
print(avg_country)
sns.barplot(x=avg_country.index, y=avg_country.values)
plt.xticks(rotation=45)
plt.title("Average Networth by Top Countries")
plt.tight_layout()
plt.show()

plt.figure(figsize=(6,4))
sns.heatmap(df[['Age','Networth']].corr(), annot=True, cmap='coolwarm')
plt.title("Correlation Heatmap")
plt.show()

top_names = df['Name'].head(30)
print(top_names)

df['Clean_Name'] = (df['Name'].str.replace('& family', '').str.strip())
print(df['Clean_Name'])

df['Wiki_URL'] = "https://en.wikipedia.org/wiki/" + df['Clean_Name'].str.replace(' ', '_')
print(df['Wiki_URL'].head())

headers = {
    "User-Agent": "Mozilla/5.0"
}

education_list = []
occupation_list = []

for url in df['Wiki_URL'].head(20):

    try:
        response = requests.get(url, headers=headers)

        if response.status_code == 200:

            soup = BeautifulSoup(response.text, "html.parser")
            infobox = soup.find("table", {"class": "infobox"})

            education = None
            occupation = None

            if infobox:
                rows = infobox.find_all("tr")

                for row in rows:
                    header = row.find("th")

                    if header:
                        header_text = header.text.strip().lower()

                        if "alma mater" in header_text or "education" in header_text:
                            education = row.find("td").text.strip()

                        if "occupation" in header_text:
                            occupation = row.find("td").text.strip()

            education_list.append(education)
            occupation_list.append(occupation)

        else:
            education_list.append(None)
            occupation_list.append(None)

        time.sleep(1)

    except:
        education_list.append(None)
        occupation_list.append(None)
        
df.loc[df.index[:20], 'Education'] = education_list
df.loc[df.index[:20], 'Occupation'] = occupation_list

print(df[['Name','Education','Occupation']].head(20))
print(df['Education'].isnull().sum())

df['Cleaned_Education'] = df['Education'].str.replace(r"\(.*\)", "", regex=True)

df['Cleaned_Education'] = df['Cleaned_Education'].str.strip()

top_universities = df['Cleaned_Education'].value_counts().head(10)

plt.figure(figsize=(8,8))
plt.pie(top_universities.values, labels=top_universities.index, autopct='%1.1f%%', startangle=140)
plt.title("Top 10 Universities Among Billionaires")
plt.tight_layout()
plt.show()

df['Main_Occupation'] = df['Occupation'].str.split().str[0]
df['Main_Occupation'] = df['Main_Occupation'].str.capitalize()

top_main_occupation = df['Main_Occupation'].value_counts().head(10)
plt.figure(figsize=(12,8))
sns.barplot(x=top_main_occupation.values, y=top_main_occupation.index, palette='pastel')
plt.title("Top 10 Main Occupations Among Billionaires")
plt.xlabel("Count")
plt.ylabel("Occupation")
plt.yticks(rotation=0)  
plt.tight_layout()
plt.show()
