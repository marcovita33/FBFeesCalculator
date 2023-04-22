#!/usr/bin/env python
# coding: utf-8

# In[1]:


import pandas as pd
import matplotlib.pyplot as plt

# Lettura del file CSV
df = pd.read_csv("C:/Users/Utente/Desktop/cakio/dcereijo-player-scores/data/appearances.csv")





# In[2]:


# 1. Numero di apparizioni per anno per ogni giocatore
df['year'] = pd.DatetimeIndex(df['date']).year
appearances_per_year = df.groupby(['player_name', 'year']).size().reset_index(name='appearances')
print(appearances_per_year)


# In[3]:


# 2. Numero di apparizioni per meno o più di 45 minuti
less_than_45 = df[df['minutes_played'] < 45].groupby(['player_name', 'year']).size().reset_index(name='less_than_45')
more_than_45 = df[df['minutes_played'] >= 45].groupby(['player_name', 'year']).size().reset_index(name='more_than_45')
print(less_than_45)
print(more_than_45)


# In[4]:


# 3. massimo valore e del valore medio di apparizioni per anno
max_appearances = appearances_per_year.groupby('year')['appearances'].max()
mean_appearances = appearances_per_year.groupby('year')['appearances'].mean()
print(mean_appearances)
print(max_appearances)


# In[ ]:


# Creazione del nuovo dataset
new_df = appearances_per_year.merge(less_than_45, on='year', how='outer')
new_df = new_df.merge(more_than_45, on='year', how='outer')


# Rinominazione delle colonne
new_df = new_df.rename(columns={'appearances': 'appearances_per_year'})

# Visualizzazione del nuovo dataset
print(new_df)


# In[9]:


new_df.to_csv(r"C:\Users\Utente\Desktop\cakio\dcereijo-player-scores\data\indexis.csv")


# In[ ]:




