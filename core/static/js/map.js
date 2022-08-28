var  sensores = L.layerGroup();

var mbAttr = 'Map data &copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors, Imagery © <a href="https://www.mapbox.com/">Mapbox</a>';
var mbUrl = 'https://api.mapbox.com/styles/v1/{id}/tiles/{z}/{x}/{y}?access_token=pk.eyJ1IjoibWFwYm94IiwiYSI6ImNpejY4NXVycTA2emYycXBndHRqcmZ3N3gifQ.rJcFIG214AriISLbB6B5aw';
var satellite = L.tileLayer(mbUrl, {id: 'mapbox/satellite-v9', tileSize: 512, zoomOffset: -1, attribution: mbAttr});

var streets = L.tileLayer(mbUrl, {id: 'mapbox/streets-v11', tileSize: 512, zoomOffset: -1, attribution: mbAttr});

var osm = L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
    maxZoom: 19,
    attribution: '&copy; <a href="http://www.openstreetmap.org/copyright">OpenStreetMap</a>'
});


function onEachFeature(feature, layer) {

    var popupContent = feature.properties.popup_content;
    layer.bindPopup(popupContent +
    '<a href="../json:' + feature.id + '/" onclick="window.location=json/">Visualizar Dados</a>');
}

var map = L.map('map', {
    center: [-22.756909, -43.674895],
    zoom: 18,
    layers: [satellite, sensores]
});

var mystyle = {
        fillColor: 'green',
        weight: 2,
        opacity: 1,
        color: 'black',
        fillOpacity: 0.5
    }



var infosensor_url = $("#infosensor_geojson").val();



$.getJSON(infosensor_url, function (data) {
              var geojsonMarkerOptions = {
                  radius: 8,
                  fillColor: "black",
                  color: "#000",
                  weight: 1,
                  opacity: 1,
                  fillOpacity: 0.5
              };
              L.geoJSON(data, {
                  onEachFeature: onEachFeature
              }).addTo(sensores);

          });


var baseLayers = {
    'OpenStreetMap': osm,
    'Streets': streets,
    'satellite': satellite
};

var overlays = {
    'Sensores': sensores
};

var layerControl = L.control.layers(baseLayers, overlays).addTo(map);

