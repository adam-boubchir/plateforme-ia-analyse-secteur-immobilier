interface Props {
    page: number;
    pageSize: number;
    total: number;
    onPageChange: (page: number) => void;
}

export default function Pagination({
    page,
    pageSize,
    total,
    onPageChange,
}: Props) {

    const totalPages = Math.ceil(total / pageSize);

    if (totalPages <= 1) {
        return null;
    }

    return (

        <div className="mt-6 flex items-center justify-between">

            <button
                className="rounded-lg bg-slate-200 px-4 py-2 disabled:cursor-not-allowed disabled:opacity-50"
                disabled={page === 1}
                onClick={() => onPageChange(page - 1)}
            >
                ← Précédent
            </button>

            <span className="font-medium">

                Page {page} / {totalPages}

            </span>

            <button
                className="rounded-lg bg-blue-600 px-4 py-2 text-white disabled:cursor-not-allowed disabled:bg-slate-300"
                disabled={page >= totalPages}
                onClick={() => onPageChange(page + 1)}
            >
                Suivant →
            </button>

        </div>

    );

}