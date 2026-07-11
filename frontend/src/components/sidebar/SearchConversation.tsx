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

    <div className="p-3 border-b border-gray-800">

      <div className="relative">

        <Search

          size={16}

          className="absolute left-3 top-1/2 -translate-y-1/2 text-gray-400"

        />

        <input

          value={value}

          onChange={(e) => onChange(e.target.value)}

          placeholder="Rechercher..."

          className="
            w-full
            rounded-lg
            bg-[#2b2b2b]
            py-2
            pl-10
            pr-3
            outline-none
          "

        />

      </div>

    </div>

  );

};

export default SearchConversation;