import frappe
from india_compliance.gst_india.doctype.purchase_reconciliation_tool.purchase_reconciliation_tool import PurchaseReconciliationTool
from erpnext.accounts.doctype.accounting_dimension.accounting_dimension import get_accounting_dimensions

class CustomPurchaseReconciliationTool(PurchaseReconciliationTool):

    def get_invoice_columns(self):
        frappe.msgprint("Custom get_invoice_columns called========================")

        # 🔹 Dimensions
        self.dimension_fields = ["project", "cost_center"] + get_accounting_dimensions()

        dimension_columns = [
            {
                "label": frappe.unscrub(dimension),
                "fieldname": dimension,
                "data_format": {"horizontal": "left"},
            }
            for dimension in self.dimension_fields
        ]

        # 🔹 Purchase Invoice Columns (Green)
        pr_columns = [
            {"label": "Bill No", "fieldname": "bill_no"},
            {"label": "Bill Date", "fieldname": "bill_date", "fieldtype": "Date"},
            {"label": "Posting Date", "fieldname": "posting_date", "fieldtype": "Date"},  # ✅ ADDED
            {"label": "GSTIN", "fieldname": "supplier_gstin"},
            {"label": "Place of Supply", "fieldname": "place_of_supply"},
            {"label": "Reverse Charge", "fieldname": "is_reverse_charge"},
            {"label": "Taxable Value", "fieldname": "taxable_value", "fieldtype": "Float"},
            {"label": "CGST", "fieldname": "cgst", "fieldtype": "Float"},
            {"label": "SGST", "fieldname": "sgst", "fieldtype": "Float"},
            {"label": "IGST", "fieldname": "igst", "fieldtype": "Float"},
            {"label": "CESS", "fieldname": "cess", "fieldtype": "Float"},
        ]

        # 🔹 Inward Supply Columns (Blue)
        inward_supply_columns = [
            {"label": "Bill No", "fieldname": "inward_supply_bill_no"},
            {"label": "Bill Date", "fieldname": "inward_supply_bill_date", "fieldtype": "Date"},
            {"label": "GSTIN", "fieldname": "inward_supply_supplier_gstin"},
            {"label": "Place of Supply", "fieldname": "inward_supply_place_of_supply"},
            {"label": "Reverse Charge", "fieldname": "inward_supply_is_reverse_charge"},
            {"label": "Taxable Value", "fieldname": "inward_supply_taxable_value", "fieldtype": "Float"},
            {"label": "CGST", "fieldname": "inward_supply_cgst", "fieldtype": "Float"},
            {"label": "SGST", "fieldname": "inward_supply_sgst", "fieldtype": "Float"},
            {"label": "IGST", "fieldname": "inward_supply_igst", "fieldtype": "Float"},
            {"label": "CESS", "fieldname": "inward_supply_cess", "fieldtype": "Float"},
        ]

        # 🔥 MAIN COLUMNS
        columns = [
            {"label": "Action Status", "fieldname": "action"},
            {"label": "Match Status", "fieldname": "match_status"},
            {"label": "Supplier Name", "fieldname": "supplier_name"},
            {"label": "PAN", "fieldname": "pan"},
            {"label": "Posting Date", "fieldname": "posting_date", "fieldtype": "Date"},  # ✅ MAIN COLUMN
            {"label": "Classification", "fieldname": "classification"},
            *dimension_columns,
            {"label": "Inward Supply Name", "fieldname": "inward_supply_name"},
            {"label": "Purchase Invoice", "fieldname": "purchase_invoice_name"},
            {"label": "Taxable Value Difference", "fieldname": "taxable_value_difference", "fieldtype": "Float"},
            {"label": "Tax Difference", "fieldname": "tax_difference", "fieldtype": "Float"},
        ]

        # 🔹 Merge All
        columns.extend(inward_supply_columns)
        columns.extend(pr_columns)

        # 🔹 Log columns for debugging
        frappe.log_error(message=str(columns), title="CustomPurchaseReconciliationTool - Columns Fetched")

        return columns
