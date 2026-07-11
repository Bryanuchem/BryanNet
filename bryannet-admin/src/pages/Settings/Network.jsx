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

import NetworkSettingsForm from "../../components/settings/network/NetworkSettingsForm";
import NetworkSettingsInfoCard from "../../components/settings/network/NetworkSettingsInfoCard";

import {

    useNetworkSettings,

    useUpdateNetworkSettings,

} from "../../hooks/useSettings";

const defaultSettings = {

    default_router: "",

    dns_primary: "",

    dns_secondary: "",

    dhcp_lease_time: 24,

    bandwidth_unit: "Mbps",

};

export default function Network() {

    const {

        data,

        isLoading,

    } = useNetworkSettings();

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

        useUpdateNetworkSettings({

            onSuccess: () => {

                setSnackbar({

                    open: true,

                    severity: "success",

                    message:

                        "Network settings updated successfully.",

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

                        "Failed to update network settings.",

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

                title="Network Settings"

                subtitle="Configure the default networking configuration used across the BryanNet ISP Platform."

            />

            <Stack spacing={3}>

                <NetworkSettingsInfoCard

                    settings={

                        settings

                    }

                />

                <NetworkSettingsForm

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