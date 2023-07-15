"""INST326 Final Project

Project Team:
    Taner Bulbul
    Caleb Andree
    Ethan Klondar 

Movie recommendation system Graphical User Interface (GUI)
References:
Basic search and autofill
https://www.youtube.com/watch?v=0CXQ3bbBLVk

"""
from tkinter import  Entry, Label,Frame, Button
from tkinter.scrolledtext import ScrolledText
import tkinter as tk

# Imprt our own module
import movie_rec_mod as pr

# A simple class to store the last movie title entered from user
class MovieTitle():
    """Keep the last movie title selected by user.
    
    Attributes:
        last_title_entered(str): last movie title entered in entry box.
    """
    def __init__(self):
        """
        Args:
          None
        """
        self.last_title_entered=""
    
    def update_title(self, last_title):
        """Update the last_title_entered
        Args:
          last_title(str): last movie title entered by user
        """
        self.last_title_entered= last_title
        
    def get_last_title(self):
        """Update the last_title_entered
        Args:
          none
        Returns:
          str: last movie title entered
        """
        return self.last_title_entered

def process_input(e):
    """Called when user types in entry box, calls the movie dataset
       for matching titles list and inserts in to the list box.
    Args:
        e(tkinter.Event): not used.
    Returns:
        none   
    """ 
    typed = text_entry.get() # get user input
    if typed == '': # if nothing in the entry, clean the entry
        text_list.delete(0, tk.END)
    
    # wait for at least 2 chracters typed before search
    if(len(typed) >= 2):
       #search the movie dataset for matching title names
       mv_info= pr.get_user_list(dataset_tuple[0],typed)
       #clear the list box and insert the new matching titles
       text_list.delete(0, tk.END)
       for i in mv_info:
           text_list.insert(tk.END,i)


def list_movies(e):
    """Called when user selects an entry in the list box, updates the
       entry text box with the selected movie title name.
    Args:
        e(tkinter.Event): not used.
    Returns:
        none   
    """ 
   
    #sel = text_list.get(tk.ACTIVE) this doesn't work with mouse clicks
    #https://stackoverflow.com/questions/15672552/tkinter-listbox-getactive-method
    #get the current list index in the entry box
    cur_selection = text_list.curselection()
    if len(cur_selection) == 0: # if list box is empty don't process anything
        return
    sel = text_list.get(cur_selection) # get the list box selection
    #print(f"selection {sel}")
    text_entry.delete(0, tk.END)
    text_entry.insert(0,sel)
    # always update the last movie title entered by user
    # so we can use for the search
    user_movie_title.update_title(sel)

def display_help():
    """Called when user selects the help button, reads the
       movie_help.txt and display help text
    Args:
        None
    Returns:
        none   
    """ 
    text.config(state = 'normal') # enable text input, read only
    # need to delete line after setting config to normal
    text.delete('1.0', tk.END) 
    # open help file
    with open('movie_help.txt') as helpfile: #open the file
        help_contents = helpfile.read() # read the file
        text.insert(tk.END,help_contents)   
    text.config(state = 'disabled')# disable text box edit
    

def start_search():
    """Called when user selects the search button, searches the
    recommended movies and updates the recommended movie list
    Args:
        None
    Returns:
        none   
    """ 
    text.config(state = 'normal') # enable text input
    # need to delete line after setting config to normal
    text.delete('1.0', tk.END)
    
    # get the last user entered movie title
    mv_info = user_movie_title.get_last_title()
    
    # Don't want to search with empty entry
    if mv_info == "":
        return
    
    #print(mv_info)
    #run the machine learning algorithm, get 10 similar movie ids
    movie_list= pr.get_recommendation_movie(mv_info, 10,movies_df)
    
    # cerate a Recommendation object
    rec= pr.Recommendations()
    
    # add the recommended movies to the recommendation list
    count = pr.add_movies(movie_list, rec)
    
    #if we found some recommendations, display to the user in the text box
    if count != 0:
        for i in rec.rec_list: #print each Movie object
            text.insert(tk.END,i) # display on text window
            text.insert(tk.END,'\n') 
    else:
        text.insert(tk.END,"Sorry we couldn't find any recommendations")
    
    text.config(state = 'disabled')# text box to read only
     
#########################################################
#  Not putting if __main__ here because this program is
#  not meant to be imported and tightly ties to
#  user interface functions above
#########################################################

# use movie_recommendation project module and read data
dataset_tuple = pr.read_dataset("tmdb_5000_credits.csv","tmdb_5000_movies.csv" )

print("Starting Movie Recommendation App.....")

# This takes a few seconds to process!!!!
movies_df = pr.create_dataset(dataset_tuple[0], dataset_tuple[1])

# create a movie title object to store last user entered title to search
user_movie_title = MovieTitle()

##########################################
# Draw the user interface and widgets
##########################################

top = tk.Tk() # create a top window
top.geometry("1000x700") # set its size
top.title('Movie Recommendation App') # add a title

# Add another user frame in the main window (top window)
# set the grid, rows and columns for the frame
uframe = Frame(top)
uframe.grid(row=0, column=0)
uframe.columnconfigure(7,weight=0)
uframe.rowconfigure(0, weight=0)


#Text entry box for user to type the movie title
text_entry=Entry(uframe,font=("Helvetica",12), width =35)
text_entry.grid(row=1, column=1)
#call process_input and process user input everytime a chracter is typed
text_entry.bind("<KeyRelease>", process_input)

# Add a label above the text entry box
text_label = Label(uframe,text="Start typing a movie title...",
        font =("Helvetica", 14), fg="grey")
text_label.grid(row=0, column=1)

# List Box for displaying list of matching movie titles as user types
# in the entry box
text_list = tk.Listbox(uframe,width=50)
text_list.grid(row=2, column=1)
# call list_movies when list box item selected by keyboard or mouse
text_list.bind("<<ListboxSelect>>",list_movies)


#add the scrolled text  box for displaying Recommended movie info
text = ScrolledText(top, heigh=30, width=110)
text.grid(row=3,column=0)

# Add a search button and call start_searchfunction when clicked
search_but = Button(uframe, text ="Search", bg='red',fg='black',\
                    width=30,command = start_search)
search_but.grid(row=1,column=5)

# Add a help button, it executes the help when clicked, calls display_help function
help_but = Button(uframe, text ="Help", bg='blue',fg='white',\
                    width=10,command = display_help)
help_but.grid(row=1,column=7)

#draw the GUI and wait for user to do something
top.mainloop()