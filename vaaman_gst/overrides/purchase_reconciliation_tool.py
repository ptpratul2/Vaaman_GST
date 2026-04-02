import importlib
import re
import frappe

from erpnext.accounts.doctype.accounting_dimension.accounting_dimension import (
    get_accounting_dimensions,
)
from india_compliance.gst_india.doctype.purchase_reconciliation_tool.purchase_reconciliation_tool import (
    BuildExcel,
    ReconciledData,
)

PRT_MODULE = "india_compliance.gst_india.doctype.purchase_reconciliation_tool.purchase_reconciliation_tool"


class CustomBuildExcel(BuildExcel):
    def get_supplier_columns(self):
        return [
            {
                "label": "Supplier Name",
                "fieldname": "supplier_name",
                "data_format": {"horizontal": "left"},
            },
            {
                "label": "Supplier GSTIN",
                "fieldname": "supplier_gstin",
                "data_format": {"horizontal": "left"},
            },
            {
                "label": "Count \n 2A/2B Docs",
                "fieldname": "inward_supply_count",
                "fieldtype": "Int",
                "data_format": {"number_format": "#,##0"},
            },
            {
                "label": "Count \n Purchase Docs",
                "fieldname": "purchase_count",
                "fieldtype": "Int",
                "data_format": {
                    "number_format": "#,##0",
                },
            },
            {
                "label": "Taxable Amount Diff \n 2A/2B - Purchase",
                "fieldname": "taxable_value_difference",
                "fieldtype": "Float",
                "data_format": {
                    "bg_color": self.COLOR_PALLATE.light_pink,
                    "number_format": "0.00",
                },
                "header_format": {
                    "bg_color": self.COLOR_PALLATE.dark_pink,
                },
            },
            {
                "label": "Tax Difference \n 2A/2B - Purchase",
                "fieldname": "tax_difference",
                "fieldtype": "Float",
                "data_format": {
                    "bg_color": self.COLOR_PALLATE.light_pink,
                    "number_format": "0.00",
                },
                "header_format": {
                    "bg_color": self.COLOR_PALLATE.dark_pink,
                },
            },
            {
                "label": "Differences",
                "fieldname": "differences",
                "fieldtype": "Data", # JS mein fieldname 'differences' hai
                "data_format": {
                    "bg_color": self.COLOR_PALLATE.light_pink,
                    "horizontal": "left",
                },
                "header_format": {
                    "bg_color": self.COLOR_PALLATE.dark_pink,
                    "width": 25,
                },
            },
            {
                "label": "%Action Taken",
                "fieldname": "action_taken_count",
                "data_format": {"number_format": "0.00%"},
                "header_format": {
                    "width": 12,
                },
            },
        ]

    def get_invoice_columns(self):
        self.dimension_fields = ["project", "cost_center"] + get_accounting_dimensions()
        dimension_columns = [
            {
                "label": frappe.unscrub(dimension),
                "fieldname": dimension,
                "data_format": {
                    "horizontal": "left",
                },
            }
            for dimension in self.dimension_fields
        ]

        self.pr_columns = [
            # ... (Green columns logic remains same)
            {
                "label": "Bill No",
                "fieldname": "bill_no",
                "compare_with": "inward_supply_bill_no",
                "data_format": {"horizontal": "left", "bg_color": self.COLOR_PALLATE.light_green},
                "header_format": {"bg_color": self.COLOR_PALLATE.green, "width": 12},
            },
            {
                "label": "Bill Date",
                "fieldname": "bill_date",
                "compare_with": "inward_supply_bill_date",
                "data_format": {"horizontal": "left", "bg_color": self.COLOR_PALLATE.light_green},
                "header_format": {"bg_color": self.COLOR_PALLATE.green, "width": 12},
            },
            {
                "label": "GSTIN",
                "fieldname": "supplier_gstin",
                "compare_with": "inward_supply_supplier_gstin",
                "data_format": {"horizontal": "left", "bg_color": self.COLOR_PALLATE.light_green},
                "header_format": {"bg_color": self.COLOR_PALLATE.green, "width": 15},
            },
            {
                "label": "Place of Supply",
                "fieldname": "place_of_supply",
                "compare_with": "inward_supply_place_of_supply",
                "data_format": {"horizontal": "left", "bg_color": self.COLOR_PALLATE.light_green},
                "header_format": {"bg_color": self.COLOR_PALLATE.green, "width": 12},
            },
            {
                "label": "Reverse Charge",
                "fieldname": "is_reverse_charge",
                "compare_with": "inward_supply_is_reverse_charge",
                "data_format": {"horizontal": "left", "bg_color": self.COLOR_PALLATE.light_green},
                "header_format": {"bg_color": self.COLOR_PALLATE.green, "width": 12},
            },
            {
                "label": "Taxable Value",
                "fieldname": "taxable_value",
                "compare_with": "inward_supply_taxable_value",
                "fieldtype": "Float",
                "data_format": {"bg_color": self.COLOR_PALLATE.light_green, "number_format": "0.00"},
                "header_format": {"bg_color": self.COLOR_PALLATE.green, "width": 12},
            },
            {
                "label": "CGST",
                "fieldname": "cgst",
                "compare_with": "inward_supply_cgst",
                "fieldtype": "Float",
                "data_format": {"bg_color": self.COLOR_PALLATE.light_green, "number_format": "0.00"},
                "header_format": {"bg_color": self.COLOR_PALLATE.green, "width": 12},
            },
            {
                "label": "SGST",
                "fieldname": "sgst",
                "compare_with": "inward_supply_sgst",
                "fieldtype": "Float",
                "data_format": {"bg_color": self.COLOR_PALLATE.light_green, "number_format": "0.00"},
                "header_format": {"bg_color": self.COLOR_PALLATE.green, "width": 12},
            },
            {
                "label": "IGST",
                "fieldname": "igst",
                "compare_with": "inward_supply_igst",
                "fieldtype": "Float",
                "data_format": {"bg_color": self.COLOR_PALLATE.light_green, "number_format": "0.00"},
                "header_format": {"bg_color": self.COLOR_PALLATE.green, "width": 12},
            },
            {
                "label": "CESS",
                "fieldname": "cess",
                "compare_with": "inward_supply_cess",
                "fieldtype": "Float",
                "data_format": {"bg_color": self.COLOR_PALLATE.light_green, "number_format": "0.00"},
                "header_format": {"bg_color": self.COLOR_PALLATE.green, "width": 12},
            },
        ]

        self.inward_supply_columns = [
            # ... (Blue columns logic remains same)
            {
                "label": "Bill No",
                "fieldname": "inward_supply_bill_no",
                "compare_with": "bill_no",
                "data_format": {"horizontal": "left", "bg_color": self.COLOR_PALLATE.light_blue},
                "header_format": {"bg_color": self.COLOR_PALLATE.sky_blue, "width": 12},
            },
            {
                "label": "Bill Date",
                "fieldname": "inward_supply_bill_date",
                "compare_with": "bill_date",
                "data_format": {"horizontal": "left", "bg_color": self.COLOR_PALLATE.light_blue},
                "header_format": {"bg_color": self.COLOR_PALLATE.sky_blue, "width": 12},
            },
            {
                "label": "GSTIN",
                "fieldname": "inward_supply_supplier_gstin",
                "compare_with": "supplier_gstin",
                "data_format": {"horizontal": "left", "bg_color": self.COLOR_PALLATE.light_blue},
                "header_format": {"bg_color": self.COLOR_PALLATE.sky_blue, "width": 15},
            },
            {
                "label": "Place of Supply",
                "fieldname": "inward_supply_place_of_supply",
                "compare_with": "place_of_supply",
                "data_format": {"horizontal": "left", "bg_color": self.COLOR_PALLATE.light_blue},
                "header_format": {"bg_color": self.COLOR_PALLATE.sky_blue, "width": 12},
            },
            {
                "label": "Reverse Charge",
                "fieldname": "inward_supply_is_reverse_charge",
                "compare_with": "is_reverse_charge",
                "data_format": {"horizontal": "left", "bg_color": self.COLOR_PALLATE.light_blue},
                "header_format": {"bg_color": self.COLOR_PALLATE.sky_blue, "width": 12},
            },
            {
                "label": "Taxable Value",
                "fieldname": "inward_supply_taxable_value",
                "compare_with": "taxable_value",
                "fieldtype": "Float",
                "data_format": {"number_format": "0.00", "bg_color": self.COLOR_PALLATE.light_blue},
                "header_format": {"bg_color": self.COLOR_PALLATE.sky_blue, "width": 12},
            },
            {
                "label": "CGST",
                "fieldname": "inward_supply_cgst",
                "compare_with": "cgst",
                "fieldtype": "Float",
                "data_format": {"number_format": "0.00", "bg_color": self.COLOR_PALLATE.light_blue},
                "header_format": {"bg_color": self.COLOR_PALLATE.sky_blue, "width": 12},
            },
            {
                "label": "SGST",
                "fieldname": "inward_supply_sgst",
                "compare_with": "sgst",
                "fieldtype": "Float",
                "data_format": {"number_format": "0.00", "bg_color": self.COLOR_PALLATE.light_blue},
                "header_format": {"bg_color": self.COLOR_PALLATE.sky_blue, "width": 12},
            },
            {
                "label": "IGST",
                "fieldname": "inward_supply_igst",
                "compare_with": "igst",
                "fieldtype": "Float",
                "data_format": {"number_format": "0.00", "bg_color": self.COLOR_PALLATE.light_blue},
                "header_format": {"bg_color": self.COLOR_PALLATE.sky_blue, "width": 12},
            },
            {
                "label": "CESS",
                "fieldname": "inward_supply_cess",
                "compare_with": "cess",
                "fieldtype": "Float",
                "data_format": {"number_format": "0.00", "bg_color": self.COLOR_PALLATE.light_blue},
                "header_format": {"bg_color": self.COLOR_PALLATE.sky_blue, "width": 12},
            },
        ]

        inv_columns = [
            {
                "label": "Action Status",
                "fieldname": "action",
                "data_format": {"horizontal": "left"},
            },
            {
                "label": "Match Status",
                "fieldname": "match_status",
                "data_format": {"horizontal": "left"},
            },
            {
                "label": "Supplier Name",
                "fieldname": "supplier_name",
                "data_format": {"horizontal": "left"},
            },
            {
                "label": "PAN",
                "fieldname": "pan",
                "data_format": {"horizontal": "center"},
                "header_format": {"width": 15},
            },
            { 
                 "label": "Posting Date",
                 "fieldname": "posting_date",
                 "fieldtype": "Date",
                 "data_format": {"horizontal": "center"}
            },
            {
                "label": "Classification",
                "fieldname": "classification",
                "data_format": {"horizontal": "left"},
                "header_format": {"width": 11},
            },
            *dimension_columns,
            {
                "label": "Inward Supply Name",
                "fieldname": "inward_supply_name",
                "data_format": {"horizontal": "left"},
            },
            {
                "label": "Purchase Document Name",
                "fieldname": "purchase_invoice_name",
                "data_format": {"horizontal": "left"},
            },
            {
                "label": "Taxable Value Difference",
                "fieldname": "taxable_value_difference",
                "fieldtype": "Float",
                "data_format": {
                    "bg_color": self.COLOR_PALLATE.light_pink,
                    "number_format": "0.00",
                },
                "header_format": {
                    "bg_color": self.COLOR_PALLATE.dark_pink,
                    "width": 12,
                },
            },
            {
                "label": "Tax Difference",
                "fieldname": "tax_difference",
                "fieldtype": "Float",
                "data_format": {
                    "bg_color": self.COLOR_PALLATE.light_pink,
                    "number_format": "0.00",
                },
                "header_format": {
                    "bg_color": self.COLOR_PALLATE.dark_pink,
                    "width": 12,
                },
            },
            # --- YEH COLUMN MAINE ADD KIYA HAI ---
            {
                "label": "Differences",
                "fieldname": "differences",
                "data_format": {
                    "bg_color": self.COLOR_PALLATE.light_pink,
                    "horizontal": "left",
                },
                "header_format": {
                    "bg_color": self.COLOR_PALLATE.dark_pink,
                    "width": 25,
                },
            },
        ]

        inv_columns.extend(self.inward_supply_columns)
        inv_columns.extend(self.pr_columns)

        return inv_columns

    def get_invoice_data(self):
        data = ReconciledData(**self.doc).get_consolidated_data(
            self.data.get("purchases"),
            self.data.get("inward_supplies"),
            prefix="inward_supply",
        )

        if not data:
            return []

        invoice_names = [
            row.get("purchase_invoice_name")
            for row in data
            if row.get("purchase_invoice_name")
        ]

        invoice_map = {}
        if invoice_names:
            invoices = frappe.get_all(
                "Purchase Invoice",
                filters={"name": ["in", invoice_names]},
                fields=["name", "posting_date"],
            )
            invoice_map = {d.name: d.posting_date for d in invoices}

        for row in data:
            row["posting_date"] = invoice_map.get(row.get("purchase_invoice_name"))

        self.supplier_name = re.sub(r"[<>[\]?:|*]", "", data[0].get("supplier_name") or "")
        self.supplier_gstin = data[0].get("supplier_gstin")

        return self.process_data(data, self.invoice_header)


def patch_build_excel():
    module = importlib.import_module(PRT_MODULE)
    module.BuildExcel = CustomBuildExcel