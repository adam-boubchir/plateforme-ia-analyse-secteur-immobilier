import { NavLink } from "react-router-dom";

const SidebarNavigation = () => {

    const linkClass = ({ isActive }: { isActive: boolean }) =>
        `
        flex
        items-center
        gap-3
        px-4
        py-3
        rounded-lg
        transition-all
        duration-200
        ${
            isActive
                ? "bg-blue-600 text-white"
                : "text-gray-300 hover:bg-white/10"
        }
    `;

    return (

        <div className="px-3 py-2 border-b border-white/10 space-y-2">

            <NavLink
                to="/chat"
                className={linkClass}
            >
                💬
                <span>Chat</span>
            </NavLink>

            <NavLink
                to="/map"
                className={linkClass}
            >
                🗺️
                <span>Carte du Maroc</span>
            </NavLink>

        </div>

    );

};

export default SidebarNavigation;