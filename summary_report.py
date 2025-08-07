from reportlab.pdfgen import canvas
from datetime import datetime

def generate_summary():
    c = canvas.Canvas("data/daily_summary.pdf")
    c.setFont("Helvetica", 14)
    c.drawString(50, 800, "Daily Summary Report")
    c.setFont("Helvetica", 10)
    c.drawString(50, 780, f"Generated on: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

    # Dummy content – you can load from JSON
    c.drawString(50, 750, "- Twitter: 30 posts scraped")
    c.drawString(50, 735, "- Google News: 10 articles scraped")
    c.drawString(50, 720, "- YouTube: 20 comments scraped")
    c.drawString(50, 705, "- Facebook: 15 posts scraped")

    c.save()

if __name__ == "__main__":
    generate_summary()