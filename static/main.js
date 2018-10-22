'use strict';

var lastWindow = null;

function initAutocomplete() {
  let myLatLng = {lat: 37.774929, lng: -122.419418};

  // Create a map object and specify the DOM element for display.
  let map = new google.maps.Map(document.getElementById('map'), {
      center: myLatLng,
      scrollwheel: false,
      zoom: 12,
      zoomControl: true,
      panControl: false,
      streetViewControl: false
  });

  // Create the search box and link it to the UI element.
  var input = document.getElementById('pac-input');
  var searchBox = new google.maps.places.SearchBox(input);

  // Bias the SearchBox results towards current map's viewport.
  map.addListener('bounds_changed', function() {
    searchBox.setBounds(map.getBounds());
  });

  // Create markers for each place.
  // For each place, get the icon, name and location.
  var bounds = new google.maps.LatLngBounds();
  var places = $('.places');

  for (let i = 0; i < places.length; i++) {
    var address = places[i].innerText;

    var infowindow = new google.maps.InfoWindow({
      content: `${address}`
    });

    var geocoder = new google.maps.Geocoder();

    codeAddress(address, geocoder, map, infowindow, bounds);

    // map.fitBounds(bounds);
  }
}

function codeAddress(place, geocoder, map, infowindow, bounds) {
    var address = place;
    geocoder.geocode( { 'address': address }, function(results, status) {
      if (status == 'OK') {
        map.setCenter(results[0].geometry.location);
        var marker = new google.maps.Marker({
            map: map,
            position: results[0].geometry.location
        });

        // bounds.extend(marker.position);

        marker.addListener('click', function() {
          if (lastWindow) { 
            lastWindow.close();
          }
          infowindow.open(map, marker);
          lastWindow = infowindow;
        });

      } else {
        alert('Geocode was not successful for the following reason: ' + status);
      }
  });
}








