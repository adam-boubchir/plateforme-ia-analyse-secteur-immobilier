const SidebarHeader = () => {
  return (
    <div className="p-4 border-b border-gray-800">

      <button
        className="
          w-full
          rounded-lg
          bg-[#2f2f2f]
          hover:bg-[#3b3b3b]
          py-3
          transition
        "
      >
        + Nouveau chat
      </button>

    </div>
  );
};

export default SidebarHeader;