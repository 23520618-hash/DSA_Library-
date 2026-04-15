import tkinter as tk
from tkinter import ttk, messagebox
import math

class RadixNode:
    def __init__(self, prefix=""):
        self.prefix = prefix
        self.children = {}
        self.is_word = False
        self.meaning = None

class DictionaryRadixTrie:
    def __init__(self):
        self.root = RadixNode("GỐC")

    def insert(self, word, meaning):
        node = self.root        
        logs = []
        
        while True:
            if not node.children:  # Tree empty at this node
                new_node = RadixNode(word)
                new_node.is_word = True
                new_node.meaning = meaning
                node.children[word] = new_node
                logs.append(f"Tạo node mới '{word}' (Nghĩa: {meaning}).")
                break

            match_found = False
            for key in list(node.children.keys()):
                # Find longest common prefix
                i = 0
                while i < len(word) and i < len(key) and word[i] == key[i]:
                    i += 1
                
                if i > 0:
                    match_found = True
                    common_prefix = word[:i]
                    remaining_key = key[i:]
                    remaining_word = word[i:]

                    if remaining_key:
                        # Split node
                        child_node = node.children.pop(key)
                        child_node.prefix = remaining_key
                        
                        new_node = RadixNode(common_prefix)
                        new_node.children[remaining_key] = child_node
                        node.children[common_prefix] = new_node
                        
                        node = new_node
                        logs.append(f"Tách node '{key}' thành '{common_prefix}' và '{remaining_key}'.")
                    else:
                        node = node.children[key]
                        logs.append(f"Đi qua node '{key}'.")
                    
                    word = remaining_word
                    break
            
            if not match_found:
                if word:
                    new_node = RadixNode(word)
                    new_node.is_word = True
                    new_node.meaning = meaning
                    node.children[word] = new_node
                    logs.append(f"Tạo nhánh mới '{word}' (Nghĩa: {meaning}).")
                else:
                    node.is_word = True
                    node.meaning = meaning
                    logs.append(f"Cập nhật từ tại node kết thúc rỗng, nghĩa: '{meaning}'.")
                break
                
        return logs

    def delete(self, word):
        node = self.root
        logs = []
        while word:
            match_found = False
            for key, child in node.children.items():
                if word.startswith(key):
                    word = word[len(key):]
                    node = child
                    match_found = True
                    break
            if not match_found:
                logs.append(f"Không tìm thấy node phù hợp để xóa tiếp.")
                return False, logs
        
        if node.is_word:
            node.is_word = False
            node.meaning = None
            logs.append(f"Đã gỡ bỏ đánh dấu kết thúc từ (Xoá thành công).")
            return True, logs
        
        logs.append("Từ này không tồn tại trong từ điển.")
        return False, logs

    def search(self, word):
        node = self.root
        logs = []
        path = []
        
        while word:
            match_found = False
            for key, child in node.children.items():
                if word.startswith(key):
                    path.append(key)
                    logs.append(f"Đi qua nhánh: '{key}'")
                    word = word[len(key):]
                    node = child
                    match_found = True
                    break
            if not match_found:
                logs.append("Không tìm thấy nhánh phù hợp, từ không tồn tại.")
                return None, logs
        
        if node.is_word:
            logs.append(f"Đã tìm thấy từ! Nghĩa là: '{node.meaning}'")
            return node.meaning, logs
        
        logs.append("Đã đến cuối nhánh nhưng đây không phải là một kết thúc từ.")
        return None, logs

class ModernTrieUI:
    def __init__(self, root):
        self.root = root
        self.root.title("TỪ ĐIỂN RADIX TRIE - VISUALIZER")
        self.root.geometry("1100x700")
        self.root.configure(bg="#1E1E2E")  # Dark theme background

        self.trie = DictionaryRadixTrie()
        
        # Color Palette
        self.colors = {
            "bg": "#1E1E2E",
            "card_bg": "#2A2A3C",
            "text": "#CDD6F4",
            "primary": "#89B4FA",
            "success": "#A6E3A1",
            "danger": "#F38BA8",
            "node_bg": "#313244",
            "node_full": "#A6E3A1",
            "line": "#6C7086"
        }

        self.setup_styles()
        self.build_ui()
        self.draw_tree()

    def setup_styles(self):
        style = ttk.Style()
        style.theme_use('clam')
        
        # Entry
        style.configure('Modern.TEntry', fieldbackground=self.colors["card_bg"], 
                        foreground=self.colors["text"], borderwidth=0, padding=10)
        
        # Buttons
        style.configure('Primary.TButton', background=self.colors["primary"], 
                        foreground="#1E1E2E", font=("Segoe UI", 10, "bold"), padding=8, borderwidth=0)
        style.map('Primary.TButton', background=[('active', '#74C7EC')])
        
        style.configure('Danger.TButton', background=self.colors["danger"], 
                        foreground="#1E1E2E", font=("Segoe UI", 10, "bold"), padding=8, borderwidth=0)
        style.map('Danger.TButton', background=[('active', '#EBA0AC')])

    def build_ui(self):
        # --- LEFT PANEL (Controls) ---
        left_panel = tk.Frame(self.root, bg=self.colors["bg"], width=350)
        left_panel.pack(side=tk.LEFT, fill=tk.Y, padx=20, pady=20)
        left_panel.pack_propagate(False)

        # Title
        tk.Label(left_panel, text="Quản lý Từ Điển", font=("Segoe UI", 18, "bold"), 
                 bg=self.colors["bg"], fg=self.colors["primary"]).pack(anchor="w", pady=(0, 20))

        # Inputs Card
        input_card = tk.Frame(left_panel, bg=self.colors["card_bg"], padx=15, pady=15)
        input_card.pack(fill=tk.X, pady=(0, 20))

        tk.Label(input_card, text="TỪ TIẾNG ANH", font=("Segoe UI", 9, "bold"), 
                 bg=self.colors["card_bg"], fg=self.colors["line"]).pack(anchor="w")
        self.entry_word = tk.Entry(input_card, font=("Segoe UI", 12), bg="#45475A", 
                                   fg=self.colors["text"], insertbackground=self.colors["text"], relief="flat")
        self.entry_word.pack(fill=tk.X, pady=(5, 15), ipady=5)

        tk.Label(input_card, text="NGHĨA TIẾNG VIỆT", font=("Segoe UI", 9, "bold"), 
                 bg=self.colors["card_bg"], fg=self.colors["line"]).pack(anchor="w")
        self.entry_meaning = tk.Entry(input_card, font=("Segoe UI", 12), bg="#45475A", 
                                      fg=self.colors["text"], insertbackground=self.colors["text"], relief="flat")
        self.entry_meaning.pack(fill=tk.X, pady=(5, 15), ipady=5)

        # Buttons
        btn_frame = tk.Frame(input_card, bg=self.colors["card_bg"])
        btn_frame.pack(fill=tk.X)
        
        ttk.Button(btn_frame, text="THÊM", style="Primary.TButton", 
                   command=self.act_add).pack(side=tk.LEFT, expand=True, fill=tk.X, padx=(0, 2))
        ttk.Button(btn_frame, text="TÌM", style="Primary.TButton", 
                   command=self.act_search).pack(side=tk.LEFT, expand=True, fill=tk.X, padx=(2, 2))
        ttk.Button(btn_frame, text="XÓA", style="Danger.TButton", 
                   command=self.act_delete).pack(side=tk.LEFT, expand=True, fill=tk.X, padx=(2, 0))

        # Logs Card
        log_card = tk.Frame(left_panel, bg=self.colors["card_bg"], padx=15, pady=15)
        log_card.pack(fill=tk.BOTH, expand=True)
        
        tk.Label(log_card, text="NHẬT KÝ THUẬT TOÁN (SỰ THAY ĐỔI DỮ LIỆU)", font=("Segoe UI", 9, "bold"), 
                 bg=self.colors["card_bg"], fg=self.colors["line"]).pack(anchor="w", pady=(0, 10))
        
        self.log_text = tk.Text(log_card, font=("Consolas", 10), bg="#1E1E2E", fg=self.colors["success"], 
                                relief="flat", wrap="word", padx=10, pady=10)
        self.log_text.pack(fill=tk.BOTH, expand=True)

        # --- RIGHT PANEL (Canvas Visualization) ---
        right_panel = tk.Frame(self.root, bg=self.colors["card_bg"], padx=15, pady=15)
        right_panel.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=(0, 20), pady=20)

        tk.Label(right_panel, text="SƠ ĐỒ TRỰC QUAN RADIX TRIE", font=("Segoe UI", 14, "bold"), 
                 bg=self.colors["card_bg"], fg=self.colors["text"]).pack(anchor="w", pady=(0, 10))

        self.canvas = tk.Canvas(right_panel, bg=self.colors["bg"], highlightthickness=0)
        self.canvas.pack(fill=tk.BOTH, expand=True)

    def write_log(self, text, clear=False):
        if clear:
            self.log_text.delete(1.0, tk.END)
        self.log_text.insert(tk.END, text + "\n")
        self.log_text.see(tk.END)

    def act_add(self):
        w = self.entry_word.get().strip().lower()
        m = self.entry_meaning.get().strip()
        if not w or not m:
            messagebox.showwarning("Lỗi", "Vui lòng nhập từ và nghĩa!")
            return
            
        self.write_log(f"\n[+] ĐANG THÊM: '{w}'")
        logs = self.trie.insert(w, m)
        for log in logs:
            self.write_log(f"   ↳ {log}")
            
        self.entry_word.delete(0, tk.END)
        self.entry_meaning.delete(0, tk.END)
        self.draw_tree()

    def act_search(self):
        w = self.entry_word.get().strip().lower()
        if not w:
            messagebox.showwarning("Lỗi", "Vui lòng nhập từ cần tìm!")
            return
            
        self.write_log(f"\n[?] ĐANG TÌM: '{w}'")
        res, logs = self.trie.search(w)
        for log in logs:
            self.write_log(f"   ↳ {log}")
            
        if res:
            messagebox.showinfo("Kết quả", f"Từ: {w}\nNghĩa: {res}")
            
        self.draw_tree()

    def act_delete(self):
        w = self.entry_word.get().strip().lower()
        if not w:
            messagebox.showwarning("Lỗi", "Vui lòng nhập từ cần xoá!")
            return
            
        self.write_log(f"\n[-] ĐANG XÓA: '{w}'")
        success, logs = self.trie.delete(w)
        for log in logs:
            self.write_log(f"   ↳ {log}")
            
        self.entry_word.delete(0, tk.END)
        self.draw_tree()

    # --- Tree Drawing Algorithm ---
    def get_tree_dimensions(self, node):
        """Trả về tuple (width, height) của cây con"""
        if not node.children:
            return 1, 1
        width = 0
        depth = 0
        for child in node.children.values():
            w, d = self.get_tree_dimensions(child)
            width += w
            depth = max(depth, d)
        return width, depth + 1

    def draw_tree(self):
        self.canvas.delete("all")
        self.canvas.update()
        canvas_w = self.canvas.winfo_width()
        canvas_h = self.canvas.winfo_height()
        
        if canvas_w < 10 or canvas_h < 10:
            # Fallback nếu canvas chưa render kịp
            canvas_w, canvas_h = 700, 600

        tree_width, _ = self.get_tree_dimensions(self.trie.root)
        
        # Draw recursively starting from root
        # root at center-top
        start_x = canvas_w / 2
        start_y = 50
        
        # Calculate dynamic x_offset based on canvas width and tree size
        base_x_offset = max(60, (canvas_w - 50) / max(1, tree_width))
        
        self._recursive_draw(self.trie.root, start_x, start_y, base_x_offset, 80)

    def _recursive_draw(self, node, x, y, x_offset, y_offset, drawn=None):
        if drawn is None:
            drawn = set()
            
        radius = 24
        
        # Vẽ các nhánh con
        child_count = len(node.children)
        if child_count > 0:
            total_children_width = sum([self.get_tree_dimensions(c)[0] for c in node.children.values()])
            
            # Phân bổ vị trí x cho các con dựa trên tỉ lệ width của chúng
            start_x = x - (total_children_width * x_offset) / 2
            
            current_x = start_x
            for key, child in node.children.items():
                child_w, _ = self.get_tree_dimensions(child)
                
                # Tọa độ x của con sẽ nằm ở giữa vùng width của nó
                child_center_x = current_x + (child_w * x_offset) / 2
                child_y = y + y_offset
                
                # Vẽ đường nối
                self.canvas.create_line(x, y, child_center_x, child_y, fill=self.colors["line"], width=2)
                
                # Gọi đệ quy vẽ con
                self._recursive_draw(child, child_center_x, child_y, x_offset, y_offset, drawn)
                
                # Dịch x_cursor đi với width của node con vừa vẽ
                current_x += child_w * x_offset

        # Vẽ node hiện tại
        color = self.colors["node_full"] if node.is_word else self.colors["node_bg"]
        text_color = "#1E1E2E" if node.is_word else self.colors["text"]
        outline_color = self.colors["primary"] if node == self.trie.root else color
        
        # Circle
        self.canvas.create_oval(x-radius, y-radius, x+radius, y+radius, 
                                fill=color, outline=outline_color, width=2)
        
        # Text prefix
        self.canvas.create_text(x, y, text=node.prefix, font=("Segoe UI", 11, "bold"), fill=text_color)
        
        # Text meaning nếu có
        if node.is_word and node.meaning:
            self.canvas.create_text(x, y+radius+10, text=node.meaning, font=("Segoe UI", 9, "italic"), fill=self.colors["primary"])

if __name__ == "__main__":
    root = tk.Tk()
    app = ModernTrieUI(root)
    root.mainloop()
