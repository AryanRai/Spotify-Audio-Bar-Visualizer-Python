// Get the hash of the url
const hash = window.location.hash
.substring(1)
.split('&')
.reduce(function (initial, item) {
  if (item) {
    var parts = item.split('=');
    initial[parts[0]] = decodeURIComponent(parts[1]);
  }
  return initial;
}, {});
window.location.hash = '';

// Set token
let _token = hash.access_token;



  

const authEndpoint = 'https://accounts.spotify.com/authorize';

// Replace with your app's client ID, redirect URI and desired scopes
const clientId = 'CLIENT ID';
const redirectUri = 'http://localhost:8000/get_token/get_token.html';
const scopes = [
  'streaming',
  'user-read-email',
  'user-read-private',
  'user-read-currently-playing',
  'user-read-playback-position',
  'user-read-playback-state',
];


if (!_token) {
  window.location = `${authEndpoint}?client_id=${clientId}&redirect_uri=${redirectUri}&scope=${scopes.join('%20')}&response_type=code&show_dialog=false`;
}


// Set up the Web Playback SDK




