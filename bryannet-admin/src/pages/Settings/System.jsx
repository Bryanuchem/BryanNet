import {

    useEffect,

    useState,

} from "react";

import {

    Stack,

} from "@mui/material";

import PageHeader from "../../components/common/PageHeader";
import AppSnackbar from "../../components/common/AppSnackbar";

import SettingsPageActions from "../../components/settings/SettingsPageActions";

import SystemSettingsForm from "../../components/settings/system/SystemSettingsForm";
import SystemSettingsInfoCard from "../../components/settings/system/SystemSettingsInfoCard";

import {

    useSystemSettings,

    useUpdateSystemSettings,

} from "../../hooks/useSettings";

const defaultSettings = {

    maintenance_mode: false,

    debug_mode: false,

    system_timezone: "UTC",

    audit_log_retention_days: 90,

    backup_retention_days: 30,

};

export default function System() {

    const {

        data,

        isLoading,

    } = useSystemSettings();

    const [

        settings,

        setSettings,

    ] = useState(

        defaultSettings,

    );

    const [

        snackbar,

        setSnackbar,

    ] = useState({

        open: false,

        message: "",

        severity: "success",

    });

    const updateSettings =

        useUpdateSystemSettings({

            onSuccess: () => {

                setSnackbar({

                    open: true,

                    severity: "success",

                    message:

                        "System settings updated successfully.",

                });

            },

            onError: (

                error,

            ) => {

                setSnackbar({

                    open: true,

                    severity: "error",

                    message:

                        error?.response?.data?.message ||

                        error?.response?.data?.detail ||

                        "Failed to update system settings.",

                });

            },

        });

    useEffect(

        () => {

            if (

                data

            ) {

                setSettings({

                    ...defaultSettings,

                    ...data,

                });

            }

        },

        [

            data,

        ],

    );

    function handleChange(

        field,

        value,

    ) {

        setSettings(

            (

                previous,

            ) => ({

                ...previous,

                [

                    field

                ]: value,

            }),

        );

    }

    function handleSave() {

        updateSettings.mutate(

            settings,

        );

    }

    function handleReset() {

        if (

            data

        ) {

            setSettings({

                ...defaultSettings,

                ...data,

            });

        }

    }

    return (

        <>

            <PageHeader

                title="System Settings"

                subtitle="Configure platform maintenance, debugging options, regional preferences and data retention policies."

            />

            <Stack spacing={3}>

                <SystemSettingsInfoCard

                    settings={

                        settings

                    }

                />

                <SystemSettingsForm

                    settings={

                        settings

                    }

                    onChange={

                        handleChange

                    }

                    disabled={

                        isLoading ||

                        updateSettings.isPending

                    }

                />

                <SettingsPageActions

                    onSave={

                        handleSave

                    }

                    onReset={

                        handleReset

                    }

                    loading={

                        updateSettings.isPending

                    }

                />

            </Stack>

            <AppSnackbar

                open={

                    snackbar.open

                }

                severity={

                    snackbar.severity

                }

                message={

                    snackbar.message

                }

                onClose={() =>

                    setSnackbar(

                        (

                            previous,

                        ) => ({

                            ...previous,

                            open: false,

                        }),

                    )

                }

            />

        </>

    );

}