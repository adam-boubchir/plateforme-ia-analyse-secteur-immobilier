import ReactMarkdown from "react-markdown";
import remarkGfm from "remark-gfm";
import rehypeHighlight from "rehype-highlight";

type Props = {
    content: string;
};

const MessageContent = ({ content }: Props) => {
    return (
        <div
            className="
                max-w-none
                prose
                prose-invert
                prose-headings:text-white
                prose-p:text-slate-200
                prose-strong:text-white
                prose-em:text-slate-300
                prose-code:text-cyan-300
                prose-pre:bg-slate-950
                prose-pre:border
                prose-pre:border-slate-700
                prose-pre:rounded-xl
                prose-th:text-white
                prose-th:border
                prose-th:border-slate-700
                prose-td:border
                prose-td:border-slate-700
                prose-td:text-slate-300
                prose-li:text-slate-200
                prose-blockquote:border-l-blue-500
                prose-blockquote:text-slate-400
                prose-a:text-blue-400
                prose-a:no-underline
                prose-a:hover:text-blue-300
                leading-8
                break-words
                selection:bg-blue-600
                selection:text-white
            "
        >
            <ReactMarkdown
                remarkPlugins={[remarkGfm]}
                rehypePlugins={[rehypeHighlight]}
            >
                {content}
            </ReactMarkdown>
        </div>
    );
};

export default MessageContent;