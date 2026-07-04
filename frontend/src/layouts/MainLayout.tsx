import Sidebar from "../components/sidebar/Sidebar";
import ChatPage from "../pages/ChatPage";

const MainLayout = () => {
  return (
    <div className="flex h-screen bg-[#212121] text-white">
      <Sidebar />
      <ChatPage />
    </div>
  );
};

export default MainLayout;