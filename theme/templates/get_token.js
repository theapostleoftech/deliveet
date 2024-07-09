import {getMessaging, getToken} from "firebase/messaging";

// Get registration token. Initially this makes a network call, once retrieved
// subsequent calls to getToken will return from cache.
const messaging = getMessaging();
getToken(messaging, {vapidKey: 'BMI2AQ8WuTckLiltwmQr1y6OKL4VMDRm8yt-joyAtxb6RoeGKEVuicuTAPsZPW1NjGm9XacKh0bGFmsENC3Sgx8'})

    .then((currentToken) => {
    if (currentToken) {
        // Send the token to your server and update the UI if necessary
        fetch('{% url "couriers:courier_delivery_tasks_fcm" %}?fcm_token=' + currentToken);
    } else {
        // Show permission request UI
        console.log('No registration token available. Request permission to generate one.');
        // ...
    }
}).catch((err) => {
    console.log('An error occurred while retrieving token. ', err);
    // ...
});