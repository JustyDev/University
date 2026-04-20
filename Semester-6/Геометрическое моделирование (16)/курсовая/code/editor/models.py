import uuid
from dataclasses import dataclass, field

from .config import DEFAULT_FILL, DEFAULT_OUTLINE
from .geometry import arc_from_three_points, arc_points_from_three, distance, flatten


@dataclass
class GraphicObject:
    kind: str
    points: list
    outline: str = DEFAULT_OUTLINE
    fill: str = DEFAULT_FILL
    fill_type: str = "none"
    width: int = 2
    obj_id: str = field(default_factory=lambda: uuid.uuid4().hex)
    canvas_ids: list = field(default_factory=list)

    def to_dict(self):
        return {
            "kind": self.kind,
            "points": self.points,
            "outline": self.outline,
            "fill": self.fill,
            "fill_type": self.fill_type,
            "width": self.width,
            "obj_id": self.obj_id,
        }

    @staticmethod
    def from_dict(data):
        return GraphicObject(
            kind=data["kind"],
            points=[tuple(p) for p in data["points"]],
            outline=data.get("outline", DEFAULT_OUTLINE),
            fill=data.get("fill", DEFAULT_FILL),
            fill_type=data.get("fill_type", "none"),
            width=data.get("width", 2),
            obj_id=data.get("obj_id", uuid.uuid4().hex),
        )

    def is_closed(self):
        if self.kind == "circle":
            return True
        if self.kind == "polyline" and len(self.points) >= 3:
            return distance(self.points[0], self.points[-1]) < 8
        return False

    def display_fill(self):
        return self.fill if self.is_closed() and self.fill_type != "none" else ""

    def stipple(self):
        if self.fill_type == "light":
            return "gray25"
        if self.fill_type == "medium":
            return "gray50"
        if self.fill_type == "dense":
            return "gray75"
        return ""

    def draw(self, canvas):
        self.canvas_ids.clear()
        if self.kind == "line":
            self._draw_line(canvas)
        elif self.kind == "circle":
            self._draw_circle(canvas)
        elif self.kind == "arc":
            self._draw_arc(canvas)
        elif self.kind == "polyline":
            self._draw_polyline(canvas)

        for item in self.canvas_ids:
            canvas.addtag_withtag(self.obj_id, item)

    def _draw_line(self, canvas):
        item = canvas.create_line(
            *flatten(self.points),
            fill=self.outline,
            width=self.width,
            capstyle="round",
        )
        self.canvas_ids.append(item)

    def _draw_circle(self, canvas):
        center, edge = self.points
        r = distance(center, edge)
        item = canvas.create_oval(
            center[0] - r,
            center[1] - r,
            center[0] + r,
            center[1] + r,
            outline=self.outline,
            fill=self.display_fill(),
            stipple=self.stipple(),
            width=self.width,
        )
        self.canvas_ids.append(item)

    def _draw_arc(self, canvas):
        arc = arc_from_three_points(*self.points)
        if arc:
            center, radius, start, extent = arc
            item = canvas.create_arc(
                center[0] - radius,
                center[1] - radius,
                center[0] + radius,
                center[1] + radius,
                start=start,
                extent=extent,
                style="arc",
                outline=self.outline,
                width=self.width,
            )
        else:
            item = canvas.create_line(*flatten([self.points[0], self.points[-1]]), fill=self.outline, width=self.width)
        self.canvas_ids.append(item)

    def _draw_polyline(self, canvas):
        segments = self.polyline_render_points()
        if self.is_closed():
            item = canvas.create_polygon(
                *flatten(segments),
                outline=self.outline,
                fill=self.display_fill(),
                stipple=self.stipple(),
                width=self.width,
            )
        else:
            item = canvas.create_line(
                *flatten(segments),
                fill=self.outline,
                width=self.width,
                capstyle="round",
                joinstyle="round",
            )
        self.canvas_ids.append(item)

    def polyline_render_points(self):
        if len(self.points) < 2:
            return self.points

        result = [self.points[0]]
        i = 0
        # Alternation: line p0-p1, arc p1-p2-p3, line p3-p4, arc p4-p5-p6...
        while i < len(self.points) - 1:
            if (i % 3) == 0:
                result.append(self.points[i + 1])
                i += 1
            elif i + 2 < len(self.points):
                arc_pts = arc_points_from_three(self.points[i], self.points[i + 1], self.points[i + 2])
                result.extend(arc_pts[1:])
                i += 2
            else:
                result.append(self.points[i + 1])
                i += 1
        return result

