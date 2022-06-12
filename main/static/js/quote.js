let url = 'https://api.quotable.io/random?minLength=90&maxLength=100';

fetch(url)
    .then(res => res.json())
    .then(data => {
        $('#quote-content').text(`"${data.content}"`);
        $('#quote-author').text(data.author);
    })
    .catch(err => {
        // Fall-back quote if somehow the API fails
        quoteContent = '"The free man is he who does not fear to go to the end of his thought."';
        quoteAuthor = 'Léon Blum';
        $('#quote-content').text(quoteContent);
        $('#quote-author').text(quoteAuthor);
    });

