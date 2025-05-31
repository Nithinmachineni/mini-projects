import pandas as pd
import matplotlib.pyplot as plt
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from reportlab.platypus import Table, TableStyle
from reportlab.lib import colors
import os

# Load CSV
df = pd.read_csv("lab_results.csv")

# Normalize test names
df['TestName_clean'] = df['TestName'].str.lower().str.replace(' ', '')
df['Date'] = pd.to_datetime(df['Date'])

# Input Patient ID
patient_id = input("Enter Patient ID: ").strip()
if not patient_id.isdigit() or int(patient_id) not in df['PatientID'].values:
    print("❌ Invalid or not found Patient ID.")
    exit()
patient_id = int(patient_id)

patient_data = df[df['PatientID'] == patient_id].copy()
patient_name = patient_data['PatientName'].iloc[0]
patient_data = patient_data.sort_values(by='Date')

# Separate test categories
bp_data = patient_data[patient_data['TestName_clean'] == 'bloodpressure']
other_tests = patient_data[patient_data['TestName_clean'] != 'bloodpressure']

# ---------- General Graph ----------
fig1, ax1 = plt.subplots(figsize=(8, 3.5))
for test in other_tests['TestName_clean'].unique():
    test_df = other_tests[other_tests['TestName_clean'] == test]
    if not test_df.empty:
        dates = test_df['Date'].dt.strftime('%Y-%m-%d')
        values = test_df['Value']
        ax1.plot(dates, values, marker='o', label=test.title())
        for i, (date, value) in enumerate(zip(dates, values)):
            ax1.annotate(str(value), (date, value), textcoords="offset points",
                         xytext=(0, 8), ha='center', fontsize=8)

ax1.set_title("General Test Trends")
ax1.set_xlabel("Date")
ax1.set_ylabel("Value")
ax1.legend()
ax1.grid(True)
plt.tight_layout()
graph1_file = "general_graph.png"
plt.savefig(graph1_file, transparent=True)
plt.close()

# ---------- Blood Pressure Graph ----------
fig2, ax2 = plt.subplots(figsize=(8, 3))
if not bp_data.empty:
    bp_dates = bp_data['Date'].dt.strftime('%Y-%m-%d')
    bp_values = bp_data['Value']
    ax2.plot(bp_dates, bp_values, marker='s', color='red', label='Blood Pressure')
    for i, (date, value) in enumerate(zip(bp_dates, bp_values)):
        ax2.annotate(str(value), (date, value), textcoords="offset points",
                     xytext=(0, 8), ha='center', fontsize=8)

ax2.set_title("Blood Pressure Trend")
ax2.set_xlabel("Date")
ax2.set_ylabel("BP Value")
ax2.legend()
ax2.grid(True)
plt.tight_layout()
graph2_file = "bp_graph.png"
plt.savefig(graph2_file, transparent=True)
plt.close()

# ---------- Generate PDF ----------
pdf_file = f"lab_report_{patient_id}.pdf"
c = canvas.Canvas(pdf_file, pagesize=A4)
width, height = A4

# Margins
margin_left = 50
margin_right = 50
margin_top = 60
margin_bottom = 50
usable_width = width - margin_left - margin_right

# --- Large Watermark ---
def draw_watermark(canvas_obj):
    canvas_obj.saveState()
    canvas_obj.setFont("Helvetica-Bold", 90)
    canvas_obj.setFillColorRGB(0.9, 0.9, 0.9)
    canvas_obj.translate(width / 2, height / 2)
    canvas_obj.rotate(40)
    canvas_obj.drawCentredString(0, 0, "LAB REPORT")
    canvas_obj.restoreState()

draw_watermark(c)

# --- Top Banner ---
c.setFillColor(colors.HexColor("#b41fa5"))
c.rect(0, height - margin_top, width, 40, fill=1)

# --- Title ---
c.setFont("Helvetica-Bold", 24)
c.setFillColor(colors.white)
c.drawCentredString(width / 2, height - margin_top + 10, "PATIENT LAB REPORT")

# --- Patient Info ---
c.setFont("Helvetica", 12)
c.setFillColor(colors.black)
c.drawString(margin_left, height - margin_top - 40, f"Patient Name: {patient_name}")
c.drawString(margin_left, height - margin_top - 60, f"Patient ID: {patient_id}")

# --- Divider Line ---
c.setStrokeColor(colors.lightgrey)
c.setLineWidth(1)
c.line(margin_left, height - margin_top - 70, width - margin_right, height - margin_top - 70)

# --- Table ---
table_data = [["Date", "Test", "Value", "Unit"]] + \
    patient_data[['Date', 'TestName', 'Value', 'Unit']].astype(str).values.tolist()

table = Table(table_data, colWidths=[110, 170, 90, 70])
table.setStyle(TableStyle([
    ('BACKGROUND', (0, 0), (-1, 0), colors.lightblue),
    ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
    ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
    ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
    ('FONTSIZE', (0, 0), (-1, 0), 12),
    ('FONTSIZE', (0, 1), (-1, -1), 11),
    ('BOTTOMPADDING', (0, 0), (-1, 0), 8),
    ('TOPPADDING', (0, 0), (-1, 0), 6),
    ('GRID', (0, 0), (-1, -1), 0.3, colors.grey),
]))

table.wrapOn(c, usable_width, height)
table.drawOn(c, margin_left, height - 420)

# --- Graphs ---
c.drawImage(graph1_file, margin_left, 240, width=usable_width, height=130, mask='auto')
c.drawImage(graph2_file, margin_left, 60, width=usable_width, height=130, mask='auto')

# Save PDF
c.showPage()
c.save()

# Cleanup
os.remove(graph1_file)
os.remove(graph2_file)

print(f"✅ Report generated successfully: {pdf_file}")