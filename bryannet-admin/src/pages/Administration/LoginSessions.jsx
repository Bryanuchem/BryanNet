import {

    useMemo,

    useState,

} from "react";

import PageHeader from "../../components/common/PageHeader";
import LoginSessionsToolbar from "../../components/admin/loginSessions/LoginSessionsToolbar";
import LoginSessionsTable from "../../components/admin/loginSessions/LoginSessionsTable";
import LoginSessionDetailsDialog from "../../components/admin/loginSessions/LoginSessionDetailsDialog";
import AppSnackbar from "../../components/common/AppSnackbar";

import {

    useAdminSessions,

} from "../../hooks/useAdminSession";

import {

    useRevokeSession,

} from "../../hooks/useRevokeSession";

import {

    useCurrentPermissions,

} from "../../hooks/useCurrentPermissions";

function LoginSessions() {

    const [

        search,

        setSearch,

    ] = useState("");

    const [

        status,

        setStatus,

    ] = useState("");

    const {

        hasPermission,

    } = useCurrentPermissions();

    const [

        browser,

        setBrowser,

    ] = useState("");

    const [

        selectedSession,

        setSelectedSession,

    ] = useState(null);

    const [

        detailsOpen,

        setDetailsOpen,

    ] = useState(false);

    const [

        snackbar,

        setSnackbar,

    ] = useState({

        open: false,

        message: "",

        severity: "success",

    });

    const filters = useMemo(

        () => ({

            search,

            isActive:

                status === ""

                    ? undefined

                    : status === "true",

            browser:

                browser || undefined,

            page: 1,

            pageSize: 25,

            sortBy: "login_time",

            sortOrder: "desc",

        }),

        [

            search,

            status,

            browser,

        ],

    );

    const {

        data,

        isLoading,

        isError,

        refetch,

    } = useAdminSessions(

        filters,

    );

    const revokeSession =

        useRevokeSession({

            onSuccess: () => {

                setSnackbar({

                    open: true,

                    severity: "success",

                    message:
                        "Login session revoked successfully.",

                });

            },

            onError: (

                error,

            ) => {

                setSnackbar({

                    open: true,

                    severity: "error",

                    message:

                        error?.response?.data?.detail ||

                        "Failed to revoke login session.",

                });

            },

        });

    function handleView(

        session,

    ) {

        if (

            !hasPermission(

                "login_sessions.view",

            )

        ) {

            return;

        }

        setSelectedSession(

            session,

        );

        setDetailsOpen(

            true,

        );

    }

    function handleRevoke(

        session,

    ) {

        if (

            !hasPermission(

                "login_sessions.revoke",

            )

        ) {

            return;

        }

        revokeSession.mutate(

            session.admin_session_id,

        );

    }

    function handleRefresh() {

        refetch();

    }

    function handleClear() {

        setSearch("");

        setStatus("");

        setBrowser("");

    }

    return (

        <>

            <PageHeader

                title="Login Sessions"

                subtitle="Monitor administrator login activity and active sessions."

            />

            <LoginSessionsToolbar

                search={search}

                onSearchChange={setSearch}

                status={status}

                onStatusChange={setStatus}

                browser={browser}

                onBrowserChange={setBrowser}

                sessions={

                    data?.items ?? []

                }

                onRefresh={handleRefresh}

                onClear={handleClear}

            />

            <LoginSessionsTable

                sessions={

                    data?.items ?? []

                }

                loading={isLoading}

                error={isError}

                onRowClick={handleView}

                onView={handleView}

                onRevoke={handleRevoke}

            />

            {hasPermission(

                "login_sessions.view",

            ) && (

                <LoginSessionDetailsDialog

                    open={

                        detailsOpen

                    }

                    session={

                        selectedSession

                    }

                    onClose={() => {

                        setDetailsOpen(

                            false,

                        );

                        setSelectedSession(

                            null,

                        );

                    }}

                />

            )}
            <AppSnackbar

                open={snackbar.open}

                message={snackbar.message}

                severity={snackbar.severity}

                onClose={() =>

                    setSnackbar((previous) => ({

                        ...previous,

                        open: false,

                    }))

                }

            />

        </>

    );

}

export default LoginSessions;    