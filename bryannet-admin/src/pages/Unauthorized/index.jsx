import {
    Box,
    Button,
    Paper,
    Stack,
    Typography,
} from "@mui/material";

import LockOutlinedIcon from "@mui/icons-material/LockOutlined";
import ArrowBackRoundedIcon from "@mui/icons-material/ArrowBackRounded";

import {

    useNavigate,

} from "react-router-dom";

export default function Unauthorized() {

    const navigate =

        useNavigate();

    return (

        <Box
            sx={{

                minHeight: "100vh",

                display: "flex",

                alignItems: "center",

                justifyContent: "center",

                bgcolor: "background.default",

                p: 3,

            }}
        >

            <Paper
                elevation={3}
                sx={{

                    maxWidth: 520,

                    width: "100%",

                    p: 5,

                    borderRadius: 4,

                    textAlign: "center",

                }}
            >

                <Stack
                    spacing={3}
                    alignItems="center"
                >

                    <LockOutlinedIcon
                        color="error"
                        sx={{
                            fontSize: 72,
                        }}
                    />

                    <Typography
                        variant="h3"
                        fontWeight={700}
                    >

                        403

                    </Typography>

                    <Typography
                        variant="h5"
                        fontWeight={600}
                    >

                        Access Denied

                    </Typography>

                    <Typography
                        color="text.secondary"
                    >

                        You do not have permission to access this page.
                        If you believe this is an error, please contact a system administrator.

                    </Typography>

                    <Button

                        variant="contained"

                        startIcon={

                            <ArrowBackRoundedIcon />

                        }

                        onClick={() =>

                            navigate(

                                "/dashboard",

                            )

                        }

                    >

                        Back to Dashboard

                    </Button>

                </Stack>

            </Paper>

        </Box>

    );

}