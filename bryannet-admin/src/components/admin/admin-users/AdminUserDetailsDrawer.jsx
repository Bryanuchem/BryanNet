import {
    Avatar,
    Box,
    Button,
    Card,
    CardContent,
    Divider,
    Drawer,
    Stack,
    Typography,
} from "@mui/material";

import BadgeChip from "../../common/BadgeChip";
import InfoField from "../../common/InfoField";

function AdminUserDetailsDrawer({

    open,

    administrator,

    onClose,

}) {

    if (!administrator) {

        return null;

    }

    const initials =

        administrator.username

            ?.split(" ")

            .filter(Boolean)

            .map((part) => part[0])

            .join("")

            .slice(0, 2)

            .toUpperCase()

            || "A";

    return (

        <Drawer

            anchor="right"

            open={open}

            onClose={onClose}

        >

            <Box

                sx={{

                    width: 450,

                    height: "100%",

                    bgcolor: "#F8FAFC",

                    display: "flex",

                    flexDirection: "column",

                }}

            >

                {/* Header */}

                <Box

                    sx={{

                        bgcolor: "primary.main",

                        color: "white",

                        p: 4,

                    }}

                >

                    <Stack

                        direction="row"

                        spacing={2}

                        alignItems="center"

                    >

                        <Avatar

                            sx={{

                                width: 72,

                                height: 72,

                                fontSize: 28,

                                bgcolor: "white",

                                color: "primary.main",

                                fontWeight: 700,

                            }}

                        >

                            {initials}

                        </Avatar>

                        <Box>

                            <Typography variant="overline">

                                Administrator Details

                            </Typography>

                            <Typography

                                variant="h4"

                                fontWeight={700}

                            >

                                {administrator.username}

                            </Typography>

                            <Typography

                                sx={{

                                    opacity: 0.85,

                                }}

                            >

                                Administrator #

                                {administrator.admin_user_id}

                            </Typography>

                        </Box>

                    </Stack>

                </Box>

                {/* Content */}

                <Box

                    sx={{

                        flex: 1,

                        overflowY: "auto",

                        p: 3,

                    }}

                >

                    <Card elevation={1}>

                        <CardContent>

                            <Typography

                                variant="subtitle2"

                                fontWeight={700}

                                gutterBottom

                            >

                                ACCOUNT INFORMATION

                            </Typography>

                            <Divider

                                sx={{

                                    mb: 3,

                                }}

                            />

                            <Stack spacing={3}>

                                <InfoField

                                    label="Username"

                                >

                                    <Typography fontWeight={500}>

                                        {administrator.username}

                                    </Typography>

                                </InfoField>

                                <InfoField

                                    label="Email"

                                >

                                    <Typography fontWeight={500}>

                                        {administrator.email}

                                    </Typography>

                                </InfoField>

                                <InfoField

                                    label="Role"

                                >

                                    <Typography fontWeight={500}>

                                        {administrator.role_name}

                                    </Typography>

                                </InfoField>

                                <InfoField

                                    label="Status"

                                >

                                    <BadgeChip

                                        status={

                                            administrator.is_active

                                                ? "active"

                                                : "inactive"

                                        }

                                        label={

                                            administrator.is_active

                                                ? "Active"

                                                : "Inactive"

                                        }

                                    />

                                </InfoField>

                            </Stack>

                        </CardContent>

                    </Card>

                    <Card

                        elevation={1}

                        sx={{

                            mt: 3,

                        }}

                    >

                        <CardContent>

                            <Typography

                                variant="subtitle2"

                                fontWeight={700}

                                gutterBottom

                            >

                                RECORD INFORMATION

                            </Typography>

                            <Divider

                                sx={{

                                    mb: 3,

                                }}

                            />

                            <Stack spacing={3}>

                                <InfoField

                                    label="Administrator ID"

                                >

                                    <Typography fontWeight={500}>

                                        {administrator.admin_user_id}

                                    </Typography>

                                </InfoField>

                                <InfoField

                                    label="Created"

                                >

                                    <Typography fontWeight={500}>

                                        {

                                            administrator.created_at

                                                ? new Date(

                                                    administrator.created_at,

                                                ).toLocaleString()

                                                : "-"

                                        }

                                    </Typography>

                                </InfoField>

                                <InfoField

                                    label="Last Updated"

                                >

                                    <Typography fontWeight={500}>

                                        {

                                            administrator.updated_at

                                                ? new Date(

                                                    administrator.updated_at,

                                                ).toLocaleString()

                                                : "-"

                                        }

                                    </Typography>

                                </InfoField>

                            </Stack>

                        </CardContent>

                    </Card>

                </Box>

                {/* Footer */}

                <Box

                    sx={{

                        p: 3,

                        bgcolor: "white",

                        borderTop: "1px solid #E5E7EB",

                    }}

                >

                    <Button

                        fullWidth

                        variant="contained"

                        size="large"

                        onClick={onClose}

                    >

                        Close

                    </Button>

                </Box>

            </Box>

        </Drawer>

    );

}

export default AdminUserDetailsDrawer;                               