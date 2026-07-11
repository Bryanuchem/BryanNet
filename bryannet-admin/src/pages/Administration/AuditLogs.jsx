import {
    useMemo,
    useState,
} from "react";

import PageHeader from "../../components/common/PageHeader";

import AuditLogFilters from "../../components/admin/audit-logs/AuditLogFilters";
import AuditLogTable from "../../components/admin/audit-logs/AuditLogTable";
import AuditLogDetailsDialog from "../../components/admin/audit-logs/AuditLogDetailsDialog";

import {
    useAuditLogs,
} from "../../hooks/useAuditLogs";

import {
    useCurrentPermissions
} from "../../hooks/useCurrentPermissions";

function AuditLogs() {

    const [

        filters,

        setFilters,

    ] = useState({

        search: "",

        action: "",

        result: "",

        admin_id: "",

    });

    const [

        selectedAuditLog,

        setSelectedAuditLog,

    ] = useState(null);

const {

    hasPermission,

} = useCurrentPermissions();

    const [

        detailsDialogOpen,

        setDetailsDialogOpen,

    ] = useState(false);

    const {

        data: auditLogs = [],

        isLoading,

        refetch,

    } = useAuditLogs(
        filters,
    );

    const filteredAuditLogs = useMemo(

        () => auditLogs,

        [

            auditLogs,

        ],

    );

    const handleFilterChange = (

        field,

        value,

    ) => {

        setFilters(

            (previous) => ({

                ...previous,

                [field]: value,

            }),

        );

    };

    const handleRefresh = () => {

        refetch();

    };

    const handleClear = () => {

        setFilters({

            search: "",

            action: "",

            result: "",

            admin_id: "",

        });

    };

    const handleView = (

        auditLog,

    ) => {

        if (

            !hasPermission(

                "audit_logs.view",

            )

        ) {

            return;

        }

        setSelectedAuditLog(

            auditLog,

        );

        setDetailsDialogOpen(

            true,

        );

    };

    const handleCloseDialog = () => {

        setSelectedAuditLog(
            null,
        );

        setDetailsDialogOpen(
            false,
        );

    };

    return (

        <>

            <PageHeader

                title="Audit Logs"

                subtitle="Review administrator and system activity across the platform."

            />

            <AuditLogFilters

                filters={filters}

                onFilterChange={

                    handleFilterChange

                }

                onRefresh={

                    handleRefresh

                }

                onClear={

                    handleClear

                }

                auditLogs={

                    filteredAuditLogs

                }

            />

            <AuditLogTable

                auditLogs={

                    filteredAuditLogs

                }

                loading={

                    isLoading

                }

                onRowClick={

                    handleView

                }

                onView={

                    handleView

                }

            />

            {hasPermission(

                "audit_logs.view",

            ) && (

                <AuditLogDetailsDialog

                    open={

                        detailsDialogOpen

                    }

                    auditLog={

                        selectedAuditLog

                    }

                    onClose={

                        handleCloseDialog

                    }

                />

            )}

        </>

    );

}

export default AuditLogs;