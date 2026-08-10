import { Outlet } from "react-router-dom";
import Sidebar from "../components/sidebar/Sidebar";

const MainLayout = () => {
  return (
    <div
      className="
        h-screen
        w-screen
        overflow-hidden

        flex

        bg-[#0b1120]
        text-white
      "
    >
      <Sidebar />

      <main
        className="
          relative

          flex-1

          overflow-hidden

          flex
          flex-col
        "
      >
        {/* Background */}

        <div
          className="
            absolute
            inset-0

            pointer-events-none

            bg-[radial-gradient(circle_at_top_right,#2563eb22,transparent_35%),radial-gradient(circle_at_bottom_left,#06b6d422,transparent_35%)]

            opacity-30
          "
        />

        {/* Content */}

        <div
          className="
            relative

            flex-1

            overflow-hidden

            flex
            flex-col
          "
        >
          <Outlet />
        </div>
      </main>
    </div>
  );
};

export default MainLayout;