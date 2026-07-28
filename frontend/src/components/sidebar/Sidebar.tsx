import SidebarHeader from "./SidebarHeader";
import SidebarNavigation from "./SidebarNavigation";
import ConversationList from "./ConversationList";
import SidebarFooter from "./SidebarFooter";

const Sidebar = () => {

    return (

        <aside
            className="
                w-80
                min-h-screen
                bg-[#171717]
                border-r
                border-white/10
                flex
                flex-col
                shadow-2xl
            "
        >

            <SidebarHeader />

            <SidebarNavigation />

            <div
                className="
                    flex-1
                    overflow-y-auto
                "
            >

                <ConversationList />

            </div>

            <SidebarFooter />

        </aside>

    );

};

export default Sidebar;