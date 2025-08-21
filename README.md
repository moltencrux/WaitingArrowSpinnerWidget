# WaitingArrowSpinnerWidget
`WaitingArrowSpinnerWidget` is an alluring and configurable, custom PyQt6 widget for displaying a unique "waiting" or "loading" spinner in Qt applications. It features arrow-shaped arcs (default: three 110° arcs) with a smooth color-cycling gradient (cyan-to-blue-to-transparent) that rotates.

![WaitingArrowSpinnerWidget Demo](images/animation.webp)
 
## Features

- **Configurable Arrows**: Adjust the number of arrow-shaped arcs (`_arrow_count`) and their sweep angle (`_sweep`).
- **Color Cycling**: Gradient colors shift hues over time for a dynamic visual effect.
- **Smooth Animation**: Uses a 16ms timer for fluid rotation and color transitions.
- **Antialiased Rendering**: High-quality arc rendering with PyQt6’s `QPainter`.
- **Flexible scaling**: Looks great at nearly any size.

Configuration
The following properties can be customized by directly modifying the widget’s attributes or subclassing:

- **Number of Arrows** (`_arrow_count`): Number of arcs (default: 3).
- **Sweep Angle** (`_sweep`): Arc span in degrees (default: `(360 / _arrow_count) - 10`).
- **Rotation Speed** (`_rotation_increment`): Degrees per frame (default: 2° every 16ms).
- **Color Cycle Speed** (`_hue_offset` increment): Hue shift per frame (default: 1° every 16ms).

## Usage

The `WaitingArrowSpinnerWidget` is easy to integrate into any PyQt6 application. Below are two examples:

### Basic Usage
Create a spinner with default settings (three 110° arcs, color-cycling gradient):

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
Create a spinner that disables its parent widget, centers in a dialog, and uses custom settings:

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
        self.spinner._arrow_count = 4  # Four arrows
        self.spinner._sweep = (360 / self.spinner._arrow_count) - 15  # Adjust sweep
        self.spinner._rotation_increment = 3  # Faster rotation
        self.spinner._disableParentWhenSpinning = True  # Disable parent
        layout.addWidget(self.spinner)
        self.spinner.start()

app = QApplication(sys.argv)
dialog = DemoDialog()
dialog.resize(400, 400)
dialog.show()
sys.exit(app.exec())
```

Currently, only a simple demo is included. A more configurable demo will be added in the future.

## Demo
To show the demo, just run `python waitingarrowspinnerwidget.py` .

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/WaitingArrowSpinnerWidget.git
   ```
2. Copy `waiting_arrow_spinner.py` to your project.
3. Import and use as shown in the usage examples.

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
