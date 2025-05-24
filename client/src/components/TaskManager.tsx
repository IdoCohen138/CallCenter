import { useState, useEffect } from "react";
import config from "../config";
import "../style/TaskManager.css";

interface Props {
  callId?: number;
  onCreated: () => void;
}

interface Task {
  id: number;
  name: string;
}

export default function TaskManager({ callId, onCreated }: Props) {
  const [taskName, setTaskName] = useState("");
  const [tasks, setTasks] = useState<Task[]>([]);
  const [editingTaskId, setEditingTaskId] = useState<number | null>(null);
  const [editedName, setEditedName] = useState("");

  const loadTasks = async () => {
    const res = await fetch(`${config.apiBaseUrl}/tasks`);
    const data = await res.json();
    setTasks(data);
  };

  useEffect(() => {
    loadTasks();
  }, []);

  const handleCreate = async () => {
    if (!taskName.trim()) return;
    await fetch(`${config.apiBaseUrl}/tasks`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ name: taskName })
    });
    setTaskName("");
    await loadTasks(); // ← טען מחדש את המשימות
    onCreated();
  };

  const handleRename = async (id: number, newName: string) => {
    if (!newName.trim() || newName === tasks.find(t => t.id === id)?.name) {
      setEditingTaskId(null);
      return;
    }
    await fetch(`${config.apiBaseUrl}/tasks/${id}`, {
      method: "PUT",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ name: newName })
    });
    setEditingTaskId(null);
    await loadTasks(); // ← גם כאן
    onCreated();
  };

  return (
    <div className="task-manager">
      <h3>{callId ? "Call Task Manager" : "Suggested Task Manager"}</h3>
      <input
        className="small-placeholder-input"
        type="text"
        placeholder="New task name"
        value={taskName}
        onChange={(e) => setTaskName(e.target.value)}
      />
      <button className="create-task" onClick={handleCreate}>Create Task</button>

      <ul>
        {tasks.map(task => (
          <li key={task.id}>
            {editingTaskId === task.id && !callId ? (
              <input
                value={editedName}
                onChange={(e) => setEditedName(e.target.value)}
                onBlur={() => handleRename(task.id, editedName)}
                autoFocus
              />
            ) : (
              <>
                <span>{task.name}</span>
                {!callId && (
                  <button
                    className="edit-button"
                    onClick={() => {
                      setEditedName(task.name);
                      setEditingTaskId(task.id);
                    }}
                  >
                    ✏️
                  </button>
                )}
              </>
            )}
          </li>
        ))}
      </ul>
    </div>
  );
}
