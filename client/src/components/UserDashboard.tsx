import { useEffect, useState } from "react";
import config from "../config";
import socket from "../socket";
import TagSelector from "./TagSelector";
import type { Tag, Task } from "../types/models";
import "../style/UserDashboard.css";

interface Call {
  id: number;
  description: string;
  created_at: string;
}

interface UserDashboardProps {
  onLogout: () => void;
}

export default function UserDashboard({ onLogout }: UserDashboardProps) {
  const [tags, setTags] = useState<Tag[]>([]);
  const [suggestedTasks, setSuggestedTasks] = useState<Task[]>([]);
  const [calls, setCalls] = useState<Call[]>([]);
  const [selectedCallId, setSelectedCallId] = useState<number | null>(null);
  const [callTags, setCallTags] = useState<Tag[]>([]);
  const [callTasks, setCallTasks] = useState<Task[]>([]);
  const [newTaskName, setNewTaskName] = useState<string>("");
  const [newCallDescription, setNewCallDescription] = useState<string>("");

  const fetchTags = async () => {
    const res = await fetch(`${config.apiBaseUrl}/tags`);
    const data = await res.json();
    setTags(data);
  };
  const fetchTasks = async () => {
    const res = await fetch(`${config.apiBaseUrl}/tasks`);
    const data = await res.json();
    console.log("datdatadataa", data);
    setSuggestedTasks(data);
  };

  const loadCalls = async () => {
    const res = await fetch(`${config.apiBaseUrl}/calls`);
    const data = await res.json();
    setCalls(data);
  };

  const loadCallDetails = async (callId: number) => {
    setSelectedCallId(callId);
    const tagRes = await fetch(`${config.apiBaseUrl}/calls/${callId}/tags`).then(res => res.json());
    const taskRes = await fetch(`${config.apiBaseUrl}/calls/${callId}/tasks`).then(res => res.json());
    setCallTags(tagRes);
    setCallTasks(taskRes);
  };

useEffect(() => {
  loadCalls();
  fetchTags();
  fetchTasks();

  const handleTagsUpdate = () => {
    fetchTags();
    if (selectedCallId !== null) {
      loadCallDetails(selectedCallId);
    }
  };
  const handleTaskUpdate = () => {
    fetchTasks();
    if (selectedCallId !== null) {
      loadCallDetails(selectedCallId);
    }
  };
  const handleTaskLinkToTag = () => {
    if (selectedCallId !== null) {
      loadCallDetails(selectedCallId);
    }
  };

  socket.on("tags_updated", handleTagsUpdate);
  socket.on("tasks_updated", handleTaskUpdate);
  socket.on("link_task_tag", handleTaskLinkToTag);

  return () => {
    socket.off("tags_updated", handleTagsUpdate);
    socket.off("tasks_updated", handleTaskUpdate);
    socket.off("link_task_tag", handleTaskLinkToTag);
  };
}, [selectedCallId]);

  const createNewCall = async () => {
    if (!newCallDescription.trim()) return;

    await fetch(`${config.apiBaseUrl}/calls`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ description: newCallDescription })
    });

    setNewCallDescription("");
    loadCalls();
  };



  useEffect(() => {
    if (selectedCallId) loadCallDetails(selectedCallId);
  }, []);

  const assignTagToCall = async (tagId: number) => {
    if (!selectedCallId) return;
    await fetch(`${config.apiBaseUrl}/calls/${selectedCallId}/tags`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ tag_id: tagId })
    });

    const relatedTasks = await fetch(`${config.apiBaseUrl}/tags/${tagId}/tasks`).then(res => res.json());
    for (const task of relatedTasks) {
      if (!callTasks.some(t => t.id === task.id)) {
        await fetch(`${config.apiBaseUrl}/calls/${selectedCallId}/tasks`, {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({ task_id: task.id })
        });
      }
    }

    await loadCallDetails(selectedCallId);
  };

  const updateTaskStatus = async (taskId: number, newStatus: string) => {
    await fetch(`${config.apiBaseUrl}/tasks/${taskId}/status`, {
      method: "PUT",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ status: newStatus })
    });
    if (selectedCallId) loadCallDetails(selectedCallId);
  };

  const createTaskForCall = async () => {
    if (!newTaskName.trim() || !selectedCallId) return;
    const res = await fetch(`${config.apiBaseUrl}/tasks`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ name: newTaskName })
    });
    const data = await res.json();
    await fetch(`${config.apiBaseUrl}/calls/${selectedCallId}/tasks`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ task_id: data.id })
    });
    setNewTaskName("");
    loadCallDetails(selectedCallId);
  };

  const assignSuggestedTaskToCall = async (taskId: number) => {
    if (!selectedCallId || callTasks.some(t => t.id === taskId)) return;
    await fetch(`${config.apiBaseUrl}/calls/${selectedCallId}/tasks`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ task_id: taskId })
    });
    loadCallDetails(selectedCallId);
  };

  return (
    <div className="user-dashboard">
      <div className="header">
        <h2>User Dashboard</h2>
        <button className="logout-button" onClick={onLogout}>Logout</button>
      </div>

      <div className="section">
        <h3>Call List</h3>
          <div className="centered-input-group">
            <input
              type="text"
              placeholder="New call description"
              value={newCallDescription}
              onChange={(e) => setNewCallDescription(e.target.value)}
            />
            <button onClick={createNewCall} disabled={!newCallDescription.trim()}>
              Add Call
            </button>
          </div>
        <div className="call-list">
            {[...calls].sort((a, b) => a.id - b.id).map(call => (
            <div
              key={call.id}
              onClick={() => loadCallDetails(call.id)}
              className={`call-item ${selectedCallId === call.id ? "active" : ""}`}
            >
              #{call.id} - {call.description}
            </div>
          ))}
        </div>
      </div>

      {selectedCallId && (
        <div className="section-box">
          <h3>Tags for Call #{selectedCallId}</h3>
          <ul>
            {callTags.map(tag => (
              <li key={tag.id}>{tag.name}</li>
            ))}
          </ul>
          <div className="centered-input-group">
            <TagSelector
              tags={tags}
              onSelect={(tag) => assignTagToCall(tag.id)}
              existingTagIds={callTags.map(t => t.id)}
            />
          </div>
          <div className="section-box">
            <h3>Tasks for Call #{selectedCallId}</h3>
            <div className="task-list">
              {callTasks.map(task => (
                <div key={task.id} className={`task-card ${task.status.replace(/\s+/g, '-').toLowerCase()}`}>
                  <p><strong>{task.name}</strong></p>
                  <select
                    value={task.status}
                    onChange={(e) => updateTaskStatus(task.id, e.target.value)}
                  >
                    <option value="Open">Open</option>
                    <option value="In Progress">In Progress</option>
                    <option value="Completed">Completed</option>
                  </select>
                </div>
              ))}
            </div>
          </div>
          <div className="centered-input-group">
            <input
              type="text"
              placeholder="New task name"
              value={newTaskName}
              onChange={(e) => setNewTaskName(e.target.value)}
            />
            <button onClick={createTaskForCall} disabled={!newTaskName.trim()}>
              Add Task
            </button>
          </div>
          <div className="section-box">
            <h4>Assign Suggested Task</h4>
            <div className="centered-input-group">
              <select
                onChange={(e) => assignSuggestedTaskToCall(Number(e.target.value))}
                defaultValue=""
              >
                <option value="">Select task</option>
                {suggestedTasks.filter(task => !callTasks.some(ct => ct.id === task.id))
                  .map(task => (
                    <option key={task.id} value={task.id}>{task.name}</option>
                  ))}
              </select>
            </div>
          </div>
        </div>
      )}
    </div>
  );
}
