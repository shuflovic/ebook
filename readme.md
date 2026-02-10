# Blogger to eBook Converter

Convert your Blogger blog posts into a compiled ebook format (HTML, Markdown, PDF, or EPUB) with a simple Python script!

## ✨ Features

- ✅ No API key required - works out of the box!
- ✅ Fetches all posts from your public Blogger blog
- ✅ Uses Blogger's public JSON feed (no authentication needed)
- ✅ Exports to HTML and Markdown formats
- ✅ Clean, professional formatting
- ✅ Chronological ordering of posts
- ✅ Preserves images and formatting
- ✅ Easy conversion to PDF, EPUB, or DOCX

## 📋 Requirements

- Python 3.7 or higher
- Internet connection
- A public Blogger blog

## 🚀 Installation

1. **Install Python** (if you don't have it):
   - Download from https://www.python.org/downloads/
   - Make sure to check "Add Python to PATH" during installation

2. **Install dependencies**:
   ```bash
   pip install requests beautifulsoup4
   ```

   Or use the requirements file:
   ```bash
   pip install -r requirements_v2.txt
   ```

## 💻 Usage

### Basic Usage

1. Run the script:
   ```bash
   python blogger_to_ebook_v2.py
   ```

2. Enter your blog URL when prompted:
   ```
   Enter your Blogger blog URL: https://myblog.blogspot.com
   ```

3. Choose your output format:
   - `1` - HTML (recommended for PDF conversion)
   - `2` - Markdown
   - `3` - Both formats

4. Done! Your ebook file(s) will be created in the same folder.

### Example

```
================================================
Blogger to eBook Converter (Web Scraping)
================================================

Enter your Blogger blog URL: https://mytravelblog.blogspot.com

Fetching posts...
Found 20 posts

✓ Successfully fetched 20 posts!

Choose output format:
1. HTML (recommended - best for PDF conversion)
2. Markdown
3. Both

Enter your choice (1-3): 1

✓ HTML file saved to: blog_ebook.html

================================================
✓ Conversion complete!
================================================
```

## 📄 Output Formats

### HTML Format (`blog_ebook.html`)
- Beautiful, professional styling
- Ready to view in any web browser
- Perfect for PDF conversion
- Best preservation of formatting and images
- Print-friendly layout

### Markdown Format (`blog_ebook.md`)
- Plain text format
- Easy to edit and customize
- Compatible with most text editors
- Can be converted to other formats

## 🔄 Converting to Other Formats

### HTML → PDF (Recommended Method)

**Using Your Browser (Easiest!):**
1. Open `blog_ebook.html` in Chrome, Firefox, or Edge
2. Press `Ctrl+P` (Windows/Linux) or `Cmd+P` (Mac)
3. In the print dialog:
   - Destination: "Save as PDF"
   - Layout: Portrait
   - Margins: Default or Custom
   - Background graphics: ✓ (to keep styling)
4. Click "Save"
5. Choose where to save your PDF

**Tips for better PDF:**
- Adjust margins to fit more content per page
- Enable "Background graphics" for better styling
- Use "Print backgrounds" option if available

### HTML/Markdown → EPUB (For E-Readers)

**Using Calibre (Free):**
1. Download and install [Calibre](https://calibre-ebook.com/)
2. Open Calibre
3. Click "Add books" → Select `blog_ebook.html`
4. Select the book and click "Convert books"
5. Choose "EPUB" as the output format
6. Click "OK" and wait for conversion
7. Right-click the book → "Open containing folder" to find your EPUB

### Markdown → DOCX (Word Document)

**Using Pandoc (Free):**
1. Download and install [Pandoc](https://pandoc.org/installing.html)
2. Open terminal/command prompt in your ebook folder
3. Run:
   ```bash
   pandoc blog_ebook.md -o blog_ebook.docx
   ```

**Or use an online converter:**
- https://www.markdowntopdf.com/
- https://dillinger.io/ (export as DOCX)

## ❓ Troubleshooting

### "No posts found!"

**Possible causes:**
- ❌ Blog URL is incorrect - double-check the URL
- ❌ Blog is set to private - make it public in Blogger settings
- ❌ Blog has no published posts (only drafts)
- ❌ Blog domain doesn't end in `.blogspot.com` - try the original Blogspot URL

**Solutions:**
1. Verify your blog URL is correct
2. Make sure your blog is public (Settings → Privacy → Blog Readers → Public)
3. Check that you have published posts (not just drafts)

### Images not showing in PDF

**This is normal!** Images are linked from Blogger's servers.

**Solutions:**
- Make sure you're connected to the internet when viewing
- In browser print dialog, enable "Background graphics"
- Images should appear in the PDF if internet is available

### Script runs but creates empty file

**Possible causes:**
- Blogger's feed format changed
- Network/firewall blocking the request

**Solutions:**
1. Try running again (might be temporary network issue)
2. Check if you can access your blog in a browser
3. Try a different internet connection

### Python not found

**Solution:**
- Make sure Python is installed: https://www.python.org/downloads/
- During installation, check "Add Python to PATH"
- Restart your terminal/command prompt after installation

## 🎯 Tips & Tricks

### For Large Blogs (50+ posts)
- The script handles pagination automatically
- It may take a minute or two to fetch all posts
- Be patient and let it complete

### For Better Formatting
- The HTML template includes custom CSS styling
- You can edit the script to customize colors, fonts, etc.
- Look for the `<style>` section in the `save_to_html()` function

### For Private Blogs
- The script only works with public blogs
- Make your blog temporarily public, run the script, then make it private again
- Or manually copy/paste each post

### Customizing the Output
- Edit the CSS in the script for different styling
- Change the sorting order (currently chronological)
- Add your own cover page or introduction

## 📚 How It Works

The script:
1. Accesses your blog's public JSON feed (same feed used by RSS readers)
2. Parses all post data (title, content, date, etc.)
3. Cleans and formats the HTML content
4. Sorts posts chronologically
5. Generates a single HTML/Markdown file with all posts

**No authentication required!** It uses publicly available data.

## 🔒 Privacy & Security

- ✅ Script only accesses public data
- ✅ No login credentials needed
- ✅ No data sent to external servers
- ✅ Everything runs locally on your computer
- ✅ Your blog posts remain on Blogger

## 🆘 Need Help?

Common questions:

**Q: Can I use this for WordPress or other platforms?**  
A: No, this is specifically for Blogger. Each platform needs its own script.

**Q: Will this work with private blogs?**  
A: No, only public blogs. Make it temporarily public to export.

**Q: Does it include comments?**  
A: No, only the post content. Comments are not included.

**Q: Can I customize the design?**  
A: Yes! Edit the CSS in the `save_to_html()` function.

**Q: What if I have 100+ posts?**  
A: Should work fine! The script can handle any number of posts.

## 📝 License

Free to use and modify for personal or commercial purposes.

## 🙏 Credits

Created to help bloggers easily archive and share their content!

---

**Enjoy your ebook! 📖**