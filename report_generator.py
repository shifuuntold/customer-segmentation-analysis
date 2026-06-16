from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet

def generate_report(total_customers,
                    total_revenue,
                    avg_revenue,
                    top_share):

    pdf_file = "customer_report.pdf"

    doc = SimpleDocTemplate(pdf_file)

    styles = getSampleStyleSheet()

    content = []

    content.append(
        Paragraph("Customer Segmentation Executive Report",
                  styles['Title'])
    )

    content.append(Spacer(1, 20))

    content.append(
        Paragraph(f"Customers: {total_customers}",
                  styles['Normal'])
    )

    content.append(
        Paragraph(f"Revenue: ${total_revenue:,.0f}",
                  styles['Normal'])
    )

    content.append(
        Paragraph(f"Average Revenue: ${avg_revenue:,.0f}",
                  styles['Normal'])
    )

    content.append(
        Paragraph(f"Top 15% Revenue Share: {top_share:.1f}%",
                  styles['Normal'])
    )

    doc.build(content)

    return pdf_file