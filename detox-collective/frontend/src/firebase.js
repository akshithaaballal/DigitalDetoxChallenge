// Minimal firebase client setup - replace placeholders with your config
import { initializeApp } from 'firebase/app';
import { getFirestore } from 'firebase/firestore';
import { getAuth } from 'firebase/auth';
import { getMessaging, onMessage, getToken } from 'firebase/messaging';

const firebaseConfig = {
  apiKey: "YOUR_API_KEY",
  authDomain: "YOUR_PROJECT.firebaseapp.com",
  projectId: "YOUR_PROJECT_ID",
  storageBucket: "YOUR_PROJECT.appspot.com",
  messagingSenderId: "YOUR_SENDER_ID",
  appId: "YOUR_APP_ID"
};

const app = initializeApp(firebaseConfig);
export const db = getFirestore(app);
export const auth = getAuth(app);
export const messaging = getMessaging(app);

// To get an FCM token for web push, call getToken() from a component after user grants permission.
export async function registerForPush(vapidKey) {
  try {
    const token = await getToken(messaging, { vapidKey });
    return token;
  } catch (err) {
    console.error('Error getting FCM token', err);
    return null;
  }
}

// Optional: listen for messages when the web app is in the foreground
export function listenForMessages(callback) {
  onMessage(messaging, (payload) => {
    callback(payload);
  });
}
