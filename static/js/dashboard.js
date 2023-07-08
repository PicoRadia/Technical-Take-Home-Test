$("#inpt_search").on('focus', function () {
	$(this).parent('label').addClass('active');
});

$("#inpt_search").on('blur', function () {
	if($(this).val().length == 0)
		$(this).parent('label').removeClass('active');
});

var animateButton = function(e) {

  e.preventDefault;
  //reset animation
  e.target.classList.remove('animate');

  e.target.classList.add('animate');
  setTimeout(function(){
    e.target.classList.remove('animate');
  },700);
};

var bubblyButtons = document.getElementsByClassName("bubbly-button");

for (var i = 0; i < bubblyButtons.length; i++) {
  bubblyButtons[i].addEventListener('click', animateButton, false);
}

// Function to handle address search suggestions
function handleAddressSearch(event) {
  const input = event.target;
  const query = input.value;

  if (query.length > 0) {
    fetch(`/address-suggestions?query=${query}`)
      .then(response => response.json())
      .then(data => {
        const suggestions = data.suggestions;
        const suggestionsElement = document.getElementById('suggestions');

        if (suggestions.length > 0) {
          suggestionsElement.innerHTML = '';
          suggestions.forEach(suggestion => {
            const p = document.createElement('p');
            p.textContent = suggestion;
            suggestionsElement.appendChild(p);
          });

          suggestionsElement.style.display = 'block';
        } else {
          suggestionsElement.style.display = 'none';
        }
      });
  } else {
    document.getElementById('suggestions').style.display = 'none';
  }
}

// Function to populate input field with selected suggestion
function selectSuggestion(event) {
  const suggestion = event.target.textContent;
  document.getElementById('inpt_search').value = suggestion;
  document.getElementById('suggestions').style.display = 'none';
}

// Attach event listeners
document.getElementById('inpt_search').addEventListener('input', handleAddressSearch);
document.getElementById('suggestions').addEventListener('click', selectSuggestion);




// dashboard.js
$(document).ready(function() {
    $('#desc').addClass('fade-in');
    $('#address-form').on('submit', function(event) {
        event.preventDefault();
        var address = $('#inpt_search').val();
        console.log('Address:', address);
        // You can send the address to the Flask backend and handle the API call here
        // using AJAX or by submitting the form to the appropriate Flask route
    });
});

