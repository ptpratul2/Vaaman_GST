import frappe

@frappe.whitelist()
def set_match_status(purchase_invoice):
    if not purchase_invoice:
        return ""

    gst_record = frappe.db.get_value(
        "GST Inward Supply",
        {"link_name": purchase_invoice},
        "match_status"
    )

    match_status = gst_record or ""

    # ✅ DB me save karo
    frappe.db.set_value(
        "Purchase Invoice",
        purchase_invoice,
        "custom_match_status",
        match_status
    )

    return match_status