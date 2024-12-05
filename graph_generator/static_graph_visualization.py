# Copyright 2024 Nicholas Fleischhauer
# SPDX-License-Identifier: GPL-3.0-or-later

from typing import Any, Dict, List, Tuple
from manim import *
import numpy as np
import argparse

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
    def construct(self) -> None:
        node_positions = {
            "1": UP,
            "2": RIGHT * 2 + UP * 0.25,
            "3": LEFT * 0.25 + DOWN * 0.75,
            "4": LEFT * 1.50 + UP * 0.05,
            "5": UP + RIGHT * 4,
            "6": RIGHT * 4.5 + DOWN * 0.50,
            "7": DOWN + RIGHT * 2.75
        }
            
        edge_definitions = [
            ("1", "2"),
            ("2", "3"),
            ("3", "1"),
            ("4", "1"),
            ("5", "6"),
            ("6", "7")
        ]
        
        graph = Graph(node_positions, edge_definitions)
        self.add(graph)
        
        # Add legend in the lower-left
        legend_node = Node('n', ORIGIN, radius=0.3)
        legend_node.scale(0.7)
        node_label = Text("= n-th city node").scale(0.5).next_to(legend_node, RIGHT, buff=0.2)
        
        dashed_line = DashedLine(LEFT * 0.5, RIGHT * 0.5, color=WHITE)
        dashed_label = Text("= Possible road").scale(0.5).next_to(dashed_line, RIGHT, buff=0.2)
        
        legend_group = VGroup(
            VGroup(legend_node, node_label).arrange(RIGHT, buff=0.2),  # Group for node legend
            VGroup(dashed_line, dashed_label).arrange(RIGHT, buff=0.2)  # Group for dashed line legend
        ).arrange(DOWN, buff=0.3).to_corner(LEFT + DOWN, buff=0.5)

        self.add(legend_group)
        
        
        # Add information in the top-left corner
        info_text = VGroup(
            Text("n = 7").scale(0.4),
            Text("c_lib = 3").scale(0.4),
            Text("c_road = 2").scale(0.4),
            Text("city_edges = [").scale(0.4),  # Starting line for city_edges
            Text("[1, 2],").scale(0.4),
            Text("[2, 3],").scale(0.4),
            Text("[3, 1],").scale(0.4),
            Text("[4, 1],").scale(0.4),
            Text("[5, 6],").scale(0.4),
            Text("[6, 7]").scale(0.4),
            Text("]").scale(0.4)  # Closing bracket aligns with "city_edges = ["
        ).arrange(DOWN, buff=0.1)

        # Align the first three lines (n, c_lib, c_road) to the left
        for text in info_text[:3]:
            text.align_to(info_text[0], LEFT)  # Align to "n = 6"

        # Align "city_edges = [" and the closing bracket "]"
        info_text[3].align_to(info_text[0], LEFT)  # Align "city_edges = [" to "n = 6"
        info_text[-1].align_to(info_text[3], LEFT)  # Align "]" to "city_edges = ["

        # Keep nested lines indented with their own spacing
        for nested_line in info_text[4:-1]:  # Lines inside "city_edges = ["
            nested_line.align_to(info_text[3], LEFT).shift(RIGHT)  # Indent relative to "city_edges = ["

        # Move to the top-left corner
        info_text.to_corner(LEFT + UP, buff=0.5)
        self.add(info_text)
