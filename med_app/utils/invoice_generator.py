import os
from fpdf import FPDF
from datetime import datetime

INVOICE_DIR = "invoices"

def generate_invoice_pdf(order_data, retailer_data, order_id: int) -> str:
    """Generate a clean, neatly aligned invoice PDF."""
    os.makedirs(INVOICE_DIR, exist_ok=True)
    file_path = os.path.join(INVOICE_DIR, f"invoice_{order_id}.pdf")

    pdf = FPDF()
    pdf.add_page()
    pdf.set_auto_page_break(auto=True, margin=15)

    # --- Header ---
    pdf.set_font("Arial", style="B", size=16)
    pdf.cell(0, 10, txt="INVOICE", ln=True, align="C")
    pdf.ln(8)

    # --- Retailer Info ---
    pdf.set_font("Arial", size=12)
    pdf.cell(0, 8, txt=f"Retailer: {retailer_data.shop_name}", ln=True)
    pdf.multi_cell(
        0,
        8,
        txt=f"Address: {retailer_data.address_line1}, "
            f"{retailer_data.city}, {retailer_data.state} - {retailer_data.zip_code}",
    )
    pdf.cell(0, 8, txt=f"GST: {retailer_data.gst_number}", ln=True)
    pdf.ln(5)

    # --- Order Info ---
    pdf.cell(0, 8, txt=f"Order ID: {order_id}", ln=True)
    pdf.cell(0, 8, txt=f"Date: {datetime.now().strftime('%Y-%m-%d')}", ln=True)
    pdf.ln(8)

    # --- Table Header ---
    pdf.set_font("Arial", style="B", size=12)
    pdf.set_fill_color(230, 230, 230)
    pdf.cell(80, 10, txt="Product", border=1, align="L", fill=True)
    pdf.cell(30, 10, txt="Qty", border=1, align="C", fill=True)
    pdf.cell(40, 10, txt="Price", border=1, align="R", fill=True)
    pdf.cell(40, 10, txt="Total", border=1, align="R", fill=True)
    pdf.ln()

    # --- Table Rows ---
    pdf.set_font("Arial", size=12)
    subtotal = 0
    for item in order_data.items:
        total = item.quantity * float(item.price)
        subtotal += total
        pdf.cell(80, 10, txt=str(item.medicine_id), border=1, align="L")
        pdf.cell(30, 10, txt=str(item.quantity), border=1, align="C")
        pdf.cell(40, 10, txt=f"{float(item.price):.2f}", border=1, align="R")
        pdf.cell(40, 10, txt=f"{total:.2f}", border=1, align="R")
        pdf.ln()

    # --- Totals Section ---
    tax = subtotal * 0.18
    total = subtotal + tax

    pdf.ln(5)
    pdf.set_font("Arial", style="B", size=12)

    pdf.cell(150, 8, txt="Subtotal:", border=0, align="R")
    pdf.cell(40, 8, txt=f"Rs. {subtotal:.2f}", ln=True, align="R")

    pdf.cell(150, 8, txt="GST (18%):", border=0, align="R")
    pdf.cell(40, 8, txt=f"Rs. {tax:.2f}", ln=True, align="R")

    pdf.cell(150, 8, txt="Total:", border=0, align="R")
    pdf.cell(40, 8, txt=f"Rs. {total:.2f}", ln=True, align="R")

    # --- Footer ---
    pdf.ln(10)
    pdf.set_font("Arial", style="I", size=10)
    pdf.cell(0, 10, txt="Thank you for your order!", ln=True, align="C")

    pdf.output(file_path)
    return file_path
