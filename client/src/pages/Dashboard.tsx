import { useEffect, useState } from "react";
import AdminDashboard from "../components/AdminDashboard";
import UserDashboard from "../components/UserDashboard";
import type { User } from "../types/models";

export default function Dashboard() {
  const [currentUser, setCurrentUser] = useState<User | null>(null);

  const handleLogout = () => {
    localStorage.removeItem("currentUser");
    window.location.href = "/";
  };

  useEffect(() => {
    const userJson = localStorage.getItem("currentUser");
    if (userJson) setCurrentUser(JSON.parse(userJson));
  }, []);

  if (!currentUser) return <div>Loading...</div>;

  return currentUser.role === "admin" ? (
    <AdminDashboard onLogout={handleLogout} />
  ) : (
    <UserDashboard onLogout={handleLogout} />
  );
}