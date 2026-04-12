//making the map and setting the view to philadelphia
var map = L.map('map').setView([39.9526, -75.1652], 13);

L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
    attribution: '© OpenStreetMap contributors'
}).addTo(map);

//getting the user's location in lattitude and longitude
navigator.geolocation.getCurrentPosition((position) => {
    let lat = position.coords.latitude;
    let long = position.coords.longitude;

     // center map on user's actual location and zooming in more
    map.setView([lat, long], 14);
    
    // adding a drop in so the user sees their location
    L.marker([lat, long]).addTo(map).bindPopup("You are here").openPopup();
});

//function to search data
function findSite(){
    console.log("search called HEREEEEEEEEEEEEEEEEEe");

    //getting the user's location in lattitude and longitude
    navigator.geolocation.getCurrentPosition((position) => {
        let lat = position.coords.latitude;
        let long = position.coords.longitude;
        console.log("got location", lat, long); // add this


    fetch("/user", {
        //sending the user's location
        method: "POST",
        headers: { "Content-Type":"application/json"},
        body: JSON.stringify({
            lat: lat,
            long:long,
            max_distance: document.getElementById("max_distance").value,
            date: document.getElementById("date").value,
            time: document.getElementById("time").value,
            user_category: document.getElementById("user_category").value
        })
    })
    .then(res => {
        console.log("got resonse", res.status);
        return res.json();
    })
    .then(response => {
        console.log(response); // add this

        //storing the data in an array
        const events = response.recommendations
        events.forEach(event => {
            let event_lat = event.lat
            let event_long = event.long
            let name = event.site_name
            L.marker([event_lat, event_long]).addTo(map).bindPopup(`<b>${name}</b><br>${event.reason}`);

            });
        });
    });
}
    