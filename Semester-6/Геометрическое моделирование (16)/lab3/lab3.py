import tkinter as tk
from tkinter import ttk, messagebox
import math

# ── Константы ─────────────────────────────────────────────────────────────
CANVAS2D_W = 480
CANVAS2D_H = 440
CANVAS3D_W = 620
CANVAS3D_H = 540
POINT_R    = 6
HIT_R      = 12
GRID_STEP  = 40

COLOR_DARK    = "#1d2d44"
COLOR_BG      = "#f0f4f8"
COLOR_GRID    = "#dde3ec"
COLOR_LINE    = "#2c7be5"
COLOR_POINT   = "#e63946"
COLOR_HOVER   = "#ff9f43"
COLOR_AXIS    = "#00b300"
COLOR_VISIBLE = "#4fc3f7"
COLOR_HIDDEN  = "#334455"
COLOR_FACE    = "#1e4a7a"


# ── Матричная арифметика (4×4, колонки-major) ──────────────────────────────

def mat_identity():
    return [[1,0,0,0],[0,1,0,0],[0,0,1,0],[0,0,0,1]]

def mat_mul(A, B):
    C = [[0]*4 for _ in range(4)]
    for i in range(4):
        for j in range(4):
            C[i][j] = sum(A[i][k]*B[k][j] for k in range(4))
    return C

def mat_transform_pt(M, p):
    """Apply 4×4 matrix to (x,y,z) → returns (x,y,z)."""
    x,y,z = p
    w = M[3][0]*x + M[3][1]*y + M[3][2]*z + M[3][3]
    return (
        (M[0][0]*x + M[0][1]*y + M[0][2]*z + M[0][3]) / w,
        (M[1][0]*x + M[1][1]*y + M[1][2]*z + M[1][3]) / w,
        (M[2][0]*x + M[2][1]*y + M[2][2]*z + M[2][3]) / w,
    )

def mat_rot_x(a):
    c,s = math.cos(a), math.sin(a)
    return [[1,0,0,0],[0,c,-s,0],[0,s,c,0],[0,0,0,1]]

def mat_rot_y(a):
    c,s = math.cos(a), math.sin(a)
    return [[c,0,s,0],[0,1,0,0],[-s,0,c,0],[0,0,0,1]]

def mat_rot_z(a):
    c,s = math.cos(a), math.sin(a)
    return [[c,-s,0,0],[s,c,0,0],[0,0,1,0],[0,0,0,1]]

def mat_translate(tx,ty,tz):
    m = mat_identity()
    m[0][3],m[1][3],m[2][3] = tx,ty,tz
    return m

def mat_scale(sx,sy,sz):
    m = mat_identity()
    m[0][0],m[1][1],m[2][2] = sx,sy,sz
    return m


# ── Вспомогательные vec3-функции ──────────────────────────────────────────

def v3_sub(a,b):  return (a[0]-b[0], a[1]-b[1], a[2]-b[2])
def v3_add(a,b):  return (a[0]+b[0], a[1]+b[1], a[2]+b[2])
def v3_scale(a,s): return (a[0]*s, a[1]*s, a[2]*s)
def v3_dot(a,b):  return a[0]*b[0]+a[1]*b[1]+a[2]*b[2]
def v3_cross(a,b):
    return (a[1]*b[2]-a[2]*b[1], a[2]*b[0]-a[0]*b[2], a[0]*b[1]-a[1]*b[0])
def v3_norm(a):
    d = math.sqrt(v3_dot(a,a))
    return (a[0]/d, a[1]/d, a[2]/d) if d > 1e-10 else (0,0,0)

def rodrigues(p, axis_n, angle):
    """Rotate 3D point p around unit-vector axis_n by angle (Rodrigues)."""
    c,s = math.cos(angle), math.sin(angle)
    k   = axis_n
    dot = v3_dot(k, p)
    crs = v3_cross(k, p)
    return (
        p[0]*c + crs[0]*s + k[0]*dot*(1-c),
        p[1]*c + crs[1]*s + k[1]*dot*(1-c),
        p[2]*c + crs[2]*s + k[2]*dot*(1-c),
    )


# ── Проекция ───────────────────────────────────────────────────────────────

def perspective_proj(pts3d, cx, cy, cam_z=700, focal=400):
    result = []
    for (x,y,z) in pts3d:
        zc = cam_z - z
        if zc < 0.1: zc = 0.1
        xp = focal * x / zc + cx
        yp = -focal * y / zc + cy
        result.append((xp, yp, zc))
    return result

def face_normal_z(vp):
    """Cross-product Z of first triangle of a face in screen-space."""
    ax,ay = vp[1][0]-vp[0][0], vp[1][1]-vp[0][1]
    bx,by = vp[2][0]-vp[0][0], vp[2][1]-vp[0][1]
    return ax*by - ay*bx


# ── Главное приложение ─────────────────────────────────────────────────────

class App:
    def __init__(self, root):
        self.root = root
        root.title("Лаб. 3 — 3D-преобразования  |  Вариант 16")
        root.configure(bg=COLOR_DARK)
        root.resizable(False, False)

        self.pts2d = []          # list of [x, y]
        self._hover_idx = None
        self._drag_idx  = None

        self.verts_base = []     # list of (x,y,z) — исходные вершины
        self.faces      = []     # list of [i0,i1,i2,i3]
        self.model_built = False

        self.transform  = mat_identity()   # накопленные преобразования
        self._view      = mat_identity()   # вращение обзора мышью
        self._drag_xy   = None

        self.render_mode = tk.StringVar(value="wire")

        self._build_ui()

    # ─────────────────────────── UI ───────────────────────────────────────

    def _build_ui(self):
        tk.Label(self.root,
                 text="Лабораторная работа №3  |  Тело вращения (вариант 16)",
                 font=("Arial",13,"bold"), bg=COLOR_DARK, fg="white", pady=6
                 ).pack(fill=tk.X)

        body = tk.Frame(self.root, bg=COLOR_DARK)
        body.pack(padx=8, pady=4)

        # ── Левая панель: 2D ──────────────────────────────────────────────
        left = tk.Frame(body, bg=COLOR_DARK)
        left.grid(row=0, column=0, padx=6, sticky="n")

        tk.Label(left, text="Ввод 2D-контура (ЛКМ — точка, ПКМ — удалить)",
                 bg=COLOR_DARK, fg="white", font=("Arial",9)).pack()

        self.c2 = tk.Canvas(left, width=CANVAS2D_W, height=CANVAS2D_H,
                             bg=COLOR_BG, cursor="crosshair")
        self.c2.pack()
        self.c2.bind("<Button-1>",        self._click2d)
        self.c2.bind("<Button-3>",        self._rclick2d)
        self.c2.bind("<B1-Motion>",       self._drag2d)
        self.c2.bind("<ButtonRelease-1>", lambda e: setattr(self, "_drag_idx", None))
        self.c2.bind("<Motion>",          self._motion2d)
        self.c2.bind("<Leave>",           lambda e: self._set_hover(None))

        br = tk.Frame(left, bg=COLOR_DARK); br.pack(pady=4)
        tk.Button(br, text="Построить 3D", font=("Arial",10,"bold"),
                  bg="#2dc653", fg="white", relief=tk.FLAT,
                  command=self._build_3d).pack(side=tk.LEFT, padx=4)
        tk.Button(br, text="Очистить", font=("Arial",10),
                  bg="#e63946", fg="white", relief=tk.FLAT,
                  command=self._clear_all).pack(side=tk.LEFT, padx=4)

        sr = tk.Frame(left, bg=COLOR_DARK); sr.pack()
        tk.Label(sr, text="Шаг (°):", bg=COLOR_DARK, fg="white",
                 font=("Arial",9)).pack(side=tk.LEFT)
        self.step_var = tk.StringVar(value="30")
        tk.Entry(sr, textvariable=self.step_var, width=5).pack(side=tk.LEFT, padx=4)

        tk.Label(left, text="Точки контура:", bg=COLOR_DARK, fg="white",
                 font=("Arial",9)).pack(anchor="w")
        tf = tk.Frame(left, bg=COLOR_DARK); tf.pack(fill=tk.BOTH)
        self.tbl = ttk.Treeview(tf, columns=("n","x","y"), show="headings", height=5)
        for col,txt,w in [("n","№",30),("x","X",80),("y","Y",80)]:
            self.tbl.heading(col, text=txt)
            self.tbl.column(col, width=w, anchor="center")
        self.tbl.pack(side=tk.LEFT)
        ttk.Scrollbar(tf, orient=tk.VERTICAL, command=self.tbl.yview
                      ).pack(side=tk.RIGHT, fill=tk.Y)

        # ── Правая панель: 3D ─────────────────────────────────────────────
        right = tk.Frame(body, bg=COLOR_DARK)
        right.grid(row=0, column=1, padx=6, sticky="n")

        tk.Label(right, text="3D-вид  (перетащи мышь для вращения)",
                 bg=COLOR_DARK, fg="white", font=("Arial",9)).pack()

        self.c3 = tk.Canvas(right, width=CANVAS3D_W, height=CANVAS3D_H, bg="#07101e")
        self.c3.pack()
        self.c3.bind("<Button-1>",        lambda e: setattr(self,"_drag_xy",(e.x,e.y)))
        self.c3.bind("<B1-Motion>",       self._view_drag)
        self.c3.bind("<ButtonRelease-1>", lambda e: setattr(self,"_drag_xy",None))

        mr = tk.Frame(right, bg=COLOR_DARK); mr.pack(pady=3, fill=tk.X)
        tk.Label(mr, text="Режим:", bg=COLOR_DARK, fg="white",
                 font=("Arial",9)).pack(side=tk.LEFT, padx=4)
        for val,lbl in [("wire","Каркас"),("solid","Реалистичный")]:
            tk.Radiobutton(mr, text=lbl, variable=self.render_mode, value=val,
                           command=self._redraw3d, bg=COLOR_DARK, fg="white",
                           selectcolor="#333").pack(side=tk.LEFT, padx=2)

        # Преобразования
        xf = tk.LabelFrame(right, text="Преобразования", bg=COLOR_DARK,
                            fg="white", font=("Arial",9,"bold"), padx=6, pady=4)
        xf.pack(fill=tk.X, padx=4, pady=4)

        params = [
            ("Перемещение X:", "tx","0"),  ("Y:", "ty","0"),  ("Z:", "tz","0"),
            ("Поворот X (°):", "rx","0"),  ("Y(°):","ry","0"),("Z(°):","rz","0"),
            ("Масштаб X:",     "sx","1"),  ("Y:", "sy","1"),  ("Z:", "sz","1"),
        ]
        self._xv = {}
        for i,(lbl,key,dflt) in enumerate(params):
            r,col = divmod(i,3)
            tk.Label(xf, text=lbl, bg=COLOR_DARK, fg="white",
                     font=("Arial",8)).grid(row=r*2, column=col, sticky="w", padx=2)
            v = tk.StringVar(value=dflt)
            self._xv[key] = v
            tk.Entry(xf, textvariable=v, width=6,
                     font=("Arial",8)).grid(row=r*2+1, column=col, padx=2, pady=1)

        br2 = tk.Frame(right, bg=COLOR_DARK); br2.pack(pady=4)
        tk.Button(br2, text="Применить", font=("Arial",10,"bold"),
                  bg="#2c7be5", fg="white", relief=tk.FLAT,
                  command=self._apply_xf).pack(side=tk.LEFT, padx=4)
        tk.Button(br2, text="Сброс", font=("Arial",10),
                  bg="#888", fg="white", relief=tk.FLAT,
                  command=self._reset_xf).pack(side=tk.LEFT, padx=4)

        self._redraw2d()
        self._redraw3d()

    # ─────────────────────────── 2D ───────────────────────────────────────

    def _w2s(self, x, y):   return x+CANVAS2D_W//2, CANVAS2D_H//2-y
    def _s2w(self, sx, sy): return sx-CANVAS2D_W//2, CANVAS2D_H//2-sy

    def _nearest(self, sx, sy):
        for i,(x,y) in enumerate(self.pts2d):
            scx,scy = self._w2s(x,y)
            if math.hypot(sx-scx, sy-scy) <= HIT_R:
                return i
        return None

    def _click2d(self, e):
        idx = self._nearest(e.x, e.y)
        if idx is not None:
            self._drag_idx = idx
            return
        wx,wy = self._s2w(e.x,e.y)
        self.pts2d.append([wx,wy])
        self._refresh_table(); self._redraw2d()

    def _rclick2d(self, e):
        idx = self._nearest(e.x, e.y)
        if idx is not None:
            self.pts2d.pop(idx)
            self._refresh_table(); self._redraw2d()

    def _drag2d(self, e):
        if self._drag_idx is not None:
            wx,wy = self._s2w(e.x,e.y)
            self.pts2d[self._drag_idx] = [wx,wy]
            self._refresh_table(); self._redraw2d()

    def _motion2d(self, e):
        idx = self._nearest(e.x, e.y)
        if idx != self._hover_idx:
            self._set_hover(idx)

    def _set_hover(self, idx):
        self._hover_idx = idx; self._redraw2d()

    def _redraw2d(self):
        c = self.c2; c.delete("all")
        for gx in range(0, CANVAS2D_W, GRID_STEP):
            c.create_line(gx,0,gx,CANVAS2D_H, fill=COLOR_GRID)
        for gy in range(0, CANVAS2D_H, GRID_STEP):
            c.create_line(0,gy,CANVAS2D_W,gy, fill=COLOR_GRID)
        mx,my = CANVAS2D_W//2, CANVAS2D_H//2
        c.create_line(0,my,CANVAS2D_W,my, fill="#bbb", dash=(4,4))
        c.create_line(mx,0,mx,CANVAS2D_H, fill="#bbb", dash=(4,4))

        if len(self.pts2d) >= 2:
            for i in range(len(self.pts2d)-1):
                x0,y0 = self._w2s(*self.pts2d[i])
                x1,y1 = self._w2s(*self.pts2d[i+1])
                c.create_line(x0,y0,x1,y1, fill=COLOR_LINE, width=2)
            # ось (первая-последняя)
            xa,ya = self._w2s(*self.pts2d[0])
            xb,yb = self._w2s(*self.pts2d[-1])
            c.create_line(xa,ya,xb,yb, fill=COLOR_AXIS, width=2, dash=(6,3))
            c.create_text((xa+xb)//2+8,(ya+yb)//2-8,
                          text="ось", fill=COLOR_AXIS, font=("Arial",8))

        for i,(x,y) in enumerate(self.pts2d):
            sx,sy = self._w2s(x,y)
            col = COLOR_HOVER if i==self._hover_idx else COLOR_POINT
            c.create_oval(sx-POINT_R,sy-POINT_R,sx+POINT_R,sy+POINT_R,
                          fill=col, outline="white", width=2)
            c.create_text(sx+POINT_R+4,sy-POINT_R-4,
                          text=f"P{i+1}({x:.0f},{y:.0f})",
                          fill=COLOR_DARK, font=("Arial",7))

    def _refresh_table(self):
        self.tbl.delete(*self.tbl.get_children())
        for i,(x,y) in enumerate(self.pts2d):
            self.tbl.insert("","end",values=(i+1,f"{x:.1f}",f"{y:.1f}"))

    # ─────────────────────────── Build 3D ─────────────────────────────────

    def _build_3d(self):
        if len(self.pts2d) < 2:
            messagebox.showwarning("Внимание","Нужно минимум 2 точки!"); return
        try:
            step_deg = float(self.step_var.get())
            if not (1 <= step_deg <= 180): raise ValueError
        except ValueError:
            messagebox.showwarning("Ошибка","Шаг — число от 1 до 180."); return

        pts = self.pts2d
        p0 = (pts[0][0], pts[0][1], 0.0)
        p1 = (pts[-1][0], pts[-1][1], 0.0)
        axis_raw = v3_sub(p1, p0)
        if v3_dot(axis_raw,axis_raw) < 1e-12:
            messagebox.showwarning("Ошибка","Первая и последняя точки совпадают."); return
        axis_n = v3_norm(axis_raw)

        n_steps = round(360 / step_deg)
        angles  = [math.radians(i * step_deg) for i in range(n_steps)]

        inner = pts[1:-1]   # промежуточные точки контура

        verts = [p0, p1]    # индексы 0 и 1 — полюса оси
        v_p0, v_p1 = 0, 1

        rings = []
        for a in angles:
            ring = []
            for pt in inner:
                p = v3_sub((pt[0], pt[1], 0.0), p0)
                rotated = rodrigues(p, axis_n, a)
                v3d = v3_add(rotated, p0)
                ring.append(len(verts))
                verts.append(v3d)
            rings.append(ring)

        faces = []
        n_rings = len(rings)
        n_inner = len(inner)

        if n_inner > 0:
            for a in range(n_rings):
                b = (a+1) % n_rings
                for i in range(n_inner-1):
                    faces.append([rings[a][i], rings[a][i+1],
                                  rings[b][i+1], rings[b][i]])
                # шапки
                faces.append([v_p0, rings[a][0], rings[b][0], v_p0])
                faces.append([v_p1, rings[a][-1], rings[b][-1], v_p1])

        self.verts_base  = verts
        self.faces       = faces
        self.model_built = True
        self.transform   = mat_identity()
        self._view       = mat_identity()
        self._redraw3d()

    # ─────────────────────────── 3D render ────────────────────────────────

    def _transformed_verts(self):
        M = mat_mul(self._view, self.transform)
        return [mat_transform_pt(M, v) for v in self.verts_base]

    def _redraw3d(self):
        c = self.c3; c.delete("all")
        cx,cy = CANVAS3D_W//2, CANVAS3D_H//2
        if not self.model_built:
            c.create_text(cx,cy, text="Постройте 3D-фигуру →",
                          fill="#335", font=("Arial",14)); return

        verts3 = self._transformed_verts()
        proj   = perspective_proj(verts3, cx, cy)

        # Оси координат
        axes_pts = [(0,0,0),(50,0,0),(0,50,0),(0,0,50)]
        axes_xf  = [mat_transform_pt(self._view, p) for p in axes_pts]
        ap       = perspective_proj(axes_xf, cx, cy)
        for i,(col,lbl) in enumerate([(  "#f55","X"),("#5f5","Y"),("#55f","Z")],1):
            c.create_line(ap[0][0],ap[0][1], ap[i][0],ap[i][1], fill=col, width=2)
            c.create_text(ap[i][0]+5,ap[i][1], text=lbl, fill=col, font=("Arial",9,"bold"))

        if self.render_mode.get() == "solid":
            self._draw_solid(c, proj)
        else:
            self._draw_wire(c, proj)

    def _draw_wire(self, c, proj):
        drawn = set()
        for face in self.faces:
            n = len(face)
            for k in range(n):
                i0,i1 = face[k], face[(k+1)%n]
                edge = (min(i0,i1), max(i0,i1))
                if edge in drawn: continue
                drawn.add(edge)
                c.create_line(proj[i0][0],proj[i0][1],
                               proj[i1][0],proj[i1][1],
                               fill=COLOR_VISIBLE, width=1)

    def _draw_solid(self, c, proj):
        # Painter's algorithm
        face_list = []
        for face in self.faces:
            vp = [proj[i] for i in face]
            avg_z = sum(v[2] for v in vp) / len(vp)
            face_list.append((avg_z, face, vp))
        face_list.sort(key=lambda x: -x[0])

        for _,face,vp in face_list:
            unique = list(dict.fromkeys(face))  # deduplicate preserving order
            if len(unique) < 3: continue
            nz = face_normal_z([proj[i] for i in unique])
            if nz >= 0: continue               # back-face culled
            coords = []
            for i in unique:
                coords.extend([proj[i][0], proj[i][1]])
            # Simple shading by depth
            avg_z = sum(proj[i][2] for i in unique) / len(unique)
            shade = max(0, min(255, int(220 - avg_z * 0.15)))
            fill  = f"#{shade//3:02x}{shade//2:02x}{shade:02x}"
            c.create_polygon(coords, fill=fill, outline=COLOR_VISIBLE, width=1)

    # ─────────────────────────── View drag ────────────────────────────────

    def _view_drag(self, e):
        if self._drag_xy is None: return
        dx = e.x - self._drag_xy[0]
        dy = e.y - self._drag_xy[1]
        self._drag_xy = (e.x, e.y)
        ry = mat_rot_y(math.radians(dx * 0.5))
        rx = mat_rot_x(math.radians(dy * 0.5))
        self._view = mat_mul(mat_mul(rx, ry), self._view)
        if self.model_built: self._redraw3d()

    # ─────────────────────────── Transforms ───────────────────────────────

    def _apply_xf(self):
        if not self.model_built: return
        try:
            tx = float(self._xv["tx"].get()); ty = float(self._xv["ty"].get())
            tz = float(self._xv["tz"].get())
            rx = math.radians(float(self._xv["rx"].get()))
            ry = math.radians(float(self._xv["ry"].get()))
            rz = math.radians(float(self._xv["rz"].get()))
            sx = float(self._xv["sx"].get()); sy = float(self._xv["sy"].get())
            sz = float(self._xv["sz"].get())
        except ValueError:
            messagebox.showwarning("Ошибка","Проверьте поля преобразований."); return

        M = mat_mul(mat_translate(tx,ty,tz),
            mat_mul(mat_rot_x(rx),
            mat_mul(mat_rot_y(ry),
            mat_mul(mat_rot_z(rz),
                    mat_scale(sx,sy,sz)))))
        self.transform = mat_mul(M, self.transform)
        self._redraw3d()

    def _reset_xf(self):
        self.transform = mat_identity()
        self._view     = mat_identity()
        self._redraw3d()

    # ─────────────────────────── Clear ────────────────────────────────────

    def _clear_all(self):
        self.pts2d.clear()
        self.model_built = False
        self.verts_base  = []
        self.faces       = []
        self._refresh_table()
        self._redraw2d()
        self._redraw3d()


def main():
    root = tk.Tk()
    App(root)
    root.mainloop()


if __name__ == "__main__":
    main()
