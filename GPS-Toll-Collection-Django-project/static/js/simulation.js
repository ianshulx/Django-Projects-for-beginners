    <script>
        let map, marker;
        let coordinates = [];
        let index = 0;
        let timeout;  // Changed from interval to timeout for correct usage
        let currentTimestamp = new Date();
        const coordinates_array = []; // Array to store coordinates_array
        let totalDistance = 0;  // Variable to store the total distance
        const sec_time = [];  // Array to store the time taken to reach each coordinate

        

        function initMap() {
            map = L.map('map').setView([0, 0], 2);
            L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
                attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
            }).addTo(map);
            marker = L.marker([0, 0]).addTo(map);
        }

        function addCoordinate(lat, lng, sec) {
            // Add the new coordinate to the array
            coordinates_array.push({ lat, lng });
            sec_time.push(sec);
            const time = sec_time.reduce((accumulator, currentValue) => accumulator + currentValue, 0); // Calculate the sum
            console.log(`Time: ${time} seconds`);

            // If there are at least two coordinates, calculate the distance between the last two
            if (coordinates_array.length > 1) {
                const previousCoord = coordinates_array[coordinates_array.length - 2];
                const currentCoord = coordinates_array[coordinates_array.length - 1];

                const distance = calculateDistance(previousCoord, currentCoord);
                totalDistance += distance;

                console.log(`Distance between last two points: ${distance.toFixed(2)} km`);
                console.log(`Total distance so far: ${totalDistance.toFixed(2)} km`);
            }
            const speed = (totalDistance.toFixed(2) * 3600) / time; // Calculate the speed in km/h
            const Distance_covered = totalDistance.toFixed(2);
            return { Distance_covered, speed };
        }
              
        function calculateDistance(coord1, coord2) {
            const R = 6371; // Radius of the Earth in km
            const lat1 = coord1.lat * Math.PI / 180;
            const lat2 = coord2.lat * Math.PI / 180;
            const deltaLat = (coord2.lat - coord1.lat) * Math.PI / 180;
            const deltaLng = (coord2.lng - coord1.lng) * Math.PI / 180;

            const a = Math.sin(deltaLat / 2) * Math.sin(deltaLat / 2) +
                Math.cos(lat1) * Math.cos(lat2) *
                Math.sin(deltaLng / 2) * Math.sin(deltaLng / 2);
            const c = 2 * Math.atan2(Math.sqrt(a), Math.sqrt(1 - a));

            return R * c; // Distance in km
        }


        function showNextCoordinate() {
            if (index < coordinates.length) {
                let coord = coordinates[index];
                let randomDelay = Math.floor(Math.random() * 6) + 5; // Random delay between 5 and 10 seconds
                const { Distance_covered, speed } = addCoordinate(coord.lat, coord.lng, randomDelay); // Add the coordinate and get the distance and speed
                var total_km = '{{ total_km|safe }}'
                let latLng = [coord.lat, coord.lng];

                marker.setLatLng(latLng);
                map.setView(latLng, 17);

                currentTimestamp.setSeconds(currentTimestamp.getSeconds() + randomDelay);
                const timestamp = currentTimestamp.toTimeString().split(' ')[0];
                storeCoordinate(coord.lat, coord.lng, timestamp, '{{ trip.vehicle_number}}','{{ uniq_uuid }}');

             //   <!-- storeCoordinate(coord.lat, coord.lng); -->
                index++;

                timeout = setTimeout(showNextCoordinate, randomDelay * 1000);

                console.log('Showing next coordinate in ' + randomDelay + ' seconds');
                
                console.log("total km " + total_km);
                const elements = [
                    { id: 'latitude', value: coord.lat },
                    { id: 'cun_latitude', value: coord.lat },
                    { id: 'longitude', value: coord.lng },
                    { id: 'cun_longitude', value: coord.lng },
                    { id: 'Distance_covered', value: Distance_covered },
                    { id: 'speed', value: speed.toFixed(3) },
                    { id : 'distance_left', value : (total_km - Distance_covered) }
                ];
                


                elements.forEach(({ id, value }) => {
                    document.getElementById(id).textContent = value;
                });
            }
        }

        function stopShowingCoordinates() {
            clearTimeout(timeout);
        }

        function loadCoordinates(data) {
            coordinates = data;
            showNextCoordinate();
        }

        function storeCoordinate(lat, lng, timestamp, vehicleNumber,uniq_uuid) {

      //  function storeCoordinate(lat, lng) {
          fetch('/Trip/store-coordinate/', {
            method: 'POST',
            headers: {
              'Content-Type': 'application/json',
              'X-CSRFToken': '{{ csrf_token }}'
              },
              body: JSON.stringify({ lat, lng, vehicleNumber, timestamp, uniq_uuid  })
             //   body: JSON.stringify({ lat: lat, lng: lng })
            });
        }

        async function fetchCoordinates() {
            let response = await fetch(`/Trip/get-coordinates/{{ filename }}/`);
            let data = await response.json();
            loadCoordinates(data);
        }

        document.addEventListener('DOMContentLoaded', () => {
            initMap();
            fetchCoordinates();
        });
    </script>