-- ודא שאתה משתמש בסכמה הנכונה
USE call_center;

-- טבלת תגיות
CREATE TABLE tags (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(255) NOT NULL UNIQUE
);

-- טבלת משימות
CREATE TABLE tasks (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    status ENUM('Open', 'In Progress', 'Completed') DEFAULT 'Open',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- טבלת שיחות
CREATE TABLE calls (
    id INT AUTO_INCREMENT PRIMARY KEY,
    description TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- קשר בין שיחות לתגיות (רבים לרבים)
CREATE TABLE call_tags (
    call_id INT,
    tag_id INT,
    PRIMARY KEY (call_id, tag_id),
    FOREIGN KEY (call_id) REFERENCES calls(id) ON DELETE CASCADE,
    FOREIGN KEY (tag_id) REFERENCES tags(id) ON DELETE CASCADE
);

-- קשר בין שיחות למשימות (רבים לרבים)
CREATE TABLE call_tasks (
    call_id INT,
    task_id INT,
    PRIMARY KEY (call_id, task_id),
    FOREIGN KEY (call_id) REFERENCES calls(id) ON DELETE CASCADE,
    FOREIGN KEY (task_id) REFERENCES tasks(id) ON DELETE CASCADE
);

-- טבלת משימות מוצעות - Bonus
CREATE TABLE suggested_tasks (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(255) NOT NULL UNIQUE
);

-- קשר בין משימות מוצעות לתגיות (משימה מוצעת יכולה להיות קשורה ליותר מתגית)
CREATE TABLE suggested_task_tags (
    suggested_task_id INT,
    tag_id INT,
    PRIMARY KEY (suggested_task_id, tag_id),
    FOREIGN KEY (suggested_task_id) REFERENCES suggested_tasks(id) ON DELETE CASCADE,
    FOREIGN KEY (tag_id) REFERENCES tags(id) ON DELETE CASCADE
);
