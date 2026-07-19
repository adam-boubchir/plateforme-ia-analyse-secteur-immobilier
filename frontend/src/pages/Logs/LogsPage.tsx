import { useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";

import { getLogs } from "../../services/logService";

import type { LogSummary } from "../../types/log";

const LogsPage = () => {

    const navigate = useNavigate();

    const [logs, setLogs] = useState<LogSummary[]>([]);

    const [loading, setLoading] = useState(true);

    const [error, setError] = useState("");

    useEffect(() => {

        loadLogs();

    }, []);

    async function loadLogs() {

        try {

            setLoading(true);

            setError("");

            const data = await getLogs();

            setLogs(data);

        }

        catch (error) {

            console.error(error);

            setError(
                "Impossible de charger les logs."
            );

        }

        finally {

            setLoading(false);

        }

    }

    if (loading) {

        return (

            <div className="flex items-center justify-center h-full">

                <p className="text-gray-400">

                    Chargement des logs...

                </p>

            </div>

        );

    }

    if (error) {

        return (

            <div className="flex items-center justify-center h-full">

                <p className="text-red-500">

                    {error}

                </p>

            </div>

        );

    }

    return (

        <div className="flex flex-col h-full p-8 overflow-auto">

            <h1 className="text-3xl font-bold mb-6">

                AI Execution Center

            </h1>

            <div
                className="
                    rounded-xl
                    border
                    border-white/10
                    bg-[#171717]
                    overflow-hidden
                "
            >

                <table className="w-full">

                    <thead
                        className="
                            bg-[#202020]
                            border-b
                            border-white/10
                        "
                    >

                        <tr>

                            <th className="text-left p-4">

                                ID

                            </th>

                            <th className="text-left p-4">

                                Question

                            </th>

                            <th className="text-left p-4">

                                Status

                            </th>

                            <th className="text-left p-4">

                                Temps

                            </th>

                            <th className="text-left p-4">

                                Date

                            </th>

                            <th className="text-center p-4">

                                Action

                            </th>

                        </tr>

                    </thead>

                    <tbody>

                        {

                            logs.map(

                                (log) => (

                                    <tr
                                        key={log.id}
                                        className="
                                            border-b
                                            border-white/5
                                            hover:bg-white/5
                                            transition
                                        "
                                    >

                                        <td className="p-4">

                                            #{log.id}

                                        </td>

                                        <td className="p-4">

                                            {log.question}

                                        </td>

                                        <td className="p-4">

                                            {

                                                log.status === "SUCCESS"

                                                    ? (

                                                        <span className="text-green-400">

                                                            SUCCESS

                                                        </span>

                                                    )

                                                    : (

                                                        <span className="text-red-400">

                                                            FAILED

                                                        </span>

                                                    )

                                            }

                                        </td>

                                        <td className="p-4">

                                            {log.execution_time_ms} ms

                                        </td>

                                        <td className="p-4">

                                            {

                                                new Date(

                                                    log.created_at

                                                ).toLocaleString()

                                            }

                                        </td>

                                        <td className="p-4 text-center">

                                            <button

                                                onClick={() =>

                                                    navigate(

                                                        `/logs/${log.id}`

                                                    )

                                                }

                                                className="
                                                    px-4
                                                    py-2
                                                    rounded-lg
                                                    bg-blue-600
                                                    hover:bg-blue-700
                                                    transition
                                                "

                                            >

                                                Voir

                                            </button>

                                        </td>

                                    </tr>

                                )

                            )

                        }

                    </tbody>

                </table>

            </div>

        </div>

    );

};

export default LogsPage;