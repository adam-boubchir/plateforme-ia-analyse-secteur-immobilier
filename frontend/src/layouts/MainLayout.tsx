import Sidebar from "../components/sidebar/Sidebar";
import ChatPage from "../pages/ChatPage";

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

        <ChatPage />

      </div>

    </div>

  );

};

export default MainLayout;