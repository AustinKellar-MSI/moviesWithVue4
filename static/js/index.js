const None = undefined;

var enumerate = function(arr) { 
    var k=0; return arr.map(function(e) {
        e._idx = k++;
    });
};

var processMovies = function() {
    enumerate(app.movies);
};

var onPageLoad = function() {
    $.getJSON(get_movies_url,
        function(response) {
            app.movies = response.movies;
            processMovies();
        }
    );
};

var insertMovie = function() {
    var newMovie = {
        title: app.newMovieTitle,
        description: app.newMovieDescription,
        rating: app.newMovieRating
    };
    $.post(insert_movie_url, newMovie, function(response) { 
        newMovie['id'] = response.new_movie_id;
        newMovie['thumb'] = null; // the new movie should not have a thumb value yet!
        newMovie['like_count'] = 0; // the like count starts at 0
        app.movies.push(newMovie);
        processMovies(); // ned to re-index the movies now that a new one has been added to thea array
    });
};

var handleThumbClick = function(movieIdx, newThumbState) {
    var jsThumbValue = newThumbState;
    var pythonThumbValue = newThumbState;
    if(app.movies[movieIdx].thumb == newThumbState) {
        jsThumbValue = null;
        pythonThumbValue = None; // this is the global variable defined at the top. None == undefined
    }

    app.movies[movieIdx].thumb = jsThumbValue; // this displays the new thumb on the screen!

    $.post(set_thumb_url, { id: app.movies[movieIdx].id, thumb_state: pythonThumbValue }, function(response) {
        // This is where we tell JS what to do when the web2py server responds. 
        // For now we don't need to do anything
    });
};

var app = new Vue({
    el: '#app',
    delimiters: ['${', '}'],
    unsafeDelimiters: ['!{', '}'],
    data: {
        newMovieTitle: "",
        newMovieDescription: "",
        newMovieRating: "",
        is_logged_in: is_logged_in,
        movies: []
    },
    methods: {
        submitMovie: insertMovie,
        clickThumb: handleThumbClick
    }
});

onPageLoad();