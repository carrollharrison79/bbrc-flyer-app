# BBRC Flyer Generator — Web App

A Flask web application that generates personalized property owner mailers for Billy Boyd Realty & Construction Inc.

**What it does:**
- Agents upload their contact info, headshot, and a property list (Excel)
- Web app auto-generates QR codes from social URLs
- Creates 1,700+ personalized 2-page PDFs per property owner
- Returns a zip download with all flyers ready to mail

---

## Local Development

### Prerequisites
- Python 3.9+
- Git

### Setup

1. **Clone the repo** (after pushing to GitHub)
   ```bash
   git clone https://github.com/YourUsername/bbrc-flyer-app.git
   cd bbrc-flyer-app
   ```

2. **Create virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # macOS/Linux
   # or
   venv\Scripts\activate  # Windows
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Set environment variables** (optional for local testing)
   ```bash
   export GOOGLE_API_KEY="AIzaSyB5kyDTIJTbI-lhiIgDaYNZoyt5hn7bxmk"
   export ANTHROPIC_API_KEY="your-key-here"
   ```

5. **Run locally**
   ```bash
   python app.py
   ```
   Visit `http://localhost:5000` in your browser.

---

## Deployment to Render

### Step 1: Push Code to GitHub

1. **Initialize git repo** (if not already done):
   ```bash
   cd /Users/harrisoncarroll/Downloads/Marketing
   git init
   git add .
   git commit -m "Initial commit: BBRC Flyer Generator web app"
   git branch -M main
   ```

2. **Create GitHub repo** and connect:
   ```bash
   git remote add origin https://github.com/YourUsername/bbrc-flyer-app.git
   git push -u origin main
   ```

### Step 2: Deploy on Render

1. **Go to [render.com](https://render.com)** and sign in with GitHub
2. **Click "New +" → "Web Service"**
3. **Select your GitHub repo** (`bbrc-flyer-app`)
4. **Configure the service:**
   - **Name:** `bbrc-flyer-generator`
   - **Region:** US East (closest to Tuscaloosa)
   - **Branch:** `main`
   - **Build Command:** `pip install -r requirements.txt`
   - **Start Command:** `gunicorn app:app`
   - **Plan:** Free tier (or Starter for better uptime)

5. **Add Environment Variables** (click "Environment"):
   ```
   GOOGLE_API_KEY = AIzaSyB5kyDTIJTbI-lhiIgDaYNZoyt5hn7bxmk
   ANTHROPIC_API_KEY = your-anthropic-key-here
   ```

6. **Click "Create Web Service"**

Render will automatically:
- Deploy the app
- Assign a public URL (e.g., `https://bbrc-flyer-generator.onrender.com`)
- Auto-redeploy on each git push to `main`

### Step 3: Use the App

Visit your Render URL and fill out the form:
- **Agent name, phone, email** (required)
- **Title** (optional, defaults to "Commercial Salesman")
- **Social media URLs** (optional, QR codes auto-generated)
- **Headshot** (optional JPG/PNG)
- **Property list** (required Excel file, same format as `Marketing_List__Final_.xlsx`)

Click **Generate Flyers** → download zip with all PDFs

---

## File Structure

```
bbrc-flyer-app/
├── app.py                  # Flask backend
├── requirements.txt        # Python dependencies
├── Procfile               # Render deployment config
├── .gitignore             # Git ignore rules
├── README.md              # This file
└── templates/
    └── index.html         # Web form
```

---

## Key Features

✓ **Personalized agent info** — name, phone, email, title, headshot  
✓ **QR code generation** — Instagram, Facebook, LinkedIn auto-generated  
✓ **Street View photos** — Google Street View API fetches property images  
✓ **Tailored messaging** — Pitch changes based on property type  
✓ **Market trends** — Q2 2026 stats by property type  
✓ **Two-page flyers** — Page 1: sales pitch + holdings; Page 2: mailing panel  
✓ **Batch processing** — Handles 100+ owners in seconds  
✓ **Zip download** — All PDFs bundled for printing  

---

## Input File Format

**Excel file** with sheet `Parcel Details`:
- Interleaved rows: owner info (name, address, zip) + parcel details (ID, address, type, use)
- Script auto-flattens and groups by owner
- Example: `Marketing_List__Final_.xlsx`

---

## API Keys & Configuration

### Google Street View API
- Key: `AIzaSyB5kyDTIJTbI-lhiIgDaYNZoyt5hn7bxmk`
- Cost: ~$12 per full run (1,700 images) under free tier
- Used to fetch property photos for each flyer

### Anthropic API (Optional)
- For future classification enhancements
- Set in environment as `ANTHROPIC_API_KEY`

---

## Troubleshooting

**"Property list file required"**
- Make sure you upload an Excel file with sheet named `Parcel Details`

**No Street View photos showing**
- ~30-40% of rural addresses have no Street View imagery (expected)
- Flyers show placeholder in these cases

**Generation taking too long**
- Free Render tier may be slower; consider upgrading to Starter
- Each property ~0.5-2 seconds depending on Street View API

**QR codes not generating**
- Make sure social URLs are valid (e.g., `https://instagram.com/yourhandle`)
- Empty URLs are fine — just skipped

---

## Future Enhancements

- [ ] Batch-classify properties by type (Anthropic API)
- [ ] Add recent deals editor via web form
- [ ] Custom market trends per agent
- [ ] Multi-agent accounts & history
- [ ] PDF preview before download
- [ ] Email flyers directly from web app
- [ ] Scheduled batch runs

---

## Support

For questions or issues, contact Harrison Carroll at `harrison@billyboydrealty.com`

---

**Version:** 1.0  
**Last Updated:** May 2026  
**Status:** Production Ready
