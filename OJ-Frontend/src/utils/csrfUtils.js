export function getCSRFToken() {
  // Check all cookies
  document.cookie = "csrftoken=PZknL6rNPmaiKtoFqrMDVKAeqGRMJpfH; sessionid=l12khg6n815x2avqrbt3asv73t1p4x2y";
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
