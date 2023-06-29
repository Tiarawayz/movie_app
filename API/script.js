$(document).ready(function() {
    function handleFormSubmit(event) {
      event.preventDefault(); 
  
      var movieTitle = $("#movieTitle").val(); 
  
      $.ajax({
        url: "http://www.omdbapi.com/",
        type: "GET",
        data: {
          apikey: "e2b6ec9a",
          t: movieTitle
        },
        success: function(response) {
          $("#genres").val(response.Genre);
          $("#year").val(response.Year);
        },
        error: function() {
          console.log("Error occurred while fetching movie data.");
        }
      });
    }
    $("#movieForm").submit(handleFormSubmit);
  });