map = L.map('map', {doubleClickZoom: false}).locate({setView: true, watch: true, maxZoom: 16});

let osm = L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'});
osm.addTo(map);

map.on('locationfound', onLocationFound);

let gpsMarker = null;
let gpsCircleMarker;

function onLocationFound(e) {
    let radius = e.accuracy / 2;
    let popupContent = "You are within " + radius + " meters from this point";

    if (gpsMarker == null) {
        gpsMarker = L.marker(e.latlng).addTo(map);
        gpsMarker.bindPopup(popupContent).openPopup();
        gpsCircleMarker = L.circle(e.latlng, radius).addTo(map);
    }
    else {
        gpsMarker.getPopup().setContent(popupContent);
        gpsMarker.setLatLng(e.latlng);
        gpsCircleMarker.setLatLng(e.latlng);
        gpsCircleMarker.setRadius(radius);
    }

    let url = '/update_location/';

    fetch(url, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': csrftoken,
        },
        body: JSON.stringify({'latitude': e.latlng.lat, 'longitude': e.latlng.lng})
    })
        .then((response) => {
            return response.json()
        })
}
