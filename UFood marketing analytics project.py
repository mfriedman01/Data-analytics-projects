#!/usr/bin/env python
# coding: utf-8

# UFood Data Analyst Case
# 
# 
# UFood is the lead food delivery app in Brazil, present in over a thousand cities.
# 
# 
# Keeping a high customer engagement is key for growing and consolidating the company’s position as the market leader.
# 
# 
# Data Analysts working within the data team are constantly challenged to provide insights and value to the company through open scope projects. This case intends to simulate that.
# 
# In this case, you are presented a sample dataset, that mocks metainformation on the customer and on UFood campaign interactions with that customer.
# 
# It is your challenge to understand the data, find business opportunities & insights and to propose any data driven action to optimize the campaigns results & generate value to the company.
# 
# You should consider that you have to present your results to both technical and business stakeholders.
# 
# 
# Key Objectives are:
# 
# 1. Explore the data – don’t just plot means and counts. Provide insights, define cause and effect. Provide a better understanding of the characteristic features of respondents;
# 
# 2. Propose and describe a customer segmentation based on customers behaviors;
# 
# 3. Visualize data and provide written reasoning behind discoveries;
# 
# 
# The Company
# 
# Consider a well-established company operating in the retail food sector. Presently they have around several hundred thousands of registered customers and serve almost one million consumers a year. They sell products from 5 major categories: wines, rare meat products, exotic fruits, specially prepared fish and sweet products. These can further be divided into gold and regular products. The customers can order and acquire products through 3 sales channels: physical stores, catalogs and company’s website. Globally, the company had solid revenues and a healthy bottom line in the past 3 years, but the profit growth perspectives for the next 3 years are not promising... For this reason, several strategic initiatives are being considered to invert this situation. One is to improve the performance of marketing activities, with a special focus on marketing campaigns.
# 
# The Marketing Department The marketing department was pressured to spend its annual budget more wisely. Desirably, the success of these activities will prove the value of the approach and convince the more skeptical within the company.

# In[1]:


import pandas as pd

food = pd.read_csv(r'/Users/mfriedman130/Desktop/data analytics practice/u_food_marketing.csv' )
food.head()


# In[2]:


pd.set_option('display.max.columns', 50)
pd.set_option('display.max.rows', 2300)


# In[3]:


food


# In[4]:


food.info()


# In[5]:


food[food.duplicated()].count()


# In[6]:


food.drop_duplicates(keep = False, inplace = True)


# In[7]:


food.info()
#now got rid of over nearly 200 entries that were duplicates
#notice how we also have no nulls in the data and it is all integers
#very little cleaning needed to be done since no null values and duplicatesd dealt with 


# In[8]:


#combine teenhome and kidhome column to create a column for just minors at home

food['Total_children'] = food[['Kidhome', 'Teenhome']].sum(axis = 1)
food.head()


# In[9]:


#replace values of marital columns so each value has unique value and not just 1 so we can combine to create
#1 marital column which unique values for each different status

food['marital_Divorced'] = food['marital_Divorced'].replace({1:5,0:0})
food['marital_Married'] = food['marital_Married'].replace({1:4,0:0})
food['marital_Single'] = food['marital_Single'].replace({1:3,0:0})
food['marital_Together'] = food['marital_Together'].replace({1:2,0:0})
food['marital_Widow'] = food['marital_Widow'].replace({1:1,0:0})



food.head()


# In[10]:


food['Marital_Status'] = food[['marital_Divorced', 'marital_Married', 'marital_Single', 'marital_Together', 'marital_Widow']].sum(axis = 1)
food.head(20)


# In[11]:


#add a column to signify what marital status with a string 

food['Marital_Status_str'] = food['Marital_Status'].map({5: 'Divorced', 4: 'Married', 3:'Single', 2:'Together', 1: 'Widow'})


# In[12]:


food.head(20)


# In[13]:


#now we are doing the same thing and creating a single column for education level and column for the string

food['education_2n Cycle'] = food['education_2n Cycle'].replace({1:1,0:0})
food['education_Basic'] = food['education_Basic'].replace({1:2,0:0})
food['education_Graduation'] = food['education_Graduation'].replace({1:3,0:0})
food['education_Master'] = food['education_Master'].replace({1:4,0:0})
food['education_PhD'] = food['education_PhD'].replace({1:5,0:0})

food['Education_Status'] = food[['education_2n Cycle', 'education_Basic', 'education_Graduation', 'education_Master', 'education_PhD']].sum(axis = 1)

food['Educational_Status_str'] = food['Education_Status'].map({5: 'PhD', 4: 'Master', 3:'Graduation', 2:'Basic', 1: '2n Cycle'})

food.head(20)


# In[14]:


#not creating unique numbers for each campaign accepted b/c the customer could accept multiple
#the previous operations on combining columns was done so the customer can only have one value, but this one adds up

food['Accepted_Campaigns'] = food[['AcceptedCmp1', 'AcceptedCmp2', 'AcceptedCmp3', 'AcceptedCmp4', 'AcceptedCmp5', 'Response']].sum(axis = 1)

food['Accepted_Campaigns']  = (food['Accepted_Campaigns'] != 0).astype(int)
#what this is doing is converting is converting it so that if a customer accepted any campaign the value will be 1
#and if not the value will be 0


# In[15]:


food[food['Accepted_Campaigns'] != 0].head()


# In[16]:


food.corr(method = 'pearson')['Accepted_Campaigns'].sort_values(ascending = False)


# In[17]:


import seaborn as sns

sns.heatmap(food.corr(method = 'pearson'))

#too many columns for this heat map to be meaningful


# In[18]:


all_corr =  food.corr(method = 'pearson')
all_corr = all_corr[(all_corr > 0.3) & (all_corr < 1)]

sns.heatmap(all_corr.corr(method = 'pearson'))

#at the moment were focusing on accepted_campaigns so look at bottom row


# In[19]:


all_corr['Accepted_Campaigns']


# In[20]:


food


# In[21]:


food['Age'].sort_values()
#shows us we have ages of 24-80


# In[24]:


age_groups = [(23,30) , (31,40), (41,50), (51,60), (61,70), (71,85)]


def assign_age_group(Age):
    for age_range in age_groups:
        if age_range[0] <= Age <= age_range[1]:
              return f'{age_range[0]} {- age_range[1]}'
    return('unknown')     

food['Age_group'] = food['Age'].apply(assign_age_group)


# In[27]:


food[['Age', 'Age_group']].head()


# In[28]:


import seaborn as sns


# In[33]:


Age_order = ['23 -30' , '31 -40', '41 -50', '51 -60', '61 -70', '71 -85']

sns.pointplot(data = food, x = 'Age_group', y = 'Accepted_Campaigns', order = Age_order )

#the vertical line is the confidence interval
#the larger the confidence interval, the less confident it is that it is in the number

#in this case the larger the confidence interval the less confident we are in the correlation
# that the age group has that strong of a correlation 


# In[34]:


food['Age_group'].value_counts()

#based on the low populations in the 23-30 and 71-85 range, we know that the confidence
#interval will be large

#bigger population = more confidence


# In[35]:


counts = food['Age_group'].value_counts()


# In[42]:


percentage = counts / food.shape[0]

percent_food = percentage.reset_index()

percent_food


# In[43]:


percent_food.columns = ['age_group', 'percentage']


# In[49]:


percent_food = percent_food.sort_values('age_group')

percent_food


# In[50]:


import matplotlib.pyplot as plt

sns.barplot(x = 'age_group', y = 'percentage', data = percent_food)


plt.title('Percentage of Accepted Campaigns per Age Group')
plt.show


# In[51]:


#it appears that the majority of our campaigns are being accepted by the groups between 31
#and 70

#lets find out how much money these people are spending
#core audience for accepting campaigns right is between 31 and 70


# In[52]:


food.head()


# In[58]:


grouped_food = food.groupby('Age_group')['MntTotal'].sum().reset_index()

#we figure the smaller segments will have lower amount spent but that doesnt mean they spend 
#less per capita


# In[59]:


sns.barplot(x = 'Age_group', y = 'MntTotal', data = grouped_food)


plt.title('Amount Spent per Age Group')
plt.show


# In[61]:


acct_campaign = food[food['Accepted_Campaigns'] != 0 ]

grouped_food = acct_campaign.groupby('Age_group')['MntTotal'].sum().reset_index()


sns.barplot(x = 'Age_group', y = 'MntTotal', data = grouped_food)


plt.title('Amount Spent per Age Group by people who accept campaigns')
plt.show


# In[62]:


#it appears that 23-30 and 71-85 accept campaigns at higher rates since theyre MntTotal
#didnt decrease by that much compared to the other age groups


# In[64]:


#looking at the different type of purchases now for web purchases, store, and catalog purchases
#see which type of campaigns we should focus on 
food.head()


# In[71]:


pd.DataFrame(food[['NumWebPurchases', 'NumCatalogPurchases', 'NumStorePurchases' ]].sum(), columns = ['Sums'])


# In[72]:


sum_food = pd.DataFrame(food[['NumWebPurchases', 'NumCatalogPurchases', 'NumStorePurchases' ]].sum(), columns = ['Sums'])


# In[74]:


sum_food = sum_food.reset_index()
sum_food


# In[76]:


sum_food.rename(columns = {'index':'Purchase_type'}, inplace = True)


# In[77]:


sum_food


# In[79]:


sns.barplot(x = 'Purchase_type', y = 'Sums', data = sum_food)


# In[81]:


acct_campaign = food[food['Accepted_Campaigns'] != 0 ]



sum_food = pd.DataFrame(acct_campaign[['NumWebPurchases', 'NumCatalogPurchases', 'NumStorePurchases' ]].sum(), columns = ['Sums'])
sum_food = sum_food.reset_index()
sum_food.rename(columns = {'index':'Purchase_type'}, inplace = True)
sns.barplot(x = 'Purchase_type', y = 'Sums', data = sum_food)


# In[82]:


#it appears that catalog purchases have a higher percentage
#of customers who accepted the campaign


# In[88]:


jplot = sns.jointplot(data = food, x = 'MntTotal' , y = 'NumWebPurchases', kind = 'kde' )
jplot.plot_joint(sns.regplot, color = 'r')


# In[91]:


jplot = sns.jointplot(data = food, x = 'MntTotal' , y = 'NumCatalogPurchases', kind = 'kde' )
jplot.plot_joint(sns.regplot, color = 'r')


# In[87]:


jplot = sns.jointplot(data = food, x = 'MntTotal' , y = 'NumStorePurchases', kind = 'kde' )
jplot.plot_joint(sns.regplot, color = 'r')


# In[92]:


#2 courses of action here:

#boost the percentage of catalog customer(they are already likely to do this and can boost this strenght)

#focus on in store or web because they have more traffic(this is a weakness that could be foritified)


# In[93]:


sns.regplot(x = 'Total_children', y = 'MntTotal', data = food)
#as people have more children they are spending less


# In[94]:


sns.regplot(x = 'Total_children', y = 'Accepted_Campaigns', data = food)

#here they are either accepting it or didnt
#if they have less kids it means they are more likely to accept campaign 

#appears that people with more kids are spending less money and accepting less campaigns 
#maybe we should be focusing on larger families for campaings?


# In[95]:


sns.regplot(x = 'Education_Status', y = 'Accepted_Campaigns', data = food)

#this one doesnt have too much different but higher levels of education tend to accept more


# In[96]:


sns.regplot(x = 'Education_Status', y = 'MntTotal', data = food)

#still appears to be a similar but slight correlation between spending and education level
#education doesnt seem to be significant in segmentation 


# In[97]:


sns.countplot(x = 'Marital_Status_str', data = food)


# In[99]:


sns.regplot(x = 'Marital_Status', y = 'Accepted_Campaigns', data = food)


# In[112]:



relation_food = food.groupby('Marital_Status_str')['MntTotal'].sum().reset_index()


# In[113]:


sns.barplot(x = 'Marital_Status_str', y = 'MntTotal', data = relation_food)

#appears that 


# In[114]:



acct = food[food['Accepted_Campaigns'] != 0 ]



relation_food = acct.groupby('Marital_Status_str')['MntTotal'].sum().reset_index()

sns.barplot(x = 'Marital_Status_str', y = 'MntTotal', data = relation_food)


#the people who seem to be accepting the most campaign and spending more money is married
# single and Together


# In[115]:


#Married, Single, Together segments are spending a lot more money thatn widowers and divorcees


# In[119]:



total  = food['Marital_Status_str'].value_counts()

Accepted = food[food['Accepted_Campaigns'] == 1]['Marital_Status_str'].value_counts()


# In[120]:


percent_marital = Accepted/total *100


# In[123]:


pc_food = percent_marital.reset_index()
pc_food.columns = ['Marital_status', 'Percentage']


# In[124]:


sns.barplot(x = 'Marital_status', y ='Percentage', data = pc_food )

#we find that widows are most likely to accept campaign 


# In[ ]:





# In[ ]:





# #overall Findings
# 
# ###1. Age: 30-70 were spending more money, but less likely to accept more campaigns. They do have higher volume
# a .we can focus on this segment to get them to buy more or accept campaigns
# 
# ###2. Catalogs were more likely to accept campgaigns, but in person spend more. Reccomend a split between them all for campagins. 
# a. push a higher margin for campaigns to catalogs so perhaps --> 40% catalog, 30% web, 30% stores
# 
# ###3. The more kids you have the less campaigns they are accepting and less they are spending
# a. focus on people with no kids since they spend more and accept more campaigns
# 
# ##4. Education has no impact on campaigns or purchases, dont target any segment on groups
# 
# ###5. Marital status doesnt playa big part in campaigns accepted since percentages are similar, but Married, Single, and Together spend more money 
# 
# 
#     KEY TAKE AWAY MONEY MAKING RECOMMENDATIONS:
#     
#     
# 1. INCREASING PULL FROM CURRENT CUSTOMERS
# TARGET MIDDLE AGED, HIGH EARNERS WITH NO KIDS. TARGET THEM ON DIFFERENT PLATFORMS WITH CAMPAIGNS MOSTLY GOING TO CATALOG AND THE REST EVENLY SPLIT TO WEB AND STORES
# 
# 2. FIND NEW CUSTOMERS
# CAN ALSO TRY TO TARGET NEW CUSTOMERS TO SPEND MONEY SINCE THE DATA REFERS TO RECURRING CUSTOMERS. CAN FOCUS ON 21-30 AND 70 AND UP SINCE THERE ARE LOWER POPULATIONS COMPARED TO OTHER SEGMENTS AS THEY ACCEPT CAMPAIGNS AT HIGHER RATES. 
# 
# 

# In[ ]:




