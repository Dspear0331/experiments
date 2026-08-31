import pdfplumber
import re
import tkinter as tk 
import datetime
from tkinter import filedialog, messagebox

# Hidden tk root window
root = tk.Tk()
root.withdraw()

# 1. Open File Dialog
file_path = filedialog.askopenfilename(
    title="Select a bank statement to process",
    filetypes=[("PDF files", "*.pdf")]
)

deductables = []

THERAPY_EXPENSE_KEYWORDS = [
    # EHR & Practice Software
    "SIMPLEPRACTICE", "SIMPLE PRAC", "THERAPYNOTES", "THERANEST", 
    "KAREO", "CERBO", "JANE APP", "JANE.APP",
    # Payment Processors & Merchant Fees
    "IVY PAY", "IVYPAY", "STRIPE", "SQUARE", "SQ *", "PAYPAL",
    # Telehealth & Communications
    "DOXY.ME", "ZOOM.US", "ZOOM", "SPRUCE HEALTH", "IPLUM", 
    "RINGCENTRAL", "DIALPAD", "VERIZON", "AT&T", "T-MOBILE",
    # Directories & Marketing
    "PSYCHOLOGY TODAY", "PSYCH TODAY", "THERAPYDEN", "GOODTHERAPY", 
    "ZENCARE", "GOOGLE ADS", "GOOGLE*ADS", "FACEBK", "META ADS", 
    "CANVA", "SQUARESPACE", "SQUAREDOMAIN", "WORDPRESS", "AUTOMATTIC", "WIX",
    # Office & Clinical Supplies / Hardware
    "AMAZON", "AMZN MKTP", "STAPLES", "OFFICE DEPOT", "OFFICEMAX", 
    "APPLE.COM", "BEST BUY", "TARGET", "WALMART",
    # CEUs, Training, Supervision & Dues
    "PESI", "EMDRIA", "PSYCHOTHERAPY NETWORKER", "APA", "AMER PSYCHOL", 
    "NASW", "ACA", "AAMFT", "CEU", "CONTINUING ED",
    # Software, Email & HIPAA Tools
    "GSUITE", "GOOGLE WORKSPACE", "HUSHMAIL", "PROTONMAIL", "PROTON", 
    "SHRED-IT", "SHREDIT", "DROPBOX", "MICROSOFT", "MSFT",     
    # Insurance, Accounting & Payroll
    "HPSO", "AON", "CPH", "AMERICAN PROFESSIONAL", "GUSTO", 
    "PAYROLL", "QUICKBOOKS", "INTUIT", "XERO",
    # Space & Utilities
    "MANAGEMENT", "REALTY", "PROPERTIES", "ELECTRIC", "UTILITIES", 
    "COMCAST", "SPECTRUM", "CONED"
]

timestamp=datetime.datetime.now().strftime("%d-%H-%M")
full_text=""
pattern = r'^(\d{2}-\d{2})\s*(.*)'

if file_path:
    try:
        # Extract text from the PDF pages
        with pdfplumber.open(file_path) as pdf:
            for page in pdf.pages[1:-1]:
                text = page.extract_text()
                if text:
                    full_text += text + '\n'

        # Parse text line by line
        for line in full_text.splitlines():
            match = re.match(pattern, line)
            if match:
                date, details = match.groups()
                details_upper = details.upper()
                
                # Check if any keyword appears in the line details
                for keyword in THERAPY_EXPENSE_KEYWORDS:
                    if keyword in details_upper:
                        deductables.append({
                            "Date": date,
                            "Keyword": keyword,
                            "Details": details
                        })
                        break

        # Output logic: Save results to a text file in the same directory
        if deductables:
            output_path = file_path.replace(".pdf", f"{timestamp}_deductibles.txt")
            with open(output_path, "w", encoding="utf-8") as f:
                f.write("FOUND DEDUCTIBLE EXPENSES:\n")
                f.write("=" * 40 + "\n")
                for item in deductables:
                    f.write(f"Date: {item['Date']} | Keyword: {item['Keyword']}\n")
                    f.write(f"Details: {item['Details']}\n")
                    f.write("-" * 40 + "\n")

            messagebox.showinfo(
                "Processing Complete", 
                f"Found {len(deductables)} deductible item(s)!\nResults saved to:\n{output_path}"
            )
        else:
            messagebox.showinfo("Processing Complete", "No deductible expenses were found in this statement.")

    except Exception as e:
        messagebox.showerror("Error", f"An error occurred while processing:\n{str(e)}")

else:
    messagebox.showwarning("Cancelled", "No file was selected.")
