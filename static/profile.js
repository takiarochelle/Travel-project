'use strict';

function redirect() {
    window.location.assign('/add-trip');
}

function logout() {
    window.location.assign('/logout');
}

function homepage() {
    window.location.assign('/');
}

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

