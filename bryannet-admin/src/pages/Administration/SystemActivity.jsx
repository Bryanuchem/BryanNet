import {
    useMemo,
    useState,
} from "react";

import PageHeader from "../../components/common/PageHeader";

import SystemActivityFilters from "../../components/admin/system-activity/SystemActivityFilters";
import SystemActivityTable from "../../components/admin/system-activity/SystemActivityTable";
import SystemActivityDetailsDialog from "../../components/admin/system-activity/SystemActivityDetailsDialog";

import {
    useSystemActivity,
} from "../../hooks/useSystemActivity";

import {

    useCurrentPermissions,

} from "../../hooks/useCurrentPermissions";

function SystemActivity() {

    const [

        filters,

        setFilters,

    ] = useState({

        search: "",

        action: "",

        result: "",

    });

    const [

        selectedActivity,

        setSelectedActivity,

    ] = useState(null);

const {

    hasPermission,

} = useCurrentPermissions();

    const [

        detailsDialogOpen,

        setDetailsDialogOpen,

    ] = useState(false);

    const {

        data: activities = [],

        isLoading,

        error,

        refetch,

    } = useSystemActivity(

        filters,

    );

    const filteredActivities = useMemo(

        () => activities,

        [

            activities,

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

        });

    };

    const handleView = (

        activity,

    ) => {

        if (

            !hasPermission(

                "system_activity.view",

            )

        ) {

            return;

        }

        setSelectedActivity(

            activity,

        );

        setDetailsDialogOpen(

            true,

        );

    };

    const handleCloseDialog = () => {

        setSelectedActivity(

            null,

        );

        setDetailsDialogOpen(

            false,

        );

    };

    return (

        <>

            <PageHeader

                title="System Activity"

                subtitle="Review automated system events, scheduled jobs and maintenance activity."

            />

            <SystemActivityFilters

                search={

                    filters.search

                }

                onSearchChange={(event) =>

                    handleFilterChange(

                        "search",

                        event.target.value,

                    )

                }

                action={

                    filters.action

                }

                onActionChange={(event) =>

                    handleFilterChange(

                        "action",

                        event.target.value,

                    )

                }

                result={

                    filters.result

                }

                onResultChange={(event) =>

                    handleFilterChange(

                        "result",

                        event.target.value,

                    )

                }

                activities={

                    filteredActivities

                }

                onRefresh={

                    handleRefresh

                }

                onClear={

                    handleClear

                }

            />

            <SystemActivityTable

                activities={

                    filteredActivities

                }

                loading={

                    isLoading

                }

                error={

                    error

                }

                onRowClick={

                    handleView

                }

                onView={

                    handleView

                }

            />

            {hasPermission(

                "system_activity.view",

            ) && (

                <SystemActivityDetailsDialog

                    open={

                        detailsDialogOpen

                    }

                    activity={

                        selectedActivity

                    }

                    onClose={

                        handleCloseDialog

                    }

                />

            )}

        </>

    );

}

export default SystemActivity;    