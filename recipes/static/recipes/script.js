function stateHeart(heart_icon) {
    return heart_icon.className.includes('far');
}
  
function toggleHeart(heart_icon) {
    if (heart_icon.className.includes('far')) {
        heart_icon.classList.remove('far');
        heart_icon.classList.add('fas');
        return true;
    }
    else if (heart_icon.className.includes('fas')) {
        heart_icon.classList.remove('fas');
        heart_icon.classList.add('far');
        return false;
    }
    else {
        console.log(heart_icon.attr('class'))
        return false
    }
}
 
function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

document.addEventListener('DOMContentLoaded', function() {
    document.addEventListener('click', function(event) {
        if (event.target.className.includes('fa-heart')) {
            id_heart = event.target.id;
            id_heart = id_heart.replace(/\D/g,'');

            event.target.parentElement.setAttribute('disabled', true);

            if (stateHeart(event.target)) {
                fetch('/favorite/create', {
                    headers: {
                        'Content-Type': 'application/json',
                        'X-CSRFToken': getCookie('csrftoken'),
                    },
                    mode: 'same-origin',
                    method: 'POST',
                    body: JSON.stringify({                        
                        recipe_id: id_heart
                    }),
                })
                .then(function (response) { 
                    toggleHeart(event.target);
                    event.target.parentElement.removeAttribute('disabled');
                })
                .catch(function (error) { console.log(error) })
            }
            else {
                fetch('/favorite/delete', {
                    headers: {
                        'Content-Type': 'application/json',
                        'X-CSRFToken': getCookie('csrftoken'),
                    },
                    mode: 'same-origin',
                    method: 'DELETE',
                    body: JSON.stringify({
                            recipe_id: id_heart
                    }),
                })
                .then(function (response) { 
                    toggleHeart(event.target);
                    event.target.parentElement.removeAttribute('disabled');
                })
                .catch(function (error) { console.log(error) })
            }
        }  
    })
})