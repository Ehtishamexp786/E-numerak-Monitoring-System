import { Routes, Route } from "react-router-dom";
import Sidebar from "./components/Layout/Sidebar";
import Dashboard from "./pages/Dashboard";
import Monitors from "./pages/Monitors";
import Alerts from "./pages/Alerts";
import Logs from "./pages/Logs";
import Settings from "./pages/Settings";

export default function App() {
  return (
    <div className="flex min-h-screen bg-void">
      <Sidebar />
      <main className="flex-1 overflow-x-hidden pb-16 md:pb-0">
        <Routes>
          <Route path="/" element={<Dashboard />} />
          <Route path="/monitors" element={<Monitors />} />
          <Route path="/alerts" element={<Alerts />} />
          <Route path="/logs" element={<Logs />} />
          <Route path="/settings" element={<Settings />} />
        </Routes>
      </main>
    </div>
  );
}
