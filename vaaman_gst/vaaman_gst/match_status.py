import frappe


@frappe.whitelist()
def set_match_status(purchase_invoice):
    if not purchase_invoice:
        return ""

    match_status = frappe.db.get_value(
        "GST Inward Supply",
        {"link_name": purchase_invoice},
        "match_status",
    ) or ""

    current = frappe.db.get_value(
        "Purchase Invoice", purchase_invoice, "custom_match_status"
    )

    if current != match_status:
        frappe.db.set_value(
            "Purchase Invoice",
            purchase_invoice,
            "custom_match_status",
            match_status,
            update_modified=False,
        )

    return match_status