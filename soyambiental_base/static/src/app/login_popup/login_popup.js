/** @odoo-module */
import { patch } from "@web/core/utils/patch";
import { LoginPopup} from "@menus_hola_calidad/app/components/login_popup/login_popup";
import { onMounted , onWillStart} from "@odoo/owl";
import { user } from "@web/core/user";


patch(LoginPopup.prototype, {
    setup() {
        const res = super.setup(...arguments)  

        onWillStart(async () => {
            this.showEnvironment = await user.hasGroup(
                "soyambiental_base.group_sga_onlyread"
            );
        })


        return res
    },
    async openEnvironmental() {
        const menu = this.menuService.getAll().find(menu => menu.xmlid=="soyambiental_base.sga_menu_root");
        console.log("menus", menu);
        if (menu) {
            await this.menuService.selectMenu(menu);
        }
    }



})
