import { create } from "zustand";

import type {

    LogDetails,

    LogSummary,

} from "../types/log";

import {

    getConversationLogs,

    getLog,

} from "../services/logService";


interface LogStore {

    logs: LogSummary[];

    selectedLog: LogDetails | null;

    loading: boolean;

    error: string | null;

    loadConversationLogs: (

        conversation_uuid: string

    ) => Promise<void>;

    loadLog: (

        id: number

    ) => Promise<void>;

    clearLogs: () => void;

    clearSelectedLog: () => void;

}


export const useLogStore = create<LogStore>((set) => ({

    logs: [],

    selectedLog: null,

    loading: false,

    error: null,

    loadConversationLogs: async (

        conversation_uuid

    ) => {

        try {

            set({

                loading: true,

                error: null,

            });

            const response = await getConversationLogs(

                conversation_uuid

            );

            set({

                logs: response.logs,

                loading: false,

            });

        }

        catch (error) {

            console.error(error);

            set({

                loading: false,

                error: "Impossible de charger les logs.",

            });

        }

    },

    loadLog: async (

        id

    ) => {

        try {

            set({

                loading: true,

                error: null,

            });

            const log = await getLog(

                id

            );

            set({

                selectedLog: log,

                loading: false,

            });

        }

        catch (error) {

            console.error(error);

            set({

                loading: false,

                error: "Impossible de charger le log.",

            });

        }

    },

    clearLogs: () =>

        set({

            logs: [],

        }),

    clearSelectedLog: () =>

        set({

            selectedLog: null,

        }),

}));