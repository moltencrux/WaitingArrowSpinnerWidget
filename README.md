# WaitingArrowSpinnerWidget
`WaitingArrowSpinnerWidget` is an alluring and configurable, custom PyQt6 widget for displaying a unique "waiting" or "loading" spinner in Qt applications. It features arrow-shaped arcs (default: three 110° arcs) with a smooth color-cycling gradient (cyan-to-blue-to-transparent) that rotates.

![WaitingArrowSpinnerWidget Demo](images/animation.webp)

## Features
- **Configurable Arrows**: Adjust the number of arrow-shaped arcs (`setArrowCount`), gap between arcs (`setGapRatio`), and arrow geometry (`setThicknessRatio`, `setArrowWidthRatio`, `setArrowLengthRatio`, `setBarbIndentRatio`).
- **Color Cycling**: Gradient colors shift hues over time for a dynamic effect, with grayscale mode when disabled.
- **Smooth Animation**: Uses a configurable timer interval (default: 16ms, ~60 FPS) for fluid rotation.
- **Antialiased Rendering**: High-quality rendering with PyQt6’s `QPainter` and `QPainterPath`.
- **Flexible Scaling**: Adapts to any widget size via normalized coordinates.
- **Interactive Controls**: Toggle spinning, pause/resume animation, and enable/disable with grayscale effect.
- **Clockwise/Counterclockwise**: Configurable rotation direction via `setClockwise`.
- **Flexible scaling**: Looks great at nearly any size.

## Configuration
The widget’s properties can be customized using setter methods or the provided demo application. Key properties include:

- **Number of Arrows** (`setArrowCount`): Number of arcs (default: 3, range: 1–20).
- **Gap Ratio** (`setGapRatio`): Gap between arcs as a fraction of the full circle divided by arrow count (default: 0.2, range: 0.0–1.0).
- **Thickness Ratio** (`setThicknessRatio`): Arc thickness as a ratio of widget size (default: 0.1, range: 0.0–1.0).
- **Arrow Width Ratio** (`setArrowWidthRatio`): Width of arrow barbs (default: 0.075, range: 0.0–1.0).
- **Arrow Length Ratio** (`setArrowLengthRatio`): Length of arrowhead (default: 0.3, range: 0.0–1.0).
- **Barb Indent Ratio** (`setBarbIndentRatio`): Indent of arrow barbs (default: 0.03, range: 0.0–1.0).
- **Rotation Speed** (`setRevolutionsPerSecond`): Rotations per second (default: 1.0, range: 0.1–10.0).
- **Frame Rate** (`setFrameRate`): Animation updates per second (default: 60 FPS, range: 1–240).
- **Clockwise** (`setClockwise`): Rotation direction (default: True for clockwise).
- **Enabled** (`setEnabled`): Enables/disables the widget, toggling animation and color (default: True).
- **Color** (`setColor`): Sets a custom base color for the gradient (default: cyan-to-blue).

## Usage
The `WaitingArrowSpinnerWidget` is easy to integrate into any PyQt6 application. Below are two examples:

### Basic Usage
Create a spinner with default settings (three arrows, 96° sweep each, color-cycling gradient):

```python
from PyQt6.QtWidgets import QApplication
from waitingarrowspinnerwidget import WaitingArrowSpinnerWidget
import sys

app = QApplication(sys.argv)
spinner = WaitingArrowSpinnerWidget()
spinner.resize(400, 400)
spinner.start()  # Starts spinning
spinner.show()
sys.exit(app.exec())
```

### Advanced Usage
Create a spinner in a dialog with custom settings, interactive toggling:

```python
from PyQt6.QtWidgets import QDialog, QVBoxLayout, QApplication
from waitingarrowspinnerwidget import WaitingArrowSpinnerWidget
import sys

class DemoDialog(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Spinner Demo")
        layout = QVBoxLayout(self)
        self.spinner = WaitingArrowSpinnerWidget(self)
        self.spinner.setArrowCount(4)  # Four arrows
        self.spinner.setGapRatio(0.25)  # Larger gaps
        self.spinner.setRevolutionsPerSecond(0.5)  # Slower rotation
        self.spinner.setClockwise(False)  # Counterclockwise
        layout.addWidget(self.spinner)
        self.spinner.start()

app = QApplication(sys.argv)
dialog = DemoDialog()
dialog.resize(400, 400)
dialog.show()
sys.exit(app.exec())
```

## Demo
A comprehensive demo is included to test all configurable properties. Run it with:

```bash
python demo.py
```

The demo provides:
- Spinboxes to adjust arrow count, gap ratio, thickness, arrow width, arrow length, barb indent, rotation speed, and frame rate.
- Checkboxes to toggle clockwise rotation and enabled state (disabling pauses the animation and grays out colors).
- Buttons to start/pause the animation and pick a custom color.
- Click the spinner to toggle between spinning and paused states.

## Installation
1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/WaitingArrowSpinnerWidget.git
   ```
2. Copy `waitingarrowspinnerwidget.py` and `demo.py` to your project.
3. Ensure PyQt6 is installed:
   ```bash
   pip install PyQt6
   ```
4. Import and use as shown in the usage examples.

## Inspiration
This project was inspired by [QtWaitingSpinner](https://github.com/z3ntu/QtWaitingSpinner) by z3ntu, which provided the foundation for a configurable spinner widget in PyQt6.

## Feedback
Please submit feedback, feature requests, or issues via [GitHub Issues](https://github.com/yourusername/WaitingArrowSpinnerWidget/issues).

## License
This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

## About
An alluring custom PyQt6 widget that features a dynamic arrow-shaped loading
spinner with color-cycling 


© 2025 moltencrux