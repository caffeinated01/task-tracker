async function fetchWithAuth(url, options = {}) {
  try {
    const res = await fetch(url, options);
    if (res.status === 401) {
      const refreshRes = await fetch("/api/auth/refresh", {
        method: "POST",
      });
      if (refreshRes.ok) {
        return fetch(url, options);
      } else {
        window.location.href = "/login";
      }
    }
    return res;
  } catch (error) {
    console.error(error);
    throw error;
  }
}

export { fetchWithAuth };
