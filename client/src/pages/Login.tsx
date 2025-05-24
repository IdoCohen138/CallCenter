import { useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";
import config from "../config";
import type { User } from "../types/models";
import "../style/Login.css";

export default function Login() {
  const [users, setUsers] = useState<User[]>([]);
  const [selectedUser, setSelectedUser] = useState("");
  const navigate = useNavigate();

  useEffect(() => {
    const fullUrl = `${config.apiBaseUrl}/users`;
    const sockerUrl = `${config.socketUrl}`;
    console.log("📍 FINAL FETCH URL:", fullUrl);
    console.log("📍 FINAL sockerUrl:", sockerUrl);

    fetch(fullUrl)
      .then((res) => {
        console.log("📍 Response object:", res);
        return res.json();
      })
      .then(setUsers)
      .catch((err) => {
        console.error("❌ FETCH ERROR:", err);
      });
  }, []);

  console.log("📍 users:", users);

  const handleLogin = () => {
    const user = users.find(u => u.username === selectedUser);
    if (user) {
      localStorage.setItem("currentUser", JSON.stringify(user));
      navigate("/dashboard");
    }
  };

  return (
    <div className="login-page">
      <h2>Log In</h2>
      <select value={selectedUser} onChange={(e) => setSelectedUser(e.target.value)}>
        <option value="">Choose User</option>
        {users.map(user => (
          <option key={user.id} value={user.username}>
            {user.display_name} ({user.role})
          </option>
        ))}
      </select>
      <button onClick={handleLogin} disabled={!selectedUser}>
        Connect
      </button>
    </div>
  );
}
