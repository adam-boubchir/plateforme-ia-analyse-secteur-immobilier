import ConversationItem from "./ConversationItem";

const ConversationList = () => {
  return (
    <div className="p-2">

      <ConversationItem title="Prix appartement Rabat" />

      <ConversationItem title="Evolution du ciment" />

      <ConversationItem title="Prix terrain Casablanca" />

      <ConversationItem title="Indice immobilier 2025" />

    </div>
  );
};

export default ConversationList;