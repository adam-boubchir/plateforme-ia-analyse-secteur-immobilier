import { Outlet } from "react-router-dom";

import Sidebar from "../components/sidebar/Sidebar";

const MainLayout = () => {

    return (

        <div
            className="
                flex
                h-screen
                overflow-hidden
                bg-[#0f0f0f]
                text-white
            "
        >

            <Sidebar />

            <div
                className="
                    flex-1
                    overflow-hidden
                    flex
                    flex-col
                "
            >

                <Outlet />

            </div>

        </div>

    );

};

export default MainLayout;