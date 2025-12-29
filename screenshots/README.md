# Screenshot Placeholder

Folder ini berisi screenshot dari aplikasi AI Bias Auditor.

## Required Screenshots

### 1. dashboard.png
- **Content**: Full dashboard overview
- **Size**: 1920x1080 (Full HD)
- **Format**: PNG
- **What to capture**:
  - Header "AUDIT REPORT: CREDIT SCORING BIAS"
  - Executive Summary cards (4 metrics)
  - Both charts (bar chart + scatter plot)
  - Detailed statistics tables

### 2. bias_detection.png
- **Content**: Audit Conclusion section
- **Size**: 1920x1080
- **Format**: PNG
- **What to capture**:
  - "BIAS DETECTED" warning box
  - Evidence list (score gap, approval gap)
  - Recommendations
  - Risk level assessment

### 3. charts.png
- **Content**: Close-up of visualizations
- **Size**: 1920x1080
- **Format**: PNG
- **What to capture**:
  - Bar chart showing score gap
  - Scatter plot showing age discrimination pattern
  - Both charts should be clearly visible

### 4. export_data.png (Optional)
- **Content**: Data export functionality
- **Size**: 1920x1080
- **Format**: PNG
- **What to capture**:
  - Download CSV button
  - Sample data preview (expanded)

## How to Take Screenshots

### Windows
1. Run aplikasi: `streamlit run app.py`
2. Maximize browser window
3. Press `Windows + Shift + S` for Snipping Tool
4. Select area and save as PNG

### macOS
1. Run aplikasi: `streamlit run app.py`
2. Maximize browser window
3. Press `Cmd + Shift + 4` then `Space`
4. Click window to capture
5. Save to screenshots folder

### Tips untuk Screenshot Berkualitas

1. **Clean Environment**
   - Close unnecessary browser tabs
   - Hide bookmarks bar
   - Use incognito mode untuk tampilan clean

2. **Good Data**
   - Run simulation dengan N=1000 (consistent results)
   - Ensure bias is detected (akan selalu detected dengan algoritma kita)

3. **Readable Text**
   - Zoom browser ke 100% (default)
   - Pastikan font tidak blur
   - Check contrast antara text dan background

4. **Annotations (Optional)**
   - Gunakan tool seperti Snagit, Greenshot
   - Tambahkan arrow/callout untuk highlight key features
   - Keep it professional (Navy Blue annotations)

## Editing Screenshots

### Recommended Free Tools
- **Windows**: Paint 3D, Greenshot
- **macOS**: Preview (built-in), Skitch
- **Cross-platform**: GIMP, Inkscape

### What to Edit
- Crop unnecessary parts (keep only dashboard area)
- Adjust brightness/contrast if needed
- Add annotations (optional, but helpful)
- Resize to 1920x1080 if needed

## Embedding in README

Setelah screenshot siap, update README.md:

```markdown
## Screenshots

### Dashboard Overview
![Dashboard](screenshots/dashboard.png)

### Bias Detection Results
![Bias Detection](screenshots/bias_detection.png)

### Data Visualization
![Visualization](screenshots/charts.png)
```

## Checklist Before Submit

- [ ] All screenshots are PNG format
- [ ] Resolution at least 1920x1080
- [ ] No personal information visible
- [ ] Images are not blurry
- [ ] Colors are accurate (Navy Blue visible)
- [ ] All screenshots referenced in README.md
- [ ] File names match exactly: dashboard.png, bias_detection.png, charts.png

---

**Note**: Ambil screenshot SETELAH aplikasi berjalan dengan baik dan menampilkan hasil yang benar.
