import axios from 'axios';

export function getCSRFToken1() {
  // Check all cookies
  const cookies = document.cookie.split(';');
  console.log('Document Cookies:', cookies); // Log all cookies to debug
  for (let cookie of cookies) {
    const [name, value] = cookie.trim().split('=');
    console.log('Checking cookie:', name); // Log each cookie name
    if (name === 'csrftoken') {
      console.log('Found CSRF Token:', value); // Log the CSRF token value
      return decodeURIComponent(value);
    }
  }
  console.log('Document Cookies:', document.cookie);
  console.warn('CSRF token not found in cookies.'); // Log warning if not found
  return null;
}

// Fetch CSRF token from Django backend
export const getCSRFToken = async () => {
  try {

    const response = await axios.get('https://onlinejudge-oj.onrender.com/csrf/');
    const csrfToken = response.data.csrfToken;
    return csrfToken;
  } catch (error) {
    console.error('Error fetching CSRF token:', error);
    return null;
  }
};

