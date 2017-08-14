var player = {}

function make_call_player()
{
	map.addSource("player", {
        "type": "geojson",
        "data": player
      });

	player.features.forEach(function(marker, i) {
	    // Create an img element for the marker
	    var el = document.createElement('div');
	    el.id = "marker-player-" + i;
	    el.className = 'player';
	    // Add markers to the map at all points
	    new mapboxgl.Marker(el, {offset: [-28, -46]})
	        .setLngLat(marker.geometry.coordinates)
	        .addTo(map);

	    map.on('zoom', function() {
	      if (map.getZoom() > 3.3) 
	      {
	        $("#marker-player-"+i).show("slow");
	      } 
	      else 
	      {
	          $("#marker-player-"+i).hide("slow");
	      }
	    });

	el.addEventListener('click', function(e){
        // 1. Fly to the point
        flyToStore(marker);

        // 2. Close all other popups and display popup for clicked store
        createPopUp(marker, "player");
    });
  });
}

function process_player(data)
{
    var data = JSON.parse(data)
    data = data["data"]
    

    var features = []
    for (var i=0; i<data.length; i++) {
        feature_element = {
            "type" : "Feature",
            "geometry" : JSON.parse(data[i]["geometry"]),
            "properties":{
            	"id"		: data[i]["id"],
                "name"      : data[i]["name"],
                "image"     : data[i]["image"],
                "description": data[i]["description"]
            }
        }
        features.push(feature_element)
    }

    player["type"] = "FeatureCollection";
    player["features"] = features;
    make_call_player();
    //console.log(JSON.stringify(player));
}