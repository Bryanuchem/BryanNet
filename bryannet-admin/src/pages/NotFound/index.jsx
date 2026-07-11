import {
    Box,
    Button,
    Paper,
    Stack,
    Typography,
} from "@mui/material";

import SearchOffRoundedIcon from "@mui/icons-material/SearchOffRounded";
import ArrowBackRoundedIcon from "@mui/icons-material/ArrowBackRounded";

import {

    useNavigate,

} from "react-router-dom";

export default function NotFound() {

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

                    <SearchOffRoundedIcon
                        color="primary"
                        sx={{
                            fontSize: 72,
                        }}
                    />

                    <Typography
                        variant="h3"
                        fontWeight={700}
                    >

                        404

                    </Typography>

                    <Typography
                        variant="h5"
                        fontWeight={600}
                    >

                        Page Not Found

                    </Typography>

                    <Typography
                        color="text.secondary"
                    >

                        The page you are looking for does not exist,
                        may have been moved, or the URL may be incorrect.

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