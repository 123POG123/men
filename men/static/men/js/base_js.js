//Get the button
let mybutton = document.getElementById("btn-back-to-top");

// When the user scrolls down 20px from the top of the document, show the button
window.onscroll = function () {
    scrollFunction();
};

function scrollFunction() {
    if (
        document.body.scrollTop > 30 ||
        document.documentElement.scrollTop > 30
    ) {
        mybutton.style.display = "block";
    } else {
        mybutton.style.display = "none";
    }
}

// When the user clicks on the button, scroll to the top of the document
mybutton.addEventListener("click", backToTop);

function backToTop() {
    document.body.scrollTop = 0;
    document.documentElement.scrollTop = 0;
}

(function ($, global) {
    'use strict';
    $(global).resize(function () {
        if (global.screen.width > 1025) {
            $('.row-flex').removeClass('g-3').addClass('g-5');
        }
    });
}(jQuery, window));

var tooltipList1 = [].slice.call(document.querySelectorAll('[data-bs-toggle = "tooltip"]'))
var tooltipList2 = tooltipList1.map(function (tooltipTriggerfun) {
    return new bootstrap.Tooltip(tooltipTriggerfun)
})

// add image before save view

$(document).ready(function () {
    var readURL = function (input) {
        if (input.files && input.files[0]) {
            var reader = new FileReader();

            reader.onload = function (e) {
                $('.avatar').attr('src', e.target.result);
            }

            reader.readAsDataURL(input.files[0]);
        }
    }
    $(".file-upload").on('change', function () {
        readURL(this);
    });
});