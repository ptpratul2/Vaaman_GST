frappe.ui.form.on('Purchase Invoice', {
    refresh: function (frm) {
        if (!frm.doc.name || frm.is_new()) return;

        frappe.call({
            method: 'vaaman_gst.vaaman_gst.match_status.set_match_status',
            args: {
                purchase_invoice: frm.doc.name,
            },
            callback: function (r) {
                if (r.message === undefined) return;
                if (frm.doc.custom_match_status === r.message) return;

                frm.doc.custom_match_status = r.message;
                frm.refresh_field('custom_match_status');
            },
        });
    },
});