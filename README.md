# patent-data-fun
You input a list of patent numbers and a list of keywords of interest, and the program scrapes data using the PatentsView API (patentsview.org) to see how many of your patents contain at least one keyword. Then, you can generate a word cloud visual showing which companies own the most keyword-containing patents.

<img width="349" alt="Image" src="https://github.com/user-attachments/assets/aebc935b-f0fe-412c-9c49-45f642991203" />

# Inspiration
I wrote this program as a personal project to satisfy my curiosity about the rise of articifical intelligence-based patents in the field of bioreactors and cell culture. However, it is adaptable to find and visualize data on various fields of patents and various keywords. I wrote this as a Python beginner and learned a lot about using Python's ability to handle API requests and visualize results in order to have fun with data. 

# What You'll Need
## User-generated files
You'll need a list of patent numbers of interest, in the form of a csv file with your patent numbers listed under the heading patentNumber. E.g., I downloaded a list of every patent granted in the year 2023 under classification C12M (the bioreactor space) from the USPTO's publicly available patent database (data.uspto.gov/patent-file-wrapper) because I was interested in those particular patents.  You'll also need a .txt file of your list of keywords of interest. E.g., I was interested in AI-related keywords such as "machine learning", "arfiticial intelligence", "deep learning", etc. 

## API key
This program requires an PatentsView API key (free but you must request it from them at patentsview.org) to make use of their wonderfully useful APIs.
*Note:* As of 04/09/2025 "long text data" is only available in the PatentsView API for 2023 and 2024 (I tested both years when writing this program).

## Import modules
You will need the following Python modules:  csv  requests  time  wordcloud   matplotlib.pyplot



