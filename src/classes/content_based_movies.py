import pandas as pd
import numpy as np


tmdb_movies_info = pd.read_csv('dataset/processed/tmdb_movies_info.csv')



class ContentRecommendationMovie:
    '''
     Save information and find similaraties and explaination of recommendated movie
    '''
    def __init__(self,movie_idx,overview_similarity):
        '''
            Input : Index of recommendated movie object ( tmdb table index )
        '''
        self.movie_idx = movie_idx
        self.movie_id =  tmdb_movies_info.loc[movie_idx,'movie_id']
        
        self.movie_title = None
        self.matching_keywords = None
        self.matching_gernes = None
        self.matching_director = None
        self.overview_similarity = round(overview_similarity,2)
   
    def calcualte_similarities(self,recommended_tmdb_idx):
        '''
            Calcluate the similarities between current movies information and given movies.
            and store it data into data members.
        '''

        cm = tmdb_movies_info.loc[self.movie_idx]
        rm = tmdb_movies_info.loc[recommended_tmdb_idx]
       
        
        # keywords 
        cm_keys = set(cm['keywords_clean'].strip().split(', '))
        rm_keys = set(rm['keywords_clean'].strip().split(', '))
        
        matching_keywords = list(rm_keys & cm_keys )
        matching_keywords.sort()
        
        # genres
        cm_genres = set(cm['genres_clean'].strip().split(', '))
        rm_genres = set(rm['genres_clean'].strip().split(', '))
    
        matching_gernes = list(cm_genres & rm_genres)
        matching_gernes.sort()
    
        # director matching
        cm_director = cm['crew_clean'].strip().split('Director: ')[1]
        rm_director = rm['crew_clean'].strip().split('Director: ')[1]
    
        if cm_director == rm_director:
            matching_director = True
        else:
            matching_director = False
    
        
        # Movie Overview

        
        self.movie_title = cm['title']
        self.matching_keywords = matching_keywords
        self.matching_gernes   = matching_gernes
        self.matching_director = matching_director

        return {
             'title'             : self.movie_title,
             'matching_keywords' :  self.matching_keywords,
             'matching_gernes'   : self.matching_gernes,
             'matching_director' : self.matching_director,
             'overview_similarity' : self.overview_similarity
        }
    

if __name__ == '__main__':
    current_movie_idx = 0
    match_score = content_based_filtering(current_movie_idx) # movie index of current movie

    recommended_movies_info = []
    for recommended_movie in match_score:
        rm = ContentRecommendationMovie(recommended_movie['index'],recommended_movie['overview_similarity'])
        rm.calcualte_similarities(current_movie_idx)

        recommended_movies_info.append(rm)

    for rmc in recommended_movies_info:
        print(f'Movie Title is : {rmc.movie_title}')
        print(f'Movie_id is : {rmc.movie_id}')
        print(f'Movie matching_keywords is : {rmc.matching_keywords}')
        print(f'Movie matching_gernes is : {rmc.matching_gernes}')
        print(f'Movie overview_similarity is : {rmc.overview_similarity}')
        print(f'Movie matching_director is : {rmc.matching_director}')
        print('-'*25)

        