import {
  Settings,
} from "lucide-react";

const SidebarFooter = () => {

  return (

    <div className="border-t border-white/10 p-4">

      <button

        className="
          w-full
          rounded-xl
          px-4
          py-3
          flex
          items-center
          gap-3
          text-gray-300
          hover:bg-[#252525]
          transition-all
        "

      >

        <Settings size={18} />

        Paramètres

      </button>

    </div>

  );

};

export default SidebarFooter;