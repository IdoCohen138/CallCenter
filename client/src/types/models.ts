export interface Tag {
  id: number;
  name: string;
}

export interface Task {
  id: number;
  name: string;
  status: "Open" | "In Progress" | "Completed";
}

export interface Call {
  id: number;
  description: string;
  created_at: string;
}

export interface User {
  id: number;
  username: string;
  display_name: string;
  role: "admin" | "user";
}
