const BASE_URL = import.meta.env.VITE_API_BASE_URL || "http://127.0.0.1:8000";

class ApiError extends Error {
  constructor(message, status) {
    super(message);
    this.status = status;
  }
}

async function request(path, options = {}) {
  let res;
  try {
    res = await fetch(`${BASE_URL}${path}`, {
      headers: { "Content-Type": "application/json" },
      ...options,
    });
  } catch (err) {
    throw new ApiError(
      "Cannot connect to the backend. Please check if the server is running.",
      0
    );
  }

  if (!res.ok) {
    let detail = `Request failed (${res.status})`;
    try {
      const body = await res.json();
      detail = body.detail || detail;
    } catch (_) {}
    throw new ApiError(detail, res.status);
  }

  if (res.status === 204) return null;
  return res.json();
}

// ---------- Monitors ----------
export const getMonitors = () => request("/api/monitors/");
export const getMonitor = (id) => request(`/api/monitors/${id}`);
export const createMonitor = (data) =>
  request("/api/monitors/", { method: "POST", body: JSON.stringify(data) });
export const updateMonitor = (id, data) =>
  request(`/api/monitors/${id}`, { method: "PUT", body: JSON.stringify(data) });
export const deleteMonitor = (id) =>
  request(`/api/monitors/${id}`, { method: "DELETE" });
export const toggleMonitor = (id) =>
  request(`/api/monitors/${id}/toggle`, { method: "PATCH" });

// ---------- Alerts ----------
export const getAlerts = () => request("/api/alerts/");
export const getMonitorAlerts = (id) => request(`/api/alerts/monitor/${id}`);
export const clearAlerts = () => request("/api/alerts/clear", { method: "DELETE" });

// ---------- Logs ----------
export const getLogs = () => request("/api/logs/");
export const getMonitorLogs = (id) => request(`/api/logs/monitor/${id}`);

// ---------- Dashboard ----------
export const getDashboardStats = () => request("/api/dashboard/stats");

export { ApiError, BASE_URL };