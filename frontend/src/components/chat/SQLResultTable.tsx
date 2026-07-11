import { useMemo, useState } from "react";
import { ArrowUpDown } from "lucide-react";

type Props = {
  rows: Record<string, unknown>[];
};

const SQLResultTable = ({ rows }: Props) => {

  const [search, setSearch] = useState("");

  const [sortColumn, setSortColumn] = useState<string | null>(null);

  const [sortDirection, setSortDirection] = useState<"asc" | "desc">("asc");

  const PAGE_SIZE = 20;

  const [currentPage, setCurrentPage] = useState(1);

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

    return [...filteredRows].sort((a, b) => {

      const valueA = String(a[sortColumn] ?? "");

      const valueB = String(b[sortColumn] ?? "");

      const result = valueA.localeCompare(
        valueB,
        undefined,
        {
          numeric: true,
          sensitivity: "base",
        }
      );

      return sortDirection === "asc"
        ? result
        : -result;

    });

  }, [filteredRows, sortColumn, sortDirection]);

  const totalPages = Math.ceil(
  sortedRows.length / PAGE_SIZE
);

const paginatedRows = sortedRows.slice(

  (currentPage - 1) * PAGE_SIZE,

  currentPage * PAGE_SIZE

);

  const exportCSV = () => {

    const header = columns.join(",");

    const data = sortedRows.map(row =>

      columns
        .map(column => `"${String(row[column] ?? "")}"`)
        .join(",")

    );

    const csv = [header, ...data].join("\n");

    const blob = new Blob(
      [csv],
      {
        type: "text/csv;charset=utf-8;",
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

    <div className="mt-5">

      <div
        className="
          mb-4
          flex
          flex-wrap
          items-center
          justify-between
          gap-3
        "
      >

        <input

          type="text"

          placeholder="🔍 Rechercher..."

          value={search}

          onChange={(e) =>

            setSearch(e.target.value)

          }

          className="
            rounded-lg
            bg-[#202020]
            px-4
            py-2
            text-sm
            outline-none
            border
            border-gray-700
            w-72
          "

        />

        <div className="flex items-center gap-3">

          <span className="text-sm text-gray-400">

            {sortedRows.length} résultat(s)

          </span>

          <button

            onClick={exportCSV}

            className="
              rounded-lg
              bg-blue-600
              hover:bg-blue-700
              px-4
              py-2
              text-sm
              transition
            "

          >

            📥 CSV

          </button>

        </div>

      </div>

      <div
        className="
          overflow-x-auto
          rounded-xl
          border
          border-gray-700
        "
      >

        <table className="min-w-full text-sm">

          <thead className="bg-[#202020]">

            <tr>

              {

                columns.map(column => (

                  <th

                    key={column}

                    className="
                      px-4
                      py-3
                      text-left
                      font-semibold
                      border-b
                      border-gray-700
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
                        transition
                      "

                    >

                      {column}

                      <ArrowUpDown size={14} />

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

                  className="
                    border-b
                    border-gray-800
                    hover:bg-[#2a2a2a]
                  "

                >

                  {

                    columns.map(column => (

                      <td

                        key={column}

                        className="
                          px-4
                          py-3
                          whitespace-nowrap
                        "

                      >

                        {

                          row[column] === null

                            ? "-"

                            : String(row[column])

                        }

                      </td>

                    ))

                  }

                </tr>

              ))

            }

          </tbody>

        </table>
        <div
  className="
    flex
    items-center
    justify-between
    p-4
    border-t
    border-gray-700
  "
>

  <button

    disabled={currentPage === 1}

    onClick={() =>

      setCurrentPage(page => page - 1)

    }

    className="
      px-4
      py-2
      rounded-lg
      bg-[#202020]
      disabled:opacity-40
    "

  >

    ← Précédent

  </button>

  <span className="text-sm text-gray-400">

    Page {currentPage} / {totalPages || 1}

  </span>

  <button

    disabled={currentPage >= totalPages}

    onClick={() =>

      setCurrentPage(page => page + 1)

    }

    className="
      px-4
      py-2
      rounded-lg
      bg-[#202020]
      disabled:opacity-40
    "

  >

    Suivant →

  </button>

</div>

      </div>

    </div>

  );

};

export default SQLResultTable;