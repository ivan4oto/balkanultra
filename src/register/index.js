// Submit post on submit
// CSS
import "./main.scss"; 
import "./csfr_cookies";
import { checkoutRedirect } from "./checkout"

const PAYMENT_ENABLED = false

$('#post-form').on('submit', function(event){
    event.preventDefault();
    console.log("form submitted!")  // sanity check
    create_post();
});


// AJAX for posting
function create_post() {
    console.log(`${race}`)
    console.log("create post is working!") // sanity check
    $.ajax({
        url: `http://127.0.0.1:8000/register/${race}`, // the endpoint
        type: "POST", // http method
        data: get_data(), // data sent with the post request

        beforeSend: function() {
            toggleLoading()
        },

        success: [
            // checkStatus(json),            
            function(json) {
                toggleLoading()
            // If PAYMENT_ENABLED flag is on proceed to checkout
                if (PAYMENT_ENABLED) {
                    console.log("success about to redirect"); // another sanity check
                    const athleteMail = {
                        email: json["email"]
                    }
                    checkoutRedirect(athleteMail)
                
                } else {
                    // If PAYMENT_ENABLED flag is NOT on trigger modal
                    var myModal = new bootstrap.Modal(document.getElementById('successModal'), {
                        keyboard: true
                    })
                    myModal.show()
                    console.log('Успешна регистрация')
                }
            }
        ],

        error: function(xhr,errmsg,err) {
            $('#results').html("<div class='alert-box alert radius' data-alert>Oops! We have encountered an error: "+errmsg+
                " <a href='#' class='close'>&times;</a></div>"); // add the error to the dom
            console.log(xhr.status + ": " + xhr.responseText); // provide a bit more info about the error to the console
        }
    });
};


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

function checkStatus(msg){
    var status = msg['status']
    // if var status == 'already exists':
    //    trigger bootstrap modal popup/alert warning user exists

    // if var status == 'success':
    //    checkoutRedirect(msg['email']) 
    
}



// Getting Data from form
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


