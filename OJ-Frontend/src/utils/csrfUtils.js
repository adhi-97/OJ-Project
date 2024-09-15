import axiosInstance from '../utils/axiosConfig';

export function getCSRFToken() {
  // Check all cookies
  const cookies = document.cookie.split(';');
  console.log('Document Cookies:', cookies); // Log all cookies to debug
  for (let cookie of cookies) {
    const [name, value] = cookie.trim().split('=');
    console.log('Checking cookie:', name); // Log each cookie name
    if (name === 'csrftoken') {
      console.log('Found CSRF Token:', value); // Log the CSRF token value
      sessionStorage.setItem('csrfToken', decodeURIComponent(value));
      return decodeURIComponent(value);
    }
  }
  console.log('Document Cookies:', document.cookie);
  console.warn('CSRF token not found in cookies.'); // Log warning if not found
  return null;
}

// Fetch CSRF token from Django backend and cache it
export const getCSRFToken1 = async () => {
  // Check if the CSRF token is already cached in local storage
  let cachedToken = sessionStorage.getItem('csrfToken');
  
  // If the token exists, return it directly
  if (cachedToken) {
    console.debug('Using cached CSRF token:', cachedToken);
    return cachedToken;
  }

  try {
    // Fetch a new CSRF token from the server
    const response = await axiosInstance.get('auth/csrf/');
    const csrfToken = response.data.csrfToken;
    console.debug('Using CSRF token:', csrfToken);
    if (csrfToken) {
      // Cache the CSRF token in local storage for future use
      sessionStorage.setItem('csrfToken', csrfToken);
      console.debug('Fetched new CSRF token:', csrfToken);
    }

    return csrfToken;
  } catch (error) {
    console.error('Error fetching CSRF token:', error);
    return null;
  }
};


