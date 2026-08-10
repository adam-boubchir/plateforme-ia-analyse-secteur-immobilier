import SidebarHeader from "./SidebarHeader";
import SidebarNavigation from "./SidebarNavigation";
import ConversationList from "./ConversationList";
import SidebarFooter from "./SidebarFooter";

const Sidebar = () => {
  return (
    <aside
      className="
        relative

        h-screen
        w-80
        shrink-0

        flex
        flex-col

        overflow-hidden

        border-r
        border-slate-700/40

        bg-gradient-to-b
        from-[#141414]
        via-[#181818]
        to-[#111111]

        shadow-[0_0_40px_rgba(0,0,0,0.45)]
      "
    >
      {/* Halo supérieur */}

      <div
        className="
          absolute
          -top-32
          -left-24

          h-72
          w-72

          rounded-full

          bg-blue-600/10

          blur-3xl

          pointer-events-none
        "
      />

      {/* Halo inférieur */}

      <div
        className="
          absolute
          bottom-0
          right-0

          h-60
          w-60

          rounded-full

          bg-cyan-500/5

          blur-3xl

          pointer-events-none
        "
      />

      <div
        className="
          relative
          z-10

          flex
          flex-col

          h-full
          overflow-hidden
        "
      >
        {/* Header */}

        <SidebarHeader />

        {/* Navigation */}

        <SidebarNavigation />

        {/* Scroll indépendant */}

        <div
          className="
            flex-1

            overflow-y-auto
            overflow-x-hidden

            px-2
            py-2
          "
        >
          <ConversationList />
        </div>

        {/* Footer fixe */}

        <SidebarFooter />
      </div>
    </aside>
  );
};

export default Sidebar;