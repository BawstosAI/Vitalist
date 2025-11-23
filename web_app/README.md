# Vitalist Web App - Quick Start Guide

## 🚀 How to Visualize the Web App

### Option 1: Using Python HTTP Server (Recommended)

1. **Open a terminal/command prompt** in the `web_app` directory:
   ```bash
   cd web_app
   ```

2. **Run the server script**:
   ```bash
   python server.py
   ```
   
   Or if you're using Python 3 explicitly:
   ```bash
   python3 server.py
   ```

3. **Open your browser** and go to:
   ```
   http://localhost:8000/index.html
   ```
   
   The browser should open automatically!

4. **To stop the server**, press `Ctrl+C` in the terminal.

---

### Option 2: Using Python's Built-in Server

If the `server.py` script doesn't work, you can use Python's built-in server:

```bash
cd web_app
python -m http.server 8000
```

Then open: `http://localhost:8000/index.html`

---

### Option 3: Using Node.js (if you have it installed)

```bash
cd web_app
npx http-server -p 8000
```

Then open: `http://localhost:8000/index.html`

---

## 📋 What You'll See

The web app displays:

1. **Executive Summary** - Overview statistics
2. **Model Performance** - Comparison of Linear vs Gradient Boosting models
3. **Age Gap Distributions** - Visualizations of age gaps across organ systems
4. **Inter-Organ Correlations** - Correlation matrix between organs

---

## 🛠️ Troubleshooting

### "Cannot load data" error

**Problem**: The browser blocks loading local JSON files due to CORS policy.

**Solution**: You **must** use a web server (Options 1, 2, or 3 above). You cannot simply open `index.html` directly in the browser.

### Port already in use

If port 8000 is busy, use a different port:

```bash
python server.py 8001
```

Then open: `http://localhost:8001/index.html`

### Python not found

Make sure Python is installed and in your PATH. You can check with:
```bash
python --version
```

---

## 📁 File Structure

```
web_app/
├── index.html          # Main web app file
├── server.py           # Python server script
├── README.md           # This file
└── public/
    └── data/           # JSON data files
        ├── age_gaps.json
        ├── metrics_summary.json
        ├── correlations.json
        └── ...
```

---

## 🎨 Features

- ✅ Interactive charts using Chart.js
- ✅ Responsive design
- ✅ Modern UI with gradient background
- ✅ Real-time data visualization
- ✅ Organ-specific color coding

---

## 🔄 Next Steps

For a more advanced web app with Next.js/React, see the main `WEB_APP_README.md` in the project root.

---

**Enjoy exploring your Vitalist data! 🧬📊**
