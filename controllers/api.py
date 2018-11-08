def insert_movie():
    # in this funciton, we take the data that the JavaScript sent us and insert it into the database!
    new_movie_id = db.movies.insert(
        title=request.vars.title,
        description=request.vars.description,
        rating=request.vars.rating
    )
    # JavaScript needs the id of the movie that was just created so that it can pass it to the clickThumbs function
    return response.json(dict(new_movie_id=new_movie_id))

def get_all_movies():
    # if the user is not logged in, don't return any movies!
    if auth.user == None:
        return response.json(dict(movies=[]))
    else:
        movies = db(db.movies).select() # this asks the database for all entries in the movies table
        thumbs = db(db.thumbs).select() # get all thumbs from the database

        movie_list = []

        for movie in movies:
            movie_to_send = dict(
                id=movie.id,
                title=movie.title,
                description=movie.description,
                rating=movie.rating,
                like_count=0,
                thumb=None # for now, set the thumb state to None, it will possibly get reassigned later
            )

            # if there is a thumb associated with this movie, change the thumb value to it's actual state
            for thumb in thumbs:
                if thumb.movie_id == movie.id:
                    if thumb.user_email == auth.user.email:
                        movie_to_send['thumb'] = thumb.thumb_state 
                    if thumb.thumb_state == 'u':
                        movie_to_send['like_count'] += 1
                    elif thumb.thumb_state == 'd':
                        movie_to_send['like_count'] -= 1

            movie_list.append(movie_to_send)


        return response.json(dict(movies=movie_list)) # return all movies as a JSON object back to JavaScript

def set_thumb():
    db.thumbs.update_or_insert(((db.thumbs.movie_id == request.vars.id) & (db.thumbs.user_email == auth.user.email)),
        movie_id=request.vars.id,
        thumb_state=request.vars.thumb_state,
        user_email=auth.user.email
    )
    # we don't have to send back the thumb's id because our JavaScript will never need to use it
    # instead, we will just respond with a success mesage.
    return "thumb updated!"
