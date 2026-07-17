import {
    Routes,
    Route,
    Navigate,
} from "react-router-dom";

import MainLayout from "../layouts/MainLayout";

import ChatPage from "../pages/ChatPage";

import ConversationLogsPage from "../pages/ConversationLogs/ConversationLogsPage";

import LogDetailsPage from "../pages/Logs/LogDetailsPage";

const AppRoutes = () => {

    return (

        <Routes>

            <Route
                path="/"
                element={<MainLayout />}
            >

                {/* Redirect */}

                <Route
                    index
                    element={<Navigate to="/chat" replace />}
                />

                {/* Chat */}

                <Route
                    path="chat"
                    element={<ChatPage />}
                />

                {/* Logs d'une conversation */}

                <Route
                    path="conversations/:conversation_uuid/logs"
                    element={<ConversationLogsPage />}
                />

                {/* Détails d'un log */}

                <Route
                    path="logs/:id"
                    element={<LogDetailsPage />}
                />

            </Route>

            {/* Route inconnue */}

            <Route
                path="*"
                element={<Navigate to="/chat" replace />}
            />

        </Routes>

    );

};

export default AppRoutes;