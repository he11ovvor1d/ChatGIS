
var map2 = new ol.Map({
  target: 'map2',
  layers: [
    new ol.layer.Tile({
      source: new ol.source.OSM()
    })
  ],
  view: new ol.View({
    center: ol.proj.fromLonLat([119,32]),
    zoom: 9
  })
});
var geoserverLayer = new ol.layer.Tile({
  source: new ol.source.TileWMS({
    url: 'http://localhost:8080/geoserver/wms',
    params: {'LAYERS': 'nj:行政区'},
    serverType: 'geoserver'
  })
});
map2.addLayer(geoserverLayer);

var select = new ol.interaction.Select({
  condition: ol.events.condition.click
});
map2.addInteraction(select);