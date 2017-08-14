var country = {};
ZOOM_THRESHOLD = 3;

function fillyeardata(id, year)
{
    for (var i = 0; i < country.features.length; i++) {
        if(country.features[i].properties.year == year && country.features[i].properties.position == 1)
        {
            $("#c1").text(country.features[i].properties.name+"  (1st)")
            $("#s1").html("<b>" + country.features[i].properties.score + "</b>")
        }
        if(country.features[i].properties.year == year && country.features[i].properties.position == 2)
        {
            $("#c2").text(country.features[i].properties.name+"  (2nd)")
        }
        if(country.features[i].properties.year == year && country.features[i].properties.position == 3)
        {
            $("#c3").text(country.features[i].properties.name+"  (3rd)")
            $("#s2").html("<b>"+country.features[i].properties.score+"</b>")
        }
        if(country.features[i].properties.year == year && country.features[i].properties.position == 4)
        {
            $("#c4").text(country.features[i].properties.name+"  (4th)")
        }
        if(country.features[i].properties.year == year && country.features[i].properties.position == 5)
        {
            $("#host_country").text(country.features[i].properties.name+"  (host)")
            $("#logo").attr("src", "https:"+country.features[i].properties.logo)
        }
    }
}

function buildCountryfill(){

    //slider value
    var year = [2006, 2008, 2010, 2012, 2013, 2015, 2017]
    $("#slider").on('input', function(e){
        var cur_year = year[parseInt(e.target.value)];
        fillyeardata(parseInt(e.target.value), cur_year);
        map.setFilter('states-layer',['==','year', cur_year]);
        $('#span_slider').text(cur_year);
        map.flyTo({
            center: CENTER,
            zoom: 2.5
          });
    });

    map.on('zoom', function(){
        if(map.getZoom() > ZOOM_THRESHOLD)
            $("#slider_animate").hide("slow");
        else
            $("#slider_animate").show(100);
    });
    
    map.on('click', 'states-layer', function(e){
        temp_latlong = e.lngLat;
        index = e.features[0].properties.index;
        country.features[index]["temp_latlong"] = temp_latlong;
        createPopUp(country.features[index], "country");
    });
}

function make_call_country() {
    map.addLayer({
            'id': 'states-layer',
            'type': 'fill',
            'maxzoom': ZOOM_THRESHOLD,
            'filter': ['==', 'year', 2006],
            'source': {
                'type': 'geojson',
                'data': country
            },
           'paint': {
                'fill-color': {
                    property: 'position',
                    stops: [
                        [1, '#ff0000'],
                        [2, '#FF5733'],
                        [3, '#FFC300'],
                        [4, '#f7dc6f'],
                        [5, '#00ff08']
                    ]
                },
                'fill-opacity': 0.75
            }
        }, 'waterway-label');
    buildCountryfill();
}

function process_country(data)
{
    var data = JSON.parse(data)
    data = data["data"]
    

    var features = []
    for (var i=0; i<data.length; i++) {
        feature_element = {
            "type" : "Feature",
            "geometry" : JSON.parse(data[i]["geometry"]),
            "properties":{
                "index"         : i,
                "id"            : data[i]["id"],
                "name"          : data[i]["name"],
                "flag"          : data[i]["flag"],
                "year"          : data[i]["year"],
                "description"   : data[i]["description"],
                "position"      : data[i]["position"],
                "logo"          : data[i]["logo"],
                "score"         : data[i]["score"]
            }
        }
        features.push(feature_element)
    }
    country["type"] = "FeatureCollection"
    country["features"] = features;
    //console.log(JSON.stringify(country));
    make_call_country()
    fillyeardata(0, 2006);
}

