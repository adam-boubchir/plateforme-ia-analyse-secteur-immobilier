type Props = {
  title: string;
};

const ConversationItem = ({ title }: Props) => {
  return (
    <button
      className="
        w-full
        text-left
        p-3
        rounded-lg
        hover:bg-[#2f2f2f]
        transition
        truncate
      "
    >
      {title}
    </button>
  );
};

export default ConversationItem;