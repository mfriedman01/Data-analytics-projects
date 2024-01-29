#!/usr/bin/env python
# coding: utf-8

# INTRODUCTION:
# 
# We are going to focus on Movie genres 
# 
# RESEARCH QUESTIONS:
# 1. which genres are the most common(Number of moves made)?
# 2. Which genres have high average budget and revenue?
# 3. which genres have high average popularity?
# 4. Which genres have the highest number of movies with a voting average >= 8?
# 
# 
# RESEARCH HYPOTHESES(H):
# 1. The best movies according to voting average return high profit and revenue.
# 2. the best movies according to popularity return high profit and revenue.
# 3. Highly budgeted movies return high revenue and profit.
# 4. Highly budgeted movies have a high popularity.

# Continue to build on these questions and ask more research questions but these are the base questions

# In[1]:


import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt


# In[91]:


movies = pd.read_csv(r'/Users/mfriedman130/Desktop/data analytics practice/imdb_movies.csv')


# In[92]:


movies.head()


# In[4]:


movies.info()


# In[93]:


pd.set_option('display.max.rows',11000)
pd.set_option('display.max.columns',22)


# In[94]:


movies[movies.duplicated()]


# In[96]:


movies.drop_duplicates(inplace = True)


# In[97]:


movies.dropna(subset = ['genres'], inplace = True)
#now have no null data in genres column and deleted a few rows


# In[98]:


movies['profit'] = movies['revenue'] - movies['budget']
#creates column for profit 


# In[99]:


movies_genre = movies[['popularity', 'budget', 'revenue', 'original_title', 'runtime', 'genres', 'release_date', 'director', 'vote_count', 'vote_average', 'profit']]


# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[100]:


movies_genre


# In[12]:


from pandas import Series, DataFrame


# In[13]:


movies_genre['genres'].str.split('|').apply(Series, 1).stack()
#we split on | and applies each piece into their own series
#using stack we are reshaping the dataframe into a multi-index


# In[74]:


split = movies_genre['genres'].str.split('|').apply(Series, 1).stack()
split.index = split.index.droplevel(-1)
split
#now we can apply this back to the dataframe

split.name = 'genres_split'
del movies_genre['genres']
movies_genre = movies_genre.join(split)


#for now our index will have each entry for the movie with the different genres entered as seperate rows
#we may or may not fix this later, but now we can group on the genre data
#we also have more than doubles the amount of rows for our dataframe


# In[15]:


movies_genre


# #end of cleaning
# Research question 1: which genres are the most common(number of movies made)?

# In[16]:


genres_count = pd.DataFrame(movies_genre.groupby('genres_split').original_title.nunique()).sort_values('original_title' , ascending= True)


# In[17]:


genres_count


# In[18]:


genres_count['original_title'].plot.pie(title = 'movies per genre in %', autopct ='%1.1f%%',figsize = (10,10))


# In[19]:


genres_count.plot.barh(title = 'Movies per Genre', color = 'DarkBlue', figsize = (10,9))


# In[20]:


#we can answer by percentages of whole data set or the count of movies in each genre


# based on this we know that the most common movies are Drama, which take up 17.6% of the data set and have a count of 4672 movies.
# The least common genre of movies are westerns which take up .06% of the dataset and count for a total of 163 movies

# In[21]:


#which genres have a high avg. budget and revenue


# In[22]:


genres_avg = movies_genre.groupby('genres_split').mean()
pd.options.display.float_format = '{:2f}'.format


# In[23]:


genres_avg


# In[24]:


genres_avg.sort_values('budget', ascending = True, inplace = True)


# In[25]:


genres_avg[['budget', 'revenue']].plot.barh(title = 'Budget, Revenue by Genre', color = ('DarkBlue', 'c'),figsize = (10,9)) 


# In[ ]:





# In[26]:


#Which genres have the highest abverage profit 


# In[27]:


genres_avg


# In[28]:


genres_avg.sort_values('profit', ascending = True, inplace = True)


# In[29]:


genres_avg[['profit']].plot.barh(title = 'Profit by Genre', color = ('g'),figsize = (10,9)) 


# In[30]:


#which genres have high avg. popularity?
genres_avg


# In[31]:


movies.head()


# In[32]:


genres_avg.sort_values('popularity', ascending = True, inplace = True)


# In[33]:


genres_avg['popularity'].plot.barh(title = 'Average Popularity by Genre', color = ('m'),figsize = (10,9)) 


# In[34]:


#which genres have highest number of movies with a voting average >= 8?


# In[35]:


movies_genre.head()


# In[36]:


vote_fifty = movies_genre[(movies_genre['vote_count'] >= 50) & (movies_genre['vote_average'] >= 8)]
vote_zero = movies_genre[movies_genre['vote_average'] >= 8]


# In[42]:


genres_vote_zero = pd.DataFrame(vote_zero.groupby('genres_split').vote_average.nunique()).sort_values('vote_average' , ascending= True)


# In[43]:


genres_vote_zero


# In[44]:


genres_vote_zero['vote_average'].plot.barh(title = 'Vote Average by Genre W/ any number of votes', color = ('DarkBlue'),figsize = (10,9)) 


# In[45]:


genres_vote_fifty = pd.DataFrame(vote_fifty.groupby('genres_split').vote_average.nunique()).sort_values('vote_average' , ascending= True)
genres_vote_fifty


# In[46]:


genres_vote_fifty['vote_average'].plot.barh(title = 'Vote Average by Genre W/ any number of votes', color = ('DarkBlue'),figsize = (10,9)) 


# In[ ]:


#The best movies according to voting average return high profit and revenue.
#the best movies according to popularity return high profit and revenue.
#Highly budgeted movies return high revenue and profit.
#Highly budgeted movies have a high popularity.


# In[48]:


#no longer need the genres_split column so circling back to reuse dataframes and repurpose them
#now only have 1 title per row and is more usable for the questions above

#will now be solving for best according to voting average and profit and revenue

movies.drop_duplicates(inplace = True)
movies['profit'] = movies['revenue'] - movies['budget']
movies_genre = movies[['popularity', 'budget', 'revenue', 'original_title', 'runtime', 'genres', 'release_date', 'director', 'vote_count', 'vote_average', 'profit']]


# In[50]:


movies_genre.head()


# In[52]:


#the best movies according to the voting average return high profit and revenue?

movies_counted = movies_genre[(movies_genre['vote_count'] >= 50)]

movies_counted.corr(method = 'spearman')
#spearmen will account for outliers better


# based on this graph there is a slight positive correlation between vote average and profit as well as a slight correlation between revenue and vote average

# In[55]:


sns.regplot(x = 'vote_average', y = 'profit', data = movies_counted, line_kws = {'color':'red'})


# In[56]:


sns.regplot(x = 'vote_average', y = 'revenue', data = movies_counted, line_kws = {'color':'red'})


# In[57]:


#will now be solving for best movie from popularity and revenue and profit

movies_counted.corr(method = 'spearman')


# In[ ]:


#shows a correlation of 0.588 for popularity to budget(moderate to strong) 
#and a correlation of 0.498 for popularity to profit(moderate)


# In[64]:


sns.regplot(x = 'popularity', y = 'revenue', data = movies_counted, line_kws = {'color':'red'})
plt.figure(figsize = (20, 20))
plt.show()


#showcases fairly accurate correlation but as the popularity goes up,
#the regression becomes less accurate and creates a wider range of expected values


# In[65]:


sns.regplot(x = 'popularity', y = 'profit', data = movies_counted, line_kws = {'color':'red'})
plt.figure(figsize = (20, 20))
plt.show()

#similar results to the popularity to revenue


# In[66]:


#starting to solve for highly budgeted movies return high profit?

movies_counted.head()


# In[68]:


sns.regplot(x = 'budget', y = 'profit', data = movies_counted, line_kws = {'color':'red'})
plt.figure(figsize = (20, 20))
plt.show()


# In[70]:


#solve for high budget to popularity?

sns.regplot(x = 'budget', y = 'popularity', data = movies_counted, line_kws = {'color':'red'})
plt.figure(figsize = (10, 5))
plt.show()


# In[ ]:


#take a look at genre profit each year


# In[71]:


movies_genre.head()


# In[104]:


movies_genre = movies[['popularity', 'budget', 'revenue', 'original_title', 'runtime', 'genres', 'release_year', 'director', 'vote_count', 'vote_average', 'profit']]
#rename release_datge column to release year

split = movies_genre['genres'].str.split('|').apply(Series, 1).stack()
split.index = split.index.droplevel(-1)
split

split.name = 'genres_split'
del movies_genre['genres']
movies_genre = movies_genre.join(split)

#reused code to split genres


# In[105]:


movies_genre.head()


# In[106]:


time_genre = pd.DataFrame(movies_genre.groupby(['release_year', 'genres_split'])['profit'].mean())


# In[107]:


time_genre


# In[108]:


final_genre = pd.pivot_table(time_genre, values = 'profit', index = ['genres_split'], columns = ['release_year'])
final_genre


# In[109]:


sns.set(rc = {'figure.figsize':(15,10)})
sns.heatmap(final_genre, cmap = 'YlGnBu', linewidths = .5)
plt.title('Genres by Profit per Year')


# In[ ]:





# In[ ]:





# In[41]:



####
RESEARCH QUESTIONS:
which genres are the most common(Number of moves made)?
get_ipython().set_next_input('Which genres have high average budget and revenue');get_ipython().run_line_magic('pinfo', 'revenue')
get_ipython().set_next_input('Which genres have a high average profit');get_ipython().run_line_magic('pinfo', 'profit')
get_ipython().set_next_input('which genres have high average popularity');get_ipython().run_line_magic('pinfo', 'popularity')
Which genres have the highest number of movies with a voting average >= 8?
get_ipython().set_next_input('Who are the most successful directors based on numerous statistics');get_ipython().run_line_magic('pinfo', 'statistics')

