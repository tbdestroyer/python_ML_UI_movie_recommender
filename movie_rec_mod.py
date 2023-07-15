"""INST326 Final Project

Project Team:
    Taner Bulbul
    Caleb Andree
    Ethan Klondar 

Movie recommendation system.
References:
https://techvidvan.com/tutorials/movie-recommendation-system-python-machine-learning/
https://www.kaggle.com/datasets/tmdb/tmdb-movie-metadata
    
"""

import numpy as np
import pandas as pd
import sys
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from ast import literal_eval
import regex


def read_dataset(file1, file2):
    """Read the CSV files and load into dataframes
    
    Args:
        file1(str): csv file name with movie credits data
        file2(str): csv file name with movie information
    Returns:
        tuple: tuple of movie credits and movie info dataframes
    """ 
    # read datasets from CSV files
    credits_df = pd.read_csv(file1)
    movies_df = pd.read_csv(file2)
    
    #retrun as a tuple of dataframes
    return (credits_df, movies_df)

def get_user_list(dataset, inp):
    """Search and find matching movie titles.
    Args:
        dataset(dataframe): credits dataset
        inp(str): movie title to search for
    Returns:
        list: matching movie title
    """ 
    count = 0 # count matching movie titles
    while(True):
        title= inp
        #convert and compare everyting in lower case
        title = title.lower()
        # Search movie titles with the matching part of user input
        # if count == 0 initially, use regex pattern for partial match
        # After the first loop, use the regex pattern 
        # for matching an exact title in the movie table
        if count > 1:
            regpattern = "^"+title+"$" # after first search match exactly
        else:
            regpattern = ".*"+ title +".*"  # First search any matching part
            
        match_titles=[] # keep list of matching titles
        count = 0 # reset count every loop
        for i in dataset["title"]: # for each title in the table
            j = str.lower(i) # convert to lower case before search
            match = regex.search(regpattern, j) # search regex pattern
            if match:
                count += 1
                match_titles.append(i) # add to the list
                    
        if count >= 1:
            return match_titles # print all matching titles
        else:
            break
   
def get_user_input(dataset):
    """Prompt user for movie title.
    Args:
        dataset(dataframe): credits dataset 
    Returns:
        str: matching movie title
    """ 
    count = 0 # count matching movie titles
    while(True):
        title= input("Enter a Title or part of a Title: ")
        #convert and compare everyting in lower case
        title = title.lower()
        # Search movie titles with the matching part of user input
        # if count == 0 initially, use regex pattern for partial match
        # After the first loop, use the regex pattern 
        # for matching an exact title in the movie table
        if count > 1:
            regpattern = "^"+title+"$" # after first search match exactly
        else:
            regpattern = ".*"+ title +".*"  # First search any matching part
            
        match_titles=[] # keep list of matching titles
        count = 0 # reset count every loop
        for i in dataset["title"]: # for each title in the table
            j = str.lower(i) # convert to lower case before search
            match = regex.search(regpattern, j) # search regex pattern
            if match:
                count += 1
                match_titles.append(i) # add to the list
                
        if count == 0: # no match found
            print("\nSorry no matching title found, try again")          
        elif count > 1:
            print("\nHere are some matching Titles you can search")
            for k in match_titles: # print all matching titles
                print(k)
            print("\nEnter one of them to narrow your search")
        else: # count == 1, if we found an exact match, break out of the loop
            break
        
    #return only one match
    return match_titles[0]
                 

def get_director_name(col):
    """search a dataframe column for "Director".
    Args:
        col(list): list of dictionaries
    Returns:
        str: Director name value
    """ 
    for i in col: # for each key:value pair
        if i["job"] == "Director": # find the job key is "Director"
            return i["name"] # return the name of Director
    # if not found return not a number (nan)
    return np.nan 


def get_col_list(col, num_of_names):
    """search a dataframe column for values".
    Args:
        col(list): list of dictionaries
        num_of_names(int): limit of number of names to include in the list
    Returns:
        list: list of string values matching the key "name"
    """
    ret_list =[]
    for i in col:
        ret_list.append( i["name"]) # add the key(name) value to the list
    if len(ret_list) > num_of_names:
        ret_list = ret_list[:num_of_names] #return upto num_of_names
    
    #return list of names found
    return ret_list

def clean_data(val):
    """Clean the spaces and convert to lower case".
    Args:
        val(list or str): list or string values
    Returns:
        str: cleaned string or empty string
    """
    if isinstance(val, list): #val argument is a list
        #list expression
        return [str.lower(i.replace(" ", "")) for i in val]
    else: #val argument is a string
        if isinstance(val, str): # val is a string
            return str.lower(val.replace(" ", ""))
        else: #if val argument not a list or str type
            return ""

def create_dataset(credit, movies):
    """merge and format the two datasets (dataframes).
    Args:
        credit(dataframe): dataframe from credit CSV file
        movies(dataframe): dataframe from movies CSV file
    Returns:
        dataframe: movies dataframe with 'cast', 'keywords','director','genres'
    """ 
    
    #copy the dataset to new variables
    credits_df = credit
    movies_df = movies
    
    #movie_id column get renamed as 'id' here as well
    credits_df.columns = ['id','title','cast','crew']

    #After merge we have 23 column in movie_df dataframe. It had only 
    # 20 columns before the merge with credits_df dataframe
    movies_df = movies_df.merge(credits_df, on="id")

    # We will use the cast, crew, keywords and genres to recommend
    # a similar movie.
    # Use literal_eval function from ast package to convert data types
    # of these 4 columns into a stable format. Values in the CSV files
    # are strings but we need to convert them to dictionaries etc.
    # that is literal_eval method is doing from ast package
    cols = ["cast", "crew", "keywords", "genres"]
    for col in cols:
        movies_df[col] = movies_df[col].apply(literal_eval)

    #Get the director name from crew column by calling get_director_name
    movies_df["director"] = movies_df["crew"].apply(get_director_name)
    
    # Get a number of names from cast,keyword and genres
    # Can change num_of_names below to adjust to more or less names instead of 3
    cols = ["cast", "keywords", "genres"]
    for col in cols:
        movies_df[col] = movies_df[col].apply(get_col_list, num_of_names = 3)
    
    # title was giving key error for movies_df, don't exactly know yet
    # but assigning title from credit table to movies table again
    movies_df["title" ] = credits_df["title"]

    #Clean spaces on the cast, keyword, director and genres values
    # by calling clean_data function
    cols = ['cast', 'keywords', 'director', 'genres']
    for col in cols:
        movies_df[col] = movies_df[col].apply(clean_data)

    #return a dataframe with 'cast', 'keywords', 'director', 'genres' columns
    return movies_df

def create_soup(col):
    """merge several columns into one string
    Args:
       col(dataframe): movies dataframe with cast', 'keywords', 'director',
                      and 'genres' columns
    Returns:
        str: merged values of 'cast', 'keywords','director','genres' columns
    """ 
    return ' '.join(col['keywords']) + ' ' + ' '.join(col['cast']) + ' ' + \
col['director'] + ' ' + ' '.join(col['genres'])


def add_movies(movie_list, rec):
    """Create recommended movie objects and add to recommendations list.
    Args:
        movie_list(list): recommended list of movie_ids
        rec(Recommendation): Recommendation object
    Returns:
        int: number of recommended movies
    """ 
    # Read the movie CSV datasets and create a new dataset
    # Original datasets were manipulated before so we need new raw tables
    dataset_tuple = read_dataset("tmdb_5000_credits.csv","tmdb_5000_movies.csv" )
    raw_credits_df = dataset_tuple[0]
    raw_movies_df = dataset_tuple[1]

    #movie_id column get renamed as id here as well
    raw_credits_df.columns = ['id','title','cast','crew']

    #merge movies_df with credits_df dataframe using (id)
    raw_movies_df = raw_credits_df.merge(raw_movies_df, on="id")
    raw_movies_df['homepage'] = raw_movies_df['homepage'].fillna('Homepage not available')

    
    k = 0 # index to the movie rows
    count = 0 # matching/recommended movie count
    for i in raw_movies_df["id"]: # for every movie row in the movie table
        for j in movie_list: # for every movie id in the recommended list
            if int(j) == i: # recommended movie found in the movie table
               
               mv_id =int(j) # extract the movie id
               title = raw_movies_df["title_x"][k] # extract title
               homepage = raw_movies_df["homepage"][k] # extract homepage
               
                # literal_eval converting string to dictionary form
                # so we can get list of genre strings
               dict_genres = literal_eval(raw_movies_df["genres"][k])  
               genre_list = get_col_list(dict_genres, 3)
               
               # literal_eval converting string to dictionary form
               # so we can get list of cast strings
               dict_cast = literal_eval(raw_movies_df["cast"][k])  
               cast_list = get_col_list(dict_cast, 3)
               if cast_list == []:
                   cast_list.append('Not available')
                   
               
               # create a Movie object
               mv = Movie(mv_id,title,genre_list, cast_list, homepage)
               # add the movie object to the recommendation object list
               rec.add_recommendation(mv)
               
               count += 1
        k +=1  
    
    #return number of recommended movies
    return count
        
def get_recommendation_movie(title, num_of_recs, movies_df):
    """For a given movie title use machine learning to find recommendations.
    Args:
        title(str): movie title to search similar movies
        num_of_recs(int): number of recommendations to find
        movies_df(dataframe): dataframe from movies
    Returns:
        list: list of recommended movie ids
    """ 
    try:
        #axis =1 causes every row sent to the create_soup function
        movies_df["soup"] = movies_df.apply(create_soup, axis=1)
        #print(movies_df["soup"].head())
        
        
        #CountVectorizer counts the frequency of each word and outputs
        # a 2D vector containing frequencies.
        count_vectorizer = CountVectorizer(stop_words="english")
        count_matrix = count_vectorizer.fit_transform(movies_df["soup"])
        
        # Calculate the below formula for two vectors (arrays)
        #Similarity = (A.B) / (||A||.||B||) 
        cosine_sim = cosine_similarity(count_matrix, count_matrix)
        
        movies_df = movies_df.reset_index() #reset the data frame index
        indices = pd.Series(movies_df.index, index=movies_df['title'])
            
        #take the cosine score of given movie
        #sort them based on cosine score
        idx = indices[title]
        sim_scores = list(enumerate(cosine_sim[idx]))
        sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)
        sim_scores = sim_scores[1:num_of_recs+1]
    
        # create list of indices, using list comprehension
        movies_indices = [ind[0] for ind in sim_scores]
        
        # Get the movie ids and put in a list and return
        movie_ids = movies_df["id"].iloc[movies_indices]
        # index= false gets rid of index numbers
        movie_str = movie_ids.to_string(index=False)
        # create list from the strings separated by new lines
        movie_id_list = movie_str.split('\n')
        
        # return list of recommended movie ids
        return movie_id_list  
    except KeyError:
        print("Sorry, search caused an error, try a diffrent title")
        sys.exit(0)
class Movie():
    """Movie object to store movie information
    
    Attributes:
        movie_id(int): unique movie identifier.
        title (str): name of the movie.
        genre(list): list of strings genre of the movie.
        cast(list): list of strings names of cast
        homepage(str): URL of movie homepage
    """   
    def __init__(self,movie_id,title,genre,cast, homepage):
        """
        Args:
            movie_id(int): unique movie identifier.
            title (str): name of the movie.
            genre(list): genre of the movie.
            cast(list): list of names of artists
            homepage(str): web Page of the movie
        """
        self.movie_id = movie_id
        self.title = title
        self.genre =genre
        self.cast = cast
        self.homepage = homepage
    
    def __repr__(self):
        """ print a Movie object
        """
        # format genre and cast as comma separated strings from list
        genre_str = ', '.join([str(elem) for elem in self.genre]) 
        cast_str = ', '.join([str(elem) for elem in self.cast])
        
        if str(self.homepage) == 'nan':
            homepage = "N/A"
        else:
            homepage = self.homepage
        return f"\nTitle: {self.title}\n" + \
                f"Genre: {genre_str}\nCast: {cast_str}\n" + \
                    f"Homepage: {homepage}"


class Recommendations():
    """List of recommended movies for the user.
    
    Attributes:
        rec_list(list): list of recommended movie objects
    """
        
    def __init__(self):
        """
        Args:
          None
        """
        self.rec_list =[] # start with empty list

    def add_recommendation(self,movie):
        """Add recommended movie info to the recommendations list
        Args:
           movie(Movie): Movie object
        """
        self.rec_list.append(movie) # add to the list


if __name__ == "__main__":
    
    #read the movie datasets from the files
    dataset_tuple = read_dataset("tmdb_5000_credits.csv","tmdb_5000_movies.csv" )
    
    #create/prepare dataset for recommendation algorithm
    # This takes a few seconds !!!!!!
    print("Creating the data set ....\n")
    movies_df = create_dataset(dataset_tuple[0], dataset_tuple[1])
    
    #ask user to enter a movie title for recommending similiar movies
    mv_info= get_user_input(dataset_tuple[0]) #prompt user for movie title
    
    print(f"\nSearching Recommended Movies like: {mv_info} ....")

    
    #run the machine learning algorithm, get 5 similar movie ids
    movie_list= get_recommendation_movie(mv_info, 5,movies_df)
    
    # cerate a Recommendation object
    rec= Recommendations()
    
    # add the recommended movies to the recommendation list
    count = add_movies(movie_list, rec)
    
    #if we found some recommendations, display to the user
    if count != 0:
        print("Here are the recommended Movies:")
        print("--------------------------------")
        for i in rec.rec_list: #print each Movie object
            print(i)
    else:
        print("Sorry we couldn't find any recommendations")
    


    