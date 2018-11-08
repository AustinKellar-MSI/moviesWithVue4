db.define_table('movies',
                Field('title'),
                Field('description', 'text'),
                Field('rating')
                )

db.define_table('thumbs',
                Field('movie_id', 'reference_movies'),
                Field('thumb_state'),
                Field('user_email')
                )