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
    fetch(`${config.apiBaseUrl}/users`)
      .then(res => res.json())
      .then(setUsers)
      .catch(console.error);
  }, []);

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
