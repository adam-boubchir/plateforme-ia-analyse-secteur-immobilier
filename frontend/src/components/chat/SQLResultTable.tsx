import { useMemo, useState } from "react";

import {
  ArrowUpDown,
  Download,
  Search,
  ChevronLeft,
  ChevronRight,
  Database,
} from "lucide-react";

type Props = {
  rows: Record<string, unknown>[];
};

const PAGE_SIZE = 20;

const SQLResultTable = ({ rows }: Props) => {

  const [search, setSearch] = useState("");

  const [sortColumn, setSortColumn] =
    useState<string | null>(null);

  const [sortDirection, setSortDirection] =
    useState<"asc" | "desc">("asc");

  const [currentPage, setCurrentPage] =
    useState(1);

  if (rows.length === 0) {

    return null;

  }

  const columns = Object.keys(rows[0]);

  const filteredRows = useMemo(() => {

    if (!search.trim()) {

      return rows;

    }

    const value = search.toLowerCase();

    return rows.filter(row =>

      Object.values(row).some(cell =>

        String(cell ?? "")

          .toLowerCase()

          .includes(value)

      )

    );

  }, [rows, search]);

  const sortedRows = useMemo(() => {

    if (!sortColumn) {

      return filteredRows;

    }

    return [...filteredRows].sort(

      (a, b) => {

        const valueA =
          String(a[sortColumn] ?? "");

        const valueB =
          String(b[sortColumn] ?? "");

        const compare =
          valueA.localeCompare(

            valueB,

            undefined,

            {

              numeric: true,

              sensitivity: "base",

            }

          );

        return sortDirection === "asc"

          ? compare

          : -compare;

      }

    );

  }, [

    filteredRows,

    sortColumn,

    sortDirection,

  ]);

  const totalPages = Math.ceil(

    sortedRows.length /

    PAGE_SIZE

  );

  const paginatedRows = sortedRows.slice(

    (currentPage - 1) * PAGE_SIZE,

    currentPage * PAGE_SIZE

  );

  const exportCSV = () => {

    const header = columns.join(",");

    const data = sortedRows.map(

      row =>

        columns

          .map(

            column =>

              `"${String(

                row[column] ?? ""

              )}"`

          )

          .join(",")

    );

    const csv = [

      header,

      ...data,

    ].join("\n");

    const blob = new Blob(

      [csv],

      {

        type:

          "text/csv;charset=utf-8;",

      }

    );

    const url = URL.createObjectURL(blob);

    const link = document.createElement("a");

    link.href = url;

    link.download = "resultats.csv";

    link.click();

    URL.revokeObjectURL(url);

  };

  return (

    <div
      className="
        mt-10
        rounded-[28px]
        border
        border-white/10
        bg-[#181818]
        shadow-2xl
        overflow-hidden
      "
    >

      {/* HEADER */}

      <div
        className="
          flex
          items-center
          justify-between
          px-8
          py-6
          border-b
          border-white/10
        "
      >

        <div>

          <div
            className="
              flex
              items-center
              gap-3
            "
          >

            <div
              className="
                h-12
                w-12
                rounded-2xl
                bg-blue-500/10
                flex
                items-center
                justify-center
              "
            >

              <Database
                className="
                  text-blue-400
                "
              />

            </div>

            <div>

              <h2
                className="
                  text-xl
                  font-bold
                "
              >

                Résultats SQL

              </h2>

              <p
                className="
                  text-sm
                  text-gray-400
                "
              >

                {sortedRows.length.toLocaleString()}
                {" "}
                lignes

              </p>

            </div>

          </div>

        </div>

        <button

          onClick={exportCSV}

          className="
            flex
            items-center
            gap-2
            rounded-xl
            bg-blue-600
            hover:bg-blue-500
            px-5
            py-3
            transition
          "

        >

          <Download size={18}/>

          Export CSV

        </button>

      </div>
            {/* TOOLBAR */}

      <div
        className="
          flex
          flex-wrap
          items-center
          justify-between
          gap-5
          px-8
          py-6
          border-b
          border-white/10
          bg-[#151515]
        "
      >

        <div
          className="
            relative
            w-full
            max-w-md
          "
        >

          <Search
            size={18}
            className="
              absolute
              left-4
              top-1/2
              -translate-y-1/2
              text-gray-500
            "
          />

          <input

            type="text"

            value={search}

            onChange={(e) => {

              setSearch(e.target.value);

              setCurrentPage(1);

            }}

            placeholder="Rechercher dans les résultats..."

            className="
              w-full
              rounded-2xl
              border
              border-white/10
              bg-[#202020]
              py-3
              pl-12
              pr-4
              text-sm
              outline-none
              transition-all
              focus:border-blue-500
              focus:ring-2
              focus:ring-blue-500/20
            "

          />

        </div>

        <div
          className="
            flex
            items-center
            gap-3
          "
        >

          <span
            className="
              rounded-full
              bg-blue-500/10
              px-4
              py-2
              text-sm
              text-blue-300
            "
          >

            {sortedRows.length.toLocaleString()} résultat(s)

          </span>

          <span
            className="
              rounded-full
              bg-white/5
              px-4
              py-2
              text-sm
              text-gray-400
            "
          >

            {columns.length} colonne(s)

          </span>

        </div>

      </div>

      {/* TABLE */}

      <div
        className="
          max-h-[55vh]
          overflow-auto
        "
      >

        <table
          className="
            w-full
            border-collapse
          "
        >

          <thead
            className="
              sticky
              top-0
              z-20
              bg-[#1b1b1b]
              backdrop-blur-lg
            "
          >

            <tr>

              {

                columns.map(column => (

                  <th

                    key={column}

                    className="
                      px-6
                      py-4
                      text-left
                      text-xs
                      uppercase
                      tracking-wider
                      font-semibold
                      border-b
                      border-white/10
                      whitespace-nowrap
                    "

                  >

                    <button

                      onClick={() => {

                        if (sortColumn === column) {

                          setSortDirection(

                            sortDirection === "asc"

                              ? "desc"

                              : "asc"

                          );

                        }

                        else {

                          setSortColumn(column);

                          setSortDirection("asc");

                        }

                      }}

                      className="
                        flex
                        items-center
                        gap-2
                        hover:text-blue-400
                        transition-colors
                      "

                    >

                      {column}

                      <ArrowUpDown size={15}/>

                    </button>

                  </th>

                ))

              }

            </tr>

          </thead>

          <tbody>
                        {

              paginatedRows.map((row, index) => (

                <tr

                  key={index}

                  className={`
                    transition-all
                    duration-200
                    border-b
                    border-white/5
                    ${
                      index % 2 === 0
                        ? "bg-transparent"
                        : "bg-white/[0.015]"
                    }
                    hover:bg-blue-500/5
                    cursor-pointer
                  `}

                >

                  {

                    columns.map(column => {

                      const value = row[column];

                      const isNumber =
                        typeof value === "number";

                      return (

                        <td

                          key={column}

                          className={`
                            px-6
                            py-4
                            whitespace-nowrap
                            text-sm
                            ${
                              isNumber
                                ? "text-right font-medium"
                                : "text-left"
                            }
                          `}

                        >

                          {

                            value === null ||

                            value === undefined ? (

                              <span
                                className="
                                  text-gray-600
                                "
                              >

                                —

                              </span>

                            )

                            : isNumber ? (

                              <span
                                className="
                                  font-semibold
                                  text-cyan-300
                                "
                              >

                                {

                                  Number(value)

                                    .toLocaleString(

                                      "fr-FR"

                                    )

                                }

                              </span>

                            )

                            : String(value).length > 45 ? (

                              <span
                                title={String(value)}
                                className="
                                  block
                                  max-w-xs
                                  truncate
                                "
                              >

                                {String(value)}

                              </span>

                            )

                            : (

                              <span>

                                {String(value)}

                              </span>

                            )

                          }

                        </td>

                      );

                    })

                  }

                </tr>

              ))

            }

          </tbody>
                  </table>

      </div>

      {/* PAGINATION */}

      <div
        className="
          flex
          flex-wrap
          items-center
          justify-between
          gap-5
          border-t
          border-white/10
          bg-[#151515]
          px-8
          py-5
        "
      >

        <div
          className="
            text-sm
            text-gray-400
          "
        >

          Affichage de{" "}

          <span className="font-semibold text-white">

            {Math.min(
              (currentPage - 1) * PAGE_SIZE + 1,
              sortedRows.length
            )}

          </span>

          {" "}à{" "}

          <span className="font-semibold text-white">

            {Math.min(
              currentPage * PAGE_SIZE,
              sortedRows.length
            )}

          </span>

          {" "}sur{" "}

          <span className="font-semibold text-blue-400">

            {sortedRows.length.toLocaleString()}

          </span>

          {" "}résultat(s)

        </div>

        <div
          className="
            flex
            items-center
            gap-3
          "
        >

          <button

            disabled={currentPage === 1}

            onClick={() =>

              setCurrentPage(page => page - 1)

            }

            className="
              flex
              items-center
              gap-2
              rounded-xl
              border
              border-white/10
              bg-[#202020]
              px-4
              py-2.5
              transition-all
              hover:bg-[#2b2b2b]
              disabled:cursor-not-allowed
              disabled:opacity-40
            "

          >

            <ChevronLeft size={18} />

            Précédent

          </button>

          <div
            className="
              rounded-xl
              border
              border-blue-500/20
              bg-blue-500/10
              px-5
              py-2.5
              text-sm
              font-semibold
              text-blue-300
            "
          >

            {currentPage}

            {" / "}

            {Math.max(totalPages, 1)}

          </div>

          <button

            disabled={
              currentPage >= totalPages
            }

            onClick={() =>

              setCurrentPage(page => page + 1)

            }

            className="
              flex
              items-center
              gap-2
              rounded-xl
              border
              border-white/10
              bg-[#202020]
              px-4
              py-2.5
              transition-all
              hover:bg-[#2b2b2b]
              disabled:cursor-not-allowed
              disabled:opacity-40
            "

          >

            Suivant

            <ChevronRight size={18} />

          </button>

        </div>

      </div>

    </div>

  );

};

export default SQLResultTable;