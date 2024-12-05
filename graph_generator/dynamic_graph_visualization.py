# Copyright 2024 Nicholas Fleischhauer
# SPDX-License-Identifier: GPL-3.0-or-later

import argparse
from typing import Any, Dict, List, Tuple
from manim import *
import numpy as np
import os

class Node(VGroup):
    def __init__(self, label: str, position: np.ndarray, radius: float = 0.3, **kwargs: Any) -> None:
        super().__init__(**kwargs)
        self.label = label
        self.position = position
        self.radius = radius
        self.circle = Circle(radius=radius, color=GREEN, fill_opacity=0.8)
        self.circle.move_to(position)
        self.text = Text(label).move_to(position)
        self.add(self.circle, self.text)
        
    def get_center(self) -> np.ndarray:
        return self.circle.get_center()

class Edge(VMobject):
    def __init__(self, u: Node, v: Node, curvature: float = 0.2, radius: float = 0.3, **kwargs: Any) -> None:
        super().__init__(**kwargs)
        self.u = u
        self.v = v
        self.curvature = curvature
        self.radius = radius
        self.create_edge()
        
    def create_edge(self) -> None:
        unit_direction: np.ndarray = self.get_unit_direction()
        
        P0: np.ndarray = self.u.get_center() + unit_direction * self.radius
        P3: np.ndarray = self.v.get_center() - unit_direction * self.radius
        
        distance: float = np.linalg.norm(P3 - P0)
        P1, P2 = self.compute_control_points(P0, P3, self.curvature, distance)
        bezier_curve = CubicBezier(P0, P1, P2, P3)
        
        self.dashed_curve = DashedVMobject(bezier_curve)
        self.add(self.dashed_curve)  
    
    def get_unit_direction(self) -> np.ndarray:
        direction = self.v.get_center() - self.u.get_center()
        return direction / np.linalg.norm(direction)
    
    @staticmethod
    def get_perpendicular_vector(vector) -> np.ndarray:
        """Returns a perpendicular vector to the input vector."""
        return np.array([-vector[1], vector[0], 0])
    
    def compute_control_points(
        self,
        P0: np.ndarray,
        P3: np.ndarray,
        curvature: float,
        distance: float) -> Tuple[np.ndarray, np.ndarray]:
        """
        Compute the two control points (P1 and P2) for a cubic Bezier curve
        to ensure symmetric curvature.
        """
        # Direction from P0 to P3
        direction: np.ndarray = P3 - P0
        unit_direction: np.ndarray = direction / np.linalg.norm(direction)
        
        # Perpendicular direction for curvature
        perp_direction: np.ndarray = self.get_perpendicular_vector(unit_direction)
        
        # Calculate P1 and P2 at t=0.25 and t=0.75 along the line
        t1: float = 0.25
        t2: float = 0.75
        
        P1: np.ndarray = P0 + (direction * t1) + (perp_direction * curvature * distance)
        P2: np.ndarray = P0 + (direction * t2) - (perp_direction * curvature * distance)
        
        return P1, P2
     
class Graph(VGroup):
    def __init__(
        self,
        nodes_data: Dict[str, np.ndarray],
        edges_data: List[Tuple[str, str]],
        **kwargs) -> None:
        super().__init__(**kwargs)
        self.nodes = {}
        self.edges = []
        self.create_nodes(nodes_data)
        self.create_edges(edges_data)
        
    def create_nodes(self, nodes_data: Dict[str, np.ndarray]) -> None:
        for label, position in nodes_data.items():
            node = Node(label, position)
            self.nodes[label] = node
            self.add(node)
    
    def create_edges(self, edges_data: List[Tuple[str, str]]) -> None:
        for u_label, v_label in edges_data:
            u: Node = self.nodes[u_label]
            v: Node = self.nodes[v_label]
            edge = Edge(u, v, curvature=0.3)
            self.edges.append(edge)
            self.add(edge)
        
class CurvyDashedGraph(Scene):
    def __init__(self, node_positions, edge_definitions, n, c_lib, c_road, city_edges, **kwargs):
        super().__init__(**kwargs)
        self.node_positions = node_positions
        self.edge_definitions = edge_definitions
        self.n = n
        self.c_lib = c_lib
        self.c_road = c_road
        self.city_edges = city_edges

    def construct(self) -> None:
        graph = Graph(self.node_positions, self.edge_definitions)
        self.add(graph)

        # Add legend in the lower-left
        legend_node = Node('n', ORIGIN, radius=0.3)
        legend_node.scale(0.7)
        node_label = Text("= n-th city node").scale(0.5).next_to(legend_node, RIGHT, buff=0.2)
        
        dashed_line = DashedLine(LEFT * 0.5, RIGHT * 0.5, color=BLACK)
        dashed_label = Text("= Possible road").scale(0.5).next_to(dashed_line, RIGHT, buff=0.2)
        
        legend_group = VGroup(
            VGroup(legend_node, node_label).arrange(RIGHT, buff=0.2),
            VGroup(dashed_line, dashed_label).arrange(RIGHT, buff=0.2)
        ).arrange(DOWN, buff=0.3).to_corner(LEFT + DOWN, buff=0.5)

        self.add(legend_group)
        
        # Add information in the top-left corner
        info_lines = [
            Text(f"n = {self.n}").scale(0.4),
            Text(f"c_lib = {self.c_lib}").scale(0.4),
            Text(f"c_road = {self.c_road}").scale(0.4),
            Text("city_edges = [").scale(0.4)
        ]
        
        # Add each city edge
        for edge in self.city_edges:
            info_lines.append(Text(f"[{edge[0]}, {edge[1]}],").scale(0.4))

        # Replace the last comma with the closing bracket
        info_lines[-1] = Text(f"[{self.city_edges[-1][0]}, {self.city_edges[-1][1]}]").scale(0.4)
        info_lines.append(Text("]").scale(0.4))
        
        info_text = VGroup(*info_lines).arrange(DOWN, buff=0.1)

        # Align the first three lines (n, c_lib, c_road) to the left
        for text in info_text[:3]:
            text.align_to(info_text[0], LEFT)

        # Align "city_edges = [" and the closing bracket "]"
        info_text[3].align_to(info_text[0], LEFT)
        info_text[-1].align_to(info_text[3], LEFT)

        # Keep nested lines indented with their own spacing
        for nested_line in info_text[4:-1]:
            nested_line.align_to(info_text[3], LEFT).shift(RIGHT)

        # Move to the top-left corner
        info_text.to_corner(LEFT + UP, buff=0.5)
        self.add(info_text)

def main():
    parser = argparse.ArgumentParser(description="Generate a graph visualization.")
    parser.add_argument("filename", type=str, help="Output filename for the graph image (e.g., graph.png).")
    args = parser.parse_args()

    # Ensure the filename ends with .png
    if not args.filename.endswith(".png"):
        raise ValueError("Output filename must have a .png extension.")

    # Prompt for input
    print("Enter number of cities (n), number of roads (m), library cost (c_lib), and road cost (c_road):")
    n, m, c_lib, c_road = map(int, input().split())

    print(f"Enter {m} pairs of cities (u_i, v_i):")
    edges = [tuple(input().split()) for _ in range(m)]

    # Generate node positions and edges
    theta = np.linspace(0, 2 * np.pi, n + 1)[:-1]
    radius = 3
    node_positions = {
        str(i): np.array([radius * np.cos(angle), radius * np.sin(angle), 0])
        for i, angle in zip(range(1, n + 1), theta)
    }

    edge_definitions = [(u, v) for u, v in edges]

    # Set up Manim configuration
    from manim import config
    config.pixel_width = 854
    config.pixel_height = 480
    config.frame_rate = 30
    config.background_color = BLACK
    config.media_dir = os.getcwd()
    config.images_dir = config.media_dir
    config.video_dir = config.media_dir
    config.save_as_gif = False
    config.save_last_frame = True

    # Create an instance of the scene
    scene = CurvyDashedGraph(
        node_positions,
        edge_definitions,
        n=n,
        c_lib=c_lib,
        c_road=c_road,
        city_edges=edges
    )

    # Render the scene
    scene.render()

    # Retrieve the actual output file path
    actual_output_file = scene.renderer.file_writer.image_file_path

    # Define the desired output directory (one level up in 'assets')
    parent_dir = os.path.dirname(os.getcwd())
    assets_dir = os.path.join(parent_dir, "assets")
    os.makedirs(assets_dir, exist_ok=True)  # Create the directory if it doesn't exist

    # Define the desired filename
    desired_filename = os.path.join(assets_dir, args.filename)

    if os.path.exists(actual_output_file):
        os.rename(actual_output_file, desired_filename)
        print(f"Graph saved as {desired_filename}")
    else:
        print("Error: The output file was not created.")

if __name__ == "__main__":
    main()