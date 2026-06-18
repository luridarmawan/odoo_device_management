/** @odoo-module **/
import { registry } from "@web/core/registry";
import { CharField, charField } from "@web/views/fields/char/char_field";

export class ListIPAddressField extends CharField {
    static template = "device_management.CopyableIPField";
}

export const listCopyableIPField = {
    ...charField,
    component: ListIPAddressField,
};

registry.category("fields").add("list.copyable_ip", listCopyableIPField);

export class RemoteLinkField extends CharField {
    static template = "device_management.RemoteLinkField";
    get hrefValue() {
        return this.props.value || '';
    }
    onLinkClick(ev) {
        ev.preventDefault();
        window.open(this.hrefValue, '_blank');
    }
}

export const remoteLinkField = {
    ...charField,
    component: RemoteLinkField,
};

registry.category("fields").add("link_protocol", remoteLinkField);
