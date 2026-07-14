import { Search } from "lucide-react";

type Props = {

  value: string;

  onChange: (value: string) => void;

};

const SearchConversation = ({

  value,

  onChange,

}: Props) => {

  return (

    <div className="px-4 py-4">

      <div className="relative">

        <Search

          size={18}

          className="
            absolute
            left-4
            top-1/2
            -translate-y-1/2
            text-gray-500
            pointer-events-none
          "

        />

        <input

          value={value}

          onChange={(e) => onChange(e.target.value)}

          placeholder="Rechercher une conversation..."

          className="
            w-full
            rounded-xl
            bg-[#232323]
            border
            border-white/5
            py-3
            pl-11
            pr-4
            text-sm
            text-white
            placeholder:text-gray-500
            outline-none
            transition-all
            duration-200
            focus:bg-[#2b2b2b]
            focus:border-blue-500
            focus:ring-2
            focus:ring-blue-500/20
          "

        />

      </div>

    </div>

  );

};

export default SearchConversation;