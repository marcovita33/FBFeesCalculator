#!/usr/bin/env python
# coding: utf-8

# In[1]:


import pandas as pd


# In[2]:


# caricamento del file csv
df2 = pd.read_csv('C:\\Users\\Utente\\Desktop\\cakio\\dcereijo-player-scores\\data\\uefarankteam2.csv', encoding='ISO-8859-1')
# selezione delle colonne di interesse
cols = df2.columns[5:18]

# somma degli elementi lungo l'asse delle colonne
uefa_sum = df2[cols].sum(axis=1)

# aggiunta della nuova colonna nel DataFrame
df2.insert(16, 'UEFAPoints', uefa_sum)

# stampa del DataFrame con la nuova colonna
print(df2)


# In[3]:




# caricamento dei due file
df1 = pd.read_csv('C:\\Users\\Utente\\Desktop\\cakio\\dcereijo-player-scores\\data\\spi_global_rankings.csv')


# unione dei due DataFrame
df = pd.merge(df1, df2, left_on='name', right_on='nome squadra', how='inner')

# manipolazione del DataFrame per ottenere la classifica unificata
df = df.sort_values('rank')
df = df[['rank', 'name', 'league', 'off', 'def', 'spi','UEFAPoints' ]]

df = df.reset_index(drop=True)

# visualizzazione dei primi 10 elementi del DataFrame risultante
print(df)


# In[4]:


from sklearn.preprocessing import StandardScaler

# Normalizza i punteggi di ogni variabile
scaler = StandardScaler()
df[['off', 'def', 'spi', 'UEFAPoints']] = scaler.fit_transform(df[['off', 'def', 'spi', 'UEFAPoints']])

# Assegna un peso diverso a ciascuna variabile
weights = {'off': 0.2, 'def': 0.2, 'spi': 0.2, 'UEFAPoints': 0.4}

# Calcola il punteggio overall per ogni squadra
df['Overall'] = (df['off']*weights['off'] + df['def']*weights['def'] +
                 df['spi']*weights['spi'] + df['UEFAPoints']*weights['UEFAPoints'])

# Normalizza il punteggio overall in modo che vari da 0 a 1
df['Overall'] = (df['Overall'] - df['Overall'].min()) / (df['Overall'].max() - df['Overall'].min())
print(df)


# In[5]:


# Ordina il DataFrame in base all'overall in ordine decrescente
df = df.sort_values(by='Overall', ascending=False)

# Aggiunge una nuova colonna di ranking in base all'overall
df['Rank'] = df['Overall'].rank(ascending=False)

# Seleziona solo le colonne 'name', 'league', 'Overall' e 'Rank'
df = df[['name', 'league', 'Overall', 'Rank']]
print(df)


# In[6]:


# Definisci la funzione per assegnare la tier in base alla posizione
def assign_tier(position):
    if position <= 15:
        return 'S'
    elif position <= 30:
        return 'A'
    elif position <= 45:
        return 'B'
    elif position <= 60:
        return 'C'
    elif position <= 75:
        return 'D'
    elif position <= 90:
        return 'F'
    else:
        return 'G'

# Aggiungi la colonna 'Tier' al DataFrame in base alla posizione
df['Tier'] = df['Rank'].apply(assign_tier)

print(df)


# In[7]:




# raggruppa il dataframe per la colonna 'league' e calcola la somma degli overall
league_overall = df.groupby('league')['Overall'].sum()

# calcola la media degli overall per ogni lega
league_overall_mean = league_overall.mean()

# ordina le leghe in base alla loro media di overall, dal più alto al più basso
sorted_leagues = league_overall.sort_values(ascending=False).index

# crea un nuovo dataframe con la media di overall per ogni lega
new_df = pd.DataFrame({'league': sorted_leagues, 'mean_overall': league_overall.loc[sorted_leagues].values / len(df['name'].unique())})

# stampa il nuovo dataframe
print(new_df)


# In[26]:


# Calcolo del punteggio overall per ogni riga del dataframe
df["summy"] = df["Overall"] * (1 - df["Rank"]/109)

# Raggruppamento per league e somma dei punteggi overall
overall_league = df.groupby("league")["summy"].sum()

# Visualizzazione dei punteggi overall per league
print(overall_league)


# In[29]:


overall_league.to_csv(r"C:\Users\Utente\Desktop\cakio\dcereijo-player-scores\data\TIERLEAGUE1.csv", index=True)


# In[ ]:




