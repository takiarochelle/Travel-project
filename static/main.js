'use strict';

/*-------------------------- DELETE TRIP ----------------------------*/

function confirmTripDelete(result) {
    $(`#${result.trip_id}-trip`).remove();
}

function deleteTrip() {
    $('input[type=checkbox]').each(function() {
        if (this.checked) {
            let formData = {"trip_id": $(this).attr('id')};
            console.log(formData);
            $.post('/delete-trip.json', formData, confirmTripDelete);
        }
    });
}

$('#save-removed-trips').on('click', deleteTrip);

/*-------------------------- INSERT COMMENT -------------------------*/

var placeNameId = $('.place-form').attr('action');
var placeId = parseInt(placeNameId.split(/[/.]/)[2]);

function showComment(result) {
    $(`#${placeId}-comment-container`).html(`<ul><li style="color: black;">${result.comment}</li></ul>`);
}

function getComment(evt) {
    evt.preventDefault();
    var formData = {'place-comment': $(`#${placeId}-comment`).val()};
    $.post(`/add-comment/${placeId}.json`, formData, showComment);
}

$(`#${placeId}-button`).on('click', getComment);

/*------------------------- OPEN COLLAPSIBLE ------------------------*/

var collapse = document.getElementsByClassName("collapsible");

for (var i = 0; i < collapse.length; i++) {
  collapse[i].addEventListener("click", function() {
    this.classList.toggle("active");
    var content = this.nextElementSibling;
    if (content.style.display === "block") {
      content.style.display = "none";
    } else {
      content.style.display = "block";
    }
  });
}

/*---------------------- ADD FRIEND TO TRIP -------------------------*/

function showFriend(result) {
    $('#invited-friends').append(`<div class="travel-buddy-list" style="text-align: center;">
                                <img src=${result.profile_img} height="80" width="95">
                                <br><span>${result.full_name}</span>
                                </div>`);
}

function addFriend() {
    $('input[type=checkbox]').each(function() {
        if (this.checked) {
            let formData = {"user_id": $(this).attr('id'),
                            "trip_id": $(this).attr('name')};
            $.get('/add-friends.json', formData, showFriend);
        }
    })
}

$('#save-friends').on('click', addFriend);

/*------------------ DELETE PLACE FROM LIST -------------------------*/

function confirmDelete(result) {
    $(`#place-${result.place_id}`).remove();
}

function deletePlace() {
    $('input[type=checkbox]').each(function() {
        if (this.checked) {
            let formData = {"place_id": $(this).attr('id')};
            $.get('/delete-place.json', formData, confirmDelete);
        }
    })
}

$('#save-delete-places').on('click', deletePlace);



        