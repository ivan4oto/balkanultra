
// CSS
import "./main.scss"; 
// JS
import "./style_moder"
import Modal from "bootstrap/js/dist/modal"



function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

function get_data() {
    return {
        email: $('#post-mail').val(),
        phone: $('#post-phone').val(),
        first_name: $('#post-first-name').val(),
        last_name: $('#post-last-name').val(),
        gender: $('#post-gender').val(),
        first_link: $('#post-first-link').val(),
        second_link: $('#post-second-link').val(),
    }
}

const csrftoken = getCookie('csrftoken');
const PAYMENT_ENABLED = false


$('#post-form').on('submit', function(event){
    event.preventDefault();
    // create_post();
    $.ajax( {
        url: `${scheme}://${host}/register/${race}`,
        type: "POST",
        beforeSend: function(request) {
            request.setRequestHeader("X-CSRFToken", csrftoken)
            toggleLoading()
        },
        data: get_data(),
        success: [       
            function(json) {
                toggleLoading()
                showModal(json);
                console.log('Успешна регистрация');
                console.log(json)
            }
        ],
        error: function(xhr,errmsg,err) {
            $('#results').html("<div class='alert-box alert radius' data-alert>Oops! We have encountered an error: "+errmsg+
                " <a href='#' class='close'>&times;</a></div>"); // add the error to the dom
            console.log(xhr.status + ": " + xhr.responseText); // provide a bit more info about the error to the console
        }
    });
})


function toggleLoading() {
    var submitBtn = $('#submitBtn')
    var spinner = $('#spinner')
    if (submitBtn.hasClass('d-none')) {
        submitBtn.removeClass('d-none')
        spinner.addClass('d-none')
    } else {
        submitBtn.addClass('d-none')
        spinner.removeClass('d-none')
    }
}

function showModal(json) {
    if (json['mail_status'] == 'success' && json['status'] == 'success') {
        var myModal = new Modal(document.getElementById('successModal'), {
            keyboard: true
        })
    } else {
        var myModal = new Modal(document.getElementById('errorModal'), {
            keyboard: true
        })
        addErrorMsg(json)
    }
    myModal.show()
}

function addErrorMsg(json) {
    var errorMsg = json['mail_error']
    if (json['status'] == 'already exists') {
        errorMsg = 'Този email е вече регистриран, моля използвайте друг email.'
    }
    var errorMsgField = document.getElementById('errorMsgField')
    var text = document.createTextNode(`${errorMsg}`);
    errorMsgField.appendChild(text);
}