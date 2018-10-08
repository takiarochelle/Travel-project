'use strict';

function initAutocomplete() {
    var map = new google.maps.Map(document.getElementById('map'), {
      center: {lat: 51.507351, lng: -0.127758},
      // center: getCurrentPosition();
      zoom: 13,
      mapTypeId: 'roadmap'
});


// let infoWindow = new google.maps.InfoWindow({
//     width: 150
// });
//     if (navigator.geolocation) {
//       navigator.geolocation.getCurrentPosition(function(position) {
//         const pos = {
//           lat: position.coords.latitude,
//           lng: position.coords.longitude
//         };

//         infoWindow.setPosition(pos);
//         infoWindow.setContent('You are here');
//         infoWindow.open(map);
//         map.setCenter(pos);
//       }, function() {
//         handleLocationError(true, infoWindow, map.getCenter());
//       });
//     } else {
//       // Browser doesn't support Geolocation
//       handleLocationError(false, infoWindow, map.getCenter());
//     }
// function handleLocationError(browserHasGeolocation, infoWindow, pos) {
//     infoWindow.setPosition(pos);
//     infoWindow.setContent(browserHasGeolocation ?
//                           'Error: The Geolocation service failed.' :
//                           'Error: Your browser doesn\'t support geolocation.');
//     }

// Create the search box and link it to the UI element.
var input = document.getElementById('pac-input');
var searchBox = new google.maps.places.SearchBox(input);

map.controls[google.maps.ControlPosition.TOP_LEFT].push(input);

// Bias the SearchBox results towards current map's viewport.
map.addListener('bounds_changed', function() {
  searchBox.setBounds(map.getBounds());
});

var markers = [];
// Listen for the event fired when the user selects a prediction and retrieve
// more details for that place.
searchBox.addListener('places_changed', function() {
  // var places = searchBox.getPlaces();
  var places = $('#list-of-places ol li');

  if (places.length == 0) {
    return;
  }

  // Clear out the old markers.
  // markers.forEach(function(marker) {
  //   marker.setMap(null);
  // });
  // markers = [];

  // For each place, get the icon, name and location.
  var bounds = new google.maps.LatLngBounds();
  places.forEach(function(place) {
    var place = place.text();
    if (!place.geometry) {
      console.log("Returned place contains no geometry");
      return;
    }
    var icon = {
      url: place.icon,
      size: new google.maps.Size(71, 71),
      origin: new google.maps.Point(0, 0),
      anchor: new google.maps.Point(17, 34),
      scaledSize: new google.maps.Size(25, 25)
    };

    markers.push(new google.maps.Marker({
      map: map,
      icon: icon,
      title: place.name,
      position: place.geometry.location
    }));

    if (place.geometry.viewport) {
      // Only geocodes have viewport.
      bounds.union(place.geometry.viewport);
    } else {
      bounds.extend(place.geometry.location);
    }
  });
  map.fitBounds(bounds);
});
}




