import SidebarHeader from "./SidebarHeader";
import SidebarNavigation from "./SidebarNavigation";
import ConversationList from "./ConversationList";
import SidebarFooter from "./SidebarFooter";

const Sidebar = () => {

    return (

        <aside
            className="
                w-80
                h-screen
                bg-[#171717]
                border-r
                border-white/10
                flex
                flex-col
                shadow-2xl
            "
        >

            {/* Header */}

            <SidebarHeader />

            {/* Navigation */}

            <SidebarNavigation />

            {/* Conversations */}

            <div
                className="
                    flex-1
                    overflow-y-auto
                "
            >

                <ConversationList />

            </div>

            {/* Footer */}

            <SidebarFooter />

        </aside>

    );

};

export default Sidebar;