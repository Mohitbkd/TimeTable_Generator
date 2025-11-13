# 🚀 Deployment Guide - Timetable Generator

## Option 1: Streamlit Community Cloud (Recommended)

### Prerequisites:
- GitHub account
- Git installed on your computer

### Steps:

1. **Initialize Git repository:**
   ```bash
   cd "d:\Time Table Generation"
   git init
   git add .
   git commit -m "Initial commit - Timetable Generator"
   ```

2. **Create GitHub repository:**
   - Go to https://github.com/new
   - Name: `timetable-generator`
   - Make it Public or Private
   - Don't initialize with README (we already have one)
   - Click "Create repository"

3. **Push to GitHub:**
   ```bash
   git remote add origin https://github.com/YOUR_USERNAME/timetable-generator.git
   git branch -M main
   git push -u origin main
   ```

4. **Deploy on Streamlit Cloud:**
   - Go to https://share.streamlit.io/
   - Click "Sign in" (use GitHub)
   - Click "New app"
   - Repository: `YOUR_USERNAME/timetable-generator`
   - Branch: `main`
   - Main file path: `app.py`
   - Click "Deploy!"

5. **Your app will be live at:**
   ```
   https://YOUR_USERNAME-timetable-generator.streamlit.app
   ```

### Updating Your App:
Just push changes to GitHub:
```bash
git add .
git commit -m "Update description"
git push
```
The app will automatically redeploy!

---

## Option 2: Hugging Face Spaces

### Steps:

1. **Create account:** https://huggingface.co/join

2. **Create new Space:**
   - Go to https://huggingface.co/new-space
   - Owner: Your username
   - Space name: `timetable-generator`
   - License: `mit`
   - Select SDK: **Streamlit**
   - Space hardware: `CPU basic` (free)
   - Click "Create Space"

3. **Upload files via web interface:**
   - Click "Files" tab
   - Click "Add file" → "Upload files"
   - Upload these files:
     - `app.py`
     - `ttv5.py`
     - `requirements.txt`
     - `README.md`
     - `.streamlit/config.toml`
   - Click "Commit changes to main"

4. **Your app will be live at:**
   ```
   https://huggingface.co/spaces/YOUR_USERNAME/timetable-generator
   ```

### Alternative: Use Git
```bash
git clone https://huggingface.co/spaces/YOUR_USERNAME/timetable-generator
cd timetable-generator
# Copy your files here
git add .
git commit -m "Add timetable generator"
git push
```

---

## Option 3: Render

### Steps:

1. **Push code to GitHub** (see Option 1, steps 1-3)

2. **Create Render account:** https://render.com/

3. **Create new Web Service:**
   - Click "New +" → "Web Service"
   - Connect your GitHub account
   - Select `timetable-generator` repository
   - Name: `timetable-generator`
   - Environment: `Python 3`
   - Build Command: `pip install -r requirements.txt`
   - Start Command: `streamlit run app.py --server.port=$PORT --server.address=0.0.0.0 --server.headless=true`
   - Instance Type: `Free`
   - Click "Create Web Service"

4. **Your app will be live at:**
   ```
   https://timetable-generator.onrender.com
   ```

**Note:** Free tier apps sleep after 15 minutes of inactivity and take ~30 seconds to wake up.

---

## Troubleshooting

### Issue: "ModuleNotFoundError"
**Solution:** Make sure `requirements.txt` includes all dependencies:
```
streamlit>=1.28.0
pandas>=2.0.0,<2.4.0
openpyxl>=3.1.0
numpy>=1.24.0,<2.0.0
python-dateutil>=2.8.0
```

### Issue: "App not loading"
**Solution:** Check the logs in your deployment platform's dashboard

### Issue: "Memory limit exceeded"
**Solution:** 
- Use Streamlit Cloud (1GB RAM)
- Or upgrade to paid tier on Render/Railway

### Issue: "App is slow"
**Solution:**
- Disable debug mode in production
- Reduce max_attempts_per_var to 100-150
- Consider batch processing for large datasets

---

## Environment Variables (Optional)

If you need to add secrets (API keys, etc.):

### Streamlit Cloud:
- Go to app settings
- Click "Secrets"
- Add in TOML format:
  ```toml
  [secrets]
  api_key = "your-key-here"
  ```

### Hugging Face:
- Go to Space settings
- Add secrets in "Repository secrets"

### Render:
- Go to service settings
- Add "Environment Variables"

---

## Sharing Your App

Once deployed, share the URL with your users:

**Streamlit Cloud:**
```
https://YOUR_USERNAME-timetable-generator.streamlit.app
```

**Hugging Face:**
```
https://huggingface.co/spaces/YOUR_USERNAME/timetable-generator
```

**Render:**
```
https://timetable-generator.onrender.com
```

Users can:
1. Upload their Excel files
2. Generate timetables
3. Download results
4. View unscheduled requirements

---

## Cost Comparison

| Platform | Free Tier | Paid Tier | Best For |
|----------|-----------|-----------|----------|
| **Streamlit Cloud** | 1GB RAM, Unlimited | N/A | Quick deployment |
| **Hugging Face** | 2GB RAM, Generous | $0.60/hr for GPU | ML/AI apps |
| **Render** | 512MB RAM, Sleeps | $7/month | Production apps |
| **Railway** | $5 credit/month | Pay as you go | Scalable apps |

**Recommendation:** Start with **Streamlit Cloud** (easiest) or **Hugging Face** (better resources).

---

## Support

For deployment issues:
- Streamlit: https://docs.streamlit.io/streamlit-community-cloud
- Hugging Face: https://huggingface.co/docs/hub/spaces
- Render: https://render.com/docs
