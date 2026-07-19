import { useEffect } from "react";

import {
    useNavigate,
    useParams,
} from "react-router-dom";

import { useLogStore } from "../../store/logStore";

const LogDetailsPage = () => {

    const navigate = useNavigate();

    const { id } = useParams();

    const {

        selectedLog,

        loading,

        error,

        loadLog,

    } = useLogStore();

    useEffect(() => {

        if (!id) {

            return;

        }

        loadLog(

            Number(id)

        );

    }, [

        id,

        loadLog,

    ]);

    if (loading) {

        return (

            <div className="flex h-full items-center justify-center">

                Chargement...

            </div>

        );

    }

    if (error) {

        return (

            <div className="flex h-full items-center justify-center text-red-500">

                {error}

            </div>

        );

    }

    if (!selectedLog) {

        return (

            <div className="flex h-full items-center justify-center">

                Aucun log.

            </div>

        );

    }

    return (

        <div className="h-full overflow-auto p-8">

            <button

                onClick={() => navigate(-1)}

                className="
                    mb-6
                    rounded-lg
                    bg-gray-700
                    px-4
                    py-2
                    hover:bg-gray-600
                "

            >

                ← Retour

            </button>

            <h1 className="mb-8 text-3xl font-bold">

                AI Execution #{selectedLog.id}

            </h1>

            <div className="space-y-6">

                <Section
                    title="Question"
                    content={selectedLog.question}
                />

                <Section
                    title="Selected Tables"
                    content={selectedLog.selected_tables}
                />

                <Section
                    title="Business Knowledge"
                    content={selectedLog.business_knowledge}
                    code
                />

                <Section
                    title="Join Knowledge"
                    content={selectedLog.join_knowledge}
                    code
                />

                <Section
                    title="Forbidden Joins"
                    content={selectedLog.forbidden_joins}
                    code
                />

                <Section
                    title="Semantic Context"
                    content={selectedLog.semantic_context}
                    code
                />

                <Section
                    title="SQL Patterns"
                    content={selectedLog.sql_patterns}
                    code
                />

                <Section
                    title="Full Context"
                    content={selectedLog.full_context}
                    code
                />

                <Section
                    title="Prompt"
                    content={selectedLog.prompt}
                    code
                />

                <Section
                    title="Generated SQL"
                    content={selectedLog.generated_sql}
                    code
                />

                <Section
                    title="Validated SQL"
                    content={selectedLog.validated_sql}
                    code
                />

                <Section
                    title="SQL Result"
                    content={selectedLog.sql_result}
                    code
                />

                <Section
                    title="Final Answer"
                    content={selectedLog.formatted_answer}
                />

                <Section
                    title="Execution Time"
                    content={`${selectedLog.execution_time_ms} ms`}
                />

                <Section
                    title="Status"
                    content={selectedLog.status}
                />

                {

                    selectedLog.error_message && (

                        <Section

                            title="Error"

                            content={selectedLog.error_message}

                        />

                    )

                }

            </div>

        </div>

    );

};

interface SectionProps {

    title: string;

    content: any;

    code?: boolean;

}

const Section = ({

    title,

    content,

    code = false,

}: SectionProps) => {

    return (

        <div
            className="
                rounded-xl
                border
                border-white/10
                bg-[#171717]
                p-6
            "
        >

            <h2
                className="
                    mb-4
                    text-xl
                    font-semibold
                "
            >

                {title}

            </h2>

            {

                code

                    ? (

                        <pre
                            className="
                                overflow-auto
                                whitespace-pre-wrap
                                rounded-lg
                                bg-[#0f0f0f]
                                p-4
                                text-sm
                            "
                        >

                            {content ?? "-"}

                        </pre>

                    )

                    : (

                        <div>

                            {content ?? "-"}

                        </div>

                    )

            }

        </div>

    );

};

export default LogDetailsPage;