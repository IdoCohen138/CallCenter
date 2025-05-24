import { useState, useEffect } from "react";
import config from "../config";
import "../style/TagManager.css";

interface Props {
  onCreated: () => void;
}

export default function TagManager({ onCreated }: Props) {
  const [tagName, setTagName] = useState("");
  const [tags, setTags] = useState<any[]>([]);
  const [editingTagId, setEditingTagId] = useState<number | null>(null);
  const [editedName, setEditedName] = useState("");

  const loadTags = async () => {
    const res = await fetch(`${config.apiBaseUrl}/tags`);
    const data = await res.json();
    setTags(data);
  };

  useEffect(() => {
    loadTags();
  }, []);

  const handleCreate = async () => {
    if (!tagName.trim()) return;
    await fetch(`${config.apiBaseUrl}/tags`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ name: tagName })
    });
    setTagName("");
    await loadTags();     // ← טען מחדש את הרשימה
    onCreated();          // ← אם צריך גם לעדכן הורה
  };

  const handleRename = async (id: number, newName: string) => {
    if (!newName.trim() || newName === tags.find(t => t.id === id)?.name) {
      setEditingTagId(null);
      return;
    }
    await fetch(`${config.apiBaseUrl}/tags/${id}`, {
      method: "PUT",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ name: newName })
    });
    setEditingTagId(null);
    await loadTags();     // ← גם כאן צריך לרענן
    onCreated();
  };

  return (
    <div className="tag-manager">
      <h3>Tag Manager</h3>
      <input
        className="small-placeholder-input"
        type="text"
        placeholder="New tag name"
        value={tagName}
        onChange={(e) => setTagName(e.target.value)}
      />
      <button className="create-tag" onClick={handleCreate}>Create Tag</button>

      <ul>
        {tags.map(tag => (
          <li key={tag.id}>
            {editingTagId === tag.id ? (
              <input
                value={editedName}
                onChange={(e) => setEditedName(e.target.value)}
                onBlur={() => handleRename(tag.id, editedName)}
                autoFocus
              />
            ) : (
              <>
                <span>{tag.name}</span>
                <button
                  className="edit-button"
                  onClick={() => {
                    setEditedName(tag.name);
                    setEditingTagId(tag.id);
                  }}
                >
                  ✏️
                </button>
              </>
            )}
          </li>
        ))}
      </ul>
    </div>
  );
}
