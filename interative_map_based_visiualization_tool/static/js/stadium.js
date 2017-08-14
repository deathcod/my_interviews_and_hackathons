stadium = {};

function buildLocationList() {
    for (i = 0; i < stadium.features.length; i++) {
      var currentFeature = stadium.features[i];
      var prop = currentFeature.properties;

      var listings = document.getElementById('listings');
      var listing = listings.appendChild(document.createElement('div'));
      listing.className = 'item';
      listing.id = "listing-" + i;

      var link = listing.appendChild(document.createElement('a'));
      link.href = '#';
      link.className = 'title';
      link.dataPosition = i;
      link.innerHTML = prop.name;

      var details = listing.appendChild(document.createElement('div'));
      details.innerHTML = prop.city;


      link.addEventListener('click', function(e){
        // Update the currentFeature to the store associated with the clicked link
        var clickedListing = stadium.features[this.dataPosition];

        // 1. Fly to the point
        flyToStore(clickedListing);

        // 2. Close all other popups and display popup for clicked store
        createPopUp(clickedListing, "stadium");

        // 3. Highlight listing in sidebar (and remove highlight for all other listings)
        var activeItem = document.getElementsByClassName('active');

        if (activeItem[0]) {
           activeItem[0].classList.remove('active');
        }
        this.parentNode.classList.add('active');

      });
    }
}


function make_call_stadium() {

      map.addSource("stadium", {
        "type": "geojson",
        "data": stadium
      });

    buildLocationList();

    stadium.features.forEach(function(marker, i) {
    // Create an img element for the marker
    var el = document.createElement('div');
    el.id = "marker-" + i;
    el.className = 'marker';
    // Add markers to the map at all points
    new mapboxgl.Marker(el, {offset: [-28, -46]})
        .setLngLat(marker.geometry.coordinates)
        .addTo(map);

    map.on('zoom', function() {
      if (map.getZoom() > 2.9) 
      {
        $("#marker-"+i).show("slow");
      } 
      else 
      {
          $("#marker-"+i).hide("slow");
      }
    });

    el.addEventListener('click', function(e){
        // 1. Fly to the point
        flyToStore(marker);

        // 2. Close all other popups and display popup for clicked store
        createPopUp(marker, "stadium");

        // 3. Highlight listing in sidebar (and remove highlight for all other listings)
        var activeItem = document.getElementsByClassName('active');

        e.stopPropagation();
        if (activeItem[0]) {
           activeItem[0].classList.remove('active');
        }

        var listing = document.getElementById('listing-' + i);
        listing.classList.add('active');

    });
  });
}


function process_stadium(data)
{
    var data = JSON.parse(data)
    data = data["data"]
    

    var features = []
    for (var i=0; i<data.length; i++) {
        feature_element = {
            "type" : "Feature",
            "geometry" : JSON.parse(data[i]["geometry"]),
            "properties":{
                "id"        : data[i]["id"],
                "name"      : data[i]["name"],
                "image"     : data[i]["image"],
                "capacity"  : data[i]["capacity"],
                "description": data[i]["description"],
                "city"      : data[i]["city"]
            }
        }
        features.push(feature_element)
    }

    stadium["type"] = "FeatureCollection";
    stadium["features"] = features;
    make_call_stadium()
}