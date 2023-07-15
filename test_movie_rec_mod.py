"""INST326 Final Project

Project Team:
    Taner Bulbul
    Caleb Andree
    Ethan Klondar 

Unit Tests for Movie recommendation system.
    
"""
import movie_rec_mod as proj
import pytest


def test_movie_object():
    """Movie object unit test.""" 
    # movie_id, title, genre, cast, homepage
    mv = proj.Movie(5, "Ant-Man",["Action","Adventure"], 
                    ["Paul Rudd,", "Michael Douglas"],
                    "http://marvel.com/movies/movie/180/ant-man")
                    
    
    assert mv.movie_id == 5, "Movie object Id failed"
    assert mv.title == "Ant-Man", "Movie object title failed"
    assert mv.genre == ["Action","Adventure"], "Movie object genre failed"
    assert mv.cast ==  ["Paul Rudd,", "Michael Douglas"],"Movie object cast failed"

def test_Recommendations_object():
    """Recommendation object unit test."""
    #Create a recmendations object
    rec=proj.Recommendations()
    
    #create a movie
    mv = proj.Movie(5, "Ant-Man",["Action","Adventure"], 
                    ["Paul Rudd,", "Michael Douglas"],
                    "http://marvel.com/movies/movie/180/ant-man")
    #add to Recommendation object
    rec.add_recommendation(mv)
    
    assert mv == rec.rec_list[0],"Rec object Failed"

def test_read_dataset():
    """read_dataset unit test."""
    
    t = proj.read_dataset("tmdb_5000_credits.csv","tmdb_5000_movies.csv")
    
    # check ut returns two objects in the tupe
    assert len(t) == 2, "failed to read datasets"
    
    #check each object is a data frame type
    assert isinstance(t[0], proj.pd.DataFrame) == True, "dataset is not DataFrame type"
    assert isinstance(t[1], proj.pd.DataFrame) == True, "dataset is not DataFrame type"
                      
                      
def test_get_director_name():
    """ Unit test: Extract Director name from a list of dictionary objects."""
    # part of data from crew column of movies table, list of dictionary object
    col = [{"credit_id": "52fe48009251416c750ac9c3", "department": "Directing", "gender": 2, 
         "id": 2710, "job": "Director", "name": "James Cameron"}]
    
    dir = proj.get_director_name(col) # get the director name
    
    assert dir == "James Cameron", "failed getting Director name"
    
 
def test_get_col_list():
    """Unit test: Extract names from a list of dictionary objects."""
    # part of data from cast column of movies table, list of dictionary object
    # col is a list of dictionary objects
    col = [{"cast_id": 1, "character": "James Bond", "credit_id": "52fe4d22c3a368484e1d8d6b",
            "gender": 2, "id": 8784, "name": "Daniel Craig", "order": 0}
         , {"cast_id": 14, "character": "Blofeld", "credit_id": "54805866c3a36829ab002592",
             "gender": 2, "id": 27319, "name": "Christoph Waltz", "order": 1}]
    
    mylist = proj.get_col_list(col,2) # get two names
    
    assert len(mylist) == 2, "failed getting required number column names"
    
    assert mylist[0] == "Daniel Craig", "failed getting name 1 value"
    
    assert mylist[1] == "Christoph Waltz", "failed getting name 2 value"
    

def test_clean_data():
    """clean_test unit test.""" 
    # if passed a list of string with spaces, removes spaces in strings
    val = ["word 1","word 2", "word 3"]
    ret = proj.clean_data(val)
    #check returned list doesn't have space in the strings
    assert ret == ["word1","word2", "word3"], "failed cleaning list of string with spaces"
    
    # if passed a string with spaces, removes spaces in strings
    val = "test me with spaces"
    ret = proj.clean_data(val)
    assert ret == "testmewithspaces", "failed cleaning string with spaces"
   
def test_the_rest_happy_case():
    """Rest of functions unit test with valid movie title"""
     
    dataset_tuple = proj.read_dataset("tmdb_5000_credits.csv","tmdb_5000_movies.csv" )

    #test with a movie title in the dataset
    mv_info= "Iron Man 3"
    
    #create/prepare dataset for recommendation algorithm
    movies_df = proj.create_dataset(dataset_tuple[0], dataset_tuple[1])
    
    #run the machine learning algorithm, get 3 similar movie ids
    movie_list= proj.get_recommendation_movie(mv_info, 3,movies_df)
    
    # cerate a Recommendation object
    rec= proj.Recommendations()
    
    # add the recommended movies to the recommendation lilst
    count = proj.add_movies(movie_list, rec)
    
    assert count == 3, "failed finding 3 recommended movies"


#Found the syetm exit catch code example here:
#https://stackoverflow.com/questions/62427205/in-python-3-using-pytest-how-do-we-test-for-exit-code-exit1-and-exit0-fo
    
def test_the_rest_edge_case():
    """Rest of functions with INVALID movie title"""
    
    with pytest.raises(SystemExit) as pytest_wrapped_e:
    
        dataset_tuple = proj.read_dataset("tmdb_5000_credits.csv","tmdb_5000_movies.csv" )
    
        #test with an INVALLID  movie title
        #should cause an exit of the program
        mv_info= "No such movie"
        
        #create/prepare dataset for recommendation algorithm
        movies_df = proj.create_dataset(dataset_tuple[0], dataset_tuple[1])
        
        #run the machine learning algorithm, get 3 similar movie ids
        movie_list= proj.get_recommendation_movie(mv_info, 3,movies_df)
        
        # cerate a Recommendation object
        rec= proj.Recommendations()
        
        # add the recommended movies to the recommendation lilst
        count = proj.add_movies(movie_list, rec)
        
        assert count != 3, "failed finding 3 recommended movies"
    assert pytest_wrapped_e.type == SystemExit
    assert pytest_wrapped_e.value.code == 0
    
def test_get_user_list():
    """Test user entered movie title text search """
    
    #read movies dataset file and store in dataframe
    dataset_tuple = proj.read_dataset("tmdb_5000_credits.csv",
                                      "tmdb_5000_movies.csv" )
    
    movies_df = dataset_tuple[1]

    #test with a partial movie title in the dataset
    mv_info= "Iron"
    
    match_list = proj.get_user_list(movies_df, mv_info)
    
    # all movie titles with matching to regex expression ".*Iron*."
    expected_list = ['Iron Man 3', 'Iron Man', 'Iron Man 2',
                         'The Iron Giant', 'The Man in the Iron Mask',
                         'Gridiron Gang', 'Ironclad',
                         'The Man with the Iron Fists', 'The Iron Lady']
    
 
    assert match_list == expected_list, "Didn't find matching titles with 'Iron'"