type Props = {
  content: string;
};

const MessageContent = ({ content }: Props) => {

  return (

    <div
      className="
        max-w-4xl
        text-[16px]
        leading-8
        text-gray-100
        whitespace-pre-wrap
        break-words
        tracking-[0.01em]
        selection:bg-blue-600
        selection:text-white
      "
    >

      {content}

    </div>

  );

};

export default MessageContent;