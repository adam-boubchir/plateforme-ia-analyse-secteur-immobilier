import SidebarHeader from "./SidebarHeader";
import ConversationList from "./ConversationList";
import SidebarFooter from "./SidebarFooter";

const Sidebar = () => {
  return (
    <aside className="w-72 h-screen bg-[#171717] border-r border-gray-800 flex flex-col">

      <SidebarHeader />

      <div className="flex-1 overflow-y-auto">
        <ConversationList />
      </div>

      <SidebarFooter />

    </aside>
  );
};

export default Sidebar;