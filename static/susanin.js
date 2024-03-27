var poligons =[]
var markers =[]
var map ={}
async function initMap() {
    await ymaps3.ready;


    await ymaps3.ready;



          // Create a custom control class for a hint window          
    const {YMap, YMapDefaultSchemeLayer,YMapDefaultFeaturesLayer,YMapFeature,
           YMapFeatureDataSource, YMapLayer} = ymaps3;

      const { YMapDefaultMarker } = await ymaps3.import('@yandex/ymaps3-markers@0.0.1');

    map = new YMap(
        document.getElementById('map'),
        {
            location: { center: [37.561833400173775,55.723162228404405], zoom: 16 },

        },
        [
              new YMapDefaultSchemeLayer({}),
              new YMapDefaultFeaturesLayer({})
            ]
    );

     areas_data.forEach(function(item, idx){

        var color = 'rgba(0, 255, 0)';

        if (item.status == 'Новая') {
            color = 'rgba(255, 0, 0)'
        }

         if (item.status == 'Завершена') {
            color = 'rgba(0, 255, 0)'
        }

          if (item.status == 'Выполняется') {
            color = 'rgba(0, 0, 255)'
        }

        var polygonFeature = new YMapFeature({
      id: 'pl'+idx,
      geometry: {
        type: 'Polygon',
        coordinates: [
                        item.coordinates
                  ]
      },
      style: {
        stroke: [{width: 0.8, color: 'rgb(30, 144, 255)'}],fill: color
      }
      });

      console.log(item.coordinates)

      

     poligons.push(polygonFeature)
     map.addChild(polygonFeature);
     

    });


}

initMap();