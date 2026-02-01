import json

# === CONFIG ===
INPUT_FILE = "chats.json"      # Ensure this matches your filename
OUTPUT_FILE = "slimchats.txt"

# === LOAD JSON ===
print("...Loading JSON")
with open(INPUT_FILE, "r", encoding="utf-8") as f:
    conversations = json.load(f)

output_lines = []

# === PROCESS EACH CONVERSATION ===
for convo in conversations:
    mapping = convo.get("mapping", {})
    
    # Find root node
    root_id = next((nid for nid, n in mapping.items() if n.get("parent") is None), None)
    if not root_id:
        continue

    # === ITERATIVE WALK (Stack-based) ===
    # Using a stack prevents RecursionError on deep trees
    stack = [root_id]
    visited = set()

    while stack:
        node_id = stack.pop() # Get the next node
        
        if node_id in visited:
            continue
        visited.add(node_id)

        node = mapping.get(node_id, {})
        
        # Process message if it exists
        message = node.get("message")
        if message:
            role = message.get("author", {}).get("role")
            content = message.get("content", {})
            parts = content.get("parts", [])
            
            # Check for valid text content
            if parts and isinstance(parts, list) and len(parts) > 0 and isinstance(parts[0], str):
                text = parts[0].strip()
                if text: 
                    if role == "user":
                        output_lines.append(f"\n[USER]: {text}")
                    elif role == "assistant":
                        output_lines.append(f"[AI]: {text}")
                    elif role == "system":
                        pass 

        # Add children to stack
        # We reverse them so the first child (main path) is processed next
        children = node.get("children", [])
        for child_id in reversed(children):
            stack.append(child_id)

    # Add a separator between conversations
    output_lines.append("\n" + "="*40 + "\n")

# === SAVE TO FILE ===
print("...Writing to file")
with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
    f.write("\n".join(output_lines))

print(f"✅ Done. Extracted memory saved to {OUTPUT_FILE}")