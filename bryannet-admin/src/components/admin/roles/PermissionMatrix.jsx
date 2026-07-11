import {
    Box,
    Card,
    CardContent,
    Checkbox,
    FormControlLabel,
    Grid,
    Stack,
    Typography,
} from "@mui/material";

import AdminPanelSettingsIcon from "@mui/icons-material/AdminPanelSettings";
import PeopleIcon from "@mui/icons-material/People";
import Inventory2Icon from "@mui/icons-material/Inventory2";
import RouterIcon from "@mui/icons-material/Router";
import PaymentsIcon from "@mui/icons-material/Payments";
import ReceiptLongIcon from "@mui/icons-material/ReceiptLong";
import SettingsIcon from "@mui/icons-material/Settings";
import ShieldIcon from "@mui/icons-material/Shield";
import BuildIcon from "@mui/icons-material/Build";
import AssessmentIcon from "@mui/icons-material/Assessment";
import SmartToyIcon from "@mui/icons-material/SmartToy";
import SecurityIcon from "@mui/icons-material/Security";


function getModuleIcon(
    module,
) {

    switch (
        module.toLowerCase()
    ) {

        case "dashboard":
            return <AssessmentIcon color="primary" />;

        case "customers":
            return <PeopleIcon color="primary" />;

        case "plans":
            return <Inventory2Icon color="primary" />;

        case "subscriptions":
            return <ReceiptLongIcon color="primary" />;

        case "payments":
            return <PaymentsIcon color="primary" />;

        case "routers":
            return <RouterIcon color="primary" />;

        case "devices":
            return <BuildIcon color="primary" />;

        case "administrator users":
            return <AdminPanelSettingsIcon color="primary" />;

        case "roles":
            return <ShieldIcon color="primary" />;

        case "automation":
            return <SmartToyIcon color="primary" />;

        case "settings":
            return <SettingsIcon color="primary" />;

        default:
            return <SecurityIcon color="primary" />;

    }

}

export default function PermissionMatrix({

    permissions,

    onPermissionChange,

}) {

    if (

        permissions.length === 0

    ) {

        return (

            <Box
                sx={{
                    py: 6,
                    textAlign: "center",
                }}
            >

                <Typography
                    variant="h6"
                    gutterBottom
                >

                    No Permissions Found

                </Typography>

                <Typography
                    color="text.secondary"
                >

                    No permissions have been configured yet.

                </Typography>

            </Box>

        );

    }

    return (

        <Grid
            container
            spacing={3}
        >

            {permissions.map(

                (
                    group,
                ) => (

                    <Grid

                        key={

                            group.id

                        }

                        size={{

                            xs: 12,

                            md: 6,

                        }}

                    >

                        <Card
                            variant="outlined"
                            sx={{
                                height: "100%",
                                borderRadius: 3,
                            }}
                        >

                            <CardContent>

                                <Stack spacing={3}>

                                    <Stack
                                        direction="row"
                                        spacing={2}
                                        alignItems="center"
                                    >

                                        {getModuleIcon(

                                            group.name,

                                        )}

                                        <Box>

                                            <Typography
                                                variant="h6"
                                            >

                                                {

                                                    group.name

                                                }

                                            </Typography>

                                            <Typography
                                                variant="body2"
                                                color="text.secondary"
                                            >

                                                {

                                                    group.description

                                                }

                                            </Typography>

                                        </Box>

                                    </Stack>

                                    <Stack
                                        spacing={1}
                                    >

                                        {group.permissions.map(

                                            (
                                                permission,
                                            ) => (

                                                <Box

                                                    key={

                                                        permission.id

                                                    }

                                                    sx={{

                                                        border: (theme) =>

                                                            `1px solid ${theme.palette.divider}`,

                                                        borderRadius: 2,

                                                        px: 2,

                                                        py: 1,

                                                    }}

                                                >

                                                    <FormControlLabel

                                                        control={

                                                            <Checkbox

                                                                checked={

                                                                    permission.enabled

                                                                }

                                                                onChange={(

                                                                    event,

                                                                ) =>

                                                                    onPermissionChange({

                                                                        groupId:

                                                                            group.id,

                                                                        permissionId:

                                                                            permission.id,

                                                                        checked:

                                                                            event.target.checked,

                                                                    })

                                                                }

                                                            />

                                                        }

                                                        label={

                                                            <Box>

                                                                <Typography
                                                                    fontWeight={600}
                                                                >

                                                                    {

                                                                        permission.name

                                                                    }

                                                                </Typography>

                                                                <Typography
                                                                    variant="body2"
                                                                    color="text.secondary"
                                                                >

                                                                    {

                                                                        permission.description

                                                                    }

                                                                </Typography>

                                                            </Box>

                                                        }

                                                        sx={{
                                                            alignItems: "flex-start",
                                                            m: 0,
                                                            width: "100%",
                                                        }}

                                                    />

                                                </Box>

                                            ),

                                        )}

                                    </Stack>

                                </Stack>

                            </CardContent>

                        </Card>

                    </Grid>

                ),

            )}

        </Grid>

    );

}