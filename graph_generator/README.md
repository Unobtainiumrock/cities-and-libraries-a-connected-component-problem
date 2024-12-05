# Command to create HackerLand Image Asset

The code in `static_graph_visualization.py` is responsible for creating the image for HackerLand used by `main.tex`.

## How to use it

1. Ensure you're in the `/graph_generator` directory
2. Run the following:

```bash
manim -pql static_graph_visualization.py CurvyDashedGraph
```

This output will be sent to the `/graph_generator/media/images/static_graph_visualization/` folder with the name `CurvyDashedGraph_ManimCE_v0.18.1.png`

# Command to create Other Image Assets

The code in `dynamic_graph_visualization.py` is responsible for creating the image for Scriptshire used by `main.tex` It can also be used to generate other image assets.


## How to use it

1. Ensure you're in the `/graph_generator` directory
2. Run the following:

```bash
python3 dynamic_graph_visualization.py output.png
```

It will then output your image asset in the `/assets` folder with the name `output.png`
