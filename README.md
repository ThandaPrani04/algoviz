# CP Visualizer

A tool to automatically generate C++ solutions and Manim visualizations for LeetCode problems using AI.

## Features
- Fetches LeetCode problem statements via GraphQL.
- Uses OpenRouter AI to generate:
  - Efficient C++ solutions
  - Manim (Python) scripts that visually explain the algorithm
- Saves outputs to files and renders the Manim animation.

## Prerequisites
- Python 3.8+
- [Manim](https://docs.manim.community/en/stable/)
- An [OpenRouter](https://openrouter.ai/) API key (for AI code generation)
- [requests](https://pypi.org/project/requests/) Python package
- [BeautifulSoup4](https://pypi.org/project/beautifulsoup4/) (if using the older script)

## Installation
1. **Clone the repository:**
   ```bash
   git clone https://github.com/yourusername/cp-visualizer.git
   cd cp-visualizer
   ```
2. **Install Python dependencies:**
   ```bash
   pip install requests beautifulsoup4
   # For Manim (if not already installed):
   pip install manim
   ```
3. **Install Manim (if not already):**
   See [Manim installation guide](https://docs.manim.community/en/stable/installation.html) for your OS.

4. **Set your OpenRouter API key:**
   - Get your API key from [OpenRouter](https://openrouter.ai/).
   - Set it as an environment variable:
     - **Linux/macOS:**
       ```bash
       export OPENROUTER_API_KEY=your_api_key_here
       ```
     - **Windows (CMD):**
       ```cmd
       set OPENROUTER_API_KEY=your_api_key_here
       ```
     - **Windows (PowerShell):**
       ```powershell
       $env:OPENROUTER_API_KEY="your_api_key_here"
       ```

## Usage
Run the script with a LeetCode problem URL:

```bash
python generate_solution_and_visual.py https://leetcode.com/problems/two-sum/
```

### What happens:
- Fetches the problem statement from LeetCode.
- Uses OpenRouter AI to generate:
  - A C++ solution (saved as `<slug>_solution.cpp`)
  - A Manim visualization script (saved as `<slug>_visualization.py`)
- Renders the Manim animation (opens a preview window).

### Example
```bash
python generate_solution_and_visual.py https://leetcode.com/problems/two-sum/
```

## Output Files
- `<slug>_solution_and_visualization.txt`: Raw AI output with both code sections.
- `<slug>_solution.cpp`: C++ solution code.
- `<slug>_visualization.py`: Manim script for visualization.

## Troubleshooting
- **API Key errors:**
  - Ensure `OPENROUTER_API_KEY` is set and valid.
- **Manim not found:**
  - Install Manim and ensure it's in your PATH.
- **LeetCode fetch errors:**
  - Check your internet connection and the problem URL format.
- **AI generation errors:**
  - The script retries up to 3 times. If it still fails, check your API key and OpenRouter status.

## Notes
- The Manim script assumes a class name of `SolutionVisualization`. If the generated script uses a different class name, update the script or the `render_manim` function accordingly.
- This tool is for educational and demonstration purposes.

## License
MIT License 