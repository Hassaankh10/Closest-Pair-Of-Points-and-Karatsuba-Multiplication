"""
Python GUI Application for Divide and Conquer Algorithms
Using tkinter for the user interface
"""

try:
    import tkinter as tk
    from tkinter import ttk, filedialog, messagebox, scrolledtext
    import matplotlib.pyplot as plt
    from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
    from matplotlib.figure import Figure
    TKINTER_AVAILABLE = True
except ImportError:
    TKINTER_AVAILABLE = False
    print("Warning: tkinter is not available. Please install it or use the command-line interface.")
    print("On macOS: brew install python-tk")
    print("On Ubuntu/Debian: sudo apt-get install python3-tk")
    print("On Windows: tkinter should be included with Python")

import time
import os
import threading
from algorithms import (
    Point,
    closest_pair_divide_conquer,
    closest_pair_brute_force,
    karatsuba_multiply,
    standard_multiply
)
from algorithms_visual import (
    closest_pair_divide_conquer_visual,
    karatsuba_multiply_visual
)


class DAAApplication:
    def __init__(self, root):
        self.root = root
        self.root.title("Divide and Conquer Algorithms - Interactive Visualization")
        self.root.geometry("1400x900")
        self.root.configure(bg='#f5f7fa')
        
        # Modern color scheme
        self.colors = {
            'bg': '#f5f7fa',
            'card': '#ffffff',
            'primary': '#667eea',
            'secondary': '#764ba2',
            'success': '#10b981',
            'info': '#3b82f6',
            'warning': '#f59e0b',
            'danger': '#ef4444',
            'text': '#2c3e50',
            'text_light': '#6b7280',
            'border': '#e5e7eb'
        }
        
        # Style configuration
        style = ttk.Style()
        style.theme_use('clam')
        
        # Configure modern styles
        style.configure('Title.TLabel', font=('Segoe UI', 18, 'bold'), background=self.colors['bg'])
        style.configure('Heading.TLabel', font=('Segoe UI', 12, 'bold'), background=self.colors['bg'])
        
        self.current_points = []
        self.current_file_data = None
        self.step_delay = 0.5
        self.is_running = False
        self.int_visualization_data = []  # Store visualization data for integer multiplication

        # Persistent visualization state for Closest Pair
        self.mid_lines = []              # Keep all divide lines to persist on plot
        self.left_pair = None            # Persist best pair from left recursion
        self.left_dist = None
        self.right_pair = None           # Persist best pair from right recursion
        self.right_dist = None

        # Karatsuba tree visualization state
        self.k_tree_nodes = {}   # id -> {id,label,type,level,parent,children:[ids],meta:{}}
        self.k_tree_stack = []   # stack of node ids representing current recursion path
        self.k_tree_next_id = 1

        # Karatsuba formula board state (root-level placeholders)
        self.k_board_state = {
            'num1': None, 'num2': None,
            'n': None, 'mid': None,
            'a': None, 'b': None, 'c': None, 'd': None,
            'ac': None, 'bd': None, 'ad_bc': None,
            'result': None,
            'active': None  # one of: 'split','ac','bd','ad_bc','result'
        }

        # Integer multiplication run controls/state
        self.int_pause_event = threading.Event()
        self.int_pause_event.set()  # not paused
        self.last_int_results = {}

        # Closest pair run controls/state
        self.cp_pause_event = threading.Event()
        self.cp_pause_event.set()  # not paused
        self.last_cp_results = {}

        self.create_widgets()
    
    def create_widgets(self):
        # Main title with gradient effect
        title_frame = tk.Frame(self.root, bg=self.colors['primary'], height=100)
        title_frame.pack(fill=tk.X, padx=0, pady=0)
        title_frame.pack_propagate(False)
        
        title_label = tk.Label(
            title_frame,
            text="🔬 Divide and Conquer Algorithms",
            font=('Segoe UI', 22, 'bold'),
            bg=self.colors['primary'],
            fg='white'
        )
        title_label.pack(pady=(12, 5))
        
        subtitle_label = tk.Label(
            title_frame,
            text="Interactive Visualization & Analysis Tool",
            font=('Segoe UI', 10),
            bg=self.colors['primary'],
            fg='#e8eaf6'
        )
        subtitle_label.pack(pady=(0, 3))
        
        credits_label = tk.Label(
            title_frame,
            text="Made by: M.Hassaan | Ebrahim Bin Moin | Usaid Shaikh",
            font=('Segoe UI', 9, 'italic'),
            bg=self.colors['primary'],
            fg='#cbd5e1'
        )
        credits_label.pack(pady=(0, 10))
        
        # Notebook for tabs
        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Footer with credits
        footer_frame = tk.Frame(self.root, bg=self.colors['primary'], height=30)
        footer_frame.pack(fill=tk.X, side=tk.BOTTOM, padx=0, pady=0)
        footer_frame.pack_propagate(False)
        
        footer_label = tk.Label(
            footer_frame,
            text="Made by: M.Hassaan | Ebrahim Bin Moin | Usaid Shaikh",
            font=('Segoe UI', 9),
            bg=self.colors['primary'],
            fg='white'
        )
        footer_label.pack(expand=True)
        
        # Closest Pair Tab
        self.create_closest_pair_tab()
        
        # Integer Multiplication Tab
        self.create_integer_multiplication_tab()
    
    def create_closest_pair_tab(self):
        # Closest Pair Frame
        closest_frame = tk.Frame(self.notebook, bg=self.colors['bg'])
        self.notebook.add(closest_frame, text="📍 Closest Pair of Points")
        
        # Left panel for controls
        left_panel = tk.Frame(closest_frame, bg=self.colors['card'], width=380, relief=tk.FLAT, bd=0)
        left_panel.pack(side=tk.LEFT, fill=tk.BOTH, padx=(0, 8), pady=8)
        left_panel.pack_propagate(False)
        
        # File selection with modern styling
        file_frame = tk.LabelFrame(left_panel, text="📁 File Selection", 
                                  bg=self.colors['card'], font=('Segoe UI', 10, 'bold'),
                                  fg=self.colors['text'], relief=tk.FLAT, bd=1)
        file_frame.pack(fill=tk.X, padx=12, pady=12)
        
        self.closest_file_var = tk.StringVar()
        file_entry = ttk.Entry(file_frame, textvariable=self.closest_file_var, state='readonly', width=30)
        file_entry.pack(side=tk.LEFT, padx=5, pady=5, fill=tk.X, expand=True)
        
        browse_btn = tk.Button(
            file_frame,
            text="📂 Browse",
            command=self.browse_closest_pair_file,
            bg=self.colors['primary'],
            fg='white',
            font=('Segoe UI', 9, 'bold'),
            relief=tk.FLAT,
            cursor='hand2',
            activebackground='#5568d3',
            padx=12,
            pady=6
        )
        browse_btn.pack(side=tk.LEFT, padx=6, pady=6)
        
        # Quick file selection
        quick_frame = tk.LabelFrame(left_panel, text="⚡ Quick Select", 
                                   bg=self.colors['card'], font=('Segoe UI', 10, 'bold'),
                                   fg=self.colors['text'], relief=tk.FLAT, bd=1)
        quick_frame.pack(fill=tk.X, padx=12, pady=12)
        
        self.quick_file_var = tk.StringVar()
        quick_combo = ttk.Combobox(quick_frame, textvariable=self.quick_file_var, state='readonly', width=30)
        quick_combo.pack(padx=5, pady=5, fill=tk.X)
        quick_combo.bind('<<ComboboxSelected>>', self.load_quick_closest_file)
        
        # Load available files
        self.load_closest_pair_files(quick_combo)
        
        # Info display
        info_frame = tk.LabelFrame(left_panel, text="ℹ️ File Information", 
                                  bg=self.colors['card'], font=('Segoe UI', 10, 'bold'),
                                  fg=self.colors['text'], relief=tk.FLAT, bd=1)
        info_frame.pack(fill=tk.X, padx=12, pady=12)
        
        self.info_text = tk.Text(info_frame, height=8, wrap=tk.WORD, 
                                 font=('Segoe UI', 9), bg='#f8f9fa',
                                 fg=self.colors['text'], relief=tk.FLAT, bd=0)
        self.info_text.pack(fill=tk.BOTH, expand=True, padx=6, pady=6)
        
        # Run button with modern styling
        run_btn = tk.Button(
            left_panel,
            text="▶ Run Algorithm",
            command=self.run_closest_pair,
            bg=self.colors['success'],
            fg='white',
            font=('Segoe UI', 12, 'bold'),
            relief=tk.FLAT,
            cursor='hand2',
            activebackground='#059669',
            height=2,
            pady=8
        )
        run_btn.pack(fill=tk.X, padx=12, pady=12)
        
        # Step-by-step display
        steps_frame = tk.LabelFrame(left_panel, text="📊 Algorithm Steps", 
                                   bg=self.colors['card'], font=('Segoe UI', 10, 'bold'),
                                   fg=self.colors['text'], relief=tk.FLAT, bd=1)
        steps_frame.pack(fill=tk.BOTH, expand=True, padx=12, pady=12)
        
        # Control buttons for step-by-step
        control_frame = tk.Frame(steps_frame, bg=self.colors['card'])
        control_frame.pack(fill=tk.X, padx=6, pady=6)
        
        self.step_delay_var = tk.DoubleVar(value=0.5)
        tk.Label(control_frame, text="⚙️ Speed:", bg=self.colors['card'], 
                font=('Segoe UI', 9), fg=self.colors['text']).pack(side=tk.LEFT, padx=4)
        delay_scale = tk.Scale(
            control_frame,
            from_=0.1,
            to=2.0,
            resolution=0.1,
            orient=tk.HORIZONTAL,
            variable=self.step_delay_var,
            length=120,
            bg=self.colors['card'],
            fg=self.colors['text'],
            troughcolor='#e5e7eb',
            activebackground=self.colors['primary']
        )
        delay_scale.pack(side=tk.LEFT, padx=4)
        # Speed info label and pause/resume
        self.cp_speed_label = tk.Label(control_frame, text="Delay ≈ 0.00s", bg=self.colors['card'], fg=self.colors['text'], font=('Segoe UI', 8))
        self.cp_speed_label.pack(side=tk.LEFT, padx=6)
        delay_scale.configure(command=self.on_closest_speed_change)

        self.cp_pause_btn = tk.Button(
            control_frame,
            text="Pause",
            command=self.toggle_cp_pause,
            bg=self.colors['warning'],
            fg='white',
            font=('Segoe UI', 9, 'bold'),
            relief=tk.FLAT,
            cursor='hand2',
            activebackground='#d97706',
            padx=10,
            pady=4
        )
        self.cp_pause_btn.pack(side=tk.RIGHT, padx=4)
        
        self.steps_text = scrolledtext.ScrolledText(
            steps_frame,
            height=10,
            wrap=tk.WORD,
            font=('Consolas', 9),
            bg='#1e293b',
            fg='#e2e8f0',
            insertbackground='white',
            relief=tk.FLAT,
            bd=0
        )
        self.steps_text.pack(fill=tk.BOTH, expand=True, padx=6, pady=6)
        # Scratchpad for closest pair
        cp_scratch = tk.LabelFrame(left_panel, text="🗃️ Scratchpad (distances)", 
                                   bg=self.colors['card'], font=('Segoe UI', 10, 'bold'),
                                   fg=self.colors['text'], relief=tk.FLAT, bd=1)
        cp_scratch.pack(fill=tk.BOTH, expand=False, padx=12, pady=(0, 12))
        cp_ctrl = tk.Frame(cp_scratch, bg=self.colors['card'])
        cp_ctrl.pack(fill=tk.X, padx=6, pady=(6, 0))
        tk.Label(cp_ctrl, text="Track δ, δL, δR, strip updates", bg=self.colors['card'], fg=self.colors['text'], font=('Segoe UI', 9)).pack(side=tk.LEFT)
        tk.Button(cp_ctrl, text="Clear", command=lambda: self.cp_storage_text.delete(1.0, tk.END),
                 bg=self.colors['danger'], fg='white', font=('Segoe UI', 9, 'bold'), relief=tk.FLAT,
                 padx=10, pady=4, cursor='hand2', activebackground='#dc2626').pack(side=tk.RIGHT)
        tk.Button(cp_ctrl, text="Copy", command=self.copy_cp_storage,
                 bg=self.colors['primary'], fg='white', font=('Segoe UI', 9, 'bold'), relief=tk.FLAT,
                 padx=10, pady=4, cursor='hand2', activebackground='#5568d3').pack(side=tk.RIGHT, padx=(0,6))
        self.cp_storage_text = scrolledtext.ScrolledText(
            cp_scratch,
            height=6,
            wrap=tk.WORD,
            font=('Consolas', 9),
            bg='#f8f9fa',
            fg=self.colors['text'],
            relief=tk.FLAT,
            bd=0
        )
        self.cp_storage_text.pack(fill=tk.BOTH, expand=True, padx=6, pady=6)
        
        # Results display
        results_frame = tk.LabelFrame(left_panel, text="✅ Final Results", 
                                     bg=self.colors['card'], font=('Segoe UI', 10, 'bold'),
                                     fg=self.colors['text'], relief=tk.FLAT, bd=1)
        results_frame.pack(fill=tk.BOTH, expand=True, padx=12, pady=12)
        
        self.results_text = scrolledtext.ScrolledText(
            results_frame,
            height=6,
            wrap=tk.WORD,
            font=('Consolas', 9),
            bg='#f8f9fa',
            fg=self.colors['text'],
            relief=tk.FLAT,
            bd=0
        )
        self.results_text.pack(fill=tk.BOTH, expand=True, padx=6, pady=6)
        # Copy buttons for final results
        cp_res_btns = tk.Frame(results_frame, bg=self.colors['card'])
        cp_res_btns.pack(fill=tk.X, padx=6, pady=(0, 6))
        tk.Button(cp_res_btns, text="Copy Distance", command=self.copy_closest_distance,
                  bg=self.colors['primary'], fg='white', font=('Segoe UI', 9, 'bold'),
                  relief=tk.FLAT, padx=8, pady=4, cursor='hand2', activebackground='#5568d3').pack(side=tk.LEFT)
        tk.Button(cp_res_btns, text="Copy Pair", command=self.copy_closest_pair,
                  bg=self.colors['secondary'], fg='white', font=('Segoe UI', 9, 'bold'),
                  relief=tk.FLAT, padx=8, pady=4, cursor='hand2', activebackground='#64748b').pack(side=tk.LEFT, padx=(6, 0))
        
        # Right panel for visualization
        right_panel = tk.Frame(closest_frame, bg=self.colors['card'], relief=tk.FLAT, bd=0)
        right_panel.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=(8, 8), pady=8)
        
        # Visualization title
        viz_title = tk.Label(right_panel, text="📈 Step-by-Step Visualization", 
                            font=('Segoe UI', 13, 'bold'), bg=self.colors['card'], 
                            fg=self.colors['text'])
        viz_title.pack(pady=(10, 5))
        
        # Matplotlib figure
        self.closest_fig = Figure(figsize=(10, 8), dpi=100, facecolor='#ffffff')
        self.closest_ax = self.closest_fig.add_subplot(111)
        self.closest_ax.set_title("Points Visualization", fontsize=13, fontweight='bold', 
                                 color=self.colors['text'], pad=15)
        self.closest_ax.set_xlabel("X Coordinate", fontsize=11, color=self.colors['text_light'])
        self.closest_ax.set_ylabel("Y Coordinate", fontsize=11, color=self.colors['text_light'])
        self.closest_ax.grid(True, alpha=0.3, color=self.colors['border'])
        self.closest_fig.patch.set_facecolor('#ffffff')
        
        self.closest_canvas = FigureCanvasTkAgg(self.closest_fig, right_panel)
        self.closest_canvas.draw()
        self.closest_canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
    
    def visualize_karatsuba(self, step_data=None):
        """Visualize Karatsuba algorithm step-by-step"""
        try:
            # Check if visualization components exist
            if not hasattr(self, 'int_ax') or not hasattr(self, 'int_canvas'):
                return
            
            self.int_ax.clear()
            self.int_ax.axis('off')
            
            if not step_data:
                self.int_ax.text(0.5, 0.5, 'Load numbers and run algorithm\nto see visualization', 
                                ha='center', va='center', fontsize=12, 
                                transform=self.int_ax.transAxes, color='#7f8c8d')
                self.int_canvas.draw()
                return
            
            # Draw current step visualization using formula board state
            step_type = step_data.get('step_type', '')
            st = getattr(self, 'k_board_state', {})
            active_slot = st.get('active')
            # Colors (active vs inactive)
            def box_color(base, active):
                return base if active else '#94a3b8'  # gray when inactive
            num1 = str(step_data.get('num1', '')) if step_data.get('num1') not in [None, ''] else ''
            num2 = str(step_data.get('num2', '')) if step_data.get('num2') not in [None, ''] else ''
            a = str(step_data.get('a', '')) if step_data.get('a') not in [None, ''] else ''
            b = str(step_data.get('b', '')) if step_data.get('b') not in [None, ''] else ''
            c = str(step_data.get('c', '')) if step_data.get('c') not in [None, ''] else ''
            d = str(step_data.get('d', '')) if step_data.get('d') not in [None, ''] else ''
            ac = str(step_data.get('ac', '')) if step_data.get('ac') not in [None, ''] else ''
            bd = str(step_data.get('bd', '')) if step_data.get('bd') not in [None, ''] else ''
            ad_bc = str(step_data.get('ad_bc', '')) if step_data.get('ad_bc') not in [None, ''] else ''
            result = str(step_data.get('result', '')) if step_data.get('result') not in [None, ''] else ''
            
            # Truncate long numbers for display
            def truncate(s, max_len=15):
                if not s:
                    return ''
                s = str(s)
                if len(s) > max_len:
                    return s[:max_len-3] + '...'
                return s
            
            num1 = truncate(num1, 20)
            num2 = truncate(num2, 20)
            a = truncate(a, 15)
            b = truncate(b, 15)
            c = truncate(c, 15)
            d = truncate(d, 15)
            ac = truncate(ac, 20)
            bd = truncate(bd, 20)
            ad_bc = truncate(ad_bc, 20)
            result = truncate(result, 25)
            
            y_pos = 0.9
            
            # Show main multiplication
            if st.get('num1') is not None and st.get('num2') is not None:
                num1 = truncate(st.get('num1'), 20)
                num2 = truncate(st.get('num2'), 20)
                main_text = f"{num1}\n  ×\n{num2}"
                self.int_ax.text(0.5, y_pos, main_text, ha='center', va='top',
                               fontsize=14, weight='bold',
                               bbox=dict(boxstyle='round,pad=1', facecolor='#667eea', alpha=0.9),
                               color='white', transform=self.int_ax.transAxes)
                y_pos -= 0.25
            
            # Show split (a,b,c,d)
            a = st.get('a'); b = st.get('b'); c = st.get('c'); d = st.get('d')
            mid = st.get('mid'); n = st.get('n')
            if all(v is not None for v in [a,b,c,d]):
                try:
                    b_len = len(str(b))
                    d_len = len(str(d))
                    split_text = f"Split:\nx = {a}×10^{b_len} + {b}\ny = {c}×10^{d_len} + {d}"
                    self.int_ax.text(0.5, y_pos, split_text, ha='center', va='top',
                                   fontsize=11,
                                   bbox=dict(boxstyle='round,pad=0.8', facecolor=box_color('#10b981', active_slot=='split'), alpha=0.9 if active_slot=='split' else 0.6),
                                   color='white', transform=self.int_ax.transAxes)
                    y_pos -= 0.2
                except Exception:
                    pass
            
            # Show formula placeholders and filled values
            ac_val = st.get('ac'); bd_val = st.get('bd'); adbc_val = st.get('ad_bc')
            if any(v is not None for v in [a,b,c,d,ac_val,bd_val,adbc_val]):
                lines = []
                if a is not None and c is not None:
                    lines.append((f"ac = {a} × {c} = {ac_val if ac_val is not None else '?'}", 'ac'))
                if b is not None and d is not None:
                    lines.append((f"bd = {b} × {d} = {bd_val if bd_val is not None else '?'}", 'bd'))
                if a is not None and b is not None and c is not None and d is not None:
                    lines.append((f"ad+bc = (a+b)(c+d) − ac − bd = {adbc_val if adbc_val is not None else '?'}", 'ad_bc'))
                if lines:
                    # Draw as a single box with dynamic highlight if any line is active
                    active = active_slot in ['ac','bd','ad_bc']
                    text = "\n".join([t for t,_ in lines])
                    self.int_ax.text(0.5, y_pos, text, ha='center', va='top', fontsize=10,
                                     bbox=dict(boxstyle='round,pad=0.6', facecolor=box_color('#f59e0b', active), alpha=0.9 if active else 0.6),
                                     color='white', transform=self.int_ax.transAxes)
                    y_pos -= 0.18
            
            # Show result
            res = st.get('result')
            if res is not None and n is not None and mid is not None:
                ac_str = str(ac_val) if ac_val is not None else 'ac'
                adbc_str = str(adbc_val) if adbc_val is not None else 'ad+bc'
                bd_str = str(bd_val) if bd_val is not None else 'bd'
                result_text = f"10^{n}·{ac_str} + 10^{mid}·({adbc_str}) + {bd_str} = {res}"
                self.int_ax.text(0.5, y_pos, result_text, ha='center', va='top',
                               fontsize=12, weight='bold',
                               bbox=dict(boxstyle='round,pad=0.8', facecolor=box_color('#ef4444', active_slot=='result'), alpha=0.95 if active_slot=='result' else 0.6),
                               color='white', transform=self.int_ax.transAxes)
            
            self.int_canvas.draw()
        except Exception as e:
            # Silently handle visualization errors to not break the algorithm
            import traceback
            print(f"Visualization error: {e}")
            traceback.print_exc()
    
    def visualize_karatsuba_safe(self, step_data=None):
        """Thread-safe wrapper for visualize_karatsuba"""
        def update_viz():
            self.visualize_karatsuba(step_data)
        self.root.after(0, update_viz)
    
    def create_integer_multiplication_tab(self):
        # Integer Multiplication Frame
        int_frame = tk.Frame(self.notebook, bg=self.colors['bg'])
        self.notebook.add(int_frame, text="🔢 Integer Multiplication")
        
        # Left panel for controls
        left_panel = tk.Frame(int_frame, bg=self.colors['card'], width=420, relief=tk.FLAT, bd=0)
        left_panel.pack(side=tk.LEFT, fill=tk.BOTH, padx=(0, 8), pady=8)
        left_panel.pack_propagate(False)
        
        # File selection
        file_frame = tk.LabelFrame(left_panel, text="📁 File Selection", 
                                  bg=self.colors['card'], font=('Segoe UI', 10, 'bold'),
                                  fg=self.colors['text'], relief=tk.FLAT, bd=1)
        file_frame.pack(fill=tk.X, padx=12, pady=12)
        
        self.int_file_var = tk.StringVar()
        file_entry = ttk.Entry(file_frame, textvariable=self.int_file_var, state='readonly', width=30)
        file_entry.pack(side=tk.LEFT, padx=5, pady=5, fill=tk.X, expand=True)
        
        browse_btn = tk.Button(
            file_frame,
            text="📂 Browse",
            command=self.browse_integer_mult_file,
            bg=self.colors['primary'],
            fg='white',
            font=('Segoe UI', 9, 'bold'),
            relief=tk.FLAT,
            cursor='hand2',
            activebackground='#5568d3',
            padx=12,
            pady=6
        )
        browse_btn.pack(side=tk.LEFT, padx=6, pady=6)
        
        # Quick file selection
        quick_frame = tk.LabelFrame(left_panel, text="⚡ Quick Select", 
                                   bg=self.colors['card'], font=('Segoe UI', 10, 'bold'),
                                   fg=self.colors['text'], relief=tk.FLAT, bd=1)
        quick_frame.pack(fill=tk.X, padx=12, pady=12)
        
        self.quick_int_var = tk.StringVar()
        quick_combo = ttk.Combobox(quick_frame, textvariable=self.quick_int_var, state='readonly', width=30)
        quick_combo.pack(padx=5, pady=5, fill=tk.X)
        quick_combo.bind('<<ComboboxSelected>>', self.load_quick_int_file)
        
        # Load available files
        self.load_integer_mult_files(quick_combo)
        
        # Input display
        input_frame = tk.LabelFrame(left_panel, text="🔢 Input Numbers", 
                                   bg=self.colors['card'], font=('Segoe UI', 10, 'bold'),
                                   fg=self.colors['text'], relief=tk.FLAT, bd=1)
        input_frame.pack(fill=tk.X, padx=12, pady=12)
        
        num1_frame = tk.Frame(input_frame, bg=self.colors['card'])
        num1_frame.pack(fill=tk.X, padx=6, pady=6)
        tk.Label(num1_frame, text="Number 1:", bg=self.colors['card'], 
                font=('Segoe UI', 9, 'bold'), fg=self.colors['text']).pack(side=tk.LEFT)
        self.num1_label = tk.Label(num1_frame, text="-", bg=self.colors['card'], 
                                   fg=self.colors['primary'], font=('Consolas', 9))
        self.num1_label.pack(side=tk.LEFT, padx=6)
        
        num2_frame = tk.Frame(input_frame, bg=self.colors['card'])
        num2_frame.pack(fill=tk.X, padx=6, pady=6)
        tk.Label(num2_frame, text="Number 2:", bg=self.colors['card'], 
                font=('Segoe UI', 9, 'bold'), fg=self.colors['text']).pack(side=tk.LEFT)
        self.num2_label = tk.Label(num2_frame, text="-", bg=self.colors['card'], 
                                   fg=self.colors['primary'], font=('Consolas', 9))
        self.num2_label.pack(side=tk.LEFT, padx=6)
        
        # Run button
        run_btn = tk.Button(
            left_panel,
            text="▶ Run Algorithm",
            command=self.run_integer_mult,
            bg=self.colors['success'],
            fg='white',
            font=('Segoe UI', 12, 'bold'),
            relief=tk.FLAT,
            cursor='hand2',
            activebackground='#059669',
            height=2,
            pady=8
        )
        run_btn.pack(fill=tk.X, padx=12, pady=12)
        
        # Step-by-step display
        steps_frame = tk.LabelFrame(left_panel, text="📊 Algorithm Steps", 
                                   bg=self.colors['card'], font=('Segoe UI', 10, 'bold'),
                                   fg=self.colors['text'], relief=tk.FLAT, bd=1)
        steps_frame.pack(fill=tk.BOTH, expand=True, padx=12, pady=12)
        
        # Control buttons for step-by-step
        control_frame = tk.Frame(steps_frame, bg=self.colors['card'])
        control_frame.pack(fill=tk.X, padx=6, pady=6)
        
        self.int_step_delay_var = tk.DoubleVar(value=0.3)
        tk.Label(control_frame, text="⚙️ Speed:", bg=self.colors['card'], 
                font=('Segoe UI', 9), fg=self.colors['text']).pack(side=tk.LEFT, padx=4)
        delay_scale = tk.Scale(
            control_frame,
            from_=0.1,
            to=2.0,
            resolution=0.1,
            orient=tk.HORIZONTAL,
            variable=self.int_step_delay_var,
            length=120,
            bg=self.colors['card'],
            fg=self.colors['text'],
            troughcolor='#e5e7eb',
            activebackground=self.colors['primary']
        )
        delay_scale.pack(side=tk.LEFT, padx=4)
        # Speed info label and pause/resume button
        self.int_speed_label = tk.Label(control_frame, text="Delay ≈ 1.8s", bg=self.colors['card'], fg=self.colors['text'], font=('Segoe UI', 8))
        self.int_speed_label.pack(side=tk.LEFT, padx=6)
        # Bind slider to update delay label
        delay_scale.configure(command=self.on_int_speed_change)

        self.int_pause_btn = tk.Button(
            control_frame,
            text="Pause",
            command=self.toggle_int_pause,
            bg=self.colors['warning'],
            fg='white',
            font=('Segoe UI', 9, 'bold'),
            relief=tk.FLAT,
            cursor='hand2',
            activebackground='#d97706',
            padx=10,
            pady=4
        )
        self.int_pause_btn.pack(side=tk.RIGHT, padx=4)

        # Follow-current-call toggle for formula board
        self.int_follow_var = tk.BooleanVar(value=True)
        follow_chk = ttk.Checkbutton(control_frame, text="Follow current call", variable=self.int_follow_var)
        follow_chk.pack(side=tk.LEFT, padx=8)
        
        self.int_steps_text = scrolledtext.ScrolledText(
            steps_frame,
            height=10,
            wrap=tk.WORD,
            font=('Consolas', 9),
            bg='#1e293b',
            fg='#e2e8f0',
            insertbackground='white',
            relief=tk.FLAT,
            bd=0
        )
        self.int_steps_text.pack(fill=tk.BOTH, expand=True, padx=6, pady=6)
        
        # Results display
        results_frame = tk.LabelFrame(left_panel, text="✅ Final Results", 
                                     bg=self.colors['card'], font=('Segoe UI', 10, 'bold'),
                                     fg=self.colors['text'], relief=tk.FLAT, bd=1)
        results_frame.pack(fill=tk.BOTH, expand=True, padx=12, pady=12)
        
        self.int_results_text = scrolledtext.ScrolledText(
            results_frame,
            height=6,
            wrap=tk.WORD,
            font=('Consolas', 9),
            bg='#f8f9fa',
            fg=self.colors['text'],
            relief=tk.FLAT,
            bd=0
        )
        self.int_results_text.pack(fill=tk.BOTH, expand=True, padx=6, pady=6)
        # Buttons to copy results
        res_btns = tk.Frame(results_frame, bg=self.colors['card'])
        res_btns.pack(fill=tk.X, padx=6, pady=(0, 6))
        tk.Button(res_btns, text="Copy Karatsuba", command=self.copy_karatsuba_result,
                  bg=self.colors['primary'], fg='white', font=('Segoe UI', 9, 'bold'),
                  relief=tk.FLAT, padx=8, pady=4, cursor='hand2', activebackground='#5568d3').pack(side=tk.LEFT)
        tk.Button(res_btns, text="Copy Standard", command=self.copy_standard_result,
                  bg=self.colors['secondary'], fg='white', font=('Segoe UI', 9, 'bold'),
                  relief=tk.FLAT, padx=8, pady=4, cursor='hand2', activebackground='#64748b').pack(side=tk.LEFT, padx=(6, 0))
        
        # Right panel for visualization and comparison
        right_panel = tk.Frame(int_frame, bg=self.colors['card'], relief=tk.FLAT, bd=0)
        right_panel.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=(8, 8), pady=8)
        
        # Visualization title
        viz_title = tk.Label(right_panel, text="📊 Karatsuba Algorithm Visualization", 
                            font=('Segoe UI', 13, 'bold'), bg=self.colors['card'], 
                            fg=self.colors['text'])
        viz_title.pack(pady=(10, 5))
        
        # Matplotlib figure for integer multiplication visualization
        self.int_fig = Figure(figsize=(10, 6), dpi=100, facecolor='#ffffff')
        self.int_ax = self.int_fig.add_subplot(111)
        self.int_ax.axis('off')
        self.int_ax.text(0.5, 0.5, 'Load numbers and run algorithm\nto see step-by-step visualization', 
                        ha='center', va='center', fontsize=13, 
                        transform=self.int_ax.transAxes, color='#7f8c8d',
                        weight='bold')
        self.int_fig.patch.set_facecolor('#ffffff')
        
        self.int_canvas = FigureCanvasTkAgg(self.int_fig, right_panel)
        self.int_canvas.draw()
        self.int_canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        # Scratchpad storage for interim numbers/results
        scratch_frame = tk.LabelFrame(right_panel, text="🗃️ Scratchpad (temporary storage)", 
                                      bg=self.colors['card'], font=('Segoe UI', 10, 'bold'),
                                      fg=self.colors['text'], relief=tk.FLAT, bd=1)
        scratch_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=(0, 10))

        # Controls for scratchpad
        sp_ctrl = tk.Frame(scratch_frame, bg=self.colors['card'])
        sp_ctrl.pack(fill=tk.X, padx=6, pady=(6, 0))
        tk.Label(sp_ctrl, text="Store sub-results here as they appear", bg=self.colors['card'],
                 fg=self.colors['text'], font=('Segoe UI', 9)).pack(side=tk.LEFT)
        clear_btn = tk.Button(sp_ctrl, text="Clear", command=lambda: self.int_storage_text.delete(1.0, tk.END),
                              bg=self.colors['danger'], fg='white', font=('Segoe UI', 9, 'bold'),
                              relief=tk.FLAT, padx=10, pady=4, cursor='hand2', activebackground='#dc2626')
        clear_btn.pack(side=tk.RIGHT)
        copy_btn = tk.Button(sp_ctrl, text="Copy", command=self.copy_int_storage,
                             bg=self.colors['primary'], fg='white', font=('Segoe UI', 9, 'bold'),
                             relief=tk.FLAT, padx=10, pady=4, cursor='hand2', activebackground='#5568d3')
        copy_btn.pack(side=tk.RIGHT, padx=(0, 6))
        save_btn = tk.Button(sp_ctrl, text="Save...", command=self.save_int_storage,
                             bg=self.colors['secondary'], fg='white', font=('Segoe UI', 9, 'bold'),
                             relief=tk.FLAT, padx=10, pady=4, cursor='hand2', activebackground='#64748b')
        save_btn.pack(side=tk.RIGHT, padx=(0, 6))

        self.int_storage_text = scrolledtext.ScrolledText(
            scratch_frame,
            height=8,
            wrap=tk.WORD,
            font=('Consolas', 9),
            bg='#f8f9fa',
            fg=self.colors['text'],
            relief=tk.FLAT,
            bd=0
        )
        self.int_storage_text.pack(fill=tk.BOTH, expand=True, padx=6, pady=6)
        
        # Results display area
        comparison_frame = tk.LabelFrame(right_panel, text="📈 Algorithm Comparison", 
                                        bg=self.colors['card'], font=('Segoe UI', 10, 'bold'),
                                        fg=self.colors['text'], relief=tk.FLAT, bd=1)
        comparison_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        self.comparison_text = scrolledtext.ScrolledText(
            comparison_frame,
            wrap=tk.WORD,
            font=('Consolas', 9),
            bg='#f8f9fa',
            fg=self.colors['text'],
            relief=tk.FLAT,
            bd=0
        )
        self.comparison_text.pack(fill=tk.BOTH, expand=True, padx=6, pady=6)
    
    def load_closest_pair_files(self, combo):
        """Load available closest pair input files"""
        files = []
        closest_dir = 'inputs/closest_pair'
        if os.path.exists(closest_dir):
            for filename in sorted(os.listdir(closest_dir)):
                if filename.endswith('.txt'):
                    files.append((filename, os.path.join(closest_dir, filename)))
        
        combo['values'] = [f[0] for f in files]
        self.closest_pair_files = dict(files)
    
    def load_integer_mult_files(self, combo):
        """Load available integer multiplication input files"""
        files = []
        int_dir = 'inputs/integer_multiplication'
        if os.path.exists(int_dir):
            for filename in sorted(os.listdir(int_dir)):
                if filename.endswith('.txt'):
                    files.append((filename, os.path.join(int_dir, filename)))
        
        combo['values'] = [f[0] for f in files]
        self.integer_mult_files = dict(files)
    
    def browse_closest_pair_file(self):
        """Browse for closest pair input file"""
        filename = filedialog.askopenfilename(
            title="Select Closest Pair Input File",
            filetypes=[("Text files", "*.txt"), ("All files", "*.*")]
        )
        if filename:
            self.closest_file_var.set(filename)
            self.load_closest_pair_file(filename)
    
    def load_quick_closest_file(self, event=None):
        """Load file from quick select combo"""
        selected = self.quick_file_var.get()
        if selected and selected in self.closest_pair_files:
            filepath = self.closest_pair_files[selected]
            self.closest_file_var.set(filepath)
            self.load_closest_pair_file(filepath)
    
    def load_closest_pair_file(self, filepath):
        """Load and parse closest pair input file"""
        try:
            with open(filepath, 'r') as f:
                lines = f.readlines()
            
            num_points = int(lines[0].strip())
            points = []
            for i in range(1, num_points + 1):
                x, y = map(float, lines[i].strip().split())
                points.append(Point(x, y))
            
            self.current_points = points
            self.current_file_data = {'type': 'closest_pair', 'points': points}
            
            # Update info
            self.info_text.delete(1.0, tk.END)
            self.info_text.insert(tk.END, f"File: {os.path.basename(filepath)}\n")
            self.info_text.insert(tk.END, f"Number of Points: {num_points}\n\n")
            self.info_text.insert(tk.END, f"X Range: [{min(p.x for p in points):.2f}, {max(p.x for p in points):.2f}]\n")
            self.info_text.insert(tk.END, f"Y Range: [{min(p.y for p in points):.2f}, {max(p.y for p in points):.2f}]\n")
            
            # Visualize points
            self.visualize_points(points)
            
            messagebox.showinfo("Success", f"Loaded {num_points} points from file")
            
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load file: {str(e)}")
    
    def browse_integer_mult_file(self):
        """Browse for integer multiplication input file"""
        filename = filedialog.askopenfilename(
            title="Select Integer Multiplication Input File",
            filetypes=[("Text files", "*.txt"), ("All files", "*.*")]
        )
        if filename:
            self.int_file_var.set(filename)
            self.load_integer_mult_file(filename)
    
    def load_quick_int_file(self, event=None):
        """Load file from quick select combo"""
        selected = self.quick_int_var.get()
        if selected and selected in self.integer_mult_files:
            filepath = self.integer_mult_files[selected]
            self.int_file_var.set(filepath)
            self.load_integer_mult_file(filepath)
    
    def load_integer_mult_file(self, filepath):
        """Load and parse integer multiplication input file"""
        try:
            with open(filepath, 'r') as f:
                lines = f.readlines()
            
            num1 = int(lines[0].strip())
            num2 = int(lines[1].strip())
            
            self.current_file_data = {'type': 'integer_multiplication', 'num1': num1, 'num2': num2}
            
            # Update labels (truncate if too long)
            num1_str = str(num1)
            num2_str = str(num2)
            if len(num1_str) > 50:
                num1_str = num1_str[:47] + "..."
            if len(num2_str) > 50:
                num2_str = num2_str[:47] + "..."
            
            self.num1_label.config(text=f"{num1_str} ({len(str(num1))} digits)")
            self.num2_label.config(text=f"{num2_str} ({len(str(num2))} digits)")
            
            messagebox.showinfo("Success", f"Loaded numbers:\nNumber 1: {len(str(num1))} digits\nNumber 2: {len(str(num2))} digits")
            
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load file: {str(e)}")
    
    def visualize_points(self, points, highlight_pair=None, left_points=None, right_points=None, 
                         mid_line=None, strip_points=None, current_checking=None,
                         left_pair=None, left_dist=None, right_pair=None, right_dist=None,
                         strip_width=None):
        """Visualize points on the plot with step-by-step highlights (thread-safe)"""
        def update_plot():
            try:
                self.closest_ax.clear()
                
                if not points:
                    self.closest_canvas.draw()
                    return
                
                # Update persistent mid-lines and left/right pairs if provided
                if mid_line is not None and mid_line not in self.mid_lines:
                    self.mid_lines.append(mid_line)
                if left_pair is not None:
                    self.left_pair = left_pair
                    self.left_dist = left_dist
                if right_pair is not None:
                    self.right_pair = right_pair
                    self.right_dist = right_dist

                # Plot all points
                xs = [p.x for p in points]
                ys = [p.y for p in points]
                self.closest_ax.scatter(xs, ys, c='#667eea', s=30, alpha=0.4, label='All Points', zorder=1)

                # Shade strip band if width provided
                if mid_line is not None and strip_width is not None:
                    left_x = mid_line - strip_width
                    right_x = mid_line + strip_width
                    self.closest_ax.axvspan(left_x, right_x, color='#93c5fd', alpha=0.2, zorder=0)
                    # annotate δ near top
                    try:
                        ymin, ymax = min(ys), max(ys)
                        self.closest_ax.text(mid_line, ymax, f"δ ≈ {strip_width:.4f}", ha='center', va='bottom',
                                             fontsize=9, color='#1f2937',
                                             bbox=dict(boxstyle='round,pad=0.2', facecolor='white', alpha=0.6))
                    except Exception:
                        pass
                
                # Highlight left half
                if left_points:
                    lxs = [p.x for p in left_points]
                    lys = [p.y for p in left_points]
                    self.closest_ax.scatter(lxs, lys, c='#28a745', s=50, alpha=0.7, label='Left Half', zorder=2)
                
                # Highlight right half
                if right_points:
                    rxs = [p.x for p in right_points]
                    rys = [p.y for p in right_points]
                    self.closest_ax.scatter(rxs, rys, c='#ffc107', s=50, alpha=0.7, label='Right Half', zorder=2)
                
                # Draw all persistent dividing lines in a muted color
                if self.mid_lines:
                    for xline in self.mid_lines:
                        # If this line is the current focus, we'll draw a highlighted version below
                        if mid_line is not None and abs(xline - mid_line) < 1e-12:
                            continue
                        self.closest_ax.axvline(x=xline, color='#9ca3af', linestyle='--', linewidth=1.5,
                                                alpha=0.6, zorder=2)

                # Draw the currently active dividing line in a distinct color to differentiate
                if mid_line is not None:
                    self.closest_ax.axvline(x=mid_line, color='#ef4444', linestyle='--', linewidth=2.5,
                                            alpha=0.9, label='Current Divide', zorder=3)
                
                # Highlight strip points
                if strip_points:
                    sxs = [p.x for p in strip_points]
                    sys = [p.y for p in strip_points]
                    self.closest_ax.scatter(sxs, sys, c='#dc3545', s=80, alpha=0.8, marker='s', 
                                           label='Strip Points', zorder=4)
                
                # Highlight currently checking pair
                if current_checking:
                    p1, p2 = current_checking
                    self.closest_ax.scatter([p1.x, p2.x], [p1.y, p2.y], c='red', s=150, marker='*', 
                                          label='Checking', zorder=5)
                    self.closest_ax.plot([p1.x, p2.x], [p1.y, p2.y], 'r-', linewidth=3, alpha=0.9, zorder=4)
                
                # Persistently draw best pairs from left and right halves with labels δL and δR
                def annotate_delta(p1, p2, text, color):
                    mx = (p1.x + p2.x) / 2.0
                    my = (p1.y + p2.y) / 2.0
                    self.closest_ax.annotate(text, (mx, my), xytext=(5, 5), textcoords='offset points',
                                             fontsize=9, color='white',
                                             bbox=dict(boxstyle='round,pad=0.3', facecolor=color, alpha=0.8),
                                             zorder=7)

                if self.left_pair and isinstance(self.left_pair, tuple):
                    lp1, lp2 = self.left_pair
                    self.closest_ax.plot([lp1.x, lp2.x], [lp1.y, lp2.y], color='#10b981', linewidth=2.5,
                                         alpha=0.9, zorder=6, label='Left δL')
                    label_text = f"δL = {self.left_dist:.4f}" if self.left_dist is not None else "δL"
                    annotate_delta(lp1, lp2, label_text, '#10b981')

                if self.right_pair and isinstance(self.right_pair, tuple):
                    rp1, rp2 = self.right_pair
                    self.closest_ax.plot([rp1.x, rp2.x], [rp1.y, rp2.y], color='#f59e0b', linewidth=2.5,
                                         alpha=0.9, zorder=6, label='Right δR')
                    label_text = f"δR = {self.right_dist:.4f}" if self.right_dist is not None else "δR"
                    annotate_delta(rp1, rp2, label_text, '#f59e0b')

                # Highlight closest pair if provided
                if highlight_pair:
                    p1, p2 = highlight_pair
                    self.closest_ax.scatter([p1.x, p2.x], [p1.y, p2.y], c='red', s=200, marker='*', 
                                          label='Closest Pair', zorder=6, edgecolors='black', linewidths=2)
                    self.closest_ax.plot([p1.x, p2.x], [p1.y, p2.y], 'r--', linewidth=3, alpha=0.9, zorder=5)
                
                self.closest_ax.set_title("Step-by-Step Visualization", fontsize=12, fontweight='bold')
                self.closest_ax.set_xlabel("X Coordinate")
                self.closest_ax.set_ylabel("Y Coordinate")
                self.closest_ax.grid(True, alpha=0.3)
                # Compose legend conditionally
                if left_points or right_points or strip_points or highlight_pair or self.mid_lines or self.left_pair or self.right_pair:
                    # Guard against duplicate labels by using handles/labels
                    handles, labels = self.closest_ax.get_legend_handles_labels()
                    by_label = dict(zip(labels, handles))
                    self.closest_ax.legend(by_label.values(), by_label.keys(), loc='upper right', fontsize=8)
                
                self.closest_canvas.draw()
            except Exception as e:
                print(f"Visualization error: {e}")
        
        self.root.after(0, update_plot)
    
    def add_step_message(self, text_widget, message, tag='info'):
        """Add a step message to the steps text widget (thread-safe)"""
        def update_gui():
            try:
                text_widget.insert(tk.END, message + "\n", tag)
                text_widget.see(tk.END)
            except:
                pass
        self.root.after(0, update_gui)

    def add_cp_storage_message(self, message):
        """Append a message to the closest pair scratchpad (thread-safe)"""
        def update_gui():
            try:
                if hasattr(self, 'cp_storage_text'):
                    self.cp_storage_text.insert(tk.END, message + "\n")
                    self.cp_storage_text.see(tk.END)
            except:
                pass
        self.root.after(0, update_gui)
    
    def run_closest_pair(self):
        """Run closest pair algorithm with step-by-step visualization"""
        if not self.current_points:
            messagebox.showwarning("Warning", "Please load a file first")
            return
        
        if self.is_running:
            messagebox.showinfo("Info", "Algorithm is already running")
            return
        
        self.is_running = True
        
        # Clear previous steps and results
        self.steps_text.delete(1.0, tk.END)
        self.results_text.delete(1.0, tk.END)
        if hasattr(self, 'cp_storage_text'):
            self.cp_storage_text.delete(1.0, tk.END)
        # Ensure not paused and reset button label
        try:
            self.cp_pause_event.set()
            if hasattr(self, 'cp_pause_btn'):
                self.cp_pause_btn.config(text="Pause")
        except Exception:
            pass
        # Reset persistent visualization state
        self.mid_lines = []
        self.left_pair = None
        self.left_dist = None
        self.right_pair = None
        self.right_dist = None
        
        # Configure text colors
        self.steps_text.tag_configure('info', foreground='#4ec9b0')
        self.steps_text.tag_configure('divide', foreground='#569cd6')
        self.steps_text.tag_configure('conquer', foreground='#ce9178')
        self.steps_text.tag_configure('combine', foreground='#dcdcaa')
        self.steps_text.tag_configure('result', foreground='#4fc1ff')
        self.steps_text.tag_configure('highlight', foreground='#ff6b6b')
        
        def step_callback(step_type, data):
            """Callback function for each algorithm step"""
            # Pause support
            try:
                self.cp_pause_event.wait()
            except Exception:
                pass
            # Speed mapping: higher speed -> lower delay
            try:
                speed_val = float(self.step_delay_var.get())
            except Exception:
                speed_val = 0.5
            delay = max(0.05, round(2.1 - max(0.1, min(2.0, speed_val)), 3))
            time.sleep(delay)
            
            message = data.get('message', '')
            tag = 'info'
            
            if step_type == 'init':
                tag = 'info'
                self.add_step_message(self.steps_text, f"▶ {message}", tag)
                self.visualize_points(self.current_points)
                
            elif step_type == 'divide_start':
                tag = 'divide'
                self.add_step_message(self.steps_text, f"\n{'='*60}\n{message}", tag)
                
            elif step_type == 'base_case':
                tag = 'conquer'
                self.add_step_message(self.steps_text, f"  {message}", tag)
                
            elif step_type == 'base_result':
                tag = 'result'
                self.add_step_message(self.steps_text, f"  ✓ {message}", tag)
                if 'pair' in data:
                    self.visualize_points(data['points'], highlight_pair=data['pair'])
                    
            elif step_type == 'divide':
                tag = 'divide'
                self.add_step_message(self.steps_text, f"  {message}", tag)
                left = data.get('left_points', [])
                right = data.get('right_points', [])
                mid_x = data.get('mid_x')
                self.visualize_points(self.current_points, left_points=left, 
                                    right_points=right, mid_line=mid_x)
                
            elif step_type in ['conquer_left', 'conquer_right']:
                tag = 'conquer'
                self.add_step_message(self.steps_text, f"  {message}", tag)
                
            elif step_type in ['conquer_left_result', 'conquer_right_result']:
                tag = 'result'
                self.add_step_message(self.steps_text, f"  ✓ {message}", tag)
                # Persistently draw δL or δR with labels
                if step_type == 'conquer_left_result':
                    self.visualize_points(self.current_points, left_pair=data.get('pair'), left_dist=data.get('distance'))
                    if data.get('distance') is not None and data.get('pair') is not None:
                        p = data.get('pair')
                        self.add_cp_storage_message(f"δL = {data.get('distance'):.4f}  pair=(({p[0].x:.2f},{p[0].y:.2f}),({p[1].x:.2f},{p[1].y:.2f}))")
                else:
                    self.visualize_points(self.current_points, right_pair=data.get('pair'), right_dist=data.get('distance'))
                    if data.get('distance') is not None and data.get('pair') is not None:
                        p = data.get('pair')
                        self.add_cp_storage_message(f"δR = {data.get('distance'):.4f}  pair=(({p[0].x:.2f},{p[0].y:.2f}),({p[1].x:.2f},{p[1].y:.2f}))")
                
            elif step_type == 'min_compare':
                tag = 'combine'
                self.add_step_message(self.steps_text, f"  {message}", tag)
                # Scratchpad note
                ld = data.get('left_distance'); rd = data.get('right_distance'); md = data.get('min_distance')
                self.add_cp_storage_message(f"min(δL={ld:.4f}, δR={rd:.4f}) = {md:.4f}")
                
            elif step_type == 'strip_identify':
                tag = 'combine'
                self.add_step_message(self.steps_text, f"  {message}", tag)
                strip = data.get('strip_points', [])
                mid_x = data.get('mid_point', Point(0, 0)).x
                self.visualize_points(self.current_points, strip_points=strip, mid_line=mid_x, strip_width=data.get('strip_width'))
                
            elif step_type == 'strip_check':
                tag = 'combine'
                checking = data.get('checking')
                if checking:
                    self.visualize_points(self.current_points, current_checking=checking)
                    
            elif step_type == 'strip_update':
                tag = 'highlight'
                self.add_step_message(self.steps_text, f"  ⚡ {message}", tag)
                if 'new_pair' in data:
                    self.visualize_points(self.current_points, highlight_pair=data['new_pair'])
                nd = data.get('new_distance')
                if nd is not None:
                    self.add_cp_storage_message(f"strip improved: δ = {nd:.4f}")
                    
            elif step_type == 'combine_result':
                tag = 'result'
                self.add_step_message(self.steps_text, f"  ✓ {message}", tag)
                if 'final_pair' in data:
                    self.visualize_points(self.current_points, highlight_pair=data['final_pair'])
                fd = data.get('final_distance')
                if fd is not None:
                    self.add_cp_storage_message(f"final δ = {fd:.4f}")
        
        def run_algorithm():
            try:
                # Run algorithm with visualization
                start_time = time.time()
                distance, pair = closest_pair_divide_conquer_visual(
                    self.current_points, 
                    step_callback=step_callback,
                    delay=self.step_delay_var.get()
                )
                execution_time = (time.time() - start_time) * 1000
            
                # Compare with brute force if small enough
                brute_time = None
                if len(self.current_points) <= 100:
                    start_brute = time.time()
                    brute_dist, brute_pair = closest_pair_brute_force(self.current_points)
                    brute_time = (time.time() - start_brute) * 1000
                
                # Display final results (thread-safe)
                def update_results():
                    try:
                        self.last_cp_results = {
                            'distance': distance,
                            'pair': pair
                        }
                        self.results_text.delete(1.0, tk.END)
                        self.results_text.insert(tk.END, "=" * 50 + "\n")
                        self.results_text.insert(tk.END, "CLOSEST PAIR RESULTS\n")
                        self.results_text.insert(tk.END, "=" * 50 + "\n\n")
                        self.results_text.insert(tk.END, f"Number of Points: {len(self.current_points)}\n")
                        self.results_text.insert(tk.END, f"Closest Distance: {distance:.6f}\n\n")
                        self.results_text.insert(tk.END, f"Point 1: ({pair[0].x:.2f}, {pair[0].y:.2f})\n")
                        self.results_text.insert(tk.END, f"Point 2: ({pair[1].x:.2f}, {pair[1].y:.2f})\n\n")
                        self.results_text.insert(tk.END, f"Execution Time: {execution_time:.4f} ms\n")
                        if brute_time:
                            self.results_text.insert(tk.END, f"Brute Force Time: {brute_time:.4f} ms\n")
                            speedup = brute_time / execution_time if execution_time > 0 else 0
                            self.results_text.insert(tk.END, f"Speedup: {speedup:.2f}x\n")
                        
                        # Final visualization
                        self.visualize_points(self.current_points, highlight_pair=pair)
                        self.add_step_message(self.steps_text, f"\n{'='*60}\n✓ Algorithm Complete!", 'result')
                    except Exception as e:
                        print(f"Error updating results: {e}")
                
                self.root.after(0, update_results)
                
            except Exception as e:
                def show_error():
                    try:
                        messagebox.showerror("Error", f"Algorithm failed: {str(e)}")
                        self.add_step_message(self.steps_text, f"\n✗ Error: {str(e)}", 'highlight')
                    except:
                        print(f"Error: {str(e)}")
                self.root.after(0, show_error)
            finally:
                def set_not_running():
                    self.is_running = False
                self.root.after(0, set_not_running)
        
        # Run in separate thread to avoid blocking GUI
        thread = threading.Thread(target=run_algorithm, daemon=True)
        thread.start()
    
    def add_int_step_message(self, text_widget, message, tag='info'):
        """Add a step message to the integer multiplication steps text widget (thread-safe)"""
        def update_gui():
            try:
                text_widget.insert(tk.END, message + "\n", tag)
                text_widget.see(tk.END)
            except:
                pass
        self.root.after(0, update_gui)

    def add_int_storage_message(self, message):
        """Append a message to the integer multiplication scratchpad (thread-safe)"""
        def update_gui():
            try:
                if hasattr(self, 'int_storage_text'):
                    self.int_storage_text.insert(tk.END, message + "\n")
                    self.int_storage_text.see(tk.END)
            except:
                pass
        self.root.after(0, update_gui)

    def on_closest_speed_change(self, value):
        """Update closest pair speed label with computed delay mapping."""
        try:
            speed = float(value)
        except Exception:
            speed = 0.5
        delay = max(0.05, round(2.1 - max(0.1, min(2.0, speed)), 3))
        if hasattr(self, 'cp_speed_label'):
            self.cp_speed_label.config(text=f"Delay ≈ {delay:.2f}s")

    def toggle_cp_pause(self):
        """Pause/resume closest pair visualization."""
        if self.cp_pause_event.is_set():
            self.cp_pause_event.clear()
            try:
                self.cp_pause_btn.config(text="Resume")
            except Exception:
                pass
        else:
            self.cp_pause_event.set()
            try:
                self.cp_pause_btn.config(text="Pause")
            except Exception:
                pass

    def copy_cp_storage(self):
        try:
            content = self.cp_storage_text.get(1.0, tk.END)
            self.root.clipboard_clear()
            self.root.clipboard_append(content)
        except Exception:
            pass

    def copy_closest_distance(self):
        try:
            val = self.last_cp_results.get('distance')
            if val is not None:
                self.root.clipboard_clear()
                self.root.clipboard_append(f"{val:.6f}")
        except Exception:
            pass

    def copy_closest_pair(self):
        try:
            pair = self.last_cp_results.get('pair')
            if pair is not None:
                s = f"({pair[0].x:.6f},{pair[0].y:.6f}) , ({pair[1].x:.6f},{pair[1].y:.6f})"
                self.root.clipboard_clear()
                self.root.clipboard_append(s)
        except Exception:
            pass

    def on_int_speed_change(self, value):
        """Update the speed info label to reflect the computed delay."""
        try:
            speed = float(value)
        except Exception:
            speed = 0.5
        delay = max(0.05, round(2.1 - max(0.1, min(2.0, speed)), 3))
        if hasattr(self, 'int_speed_label'):
            self.int_speed_label.config(text=f"Delay ≈ {delay:.2f}s")

    def toggle_int_pause(self):
        """Pause/resume the integer multiplication visualization."""
        if self.int_pause_event.is_set():
            # Pause
            self.int_pause_event.clear()
            try:
                self.int_pause_btn.config(text="Resume")
            except Exception:
                pass
        else:
            # Resume
            self.int_pause_event.set()
            try:
                self.int_pause_btn.config(text="Pause")
            except Exception:
                pass

    def copy_int_storage(self):
        try:
            content = self.int_storage_text.get(1.0, tk.END)
            self.root.clipboard_clear()
            self.root.clipboard_append(content)
        except Exception:
            pass

    def save_int_storage(self):
        try:
            content = self.int_storage_text.get(1.0, tk.END)
            filename = filedialog.asksaveasfilename(
                title="Save Scratchpad",
                defaultextension=".txt",
                filetypes=[("Text files", "*.txt"), ("All files", "*.*")]
            )
            if filename:
                with open(filename, 'w', encoding='utf-8') as f:
                    f.write(content)
        except Exception:
            pass

    def copy_karatsuba_result(self):
        try:
            val = self.last_int_results.get('karatsuba')
            if val is not None:
                self.root.clipboard_clear()
                self.root.clipboard_append(str(val))
        except Exception:
            pass

    def copy_standard_result(self):
        try:
            val = self.last_int_results.get('standard')
            if val is not None:
                self.root.clipboard_clear()
                self.root.clipboard_append(str(val))
        except Exception:
            pass
    
    def run_integer_mult(self):
        """Run integer multiplication algorithm with step-by-step visualization"""
        if not self.current_file_data or self.current_file_data['type'] != 'integer_multiplication':
            messagebox.showwarning("Warning", "Please load a file first")
            return
        
        if self.is_running:
            messagebox.showinfo("Info", "Algorithm is already running")
            return
        
        self.is_running = True
        
        # Clear previous steps and results
        self.int_steps_text.delete(1.0, tk.END)
        self.int_results_text.delete(1.0, tk.END)
        self.comparison_text.delete(1.0, tk.END)
        if hasattr(self, 'int_storage_text'):
            self.int_storage_text.delete(1.0, tk.END)
        # Ensure running state not paused and reset button label
        try:
            self.int_pause_event.set()
            if hasattr(self, 'int_pause_btn'):
                self.int_pause_btn.config(text="Pause")
        except Exception:
            pass
        
        # Configure text colors
        self.int_steps_text.tag_configure('info', foreground='#4ec9b0')
        self.int_steps_text.tag_configure('split', foreground='#569cd6')
        self.int_steps_text.tag_configure('recursive', foreground='#ce9178')
        self.int_steps_text.tag_configure('combine', foreground='#dcdcaa')
        self.int_steps_text.tag_configure('result', foreground='#4fc1ff')
        self.int_steps_text.tag_configure('highlight', foreground='#ff6b6b')
        
        def step_callback(step_type, data):
            """Callback function for each algorithm step"""
            # Block if paused
            try:
                self.int_pause_event.wait()
            except Exception:
                pass
            # Map slider (speed) to delay so higher value -> faster animation
            try:
                speed_val = float(self.int_step_delay_var.get())
            except Exception:
                speed_val = 0.5
            # Reverse within [0.1, 2.0] to a delay in the same bounds
            delay = max(0.05, round(2.1 - max(0.1, min(2.0, speed_val)), 3))
            time.sleep(delay)
            
            message = data.get('message', '')
            tag = 'info'
            
            # Prepare visualization data
            viz_data = {'step_type': step_type}
            viz_data.update(data)

            # Update formula board state (root-level only)
            st = self.k_board_state
            if step_type == 'init':
                st.update({'num1': data.get('num1'), 'num2': data.get('num2'),
                           'n': None, 'mid': None, 'a': None, 'b': None, 'c': None, 'd': None,
                           'ac': None, 'bd': None, 'ad_bc': None, 'result': None, 'active': None})
            elif step_type == 'normalize':
                # If following current call, update n each time; else only set once
                if self.int_follow_var.get() or st.get('n') is None:
                    st['n'] = data.get('n')
            elif step_type == 'split':
                if self.int_follow_var.get() or st.get('a') is None:
                    st.update({'a': data.get('a'), 'b': data.get('b'), 'c': data.get('c'), 'd': data.get('d'), 'mid': data.get('mid')})
                    st['ac'] = None; st['bd'] = None; st['ad_bc'] = None; st['result'] = None
                st['active'] = 'split'
            elif step_type == 'recursive_ac':
                st['active'] = 'ac'
            elif step_type == 'recursive_ac_result':
                # Accept if matches current context
                if st.get('a') == data.get('a') and st.get('c') == data.get('c'):
                    st['ac'] = data.get('ac')
                    st['active'] = None
            elif step_type == 'recursive_bd':
                st['active'] = 'bd'
            elif step_type == 'recursive_bd_result':
                if st.get('b') == data.get('b') and st.get('d') == data.get('d'):
                    st['bd'] = data.get('bd')
                    st['active'] = None
            elif step_type == 'recursive_ad_bc':
                st['active'] = 'ad_bc'
            elif step_type == 'recursive_ad_bc_result':
                # Match current split context
                if st.get('a') == data.get('a') and st.get('b') == data.get('b') and st.get('c') == data.get('c') and st.get('d') == data.get('d'):
                    st['ad_bc'] = data.get('ad_bc')
                    st['active'] = None
            elif step_type == 'combine':
                # Prefer following the current call; otherwise update only if it matches root context
                if self.int_follow_var.get():
                    st.update({'a': data.get('a'), 'b': data.get('b'), 'c': data.get('c'), 'd': data.get('d'),
                               'n': data.get('n'), 'mid': data.get('mid'),
                               'ac': data.get('ac'), 'bd': data.get('bd'), 'ad_bc': data.get('ad_bc'),
                               'result': data.get('result'), 'active': 'result'})
                else:
                    if st.get('n') == data.get('n') and st.get('mid') == data.get('mid') and \
                       st.get('a') == data.get('a') and st.get('b') == data.get('b') and \
                       st.get('c') == data.get('c') and st.get('d') == data.get('d'):
                        st.update({'ac': data.get('ac'), 'bd': data.get('bd'), 'ad_bc': data.get('ad_bc'),
                                   'result': data.get('result'), 'active': 'result'})
            
            if step_type == 'init':
                tag = 'info'
                self.add_int_step_message(self.int_steps_text, f"▶ {message}", tag)
                self.visualize_karatsuba_safe(viz_data)
                
            elif step_type == 'normalize':
                tag = 'split'
                self.add_int_step_message(self.int_steps_text, f"  {message}", tag)
                self.visualize_karatsuba_safe(viz_data)
                
            elif step_type == 'split':
                tag = 'split'
                self.add_int_step_message(self.int_steps_text, f"\n{'='*60}\n  {message}", tag)
                self.visualize_karatsuba_safe(viz_data)
                
            elif step_type in ['recursive_ac', 'recursive_bd', 'recursive_ad_bc']:
                tag = 'recursive'
                self.add_int_step_message(self.int_steps_text, f"  → {message}", tag)
                self.visualize_karatsuba_safe(viz_data)
                
            elif step_type in ['recursive_ac_result', 'recursive_bd_result', 'recursive_ad_bc_result']:
                tag = 'result'
                self.add_int_step_message(self.int_steps_text, f"    ✓ {message}", tag)
                self.visualize_karatsuba_safe(viz_data)
                # Store sub-results in scratchpad
                if step_type == 'recursive_ac_result':
                    a_val, c_val, ac_val = data.get('a'), data.get('c'), data.get('ac')
                    self.add_int_storage_message(f"ac = {a_val} × {c_val} = {ac_val}")
                elif step_type == 'recursive_bd_result':
                    b_val, d_val, bd_val = data.get('b'), data.get('d'), data.get('bd')
                    self.add_int_storage_message(f"bd = {b_val} × {d_val} = {bd_val}")
                elif step_type == 'recursive_ad_bc_result':
                    a_val, b_val, c_val, d_val, ad_val = data.get('a'), data.get('b'), data.get('c'), data.get('d'), data.get('ad_bc')
                    self.add_int_storage_message(f"ad+bc = (a+b)(c+d) − ac − bd = {ad_val}  [a={a_val}, b={b_val}, c={c_val}, d={d_val}]")
                
            elif step_type == 'base_case':
                tag = 'recursive'
                self.add_int_step_message(self.int_steps_text, f"    {message}", tag)
                self.visualize_karatsuba_safe(viz_data)
                
            elif step_type == 'base_result':
                tag = 'result'
                self.add_int_step_message(self.int_steps_text, f"    ✓ {message}", tag)
                self.visualize_karatsuba_safe(viz_data)
                # Store base sub-result
                self.add_int_storage_message(f"base: {data.get('num1')} × {data.get('num2')} = {data.get('result')}")
                
            elif step_type == 'combine':
                tag = 'combine'
                self.add_int_step_message(self.int_steps_text, f"\n  {message}", tag)
                self.visualize_karatsuba_safe(viz_data)
                # Store final combine for this context
                a, b, c, d = data.get('a'), data.get('b'), data.get('c'), data.get('d')
                ac, bd, adbc = data.get('ac'), data.get('bd'), data.get('ad_bc')
                n, mid, res = data.get('n'), data.get('mid'), data.get('result')
                self.add_int_storage_message(f"combine: 10^{n}·{ac} + 10^{mid}·({adbc}) + {bd} = {res}")
        
        def run_algorithm():
            try:
                num1 = self.current_file_data['num1']
                num2 = self.current_file_data['num2']
                # Run Karatsuba with visualization (compact board)
                start_karatsuba = time.time()
                karatsuba_result = karatsuba_multiply_visual(
                    num1,
                    num2,
                    step_callback=step_callback,
                    delay=self.int_step_delay_var.get()
                )
                karatsuba_time = (time.time() - start_karatsuba) * 1000
                # Run standard multiplication (quick, no visualization)
                start_standard = time.time()
                standard_result = standard_multiply(num1, num2)
                standard_time = (time.time() - start_standard) * 1000
                # Verify correctness
                is_correct = (karatsuba_result == standard_result)
                def update_results():
                    try:
                        # store last results for copy buttons
                        self.last_int_results = {
                            'karatsuba': karatsuba_result,
                            'standard': standard_result
                        }
                        self.int_results_text.delete(1.0, tk.END)
                        self.int_results_text.insert(tk.END, "=" * 50 + "\n")
                        self.int_results_text.insert(tk.END, "INTEGER MULTIPLICATION RESULTS\n")
                        self.int_results_text.insert(tk.END, "=" * 50 + "\n\n")
                        self.int_results_text.insert(tk.END, f"Number 1: {len(str(num1))} digits\n")
                        self.int_results_text.insert(tk.END, f"Number 2: {len(str(num2))} digits\n\n")
                        self.int_results_text.insert(tk.END, f"Karatsuba Result: {karatsuba_result}\n\n")
                        self.int_results_text.insert(tk.END, f"Standard Result: {standard_result}\n\n")
                        self.int_results_text.insert(tk.END, f"Correctness: {'✓ CORRECT' if is_correct else '✗ INCORRECT'}\n\n")
                        self.int_results_text.insert(tk.END, f"Karatsuba Time: {karatsuba_time:.4f} ms\n")
                        self.int_results_text.insert(tk.END, f"Standard Time: {standard_time:.4f} ms\n")
                        if standard_time > 0:
                            speedup = standard_time / karatsuba_time if karatsuba_time > 0 else 0
                            self.int_results_text.insert(tk.END, f"Speedup: {speedup:.2f}x\n")
                        # Display comparison
                        self.comparison_text.delete(1.0, tk.END)
                        self.comparison_text.insert(tk.END, "ALGORITHM COMPARISON\n")
                        self.comparison_text.insert(tk.END, "=" * 50 + "\n\n")
                        self.comparison_text.insert(tk.END, f"Input Size: {len(str(num1))} × {len(str(num2))} digits\n\n")
                        self.comparison_text.insert(tk.END, f"Karatsuba Algorithm:\n")
                        self.comparison_text.insert(tk.END, f"  Time: {karatsuba_time:.4f} ms\n")
                        self.comparison_text.insert(tk.END, f"  Complexity: O(n^log2(3)) ≈ O(n^1.585)\n\n")
                        self.comparison_text.insert(tk.END, f"Standard Multiplication:\n")
                        self.comparison_text.insert(tk.END, f"  Time: {standard_time:.4f} ms\n")
                        self.comparison_text.insert(tk.END, f"  Complexity: O(n²)\n\n")
                        if standard_time > 0 and karatsuba_time > 0:
                            speedup = standard_time / karatsuba_time if karatsuba_time > 0 else 0
                            self.comparison_text.insert(tk.END, f"Performance: Karatsuba is {speedup:.2f}x {'faster' if speedup > 1 else 'slower'}\n")
                        self.add_int_step_message(self.int_steps_text, f"\n{'='*60}\n✓ Algorithm Complete!", 'result')
                    except Exception as e:
                        print(f"Error updating results: {e}")
                self.root.after(0, update_results)
            except Exception as e:
                def show_error():
                    try:
                        messagebox.showerror("Error", f"Algorithm failed: {str(e)}")
                        self.add_int_step_message(self.int_steps_text, f"\n✗ Error: {str(e)}", 'highlight')
                    except:
                        print(f"Error: {str(e)}")
                self.root.after(0, show_error)
            finally:
                def set_not_running():
                    self.is_running = False
                self.root.after(0, set_not_running)

        # Run in separate thread to avoid blocking GUI
        thread = threading.Thread(target=run_algorithm, daemon=True)
        thread.start()


def main():
    if not TKINTER_AVAILABLE:
        print("\n" + "=" * 70)
        print("ERROR: tkinter is not available on this system")
        print("=" * 70)
        print("\nTo install tkinter:")
        print("  macOS: brew install python-tk")
        print("  Ubuntu/Debian: sudo apt-get install python3-tk")
        print("  Windows: tkinter should be included with Python")
        print("\nAlternatively, use the command-line interface:")
        print("  python3 run_demo.py")
        print("=" * 70 + "\n")
        return
    
    root = tk.Tk()
    app = DAAApplication(root)
    root.mainloop()


if __name__ == "__main__":
    main()

