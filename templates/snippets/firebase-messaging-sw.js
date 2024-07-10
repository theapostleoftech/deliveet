importScripts("https://www.gstatic.com/firebasejs/8.10.1/firebase-app.js");
importScripts("https://www.gstatic.com/firebasejs/8.10.1/firebase-messaging.js");

firebase.initializeApp({
    apiKey: "{{ firebase_config.API_KEY }}",
    authDomain: "{{ firebase_config.AUTH_DOMAIN }}",
    projectId: "{{ firebase_config.PROJECT_ID }}",
    storageBucket: "{{ firebase_config.STORAGE_BUCKET }}",
    messagingSenderId: "{{ firebase_config.MESSAGING_SENDER_ID }}",
    appId: "{{ firebase_config.APP_ID }}"
});

const messaging = firebase.messaging();

messaging.onBackgroundMessage(function (payload) {
    console.log('[firebase-messaging-sw.js] Received background message ', payload);
    // Customize notification here
    const notificationTitle = 'Background Message Title';
    const notificationOptions = {
        body: 'Background Message body.',
        icon: '/firebase-logo.png'
    };

    self.registration.showNotification(notificationTitle,
        notificationOptions);
});