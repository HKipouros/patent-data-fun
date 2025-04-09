# -*- coding: utf-8 -*-
"""
Created on Mon Mar 31 14:29:01 2025

@author: holly
"""
# This program takes an input of a list of user-supplied patent numbers of 
# interest and returns some data we can play with and visualize, such as a 
# frequency of user-supplied keywords in those patents.

#import relevant modules
import csv 
import requests
import time
from wordcloud import WordCloud
import matplotlib.pyplot as plt

# PART I
# Input your file of patents.
# This program is designed to handle csv files like those obtained from USPTO's
# public Patent File Wrapper database, which have a column 'patentNumber'
# Your input file must also have a column with this header
dataset_csv=input('Enter filepath of csv file containing patents of interest (must have patentNumber as column header):\n',)


# Define function to create list of patent numbers extracted from csv file
def csv_to_list(filename):
    openfile=open(filename, 'r')
    file=csv.DictReader(openfile)
    list_patents=[]
    for col in file:
        list_patents.append(col['patentNumber'])
    return list_patents

# Make a list of patents from the input csv file
list_patents_interest=csv_to_list(dataset_csv)


# Input your .txt file of keywords
keywords_file = open(input('Enter filepath of txt file containing keywords of interest:\n'), "r") 
  
# reading the file 
data = keywords_file.read() 
  
# replacing end splitting the text when newline ('\n') is seen. 
keywords_list = data.split("\n") 
 
keywords_file.close()

# Now we use the PatentsView API to scrape the detailed description for each
# patent in the list. Currently works for 2023-2024 patents

# Define the API endpoint
api_url = 'https://search.patentsview.org/api/v1/g_detail_desc_text'

# Define the API key
api_key = input('Enter your PatentsView API key:\n')

# Define the headers
headers = {
    'X-Api-Key': api_key
}


# Define a function to get detailed description data for a desired patent
def get_detd(patent_id):
    params = {
        'q': f'{{"patent_id": "{patent_id}"}}', 
        's': '[{"patent_id": "asc" }]',
        'f': '["patent_id", "description_text"]',
        'o': '{ "size": 100, "pad_patent_id": false }'
    }

    # Make the GET request
    response = requests.get(api_url, headers=headers, params=params)

    # Check if the request was successful
    if response.status_code == 200:
        data = response.json()
        try:
            biglist=data.get("g_detail_desc_texts")
            datadic=biglist[0]
            detd_text=datadic.get("description_text")
            return detd_text
        except:
            print(patent_id, "error reading the json")
    else:
        print(patent_id, "error could not be added to dictionary")


# Define function to check if ANY keyword is in det. desc. of patent
def fun_check_patent(patent_num):
   patent_text=get_detd(patent_num)
   res=any(elem in patent_text for elem in keywords_list)
   return res


# Create a list of patents containing keywords in det. desc.
list_patents_keyword=[]
itvar=0 
counter=0

# Check each patent from your file. This can take several minutes as a pause is
# built in every 40 checks so as not to exceed the API rate
print("Scraping patent detailed description data...")
for patent in list_patents_interest:
    try:
        if fun_check_patent(patent)==True:
            list_patents_keyword.append(patent)
    except:
            print("error checking patent:", patent)
    counter=counter+1 
    itvar=itvar+1 
    if itvar==40:
        time.sleep(60)
        itvar=0

# Output a result of how many patents were entered total, and how many of these
# contained at least one keyword
print("Your data contained ",len(list_patents_interest)," total patents. Of these, ",len(list_patents_keyword),"contained one or more keywords in the Detailed Description.")
  

# Ask if user wants a results file
file_ask=input('Would you like to create a file of patents containing keywords? Y or N:\n')

# Define a function to write list to csv file
def write_to_csv(your_list):
    with open(file_path, 'w') as csvfile:
        for domain in your_list:
            csvfile.write(domain + '\n')
            
if file_ask=='Y':
    file_path = input("Enter a filepath to write results:\n")
    write_to_csv(list_patents_keyword)
    print("Complete! A list of patents containing one or more of the keywords was written to:", file_path)

# PART II
# Now let's scrape some more data from the keywords patents

# Use the PatentsView API to get assignee and country for each keyword patent

# Define the API endpoint
api_url = 'https://search.patentsview.org/api/v1/patent'

#define the headers
headers = {
    'X-Api-Key': api_key
}


#Define a function to get assignee data for a desired patent
def get_assignee(patent_id):
    params = {
        'q': f'{{"patent_id": "{patent_id}"}}', 
        's': '[{"patent_id": "asc" }]',
        'f': '["assignees.assignee_organization"]',
        'o': '{ "size": 100, "pad_patent_id": false }'
    }
    response = requests.get(api_url, headers=headers, params=params)

    # Check if the request was successful
    if response.status_code == 200: 
       data = response.json()
       assignee_name=data['patents'][0]['assignees']
       for item in assignee_name:
           for key,value in item.items():
               return value
       
    else:
        print(patent_id, "API request error")



#Generate a list of every assignee company for the keywords-containing patents 
assignee_list= list()
#For some patents, there is no assigne company listed as an individual owns the patent
patents_with_individual_as_assignee=list()

#Iterate through your list, adding a pause every so often so as not to exceed
# API rate limits
print("Scraping assignee and location country data...")
for elem in list_patents_keyword:
    itvar=itvar+1 
    if itvar==40:
        time.sleep(60)
        itvar=0
    try: 
        name=get_assignee(elem)
        assignee_list.append(name)
    except:
        patents_with_individual_as_assignee.append(elem)                 
  

#Make a histogram of assignee:count across list of keywords-containing patents
dic_count={}
for assignee in assignee_list:
    dic_count[assignee]=dic_count.get(assignee, 0) + 1


#Find the most common assignee
big_count=None
big_assignee=None
for key, value in dic_count.items():
    if big_count==None or value>big_count:
        big_count=value
        big_assignee=key


#Define a function to get assignee country for a desired patent
def get_assignee_country(patent_id):
    params = {
        'q': f'{{"patent_id": "{patent_id}"}}', 
        's': '[{"patent_id": "asc" }]',
        'f': '["assignees.assignee_country"]',
        'o': '{ "size": 100, "pad_patent_id": false }'
    }
    response = requests.get(api_url, headers=headers, params=params)

    # Check if the request was successful
    if response.status_code == 200: 
       data = response.json()
       assignee_country=data['patents'][0]['assignees'][0]['assignee_country']
       return assignee_country
    else:
        print(patent_id, "API request error")


#Generate a list of every assignee company for the patents in your list 
assignee_country_list= list()
#For some patents, there is no assigne company listed as an individual owns the patent
patents_with_individual_as_assignee_country=list()

#Iterate through your list, adding a pause every so often so as not to exceed
# API rate limits
for elem in list_patents_keyword:
    itvar=itvar+1 
    if itvar==40:
        time.sleep(60)
        itvar=0
    try: 
        name=get_assignee_country(elem)
        assignee_country_list.append(name)
    except:
        patents_with_individual_as_assignee_country.append(elem)                 


#Make a histogram of assignee:count across entire list of patents
dic_count_country={}
for country in assignee_country_list:
    dic_count_country[country]=dic_count_country.get(country, 0) + 1


#Find the country with highest count
big_count_country=None
big_country=None
for key, value in dic_count_country.items():
    if big_count_country==None or value>big_count_country:
        big_count_country=value
        big_country=key

#Generate the output statement and write result files
print("For the",len(list_patents_keyword),"patents containing the entered keywords, the most common assignee company was", big_assignee, "with", big_count, "instances. The most common country was", big_country, "with", big_count_country, "instances")

#Ask if user would like a word cloud of assignees
word_ask=input('Would you like to generate word cloud visuals of the most common assignees and countries? Y or N:\n')

if word_ask=='Y':
    wordcloud=WordCloud(width=900,height=500,max_words=1628,relative_scaling=1,normalize_plurals=False).generate_from_frequencies(dic_count)
    plt.imshow(wordcloud, interpolation='bilinear')
    plt.axis("off")
    plt.show()  
    wordcloud=WordCloud(width=900,height=500,max_words=10,relative_scaling=0.7,normalize_plurals=False).generate_from_frequencies(dic_count_country)
    plt.imshow(wordcloud, interpolation='bilinear')
    plt.axis("off")
    plt.show()  
print("Complete! Thank you for using my program!")




