import { useState, useEffect } from "react";
import TagManager from "./TagManager";
import TaskManager from "./TaskManager";
import config from "../config";
import "../style/AdminDashboard.css";

interface AdminDashboardProps {
  onLogout: () => void;
}

interface Tag {
  id: number;
  name: string;
}

interface Task {
  id: number;
  name: string;
}

export default function AdminDashboard({ onLogout }: AdminDashboardProps) {
  const [tags, setTags] = useState<Tag[]>([]);
  const [tasks, setTasks] = useState<Task[]>([]);
  const [taskTagLinks, setTaskTagLinks] = useState<{ tagName: string; taskName: string }[]>([]);
  const [selectedTagId, setSelectedTagId] = useState<number | null>(null);
  const [selectedTaskId, setSelectedTaskId] = useState<number | null>(null);

  const loadData = async () => {
    const tagsUrl = `${config.apiBaseUrl}/tags`;
    const tasksUrl = `${config.apiBaseUrl}/tasks`;
    const linksUrl = `${config.apiBaseUrl}/tasks/links`;
    console.log(tagsUrl);
    const [tagsRes, tasksRes, linksRes] = await Promise.all([
      fetch(tagsUrl),
      fetch(tasksUrl),
      fetch(linksUrl)
    ]);
    const [tags, tasks, links] = await Promise.all([
      tagsRes.json(),
      tasksRes.json(),
      linksRes.json()
    ]);
    setTags(tags);
    setTasks(tasks);
    setTaskTagLinks(links);
  };

  useEffect(() => {
    loadData();
  }, []);

  
  const linkTaskToTag = async () => {
    if (!selectedTagId || !selectedTaskId) return;
    await fetch(`${config.apiBaseUrl}/tasks/${selectedTaskId}/tags`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ tag_id: selectedTagId })
    });
    loadData();
  };


  return (
    <div className="admin-dashboard">
      <div className="header">
        <h2>Admin Dashboard</h2>
        <div className="logout-wrapper">
          <button className="logout-button" onClick={onLogout}>Logout</button>
        </div>
      </div>
      <div className="section">
        <TagManager onCreated={loadData}/>
      </div>
      <div className="section">
        <TaskManager onCreated={loadData} />
      </div>
      <div className="section link-section">
        <h3>Link Task to Tag</h3>
        <div className="row">
          <select onChange={(e) => setSelectedTagId(Number(e.target.value))} value={selectedTagId || ""}>
            <option value="">Select Tag</option>
            {tags.map(tag => <option key={tag.id} value={tag.id}>{tag.name}</option>)}
          </select>
          <select onChange={(e) => setSelectedTaskId(Number(e.target.value))} value={selectedTaskId || ""}>
            <option value="">Select Task</option>
            {tasks.map(task => <option key={task.id} value={task.id}>{task.name}</option>)}
          </select>
          <button onClick={linkTaskToTag}>Link</button>
        </div>
        <div className="task-tag-links">
          {taskTagLinks.map((link, index) => (
            <div className="link-card" key={index}>
              <span className="tag-label">{link.tagName}</span>
              <span className="arrow">→</span>
              <span className="task-label">{link.taskName}</span>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
}
