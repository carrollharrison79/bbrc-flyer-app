# BBRC Flyer Generator — Agent User Guide

## Quick Start (3 Steps)

### 1. Open the App
Go to: **https://bbrc-flyer-generator.onrender.com**

You'll see a blue form with these sections:
- **Agent Information**
- **Social Media** (optional)
- **Files**

### 2. Fill Out the Form

#### Required Fields (marked with *)
- **Full Name:** Your name as you want it on the flyer
- **Phone:** Your phone number
- **Email:** Your contact email
- **Property List:** Upload your Excel file (see format below)

#### Optional Fields
- **Title:** How you want to be described (defaults to "Commercial Salesman")
- **Social Media:** Instagram, Facebook, LinkedIn URLs
  - Leave blank if you don't want them
  - QR codes auto-generate from these URLs
- **Headshot:** Your professional photo (JPG or PNG)
  - Will appear as circular image on sidebar
  - Auto-resized and cropped to square

### 3. Generate & Download
Click **Generate Flyers** → download zip file with all PDFs

**That's it!** 1,700+ personalized flyers in minutes.

---

## Input File: Property List (Excel)

### Format
Your Excel file must have a sheet named **"Parcel Details"** with these columns:

| Column | Example | Notes |
|--------|---------|-------|
| Owner Name / Entity | John Smith LLC | Who owns it |
| Owner Address | 123 Main St | Mailing address |
| Owner Zip | 35401 | Zip code |
| Parcel ID | 12-34-567-8 | Unique ID |
| Property Address | 500 Industrial Blvd | Street address |
| Property Zip | 35401 | Property zip |
| Type | Industrial/Warehouse | Property type |
| Use | Light Manufacturing | Current use |

### How It Works
- Rows alternate: owner info → parcel details → owner info → parcel details
- Script **auto-flattens** and groups by owner
- One owner can have multiple properties → all listed on their flyer
- Properties appear in 2-column format

### Property Types (for market messaging)
Script uses these to customize the pitch on each flyer:

✓ Commercial Retail  
✓ Vacant Land  
✓ Industrial/Warehouse  
✓ Multifamily Residential  
✓ Commercial Office  
✓ Self-Storage  
✓ Mining/Extraction  
✓ Agricultural  
✓ Religious  
✓ HOA/Common Area  
✓ Marina/Recreational  
✓ Mixed Use  
✓ Single-Family Residential  
✓ Utility/Infrastructure  
✓ Unknown  

---

## What You'll Get

### Per Property Owner: 2-Page PDF

**Page 1 — Sales Pitch + Holdings**
- Left sidebar (blue):
  - Your circular headshot
  - Your name (bold white)
  - Your title (light blue text)
  - Phone, email, company name, website
  - 3 QR codes (Instagram, Facebook, LinkedIn) — auto-generated
  - Company logo

- Right content (white):
  - Header: "PROPERTY OWNER" + owner name + mailing address
  - "YOUR HOLDINGS" — list of all their properties in 2 columns
  - Property photo (from Google Street View)
  - "MARKET SNAPSHOT" — 3 tailored stats for their property type
  - "RECENT BBRC ACTIVITY" — recent deals
  - "A NOTE FROM YOU" — tailored pitch message (changes by property type)

**Page 2 — Mailing Panel**
- Your return address (top left)
- Stamp box (top right, 1.1" x 0.85")
- Recipient address (centered, lower half)
- "FIRST CLASS MAIL" text
- Fold guide (dashed line down the middle)

### File Format
- **Type:** PDF (print-ready)
- **Size:** 8.5" x 6" landscape
- **Color:** Full color, bleeds to edges
- **Quality:** 300 DPI equivalent (ReportLab standard)

---

## Social Media URLs

### How to Format Them

**Instagram:**
- ✓ `https://instagram.com/yourhandle`
- ✓ `https://instagram.com/your.name`

**Facebook:**
- ✓ `https://facebook.com/yourname`
- ✓ `https://facebook.com/your.name`

**LinkedIn:**
- ✓ `https://linkedin.com/in/your-name`
- ✓ `https://linkedin.com/in/yourname`

### What Happens
- Each URL → QR code (auto-generated)
- 3 QR codes stacked on sidebar of flyer
- Recipients can scan → link to your profile
- Leave blank if you don't have one

---

## Headshot Photo

### Requirements
- **Format:** JPG or PNG
- **Size:** Any size (auto-resized)
- **Best if:** 
  - Professional headshot
  - Face centered
  - Landscape or portrait orientation
  - Good lighting
  - High resolution (1000+ pixels)

### What Happens
- Photo auto-cropped to square
- Resized to 220x220 pixels
- Appears as circular image on sidebar
- White ring around circle

**Skip it** if you don't have a photo — placeholder shows on flyers.

---

## Printing & Mailing

### Print Settings
- **Paper:** Standard 8.5" x 11" white (cut to 8.5" x 6" landscape after printing)
- **Color:** Full color recommended (blue sidebar looks professional)
- **Quality:** Standard (300 DPI equivalent)
- **Duplex:** 2-sided printing (page 1 on front, page 2 on back)

### Mailing
- **Postage:** USPS Large Postcard rate (~$0.56 each)
- **Fold:** Fold in half at dashed line (page 1 inside, page 2 outside)
- **Sealing:** Self-sealing (no envelope needed, just seal the fold)
- **Addressing:** Already on back (page 2)

### Cost Estimate
- **1,700 flyers:** ~$950 in postage
- **Design/printing:** Per your printer
- **ROI:** Depends on response rate

---

## Troubleshooting

### "Form Won't Load"
- Refresh the page
- Check your internet connection
- Try a different browser (Chrome, Safari, Firefox)

### "File Upload Not Working"
- File is **under 100MB** (usually not an issue for Excel)
- Excel file has sheet named **"Parcel Details"** (exact name matters)
- Try uploading the file directly (don't drag-drop)

### "Generation Takes Forever"
- Normal for large batches (1,700 owners = ~15-30 minutes)
- Server is fetching Street View photos (takes time)
- **Don't refresh** — let it finish
- Check browser status bar for progress

### "No Street View Photos on Flyers"
- ~30-40% of rural addresses have no Google Street View imagery (normal)
- App shows light blue placeholder instead
- This is expected — not an error

### "QR Codes Aren't Showing"
- Social URLs might have typos
- Leave them blank if you're not sure
- QR codes are optional

### "Email Missing from Sidebar"
- Check form — required field (marked with *)
- Email is mandatory for contact

---

## Tips for Best Results

✓ **Professional headshot** — makes flyer look polished  
✓ **Correct social URLs** — QR codes actually work  
✓ **Clean property list** — no blank rows, consistent formatting  
✓ **Recent property list** — updates should be current  
✓ **Multiple properties per owner** — flyer lists all of them  
✓ **Consider the data quality** — bad data in = bad flyers out  

---

## FAQ

**Q: Can I edit the flyers after downloading?**  
A: Yes, they're standard PDFs. You can edit in any PDF editor, but it's easier to re-generate with corrections.

**Q: What if I want to change property details?**  
A: Update your Excel file, re-upload, and generate again. Takes ~5 minutes.

**Q: Can multiple agents use this?**  
A: Yes! Each agent fills their own form with their own info/photo/socials. One app, many agents.

**Q: How long do flyers stay generated?**  
A: You download immediately. No storage on server. If you want them again, just re-generate.

**Q: Can I print just some flyers?**  
A: Unzip the folder, delete the PDFs you don't need, print the rest.

**Q: Will my email/phone appear on the mailing panel?**  
A: Only your name and company address appear on back (mailing panel). Phone/email only on front.

**Q: What if I don't have a professional headshot?**  
A: Leave it blank — white placeholder appears on flyer.

**Q: Can I use a logo instead of a headshot?**  
A: Not with this version, but you can request this feature.

---

## Support

**Something not working?** Contact Harrison Carroll at:
- **Email:** harrison@billyboydrealty.com
- **Phone:** 205-534-2628

**Or check:**
- README.md (full app documentation)
- DEPLOYMENT_CHECKLIST.md (technical details)

---

## Example Workflow

```
Monday morning:
  1. Export latest property data to Excel
  2. Go to app URL
  3. Fill in your info (2 minutes)
  4. Upload Excel file
  5. Click Generate (wait ~20 min)
  6. Download zip
  
Tuesday:
  7. Send zip to printer
  8. Printer formats → prints → cuts → binds
  
Wednesday:
  9. Receive printed stacks
  10. Fold flyers at dashed line
  11. Seal (no envelope needed)
  12. Add stamp
  13. Take to post office
  
2-3 weeks later:
  14. Responses & leads!
```

---

## Quick Reference Card

| What | How |
|------|-----|
| **Open app** | https://bbrc-flyer-generator.onrender.com |
| **Required fields** | Name, Phone, Email, Property List |
| **Optional fields** | Title, Social URLs, Headshot |
| **Property file format** | Excel with sheet "Parcel Details" |
| **Generation time** | 15-30 min for 1,700 flyers |
| **Download format** | ZIP with PDFs (print-ready) |
| **Print size** | 8.5" x 6" landscape (2-page per owner) |
| **Postage** | USPS Large Postcard (~$0.56/piece) |
| **Support** | harrison@billyboydrealty.com |

---

**Version:** 1.0  
**Last Updated:** May 2026  
**Questions?** Ask Harrison!
