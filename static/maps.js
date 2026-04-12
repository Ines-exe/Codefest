navigator.geolocation.getCurrentPosition((position) => {
    lat = position.coords.latitude
    long = position.coords.longitude

    fetch("/user", {
        method: "POST",
        headers: { "Content-Type":"application/json"},
        body: JSON.stringify({lat: lat, long:long})
    }

    ) 
});