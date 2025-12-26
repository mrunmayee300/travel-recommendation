// API configuration
export const API_BASE = 
  import.meta.env.VITE_API_BASE || "http://localhost:8000/api";

// Helper function to build API URLs
export const apiUrl = (endpoint: string): string => {
  // Remove leading slash if present to avoid double slashes
  const cleanEndpoint = endpoint.startsWith("/") ? endpoint.slice(1) : endpoint;
  // Ensure API_BASE doesn't have trailing slash
  const cleanBase = API_BASE.endsWith("/") ? API_BASE.slice(0, -1) : API_BASE;
  return `${cleanBase}/${cleanEndpoint}`;
};

