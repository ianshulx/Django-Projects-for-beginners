document.addEventListener("DOMContentLoaded", function () {
    getLocation();
});

function getLocation() {
    if (navigator.permissions) {
        navigator.permissions.query({ name: 'geolocation' }).then(function (permissionStatus) {
            if (permissionStatus.state === 'granted' || permissionStatus.state === 'prompt') {
                navigator.geolocation.getCurrentPosition(showPosition, failedGetPosition);
            } else {
                alert('Permission to access location denied.');
            }
        });
    } else if (navigator.geolocation) {
        navigator.geolocation.getCurrentPosition(showPosition, failedGetPosition);
    } else {
        alert('Geolocation is not supported by this browser.');
    }
}

function showPosition(position) {
    const latitude = position.coords.latitude;
    const longitude = position.coords.longitude;

    var map = L.map('map').setView([latitude, longitude], 13);

    var osmLayer = L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
        maxZoom: 19,
    });

    var esriSatelliteLayer = L.tileLayer('https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{z}/{y}/{x}', {
        maxZoom: 19,

    });

    osmLayer.addTo(map);

    var homeIcon = L.icon({
        iconUrl: '{% static  ".\img\mark.jpg" %}',
        iconSize: [32, 32],
        iconAnchor: [16, 32],
        popupAnchor: [0, -32]
    });

    var marker = L.marker([latitude, longitude], {icon: homeIcon}).addTo(map);
    marker.bindPopup('Your current location').openPopup();

    var baseMaps = {
        "OpenStreetMap": osmLayer,
        "ESRI Satellite": esriSatelliteLayer
    };

    

    L.control.layers(baseMaps).addTo(map);

    const provider = new GeoSearch.OpenStreetMapProvider();

    const searchControl = new GeoSearch.GeoSearchControl({
        provider: provider,
        style: 'bar',
        showMarker: true,
        marker: {
            icon: new L.Icon.Default(),
            draggable: false,
        },
        updateMap: true
    });

    

   
    // Add the search control to the map
    map.addControl(searchControl);

    // Event listener for the search results
    map.on('geosearch/showlocation', function (result) {
        const coordinates = [result.location.y, result.location.x];
        map.setView(coordinates, 13);

        L.marker(coordinates)
            .addTo(map)
            .bindPopup(result.location.label)
            .openPopup();
    });

}

function failedGetPosition() {
    alert('Unable to retrieve your location.');
}

