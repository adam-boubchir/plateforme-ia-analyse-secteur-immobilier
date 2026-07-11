import { useEffect, useState } from "react";

import ConversationItem from "./ConversationItem";
import SearchConversation from "./SearchConversation";

import { useConversationStore } from "../../store/conversationStore";

const ConversationList = () => {

  const conversations = useConversationStore(
    state => state.conversations
  );

  const loadConversations = useConversationStore(
    state => state.loadConversations
  );

  const [search, setSearch] = useState("");

  useEffect(() => {

    loadConversations();

  }, []);

  const filteredConversations = conversations.filter(

    conversation =>

      (conversation.title ?? "")

        .toLowerCase()

        .includes(

          search.toLowerCase()

        )

  );

  return (

    <>

      <SearchConversation

        value={search}

        onChange={setSearch}

      />

      <div className="p-2">

        {

          filteredConversations.map(

            conversation => (

              <ConversationItem

                key={conversation.conversation_uuid}

                conversation={conversation}

              />

            )

          )

        }

      </div>

    </>

  );

};

export default ConversationList;