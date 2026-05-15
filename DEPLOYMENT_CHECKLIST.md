# BBRC Flyer Generator — Deployment Checklist

## Pre-Deployment (Local Testing)

- [ ] Python 3.11+ installed
- [ ] All files created:
  - `app.py`
  - `templates/index.html`
  - `requirements.txt`
  - `Procfile`
  - `runtime.txt`
  - `README.md`
  - `.gitignore`
- [ ] Test locally:
  ```bash
  python app.py
  # Visit http://localhost:5000
  # Test form submission with sample property list
  ```
- [ ] Form validation works
- [ ] File uploads work
- [ ] No Python errors in terminal

---

## Step 1: GitHub Setup (5 minutes)

### 1a: Create GitHub Repository

1. Go to [github.com/new](https://github.com/new)
2. **Repository name:** `bbrc-flyer-app`
3. **Description:** "Web app for generating personalized property owner mailers"
4. **Public** (so Render can access it)
5. **Skip** "Initialize with README" (you already have one)
6. Click **Create Repository**

### 1b: Connect Local Repo

In Terminal:
```bash
cd /Users/harrisoncarroll/Downloads/Marketing

# Initialize git if not already done
git init
git add .
git commit -m "Initial commit: BBRC Flyer Generator web app"
git branch -M main

# Add remote and push
git remote add origin https://github.com/YourUsername/bbrc-flyer-app.git
git push -u origin main
```

**Replace `YourUsername`** with your GitHub username.

- [ ] GitHub repo created at `github.com/YourUsername/bbrc-flyer-app`
- [ ] All files pushed to main branch
- [ ] Repo is **Public**

---

## Step 2: Render Deployment (10 minutes)

### 2a: Sign Up / Log In to Render

1. Go to [render.com](https://render.com)
2. Click **Sign Up** (or log in)
3. **Sign in with GitHub** (authorize Render)
4. Approve Render to access your repositories

### 2b: Create Web Service

1. Click **New +** → **Web Service**
2. Select your `bbrc-flyer-app` repository from the list
3. If you don't see it, click **Configure GitHub App** to grant Render access to more repos

### 2c: Configure Service

Fill in:

| Setting | Value |
|---------|-------|
| **Name** | `bbrc-flyer-generator` |
| **Region** | `US East` (closest to Tuscaloosa) |
| **Branch** | `main` |
| **Build Command** | `pip install -r requirements.txt` |
| **Start Command** | `gunicorn app:app` |
| **Plan** | Free tier (or Starter $7/month for better uptime) |

### 2d: Add Environment Variables

Scroll down to **Environment** section:

Click **Add Environment Variable** twice:

**Variable 1:**
- Key: `GOOGLE_API_KEY`
- Value: `AIzaSyB5kyDTIJTbI-lhiIgDaYNZoyt5hn7bxmk`

**Variable 2:**
- Key: `ANTHROPIC_API_KEY`
- Value: *(leave empty or add your key if available)*

### 2e: Deploy

Click **Create Web Service**

Render will:
- Build the app (~2-3 minutes)
- Deploy to a live URL
- Show **Live** status when ready

- [ ] Service created on Render
- [ ] Build completed successfully
- [ ] Status shows **Live** (not Deploying)
- [ ] Render assigned a URL like `https://bbrc-flyer-generator.onrender.com`

---

## Step 3: Test Production App (5 minutes)

1. Click on your service URL (shown in Render dashboard)
2. Form should load (nice blue header, white form)
3. Test with dummy data:
   - **Name:** Test Agent
   - **Phone:** 205-534-2628
   - **Email:** test@example.com
   - **Headshot:** (skip, optional)
   - **Property List:** Upload `Marketing_List__Final_.xlsx`
4. Click **Generate Flyers**
5. Should download a zip file with PDFs

- [ ] App loads on Render URL
- [ ] Form is responsive and styled correctly
- [ ] Can upload property list
- [ ] Can generate sample flyers
- [ ] Download works

---

## Step 4: Share with Team

### How Agents Use It

1. **Go to:** `https://bbrc-flyer-generator.onrender.com`
2. **Fill form:**
   - Name, phone, email
   - Social URLs (optional, for QR codes)
   - Upload headshot (optional)
   - Upload property list (required — Excel, same format)
3. **Click Generate**
4. **Download zip**
5. **Send to printer**

### Cost to Mail

Rough estimates:
- **Per flyer:** ~$0.56 (USPS Large Postcard)
- **Full batch (1,700):** ~$950 + design/printing

---

## Ongoing Maintenance

### Auto-Redeploy
- Any `git push` to `main` branch auto-triggers Render redeploy
- No manual action needed

### Monitor Uptime
- Render dashboard shows uptime and error logs
- Free tier may auto-sleep if no traffic for 15 minutes (wakes on request)
- Starter plan ($7/month) keeps app always awake

### Update Code
```bash
cd /Users/harrisoncarroll/Downloads/Marketing
# Make changes to app.py, index.html, etc.
git add .
git commit -m "Description of changes"
git push
# Render auto-deploys within 1-2 minutes
```

- [ ] Render redeploy works on git push
- [ ] Understand free tier may sleep
- [ ] Know how to check Render logs if issues arise

---

## Troubleshooting

### "Build failed"
- Check Render logs (dashboard → Logs tab)
- Common causes:
  - Typo in `requirements.txt`
  - Missing `Procfile` or `runtime.txt`
  - Python syntax error in `app.py`

### "Deploy failed"
- Same as above — check logs

### App loads but form doesn't work
- Check browser console (F12 → Console tab)
- Check Render logs for Python errors

### Files not uploading
- Max size is 100MB (should be fine for Excel files)
- Supported: `.xlsx`, `.xls` for property list; `.jpg`, `.png` for headshot

### No Street View photos on flyers
- ~30-40% of rural addresses have no Street View imagery (normal)
- Flyers show placeholder in these cases
- API is working fine

### QR codes not generating
- Make sure social URLs are valid
- Example good: `https://instagram.com/your_handle`
- Empty fields are fine (just skipped)

---

## Next Steps (Future Enhancements)

Once deployed and working:

1. **Get feedback** from other agents
2. **Add custom recent deals** editor (web form)
3. **Add classification step** — auto-detect property types via AI
4. **Multi-agent support** — agents have separate accounts
5. **Batch history** — store generated flyer sets
6. **Email integration** — send flyers directly from app

---

## Useful Links

- **Render Dashboard:** https://dashboard.render.com
- **GitHub Repo:** https://github.com/YourUsername/bbrc-flyer-app
- **This App URL:** https://bbrc-flyer-generator.onrender.com (after deployment)
- **Render Docs:** https://render.com/docs

---

## Done! 🎉

Once you see **Live** status on Render and can successfully generate flyers, you're ready to share with the team.

**Questions?** Check the README.md or contact Harrison Carroll at harrison@billyboydrealty.com
