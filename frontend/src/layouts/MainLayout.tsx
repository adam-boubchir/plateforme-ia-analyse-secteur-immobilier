import { Outlet } from "react-router-dom";
import Sidebar from "../components/sidebar/Sidebar";

const MainLayout = () => {
    return (
        <div
            className="
                flex
                min-h-screen
                bg-[#0f0f0f]
                text-white
            "
        >
            <Sidebar />

            <main
                className="
                    flex-1
                    flex
                    flex-col
                    overflow-y-auto
                "
            >
                <Outlet />
            </main>
        </div>
    );
};

export default MainLayout;