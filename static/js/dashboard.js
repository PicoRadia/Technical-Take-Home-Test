$(document).ready(function() {
    $("#inpt_search").on('focus', function () {
        $(this).parent('label').addClass('active');
    });

    $("#inpt_search").on('blur', function () {
        if ($(this).val().length == 0)
            $(this).parent('label').removeClass('active');
    });

    var animateButton = function (e) {
        e.preventDefault();
        // reset animation
        e.target.classList.remove('animate');
        e.target.classList.add('animate');
        setTimeout(function () {
            e.target.classList.remove('animate');
        }, 700);
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
                })
                .catch(error => {
                    console.error('Error occurred during address search:', error);
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
    $('#inpt_search').on('input', handleAddressSearch);
    $('#suggestions').on('click', 'p', selectSuggestion);

    // Function to handle form submission
    function handleFormSubmit(event) {
        event.preventDefault();

        const addressInput = document.getElementById('inpt_search');
        const address = addressInput.value.trim();

        console.log('Address:', address); // Log the address

        if (address.length > 0) {
            console.log('Sending API request...');

            fetch(`/utility-rate`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({ address: address })
            })
                .then(response => {
                    console.log('Received API response:', response);
                    return response.json();
                })
                .then(data => {
                    console.log('API response data:', data);

                    const resultAddressElement = document.getElementById('result-address');
                    const resultRateElement = document.getElementById('result-rate');
                    const resultContainer = document.getElementById('result-container');

                    if (data.utility_rate) {
                        resultAddressElement.textContent = `Address: ${address}`;
                        resultRateElement.textContent = `Utility Rate: ${data.utility_rate}`;
                        resultContainer.style.display = 'block';
                    } else {
                        resultContainer.style.display = 'none';
                    }
                })
                .catch(error => {
                    console.error('Error occurred during API request:', error);
                });
        } else {
            // Clear previous result and hide result container
            const resultContainer = document.getElementById('result-container');
            resultContainer.style.display = 'none';
        }
    }

    // Attach event listener to form submit
    $('#address-form').on('submit', handleFormSubmit);
    console.log('Form submit listener attached.');
    
    // Attach event listener to button click
    $('.bubbly-button').on('click', function() {
        const address = document.getElementById('inpt_search').value.trim();
        console.log('Address:', address); // Log the address
    });
    console.log('Button click listener attached.');
});
