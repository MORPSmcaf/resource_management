/** @odoo-module */
import { ListController } from "@web/views/list/list_controller";
import { registry } from '@web/core/registry';
import { listView } from '@web/views/list/list_view';
export class ResourceListController extends ListController {
   setup() {
       super.setup();
   }
OnTestClick() {
       // Check if the user belongs to the required group
       const isGroupUser = this.env.services.rpc({
           model: 'res.users',
           method: 'has_group',
           args: ['resource_reservation.group_resource_admin'],
       });

       if (isGroupUser) {
           // User belongs to the group, proceed with the action
           console.log("I am here")
           this.actionService.doAction({
              type: 'ir.actions.act_window',
              name: 'Resource Reservations - Pivot View',
              res_model: 'resource.reservation',
              view_mode: 'pivot',
              view_type: 'pivot',
              views: [[false, 'pivot']],
              target: 'current',
              res_id: false,
          });
       } else {
           // User does not belong to the group, raise an access error
           throw new AccessError(_t("Access Denied. You do not have the required group."));
       }
   }
}
registry.category("views").add("button_in_tree", {
   ...listView,
   Controller: ResourceListController,
   buttonTemplate: "resource_reservation.ListView.Buttons",
});