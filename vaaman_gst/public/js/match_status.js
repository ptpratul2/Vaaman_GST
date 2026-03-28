frappe.ui.form.on('Purchase Invoice', {
    refresh: function(frm) {
        if (!frm.doc.name || frm.is_new()) return;

        frappe.call({
            method: "vaaman_gst.vaaman_gst.match_status.set_match_status",
            args: {
                purchase_invoice: frm.doc.name
            },
            callback: function(r) {
                if (r.message !== undefined && frm.doc.custom_match_status !== r.message) {
                    frm.set_value('custom_match_status', r.message);
                    // frm.save();  // ✅ DB save
                }
            }
        });
    }
});