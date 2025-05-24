import type { Tag } from "../types/models";

interface TagSelectorProps {
  tags: Tag[];
  onSelect?: (tag: Tag) => void;
  existingTagIds?: number[];
}
export default function TagSelector({
  tags,
  onSelect,
  existingTagIds = []
}: TagSelectorProps) {
  const availableTags = tags.filter(tag => !existingTagIds.includes(tag.id));
  console.log(tags)
  return (
    <select
      onChange={(e) => {
        const tag = availableTags.find(t => t.id === Number(e.target.value));
        if (tag && onSelect) {
          onSelect(tag);
        }
      }}
    >
      <option value="">Choose Tag</option>
      {availableTags.map(tag => (
        <option key={tag.id} value={tag.id}>
          {tag.name}
        </option>
      ))}
    </select>
  );
}
