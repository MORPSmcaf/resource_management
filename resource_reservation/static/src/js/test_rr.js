/** @odoo-module */
import { ListController } from "@web/views/list/list_controller";
import { registry } from '@web/core/registry';
import { listView } from '@web/views/list/list_view';
//export class ResourceListController extends ListController {
//   setup() {
//       super.setup();
//   }
//   OnTestClick() {
//       this.actionService.doAction({
//          type: 'ir.actions.act_window',
//          name: 'Resource Reservations - Pivot View',
//          res_model: 'resource.reservation',
//          view_mode: 'pivot',
//          view_type: 'pivot',
//          views: [[false, 'pivot']],
//          target: 'current',
//          res_id: false,
//      });
//   }
//}
//registry.category("views").add("button_in_tree", {
//   ...listView,
//   Controller: ResourceListController,
//   buttonTemplate: "resource_reservation.ListView.Buttons",
//});

export class Resourcetest extends ListController {
   setup() {
       super.setup();
   }
   OnTestClick() {
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
   }
}