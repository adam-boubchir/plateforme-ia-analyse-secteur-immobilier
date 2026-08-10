import MessageHeader from "./MessageHeader";
import MessageContent from "./MessageContent";
import SQLViewer from "./SQLViewer";
import KPICards from "./KPICards";
import ChartViewer from "./ChartViewer";
import SQLResultTable from "./SQLResultTable";

import { API_BASE_URL } from "../../api/axios";

type Props = {
    role: "user" | "assistant";
    content: string;
    sql?: string | null;
    rows?: unknown[];
    pdf_path?: string | null;
};

const MessageBubble = ({
    role,
    content,
    sql,
    rows,
    pdf_path,
}: Props) => {

    const isUser = role === "user";

    // ======================================================
    // PDF URL
    // ======================================================

    const pdfUrl = (() => {

            if (!pdf_path) {
                return null;
            }

            if (pdf_path.startsWith("http")) {
                return pdf_path;
            }

            const normalizedPath = pdf_path
                .replace(/\\/g, "/")
                .replace(/^\/+/, "");

            return `${API_BASE_URL}/${normalizedPath}`;

        })();

    console.log("========== PDF DEBUG ==========");
    console.log("pdf_path =", pdf_path);
    console.log("API_BASE_URL =", API_BASE_URL);
    console.log("pdfUrl =", pdfUrl);
    console.log("================================");

    const handleDownload = async () => {

        if (!pdfUrl) {
            return;
        }

        try {

            console.log("Downloading PDF:", pdfUrl);

            const response = await fetch(pdfUrl);

            if (!response.ok) {

                throw new Error(
                    `Erreur HTTP ${response.status}`
                );

            }

            const blob = await response.blob();

            const blobUrl = window.URL.createObjectURL(
                blob
            );

            const link = document.createElement("a");

            link.href = blobUrl;

            const filename =
                pdf_path
                    ?.replace(/\\/g, "/")
                    .split("/")
                    .pop()
                || "rapport.pdf";

            link.download = filename;

            document.body.appendChild(link);

            link.click();

            document.body.removeChild(link);

            window.URL.revokeObjectURL(
                blobUrl
            );

        } catch (error) {

            console.error(
                "Erreur téléchargement PDF:",
                error
            );

            alert(
                "Impossible de télécharger le rapport PDF."
            );

        }

    };

    // ======================================================
    // USER MESSAGE
    // ======================================================

    if (isUser) {

        return (
            <div className="flex justify-end">

                <div
                    className="
                        max-w-3xl

                        rounded-[28px]

                        bg-gradient-to-br
                        from-blue-600
                        via-blue-500
                        to-cyan-500

                        px-7
                        py-6

                        shadow-xl
                        shadow-blue-500/20
                    "
                >

                    <MessageHeader
                        role={role}
                    />

                    <div className="mt-5">

                        <MessageContent
                            content={content}
                        />

                    </div>

                </div>

            </div>
        );
    }

    // ======================================================
    // ASSISTANT MESSAGE
    // ======================================================

    return (

        <div
            className="
                group
                relative
                overflow-hidden

                rounded-[30px]

                border
                border-white/10

                bg-[#181818]

                shadow-2xl
            "
        >

            {/* ==================================================
                DECORATIVE HALOS
            ================================================== */}

            <div
                className="
                    pointer-events-none

                    absolute
                    -right-32
                    -top-32

                    h-72
                    w-72

                    rounded-full

                    bg-blue-500/5

                    blur-3xl
                "
            />

            <div
                className="
                    pointer-events-none

                    absolute
                    -left-32
                    bottom-0

                    h-56
                    w-56

                    rounded-full

                    bg-cyan-500/5

                    blur-3xl
                "
            />

            {/* ==================================================
                HEADER
            ================================================== */}

            <div
                className="
                    relative

                    border-b
                    border-white/10

                    px-8
                    lg:px-10

                    py-6
                "
            >

                <MessageHeader
                    role={role}
                />

            </div>

            {/* ==================================================
                MESSAGE CONTENT
            ================================================== */}

            <div
                className="
                    relative

                    px-8
                    lg:px-10

                    py-8
                "
            >

                <MessageContent
                    content={content}
                />

            </div>

            {/* ==================================================
                SQL VIEWER
            ================================================== */}

            {sql && (

                <div
                    className="
                        border-t
                        border-white/10

                        px-8
                        lg:px-10

                        pb-8
                    "
                >

                    <SQLViewer
                        sql={sql}
                    />

                </div>

            )}

            {/* ==================================================
                DATA RESULTS
            ================================================== */}

            {rows && rows.length > 0 && (

                <>

                    {/* ==================================================
                        KPI CARDS
                    ================================================== */}

                    <div
                        className="
                            border-t
                            border-white/10

                            px-8
                            lg:px-10

                            py-8
                        "
                    >

                        <KPICards
                            rows={
                                rows as Record<
                                    string,
                                    unknown
                                >[]
                            }
                        />

                    </div>

                    {/* ==================================================
                        CHARTS
                    ================================================== */}

                    <div
                        className="
                            border-t
                            border-white/10

                            px-8
                            lg:px-10

                            py-8
                        "
                    >

                        <ChartViewer
                            rows={
                                rows as Record<
                                    string,
                                    unknown
                                >[]
                            }
                        />

                    </div>

                    {/* ==================================================
                        SQL RESULT TABLE
                    ================================================== */}

                    <div
                        className="
                            border-t
                            border-white/10

                            px-8
                            lg:px-10

                            py-8
                        "
                    >

                        <div
                            className="
                                mb-5

                                flex
                                items-center
                                justify-between

                                text-sm
                                text-slate-400
                            "
                        >

                            <span>
                                {rows.length.toLocaleString()}
                                {" "}
                                lignes retournées
                            </span>

                            <span>
                                SQL Server
                            </span>

                        </div>

                        <SQLResultTable
                            rows={
                                rows as Record<
                                    string,
                                    unknown
                                >[]
                            }
                        />

                    </div>

                </>

            )}

            {/* ==================================================
                PDF REPORT
            ================================================== */}

            {pdfUrl && (

                <div
                    className="
                        relative

                        border-t
                        border-white/10

                        px-8
                        lg:px-10

                        py-8
                    "
                >

                    <div
                        className="
                            rounded-2xl

                            border
                            border-blue-500/20

                            bg-blue-500/5

                            p-6
                        "
                    >

                        <div
                            className="
                                flex
                                flex-col
                                items-start

                                justify-between

                                gap-5

                                sm:flex-row
                                sm:items-center
                            "
                        >

                            {/* ==================================================
                                PDF INFORMATION
                            ================================================== */}

                            <div>

                                <h3
                                    className="
                                        text-lg
                                        font-semibold
                                        text-white
                                    "
                                >
                                    📄 Rapport PDF généré
                                </h3>

                                <p
                                    className="
                                        mt-2

                                        text-sm
                                        leading-6

                                        text-slate-400
                                    "
                                >
                                    Le rapport professionnel contenant
                                    l'analyse complète, les tableaux et
                                    les visualisations est disponible.
                                </p>

                            </div>

                            {/* ==================================================
                                DOWNLOAD BUTTON
                            ================================================== */}

                            <button
                                type="button"
                                onClick={handleDownload}
                                className="
                                    shrink-0

                                    rounded-xl

                                    bg-blue-600

                                    px-5
                                    py-3

                                    font-medium
                                    text-white

                                    transition-all
                                    duration-300

                                    hover:bg-blue-700

                                    hover:shadow-lg
                                    hover:shadow-blue-500/20

                                    active:scale-95
                                "
                            >
                                📥 Télécharger
                            </button>

                        </div>

                    </div>

                </div>

            )}

        </div>
    );
};

export default MessageBubble;