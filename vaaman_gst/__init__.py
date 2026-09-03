__version__ = "0.0.1"


def _patch_purchase_reconciliation_excel():
	try:
		from vaaman_gst.overrides.purchase_reconciliation_tool import patch_build_excel

		patch_build_excel()
	except ImportError:
		# india_compliance not installed on this bench — Purchase Reconciliation Excel patch skipped
		pass


_patch_purchase_reconciliation_excel()

from vaaman_gst.vaaman_gst.custom_ledger import execute as custom_general_ledger_execute
import erpnext.accounts.report.general_ledger.general_ledger
erpnext.accounts.report.general_ledger.general_ledger.execute = custom_general_ledger_execute



