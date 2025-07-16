# AlgoViz

🧩 Generate optimal C++ solutions and beautiful Manim visualizations for LeetCode problems — right from your browser.

A Chrome Extension + Python Backend that lets you click on a LeetCode problem page, run the pipeline, and save a rendered .mp4 video and code files into your local folder.

## ✨ Features

🔷 One-click integration with LeetCode.

🔷 Generates:

✅ Optimal C++ solution

✅ Clean Manim animation video

🔷 Checks correctness against top discussion posts.

🔷 Saves all files in your local folder automatically.

## 📂 Project Structure

```
leetcode-visualizer/
├── backend/
│   ├── server.py                  # Flask server
│   └── leetcode_visualizer.py    # Full pipeline
├── extension/
│   ├── manifest.json              # Chrome extension manifest
│   ├── popup.html                 # Extension UI
│   ├── popup.js                   # Extension logic
│   └── icon.png                   # Extension icon
├── README.md
```

## 🚀 Installation & Setup

### 1️⃣ Clone the repository
```bash
git clone https://github.com/<your-username>/algoviz.git
cd algoviz
```

### 2️⃣ Install backend dependencies
- ✅ Install Python ≥ 3.8
- ✅ Install required Python libraries:

```bash
pip install flask requests beautifulsoup4
```
- ✅ Install Manim:
  - Follow the [Manim installation guide](https://docs.manim.community/en/stable/installation.html)

### 3️⃣ Get OpenRouter API Key
- Sign up at [OpenRouter](https://openrouter.ai/).
- Copy your API key.
- Set it as an environment variable:

```bash
export OPENROUTER_API_KEY=your_api_key_here
```
Or add it to your shell profile (`.bashrc`, `.zshrc`, etc.)

### 4️⃣ Load the Chrome Extension
- Open Chrome and go to: `chrome://extensions/`
- Enable Developer Mode (toggle at the top-right).
- Click **Load unpacked**.
- Select the `extension/` folder.
- You should now see the extension icon in your browser toolbar. 🎉

## 🖥️ Usage

### 🔷 Start the backend server
```bash
cd backend
python server.py
```
The server runs at: [http://localhost:5000/](http://localhost:5000/)

### 🔷 Open a LeetCode problem
For example:
https://leetcode.com/problems/two-sum/

Click the extension icon → Click **Generate Visualization**.

✅ Done!

### 🔷 Output files
After the pipeline runs, the following files are saved in your backend folder:

| File                              | Description                  |
|-----------------------------------|------------------------------|
| slug_solution_and_visualization.txt | Raw output from LLM         |
| slug_solution.cpp                 | Optimal C++ solution         |
| slug_visualization.py             | Manim animation script       |
| media/videos/                     | Rendered .mp4 video (Manim’s default output) |

🎬 You can play the video or upload it anywhere!

## 📝 Notes
- ⚠️ The backend server must be running when you click the extension.
- ⚠️ Make sure your `OPENROUTER_API_KEY` is set.
- ⚠️ Rendering a video can take up to ~30 seconds, depending on the problem.

## 🧹 Optional: High-Quality Videos
By default, videos are rendered in low quality (`-pql` for faster preview).
You can change `render_manim()` in `leetcode_visualizer.py` to use `-pqh` for high quality.

## 📦 Roadmap
- ✅ Basic Chrome + Backend pipeline
- ⬜ Real-time progress updates in the popup
- ⬜ Support more programming languages
- ⬜ Direct cloud upload of videos
- ⬜ Installer & packaged releases

## 🤝 Contributing
Contributions are welcome!
Please open an issue or a pull request if you have suggestions or find bugs.


📌 Happy Coding & Visualizing! 🚀✨ 