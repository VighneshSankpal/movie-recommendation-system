from sklearn.metrics.pairwise import cosine_similarity
import pandas as pd
import numpy as np

tmdb_movies_info = pd.read_csv('dataset/processed/tmdb_movies_info.csv')
movieId_lookup = pd.read_csv('dataset/processed/movieId_lookup.csv')

combined_embeddings = np.load('artifact/embeddings/final_embeddings.npy')
director_embeddings = np.load('artifact/embeddings/director_embeddings.npy')
keyword_embeddings = np.load('artifact/embeddings/keyword_embeddings.npy')
genre_embeddings = np.load('artifact/embeddings/genre_embeddings.npy')
overview_embeddings = np.load('artifact/embeddings/overview_embeddings.npy')



from src.classes.content_based_movies import ContentRecommendationMovie

def get_movies_content_based(movie_idx):

    '''
    Return the top movies of it.
    '''
     
    match_score = content_based_filtering(movie_idx) # movie index of current movie

    recommended_movies_info = []
    for recommended_movie in match_score:
        rm = ContentRecommendationMovie(recommended_movie['index'],recommended_movie['overview_similarity'])
        rm.calcualte_similarities(movie_idx)

        recommended_movies_info.append(rm)
    
    return recommended_movies_info



# get movies intedex 

def content_based_filtering(movie_idx):
    '''
    apply content based filtering on given movie index and return the top similarities movies.
    input:
    movie_idx : index value of movieId_lookup table.

    return :
    top similarity movies list.
    '''
   
    # find the index of tmdb movie based on index value
    tmdb_movieId = movieId_lookup.iloc[movie_idx]['tmdb_movieId']
    
    # calculate movie similarity based on embedded text vector metrix.
    tmdb_index = tmdb_movies_info[tmdb_movies_info['movie_id'] == tmdb_movieId].index[0]
    similarities = cosine_similarity([combined_embeddings[tmdb_index]],combined_embeddings)[0]

    # sort index based on values then change the order into descending and give first 10 values index
    top_indicies = similarities.argsort()[::-1][:11]

    # # calculate score of movide matching
    top_similar_movies  = []
    for  rm in top_indicies[1:]:
        
        movie_info = {'movie_title' : tmdb_movies_info.loc[rm,'title'],'index' :rm}
        
        movie_similarity = get_similarity_explaination(tmdb_index,rm)
        
        movie_info.update(movie_similarity)
        
        top_similar_movies.append(movie_info)

        

    return top_similar_movies
    
    # for similary_tmdb_id in top_indicies:
    # for movie_title in  tmdb_movies_info.loc[top_indicies,'title']:
    #     print(movie_title)
    # return tmdb_movies_info.loc[top_indicies,'title'],match_score
    
    
   





def get_similarity_explaination(movie_idx,remm_idx):
    gen_sim = cosine_similarity(genre_embeddings[movie_idx].reshape(1,-1),genre_embeddings[remm_idx].reshape(1,-1))[0,0]

    overview_sim = cosine_similarity(overview_embeddings[movie_idx].reshape(1,-1),overview_embeddings[remm_idx].reshape(1,-1))[0,0]

    keyword_sim = cosine_similarity(keyword_embeddings[movie_idx].reshape(1,-1),keyword_embeddings[remm_idx].reshape(1,-1))[0,0]

    final_score =(gen_sim*30 + overview_sim*40 + keyword_sim  *30 )
    

    return {
            'genre_similarity' : np.round(gen_sim, 2),
            "keyword_similarity": np.round(keyword_sim,2),
            "overview_similarity": np.round((overview_sim*100),2),      
            "final_score": np.round(final_score,2)
            }






#  COllaborative filtering Area::

import json
import pickle

# Import trained SVD model.
with open('artifact/svd_model.pkl','rb') as file:
    svd_model = pickle.load(file)

# user watched movies data
with open('dataset/processed/userWatched_movies.json','r') as file:
    userWatched_movies = json.load(file)
userWatched_movies = pd.Series(userWatched_movies)



def collaborative_based_filtering(user_id):
    '''
    apply collaborative based filtering on given movie index and return the top similarities movies.
    input:
    user_id : moviesLens rating user_id which we want to recommand movies.

    return :
    top similarity movies list.
    ''' 

     # find the index of movielens movie based on index value
    # get all movies which exist in dataset.
    all_movies = set(movieId_lookup['movieLens_movieId'].tolist())
    
    movies_watched = set(userWatched_movies[str(user_id)])
    
    
    if not type(movies_watched) == set:
        movie_watched = set(movie_watched)
        
    unwatched_movies = all_movies - movies_watched

    
    predictions = []
    # calculate the prediction rating for user U for unwatched movie uM
    for movie in unwatched_movies:
        pred_rating = svd_model.predict(user_id,movie).est
        predictions.append([movie,pred_rating])
       
    
    # sort the predicted rating by highly rated movie prediction
    predictions.sort(key=lambda x : x[1],reverse=True)


    
    movie_lookup = dict(zip(movieId_lookup['movieLens_movieId'],movieId_lookup['title_clean']))
    
    top_predictions = []
    for movieId, rating in predictions[:12]:
        #conver prediction movies into diction object
        rm_dict =  {
            "title": movie_lookup[movieId],
            "predicted_rating": np.round(rating,2),
            'movieId' :movieId

            }

        # append rm object into list
        top_predictions.append(rm_dict)

    return top_predictions    

    


#  Test Content Based filters

# if __name__ == '__main__':
#     movie_idx = 76
#     recommended_movies_info =get_movies_content_based(movie_idx)

#     for rmc in recommended_movies_info:
#         print(f'Movie Title is : {rmc.movie_title}')
#         print(f'Movie matching_keywords is : {rmc.matching_keywords}')
#         print(f'Movie matching_gernes is : {rmc.matching_gernes}')
#         print(f'Movie overview_similarity is : {rmc.overview_similarity}')
#         print(f'Movie matching_director is : {rmc.matching_director}')
#         print('-'*25)




#  Test Collaborative Based filters  

if __name__ == '__main__':
    print('Collaborative Filtering result : ')
    result = collaborative_based_filtering(user_id=4019)
    for rm in result:
        print(f'Title : {rm['title']}, rating : {rm['predicted_rating']}, movieId is {rm['movieId']}')